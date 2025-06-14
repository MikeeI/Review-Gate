const fs = require('fs');
const path = require('path');

// Linux temp directory helper
function getTempPath(filename) {
    return path.join('/tmp', filename);
}

class FileWatcher {
    constructor(popupManager) {
        this.popupManager = popupManager;
        this.cursorEnhancerWatcher = null;
        this.currentTriggerData = null;
        this.mcpStatus = false;
        this.statusCheckInterval = null;
    }

    startCursorEnhancerIntegration(context) {
        console.log('Starting Cursor Enhancer integration...');

        // Watch for Cursor Enhancer trigger file
        const triggerFilePath = getTempPath('review_gate_trigger.json');

        // Check for existing trigger file first
        this.checkTriggerFile(context, triggerFilePath);

        // Use polling approach for better reliability
        const pollInterval = setInterval(() => {
            // Check main trigger file
            this.checkTriggerFile(context, triggerFilePath);

            // Check backup trigger files
            for (let i = 0; i < 3; i++) {
                const backupTriggerPath = getTempPath(`review_gate_trigger_${i}.json`);
                this.checkTriggerFile(context, backupTriggerPath);
            }
        }, 250); // Check every 250ms for better performance

        // Store the interval for cleanup
        this.cursorEnhancerWatcher = pollInterval;

        // Add to context subscriptions for proper cleanup
        context.subscriptions.push({
            dispose: () => {
                if (pollInterval) {
                    clearInterval(pollInterval);
                }
            }
        });

        // Immediate check on startup
        setTimeout(() => {
            this.checkTriggerFile(context, triggerFilePath);
        }, 100);

        console.log('Cursor Enhancer MCP integration ready!');
    }

    checkTriggerFile(context, filePath) {
        try {
            if (fs.existsSync(filePath)) {
                const data = fs.readFileSync(filePath, 'utf8');
                const triggerData = JSON.parse(data);

                // Check if this is for Cursor and Cursor Enhancer
                if (triggerData.editor && triggerData.editor !== 'cursor') {
                    return;
                }

                if (triggerData.system && triggerData.system !== 'review-gate-v2') {
                    return;
                }

                console.log(`Cursor Enhancer triggered: ${triggerData.data.tool}`);

                // Store current trigger data for response handling
                this.currentTriggerData = triggerData.data;

                this.handleCursorEnhancerToolCall(context, triggerData.data);

                // Clean up trigger file immediately
                try {
                    fs.unlinkSync(filePath);
                } catch (cleanupError) {
                    console.log(`Could not clean trigger file: ${cleanupError.message}`);
                }
            }
        } catch (error) {
            if (error.code !== 'ENOENT') {
                console.log(`Error reading trigger file: ${error.message}`);
            }
        }
    }

    handleCursorEnhancerToolCall(context, toolData) {
        console.log(`Handling Cursor Enhancer tool call: ${toolData.tool}`);

        // Send extension acknowledgement
        if (toolData.trigger_id) {
            this.sendExtensionAcknowledgement(toolData.trigger_id, toolData.tool);
        }

        // Determine special handling mode
        let specialHandling = null;
        if (toolData.tool === 'file_review') {
            specialHandling = 'file_picker';
        } else if (toolData.tool === 'quick_review') {
            specialHandling = 'quick_input';
        } else if (toolData.tool === 'ingest_text') {
            specialHandling = 'text_processing';
        }

        // Open the popup with tool-specific options
        this.popupManager.openCursorEnhancerPopup(context, {
            message:
                toolData.message ||
                toolData.prompt ||
                toolData.instruction ||
                'Please provide your input:',
            title: toolData.title || 'Cursor Enhancer',
            autoFocus: true,
            toolData: toolData,
            mcpIntegration: true,
            triggerId: toolData.trigger_id,
            specialHandling: specialHandling
        });
    }

    sendExtensionAcknowledgement(triggerId, toolType) {
        try {
            const ackData = {
                timestamp: new Date().toISOString(),
                trigger_id: triggerId,
                acknowledged: true,
                tool_type: toolType,
                extension: 'review-gate-v2'
            };
            const ackFile = getTempPath(`review_gate_ack_${triggerId}.json`);
            fs.writeFileSync(ackFile, JSON.stringify(ackData, null, 2));
            console.log(`Extension acknowledgement sent: ${ackFile}`);
        } catch (error) {
            console.error(`Failed to send acknowledgement: ${error.message}`);
        }
    }

    startMcpStatusMonitoring(context) {
        console.log('Starting MCP status monitoring...');

        // Check MCP status periodically
        this.statusCheckInterval = setInterval(() => {
            this.checkMcpStatus();
        }, 2000);

        // Add to context subscriptions for cleanup
        context.subscriptions.push({
            dispose: () => {
                if (this.statusCheckInterval) {
                    clearInterval(this.statusCheckInterval);
                }
            }
        });

        // Initial check
        this.checkMcpStatus();
    }

    checkMcpStatus() {
        try {
            const logFile = getTempPath('review_gate_v2.log');

            if (fs.existsSync(logFile)) {
                const stats = fs.statSync(logFile);
                const now = Date.now();
                const fileAge = now - stats.mtime.getTime();

                // Consider MCP active if log file was modified in the last 30 seconds
                const isActive = fileAge < 30000;

                if (isActive !== this.mcpStatus) {
                    this.mcpStatus = isActive;
                    this.updateChatPanelStatus();
                    console.log(`MCP status changed: ${isActive ? 'ACTIVE' : 'INACTIVE'}`);
                }
            } else {
                if (this.mcpStatus) {
                    this.mcpStatus = false;
                    this.updateChatPanelStatus();
                    console.log('MCP status: INACTIVE (log file not found)');
                }
            }
        } catch (error) {
            console.error(`MCP status check error: ${error.message}`);
        }
    }

    updateChatPanelStatus() {
        // Update the popup manager's chat panel if it exists
        if (this.popupManager && this.popupManager.chatPanel) {
            this.popupManager.chatPanel.webview.postMessage({
                command: 'updateMcpStatus',
                active: this.mcpStatus
            });
        }
    }

    writeResponseFile(triggerId, userInput, attachments = []) {
        try {
            const timestamp = new Date().toISOString();
            const responsePatterns = [
                getTempPath(`review_gate_response_${triggerId}.json`),
                getTempPath('review_gate_response.json'),
                getTempPath(`mcp_response_${triggerId}.json`),
                getTempPath('mcp_response.json')
            ];

            const responseData = {
                timestamp: timestamp,
                trigger_id: triggerId,
                user_input: userInput,
                response: userInput,
                message: userInput,
                attachments: attachments,
                event_type: 'MCP_RESPONSE',
                source: 'review_gate_extension'
            };

            const responseJson = JSON.stringify(responseData, null, 2);

            responsePatterns.forEach(responseFile => {
                try {
                    fs.writeFileSync(responseFile, responseJson);
                    console.log(`MCP response written: ${responseFile}`);
                } catch (writeError) {
                    console.error(
                        `Failed to write response file ${responseFile}: ${writeError.message}`
                    );
                }
            });
        } catch (error) {
            console.error(`Error writing response files: ${error.message}`);
        }
    }

    logToFile(message) {
        try {
            const logFile = getTempPath('review_gate_user_inputs.log');
            const timestamp = new Date().toISOString();
            const logMsg = `[${timestamp}] ${message}\n`;
            fs.appendFileSync(logFile, logMsg);
        } catch (error) {
            console.error(`Error writing to log file: ${error.message}`);
        }
    }

    dispose() {
        if (this.reviewGateWatcher) {
            clearInterval(this.reviewGateWatcher);
            this.cursorEnhancerWatcher = null;
        }
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
            this.statusCheckInterval = null;
        }
        this.currentTriggerData = null;
    }
}

module.exports = FileWatcher;

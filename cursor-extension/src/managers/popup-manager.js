const vscode = require('vscode');

class PopupManager {
    constructor() {
        this.chatPanel = null;
        this.currentTriggerData = null;
        this.outputChannel = null;
    }

    setOutputChannel(outputChannel) {
        this.outputChannel = outputChannel;
    }

    openCursorEnhancerPopup(context, options = {}) {
        const {
            message = 'Welcome to Cursor Enhancer! Please provide your review or feedback.',
            title = 'Cursor Enhancer',
            autoFocus = false,
            toolData = null,
            mcpIntegration = false,
            triggerId = null,
            specialHandling = null
        } = options;

        // Store trigger ID in current trigger data for use in message handlers
        if (triggerId) {
            this.currentTriggerData = { ...toolData, trigger_id: triggerId };
        }

        if (this.chatPanel) {
            this.chatPanel.reveal(vscode.ViewColumn.One);
            this.chatPanel.title = 'Cursor Enhancer';

            // Set MCP status to active when revealing panel for new input
            if (mcpIntegration) {
                setTimeout(() => {
                    this.chatPanel.webview.postMessage({
                        command: 'updateMcpStatus',
                        active: true
                    });
                }, 100);
            }

            // Auto-focus if requested
            if (autoFocus) {
                setTimeout(() => {
                    this.chatPanel.webview.postMessage({
                        command: 'focus'
                    });
                }, 200);
            }

            return;
        }

        // Create webview panel
        this.chatPanel = vscode.window.createWebviewPanel(
            'cursorEnhancerChat',
            title,
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        // Set the HTML content
        this.chatPanel.webview.html = this.getCursorEnhancerHTML(title, mcpIntegration);

        // Handle messages from webview
        this.chatPanel.webview.onDidReceiveMessage(
            webviewMessage => {
                // Get trigger ID from current trigger data or passed options
                const currentTriggerId =
                    (this.currentTriggerData && this.currentTriggerData.trigger_id) || triggerId;

                this.handleWebviewMessage(
                    webviewMessage,
                    currentTriggerId,
                    mcpIntegration,
                    specialHandling,
                    toolData
                );
            },
            undefined,
            context.subscriptions
        );

        // Clean up when panel is closed
        this.chatPanel.onDidDispose(
            () => {
                this.chatPanel = null;
                this.currentTriggerData = null;
            },
            null,
            context.subscriptions
        );

        // Auto-focus if requested
        if (autoFocus) {
            setTimeout(() => {
                this.chatPanel.webview.postMessage({
                    command: 'focus'
                });
            }, 200);
        }
    }

    handleWebviewMessage(
        webviewMessage,
        currentTriggerId,
        mcpIntegration,
        specialHandling,
        toolData
    ) {
        switch (webviewMessage.command) {
            case 'send':
                // Log the user input and write response file for MCP integration
                const eventType = mcpIntegration ? 'MCP_RESPONSE' : 'REVIEW_SUBMITTED';
                this.logUserInput(
                    webviewMessage.text,
                    eventType,
                    currentTriggerId,
                    webviewMessage.attachments || []
                );

                this.handleReviewMessage(
                    webviewMessage.text,
                    webviewMessage.attachments,
                    currentTriggerId,
                    mcpIntegration,
                    specialHandling
                );
                break;
            case 'attach':
                this.logUserInput(
                    'User clicked attachment button',
                    'ATTACHMENT_CLICK',
                    currentTriggerId
                );
                this.handleFileAttachment(currentTriggerId);
                break;
            case 'uploadImage':
                this.logUserInput(
                    'User clicked image upload button',
                    'IMAGE_UPLOAD_CLICK',
                    currentTriggerId
                );
                this.handleImageUpload(currentTriggerId);
                break;
            case 'showError':
                vscode.window.showErrorMessage(webviewMessage.message);
                break;
            case 'ready':
                // Send initial MCP status
                this.chatPanel.webview.postMessage({
                    command: 'updateMcpStatus',
                    active: mcpIntegration ? true : false // Will be updated by file watcher
                });
                // Only send welcome message for manual opens, not MCP tool calls
                if (
                    webviewMessage.text &&
                    !mcpIntegration &&
                    !webviewMessage.text.includes('I have completed')
                ) {
                    this.chatPanel.webview.postMessage({
                        command: 'addMessage',
                        text: webviewMessage.text,
                        type: 'system',
                        plain: true,
                        toolData: toolData,
                        mcpIntegration: mcpIntegration,
                        triggerId: currentTriggerId,
                        specialHandling: specialHandling
                    });
                }
                break;
        }
    }

    logUserInput(inputText, eventType = 'MESSAGE', triggerId = null, attachments = []) {
        const timestamp = new Date().toISOString();
        const logMsg = `[${timestamp}] ${eventType}: ${inputText}`;
        console.log(`CURSOR ENHANCER USER INPUT: ${inputText}`);

        if (this.outputChannel) {
            this.outputChannel.appendLine(logMsg);
        }

        // Write to file for external monitoring - to be implemented by file watcher
        // This will be delegated to file watcher in the refactored version
    }

    getCursorEnhancerHTML(title = 'Cursor Enhancer', mcpIntegration = false) {
        // Simplified HTML for demo - in real implementation, this would be the full HTML
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <style>
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background: var(--vscode-editor-background);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        textarea {
            width: 100%;
            height: 100px;
            margin: 10px 0;
            padding: 10px;
            background: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
        }
        button {
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: 8px 16px;
            margin: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>${title}</h2>
        <div id="messages"></div>
        <textarea id="messageInput" placeholder="Type your message here..."></textarea>
        <div>
            <button onclick="sendMessage()">Send</button>
            <button onclick="attachFile()">📎 Attach</button>
            <button onclick="uploadImage()">📷 Image</button>
        </div>
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            if (input.value.trim()) {
                vscode.postMessage({
                    command: 'send',
                    text: input.value,
                    attachments: []
                });
                input.value = '';
            }
        }
        
        function attachFile() {
            vscode.postMessage({ command: 'attach' });
        }
        
        function uploadImage() {
            vscode.postMessage({ command: 'uploadImage' });
        }
        
        
        // Send ready message when loaded
        window.addEventListener('load', () => {
            vscode.postMessage({ command: 'ready' });
        });
    </script>
</body>
</html>`;
    }

    // Placeholder methods to be implemented with other managers
    handleReviewMessage(text, attachments, triggerId, mcpIntegration, specialHandling) {
        console.log('handleReviewMessage called:', text);
        // To be implemented with file watcher integration
    }

    handleFileAttachment(triggerId) {
        console.log('handleFileAttachment called');
        // To be implemented with file watcher integration
    }

    handleImageUpload(triggerId) {
        console.log('handleImageUpload called');
        // To be implemented with file watcher integration
    }

    dispose() {
        if (this.chatPanel) {
            this.chatPanel.dispose();
            this.chatPanel = null;
        }
        this.currentTriggerData = null;
    }
}

module.exports = PopupManager;

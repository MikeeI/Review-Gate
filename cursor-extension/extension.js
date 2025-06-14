const vscode = require('vscode');

// Import modular components
const PopupManager = require('./src/managers/popup-manager');
const FileWatcher = require('./src/managers/file-watcher');

// Global state
let popupManager = null;
let fileWatcher = null;
let outputChannel = null;

function activate(context) {
    console.log('Cursor Enhancer extension is now active in Cursor for MCP integration!');

    // Create output channel for logging
    outputChannel = vscode.window.createOutputChannel('Cursor Enhancer - Enhanced IDE');
    context.subscriptions.push(outputChannel);

    // Initialize modular components
    popupManager = new PopupManager();
    fileWatcher = new FileWatcher(popupManager);

    // Connect components
    popupManager.setOutputChannel(outputChannel);

    // Connect popup manager methods to file watcher and audio handler
    popupManager.handleReviewMessage = (
        text,
        attachments,
        triggerId,
        mcpIntegration,
        specialHandling
    ) => {
        handleReviewMessage(text, attachments, triggerId, mcpIntegration, specialHandling);
    };

    popupManager.handleFileAttachment = triggerId => {
        handleFileAttachment(triggerId);
    };

    popupManager.handleImageUpload = triggerId => {
        handleImageUpload(triggerId);
    };

    // Silent activation - only log to console, not output channel
    console.log(
        'Cursor Enhancer extension activated for Cursor MCP integration by Lakshman Turlapati'
    );

    // Register command to open Cursor Enhancer manually
    const disposable = vscode.commands.registerCommand('cursorEnhancer.openChat', () => {
        popupManager.openCursorEnhancerPopup(context, {
            message: 'Welcome to Cursor Enhancer! Please provide your review or feedback.',
            title: 'Cursor Enhancer'
        });
    });

    context.subscriptions.push(disposable);

    // Start MCP status monitoring and file watching
    fileWatcher.startMcpStatusMonitoring(context);
    fileWatcher.startCursorEnhancerIntegration(context);

    // Show activation notification
    vscode.window.showInformationMessage(
        'Cursor Enhancer activated! Use Ctrl+Shift+R to open manually.'
    );
}

// Helper functions that connect the components

function handleReviewMessage(text, attachments, triggerId, mcpIntegration, specialHandling) {
    console.log('Processing review message:', text);

    // Log the input
    fileWatcher.logToFile(`USER_INPUT: ${text}`);

    // If this is MCP integration, write response file
    if (mcpIntegration && triggerId) {
        fileWatcher.writeResponseFile(triggerId, text, attachments);
    }

    // Handle special processing modes
    if (specialHandling === 'file_picker') {
        // File picker was handled, close popup after response
        setTimeout(() => {
            if (popupManager.chatPanel) {
                popupManager.chatPanel.dispose();
            }
        }, 1000);
    } else if (specialHandling === 'quick_input') {
        // Quick input was handled, close popup quickly
        setTimeout(() => {
            if (popupManager.chatPanel) {
                popupManager.chatPanel.dispose();
            }
        }, 500);
    }
}

function handleFileAttachment(triggerId) {
    console.log('Handling file attachment for trigger:', triggerId);

    const options = {
        canSelectFiles: true,
        canSelectFolders: false,
        canSelectMany: true,
        openLabel: 'Select Files for Review'
    };

    vscode.window.showOpenDialog(options).then(fileUris => {
        if (fileUris && fileUris.length > 0) {
            const filePaths = fileUris.map(uri => uri.fsPath);
            const fileNames = fileUris.map(uri => uri.fsPath.split('/').pop());

            console.log('Files selected:', fileNames);

            // Log file selection
            fileWatcher.logToFile(`Files selected for review: ${fileNames.join(', ')}`);

            // Send file info to popup
            if (popupManager.chatPanel) {
                popupManager.chatPanel.webview.postMessage({
                    command: 'addMessage',
                    text: `Files attached for review:\n${fileNames.map(name => '• ' + name).join('\n')}\n\nPaths:\n${filePaths.map(fp => '• ' + fp).join('\n')}`,
                    type: 'system'
                });
            }
        } else {
            console.log('No files selected');
        }
    });
}

function handleImageUpload(triggerId) {
    console.log('Handling image upload for trigger:', triggerId);

    const options = {
        canSelectFiles: true,
        canSelectFolders: false,
        canSelectMany: true,
        openLabel: 'Select Images',
        filters: {
            Images: ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']
        }
    };

    vscode.window.showOpenDialog(options).then(fileUris => {
        if (fileUris && fileUris.length > 0) {
            const attachments = [];

            for (const uri of fileUris) {
                try {
                    const fs = require('fs');
                    const path = require('path');
                    const filePath = uri.fsPath;
                    const fileName = path.basename(filePath);
                    const mimeType = getMimeType(fileName);

                    if (mimeType.startsWith('image/')) {
                        const imageBuffer = fs.readFileSync(filePath);
                        const base64Data = imageBuffer.toString('base64');

                        attachments.push({
                            fileName: fileName,
                            mimeType: mimeType,
                            base64Data: base64Data,
                            size: imageBuffer.length
                        });

                        console.log(`Image attached: ${fileName} (${imageBuffer.length} bytes)`);
                    }
                } catch (error) {
                    console.error(`Error processing image ${uri.fsPath}:`, error.message);
                }
            }

            if (attachments.length > 0) {
                // Send images to popup
                if (popupManager.chatPanel) {
                    popupManager.chatPanel.webview.postMessage({
                        command: 'imagesUploaded',
                        attachments: attachments
                    });
                }

                console.log(`${attachments.length} images uploaded successfully`);
            }
        }
    });
}

function getMimeType(fileName) {
    const extension = fileName.split('.').pop().toLowerCase();
    const mimeTypes = {
        png: 'image/png',
        jpg: 'image/jpeg',
        jpeg: 'image/jpeg',
        gif: 'image/gif',
        bmp: 'image/bmp',
        webp: 'image/webp'
    };
    return mimeTypes[extension] || 'application/octet-stream';
}

function deactivate() {
    console.log('Cursor Enhancer extension is being deactivated');

    // Clean up components
    if (popupManager) {
        popupManager.dispose();
        popupManager = null;
    }

    if (fileWatcher) {
        fileWatcher.dispose();
        fileWatcher = null;
    }

    if (outputChannel) {
        outputChannel.dispose();
        outputChannel = null;
    }
}

module.exports = {
    activate,
    deactivate
};

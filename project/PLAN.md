# Implementation Plan: Option B - Moderate Restructure

## Problem Statement

The current codebase violates Single Responsibility Principle with monolithic 1000+ line files that
mix MCP protocol handling, business logic, configuration, and utility functions. This creates
maintenance friction and prevents proper unit testing.

## Solution Overview

Systematically split the monolithic `ReviewGateServer` class and `extension.js` into focused,
single-purpose components following SRP principles. Extract all configuration into centralized
management and eliminate DRY violations through proper abstraction layers.

## Technical Architecture

- **Components**: Configuration manager, MCP protocol handler, tool executor, response manager,
  trigger manager, popup manager, file watcher, audio handler
- **Dependencies**: Existing mcp>=1.9.2, faster-whisper, vscode APIs, new internal module structure
- **Integration Points**: Main entry points `review_gate_v2_mcp.py` and `extension.js` will import
  and coordinate new focused components

## Implementation Phases

#### Phase 1: Create Directory Structure and Configuration

##### Phase 1.1: Setup Project Structure

- [ ] Step 1.1.1: Create `src/` directory in `/root/projects/project-cursor-enhancer/src/`
- [ ] Step 1.1.2: Create `src/config/` directory in
      `/root/projects/project-cursor-enhancer/src/config/`
- [ ] Step 1.1.3: Create `src/protocol/` directory in
      `/root/projects/project-cursor-enhancer/src/protocol/`
- [ ] Step 1.1.4: Create `src/services/` directory in
      `/root/projects/project-cursor-enhancer/src/services/`
- [ ] Step 1.1.5: Create `src/managers/` directory in
      `/root/projects/project-cursor-enhancer/src/managers/`
- [ ] Step 1.1.6: Create `src/utils/` directory in
      `/root/projects/project-cursor-enhancer/src/utils/`

##### Phase 1.2: Create Configuration Management

- [ ] Step 1.2.1: Create `src/config/constants.py` in
      `/root/projects/project-cursor-enhancer/src/config/constants.py`
    ```python
    # Centralized configuration constants
    class TimeoutConfig:
        DEFAULT_USER_INPUT = 120  # seconds
        QUICK_REVIEW = 90  # seconds
        EXTENSION_ACKNOWLEDGEMENT = 30  # seconds
        PROCESSING_DELAY = 0.5  # seconds
        ERROR_DELAY = 1.0  # seconds
        HEARTBEAT_INTERVAL = 10  # seconds

    class FilePatterns:
        TRIGGER_PREFIX = "review_gate_trigger"
        RESPONSE_PREFIX = "review_gate_response"
        MCP_RESPONSE_PREFIX = "mcp_response"
        SPEECH_TRIGGER_PREFIX = "review_gate_speech_trigger"

    class WhisperConfig:
        MODEL_SIZE = "base"
        DEVICE = "cpu"
        COMPUTE_TYPE = "int8"
    ```
- [ ] Step 1.2.2: Create `src/config/__init__.py` in
      `/root/projects/project-cursor-enhancer/src/config/__init__.py`

#### Phase 2: Extract Utility Functions

##### Phase 2.1: Create Shared Utilities

- [ ] Step 2.1.1: Create `src/utils/file_operations.py` in
      `/root/projects/project-cursor-enhancer/src/utils/file_operations.py`
    ```python
    import os
    import json
    from pathlib import Path
    from typing import Dict, Any

    def get_temp_path(filename: str) -> str:
        """Get temporary file path for Linux systems"""
        return os.path.join("/tmp", filename)

    def write_json_file(file_path: str, data: Dict[str, Any]) -> bool:
        """Write JSON data to file with error handling"""
        try:
            Path(file_path).write_text(json.dumps(data, indent=2))
            return True
        except Exception:
            return False

    def read_json_file(file_path: str) -> Dict[str, Any] | None:
        """Read JSON data from file with error handling"""
        try:
            return json.loads(Path(file_path).read_text())
        except Exception:
            return None
    ```
- [ ] Step 2.1.2: Create `src/utils/logging_utils.py` in
      `/root/projects/project-cursor-enhancer/src/utils/logging_utils.py`
- [ ] Step 2.1.3: Create `src/utils/__init__.py` in
      `/root/projects/project-cursor-enhancer/src/utils/__init__.py`

#### Phase 3: Extract MCP Protocol Handler

##### Phase 3.1: Create MCP Protocol Handler

- [ ] Step 3.1.1: Create `src/protocol/mcp_handler.py` in
      `/root/projects/project-cursor-enhancer/src/protocol/mcp_handler.py`
    ```python
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from typing import Dict, Any, List
    import logging

    class McpProtocolHandler:
        def __init__(self, tool_executor):
            self.server = Server("review-gate-v2")
            self.tool_executor = tool_executor
            self.logger = logging.getLogger(__name__)
            self.setup_handlers()

        def setup_handlers(self):
            """Set up MCP request handlers"""
            @self.server.list_tools()
            async def list_tools():
                return self._get_available_tools()

            @self.server.call_tool()
            async def call_tool(name: str, arguments: dict):
                return await self.tool_executor.execute_tool(name, arguments)

        def _get_available_tools(self) -> List[Tool]:
            """Get list of available tools"""
            # Tool definitions moved from original setup_handlers
            pass
    ```
- [ ] Step 3.1.2: Create `src/protocol/__init__.py` in
      `/root/projects/project-cursor-enhancer/src/protocol/__init__.py`

#### Phase 4: Extract Tool Execution Logic

##### Phase 4.1: Create Tool Executor

- [ ] Step 4.1.1: Create `src/services/tool_executor.py` in
      `/root/projects/project-cursor-enhancer/src/services/tool_executor.py`
    ```python
    from typing import Dict, Any, List
    from mcp.types import TextContent
    import asyncio
    import logging
    from ..config.constants import TimeoutConfig

    class ToolExecutor:
        def __init__(self, response_manager, trigger_manager):
            self.response_manager = response_manager
            self.trigger_manager = trigger_manager
            self.logger = logging.getLogger(__name__)

        async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute the specified tool with given arguments"""
            await asyncio.sleep(TimeoutConfig.PROCESSING_DELAY)

            if name == "review_gate_chat":
                return await self._handle_review_gate_chat(arguments)
            elif name == "quick_review":
                return await self._handle_quick_review(arguments)
            # Additional tool handlers...
    ```
- [ ] Step 4.1.2: Create `src/services/review_gate_service.py` in
      `/root/projects/project-cursor-enhancer/src/services/review_gate_service.py`
- [ ] Step 4.1.3: Create `src/services/__init__.py` in
      `/root/projects/project-cursor-enhancer/src/services/__init__.py`

#### Phase 5: Extract Response and Trigger Management

##### Phase 5.1: Create Response Manager

- [ ] Step 5.1.1: Create `src/managers/response_manager.py` in
      `/root/projects/project-cursor-enhancer/src/managers/response_manager.py`
    ```python
    import asyncio
    import glob
    from typing import Optional
    from ..config.constants import TimeoutConfig, FilePatterns
    from ..utils.file_operations import get_temp_path, read_json_file

    class ResponseManager:
        def __init__(self):
            self.logger = logging.getLogger(__name__)

        async def wait_for_user_input(self, trigger_id: str, timeout: int = None) -> Optional[str]:
            """Wait for user input with specified timeout"""
            if timeout is None:
                timeout = TimeoutConfig.DEFAULT_USER_INPUT
            # Implementation moved from _wait_for_user_input

        async def wait_for_extension_acknowledgement(self, trigger_id: str, timeout: int = None) -> bool:
            """Wait for extension acknowledgement"""
            if timeout is None:
                timeout = TimeoutConfig.EXTENSION_ACKNOWLEDGEMENT
            # Implementation moved from _wait_for_extension_acknowledgement
    ```

##### Phase 5.2: Create Trigger Manager

- [ ] Step 5.2.1: Create `src/managers/trigger_manager.py` in
      `/root/projects/project-cursor-enhancer/src/managers/trigger_manager.py`
- [ ] Step 5.2.2: Create `src/managers/__init__.py` in
      `/root/projects/project-cursor-enhancer/src/managers/__init__.py`

#### Phase 6: Refactor Extension.js into Modules

##### Phase 6.1: Create Extension Module Structure

- [ ] Step 6.1.1: Create `cursor-extension/src/` directory in
      `/root/projects/project-cursor-enhancer/cursor-extension/src/`
- [ ] Step 6.1.2: Create `cursor-extension/src/managers/` directory in
      `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/`
- [ ] Step 6.1.3: Create `cursor-extension/src/utils/` directory in
      `/root/projects/project-cursor-enhancer/cursor-extension/src/utils/`

##### Phase 6.2: Extract Popup Manager

- [ ] Step 6.2.1: Create `cursor-extension/src/managers/popup-manager.js` in
      `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/popup-manager.js`
    ```javascript
    const vscode = require('vscode');

    class PopupManager {
        constructor() {
            this.chatPanel = null;
            this.currentTriggerData = null;
        }

        openReviewGatePopup(context, options = {}) {
            // Implementation moved from openReviewGatePopup function
        }

        getReviewGateHTML(title = 'Review Gate', mcpIntegration = false) {
            // Implementation moved from getReviewGateHTML function
        }
    }

    module.exports = PopupManager;
    ```

##### Phase 6.3: Extract File Watcher

- [ ] Step 6.3.1: Create `cursor-extension/src/managers/file-watcher.js` in
      `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/file-watcher.js`

##### Phase 6.4: Extract Audio Handler

- [ ] Step 6.4.1: Create `cursor-extension/src/managers/audio-handler.js` in
      `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/audio-handler.js`

#### Phase 7: Update Main Entry Points

##### Phase 7.1: Refactor Main MCP Server

- [ ] Step 7.1.1: Modify `review_gate_v2_mcp.py` in
      `/root/projects/project-cursor-enhancer/review_gate_v2_mcp.py`
    ```python
    #!/usr/bin/env python3
    from src.protocol.mcp_handler import McpProtocolHandler
    from src.services.tool_executor import ToolExecutor
    from src.managers.response_manager import ResponseManager
    from src.managers.trigger_manager import TriggerManager

    class ReviewGateServer:
        def __init__(self):
            self.response_manager = ResponseManager()
            self.trigger_manager = TriggerManager()
            self.tool_executor = ToolExecutor(self.response_manager, self.trigger_manager)
            self.mcp_handler = McpProtocolHandler(self.tool_executor)

        async def run(self):
            # Simplified run method coordinating components
            pass
    ```

##### Phase 7.2: Refactor Main Extension File

- [ ] Step 7.2.1: Modify `cursor-extension/extension.js` in
      `/root/projects/project-cursor-enhancer/cursor-extension/extension.js`
    ```javascript
    const PopupManager = require('./src/managers/popup-manager');
    const FileWatcher = require('./src/managers/file-watcher');
    const AudioHandler = require('./src/managers/audio-handler');

    let popupManager = null;
    let fileWatcher = null;
    let audioHandler = null;

    function activate(context) {
        popupManager = new PopupManager();
        fileWatcher = new FileWatcher(popupManager);
        audioHandler = new AudioHandler();
        // Coordinate components
    }
    ```

#### Phase 8: Update Package Configuration

##### Phase 8.1: Update Extension Package

- [ ] Step 8.1.1: Modify `cursor-extension/package.json` in
      `/root/projects/project-cursor-enhancer/cursor-extension/package.json`
- [ ] Step 8.1.2: Add `src/` to extension main path and update build scripts

##### Phase 8.2: Update Python Package Structure

- [ ] Step 8.2.1: Create `src/__init__.py` in
      `/root/projects/project-cursor-enhancer/src/__init__.py`
- [ ] Step 8.2.2: Update `requirements_simple.txt` if needed in
      `/root/projects/project-cursor-enhancer/requirements_simple.txt`

## Technical Details

- **Files to Create**:

    - `/root/projects/project-cursor-enhancer/src/config/constants.py`
    - `/root/projects/project-cursor-enhancer/src/protocol/mcp_handler.py`
    - `/root/projects/project-cursor-enhancer/src/services/tool_executor.py`
    - `/root/projects/project-cursor-enhancer/src/services/review_gate_service.py`
    - `/root/projects/project-cursor-enhancer/src/managers/response_manager.py`
    - `/root/projects/project-cursor-enhancer/src/managers/trigger_manager.py`
    - `/root/projects/project-cursor-enhancer/src/utils/file_operations.py`
    - `/root/projects/project-cursor-enhancer/src/utils/logging_utils.py`
    - `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/popup-manager.js`
    - `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/file-watcher.js`
    - `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/audio-handler.js`

- **Files to Modify**:

    - `/root/projects/project-cursor-enhancer/review_gate_v2_mcp.py` - Replace monolithic class with
      component coordination
    - `/root/projects/project-cursor-enhancer/cursor-extension/extension.js` - Replace large file
      with module imports
    - `/root/projects/project-cursor-enhancer/cursor-extension/package.json` - Update main path and
      scripts

- **Key Functions/Classes**:
    - `McpProtocolHandler` - Handles MCP server protocol in `src/protocol/mcp_handler.py`
    - `ToolExecutor` - Executes tool requests in `src/services/tool_executor.py`
    - `ResponseManager` - Manages user input waiting in `src/managers/response_manager.py`
    - `TriggerManager` - Manages popup triggers in `src/managers/trigger_manager.py`
    - `PopupManager` - Manages VSCode popup interface in
      `cursor-extension/src/managers/popup-manager.js`

## Validation Strategy

- **Unit Tests**: Create `tests/test_config.py`, `tests/test_tool_executor.py`,
  `tests/test_response_manager.py` to test individual components
- **Integration Tests**: Run `python review_gate_v2_mcp.py` and verify MCP server starts correctly,
  test extension loading with `cursor --install-extension`
- **Success Criteria**:
    - Each new module under 300 lines: `wc -l src/**/*.py cursor-extension/src/**/*.js`
    - MCP server starts:
      `timeout 5s python review_gate_v2_mcp.py | grep "Review Gate 2.0 server initialized"`
    - Extension loads: Check VSCode extension host logs contain "Review Gate V2 extension is now
      active"
    - Tool execution works: Test `review_gate_chat` tool through MCP protocol

## Risk Mitigation

- **Known Challenges**:

    - Import path dependencies require careful coordination - mitigate by creating all `__init__.py`
      files first
    - Existing tool functionality must remain unchanged - mitigate by keeping same external
      interfaces
    - Extension module loading may require path updates - mitigate by testing imports before moving
      code

- **Decision Points**:
    - Whether to use absolute or relative imports - choose relative imports for internal modules
    - How to handle shared state between components - use dependency injection pattern
    - Whether to maintain backward compatibility - keep same entry point signatures

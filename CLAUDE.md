# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

## Project Overview

Cursor Enhancer is a Cursor IDE enhancement that creates an interactive popup system for extended AI
conversations. It leverages the Model Context Protocol (MCP) to enable multi-modal interactions
including text input and image uploads within Cursor IDE sessions. The system is optimized for Linux
environments with comprehensive automated installation.

## Core Architecture

### MCP Server (`cursor_enhancer_mcp.py`)

- Python-based MCP server that handles communication between Cursor and the popup interface
- Implements modular architecture following Single Responsibility Principle
- Manages file-based communication protocol for reliability
- Runs as a standalone process with specific environment variables
- Refactored from monolithic design to focused components under `src/`

### Cursor Extension (`cursor-extension/`)

- VSCode extension that creates the popup interface in Cursor
- Handles text input and image uploads (audio functionality removed for simplicity)
- Uses Linux file watching to communicate with MCP server
- Built as a `.vsix` package for distribution
- Modular structure with separated popup, file-watcher, and utility managers

### Installation Scripts (`scripts/`)

- Linux installer: `scripts/install.sh` (Linux Ubuntu/Debian only)
- Comprehensive uninstall script: `scripts/uninstall.sh`
- Automated dependency management using apt-get package manager
- Global installation in `~/cursor-extensions/cursor-enhancer/`
- Linux-specific documentation in `documentation/Installation-Linux.md`

### Modular Source Structure (`src/`)

- `src/config/` - Centralized configuration constants
- `src/services/` - Business logic and service classes
- `src/managers/` - Response and trigger file managers
- `src/protocol/` - MCP protocol handling
- `src/utils/` - Shared utilities and logging

## Common Development Commands

### Package Management

```bash
# Install dependencies (prefer pnpm)
pnpm install
# OR
npm install

# Python dependencies
pip install -r requirements_simple.txt
```

### Build System

```bash
# Use the comprehensive build script
cd cursor-extension/
./build.sh dev          # Development build and install
./build.sh release      # Production build and install
./build.sh install      # Install dependencies only
./build.sh lint         # Run linter and fix issues
./build.sh clean        # Clean build artifacts
./build.sh bump patch   # Bump version (patch/minor/major)
```

### Linting and Formatting

```bash
# JavaScript linting (ESLint)
npm run lint            # Root project
cd cursor-extension/ && pnpm run lint:fix  # Extension

# Python linting (ruff)
npm run lint:py

# Format code (Prettier)
prettier --write .

# Lint all code
npm run lint:all
```

### MCP Server Development

```bash
# Run MCP server directly for testing
python cursor_enhancer_mcp.py

# Check MCP server logs
tail -f /tmp/cursor_enhancer.log

# Test modular imports
python -c "from src.config.constants import TimeoutConfig, FilePatterns; print('✅ Imports work')"
```

### Extension Development

```bash
# Navigate to extension directory
cd cursor-extension/

# Development workflow
pnpm run dev            # Build and install in Cursor (dev mode)
pnpm run release        # Build and install in Cursor (production)

# Manual packaging
pnpm run build          # Build for release
pnpm run build:dev      # Build for development
pnpm run package        # Create .vsix package

# Version management
pnpm run version:patch  # Bump patch version
pnpm run version:minor  # Bump minor version
pnpm run version:major  # Bump major version
```

### Installation Testing

```bash
# Test automated installation
./scripts/install.sh     # Linux only

# Test uninstallation
./scripts/uninstall.sh   # Linux only

# Verify MCP configuration
cat ~/.cursor/mcp.json
```

## Platform Information

### Linux Ubuntu/Debian Only

- Comprehensive Ubuntu/Debian support with apt-get package manager
- Automated Python environment setup and dependency management
- Detailed installation guide in `documentation/Installation-Linux.md`
- Installation path: `~/cursor-extensions/cursor-enhancer/`
- Windows and macOS support removed for simplification

## Key Configuration Files

### `mcp.json` Structure

```json
{
    "mcpServers": {
        "cursor-enhancer": {
            "command": "/path/to/python",
            "args": ["/path/to/cursor_enhancer_mcp.py"],
            "env": {
                "PYTHONPATH": "/path/to/extension",
                "PYTHONUNBUFFERED": "1",
                "CURSOR_ENHANCER_MODE": "cursor_integration"
            }
        }
    }
}
```

### `CursorEnhancerV2.mdc` - The Core Rule

This file contains the AI behavior rules that must be copied to Cursor's settings. It defines:

- Phase 1: Primary task execution
- Phase 2: Mandatory MCP tool activation using `cursor_enhancer_chat` tool
- Phase 3: Interactive review loop processing

### Code Style Configuration

#### `.prettierrc` - Formatting Standards

```json
{
    "printWidth": 100,
    "tabWidth": 4,
    "useTabs": false,
    "semi": true,
    "singleQuote": true,
    "trailingComma": "none"
}
```

#### `eslint.config.js` - JavaScript Linting

- ECMAScript 2022 support
- Module-based configuration
- Single quotes, semicolons required
- Console statements allowed

#### `pnpm-workspace.yaml` - Package Management

- Workspace configuration for extension development
- Shared dependency catalog
- VSCode extension tooling integration

## Critical Dependencies

### Python Packages (requirements_simple.txt)

- `mcp>=1.9.2` - Model Context Protocol implementation
- `Pillow>=10.0.0` - Image processing for multimodal inputs
- `typing-extensions>=4.14.0` - Enhanced type annotations
- `asyncio` - Asynchronous I/O support

### System Dependencies

- **Python 3.8+**: Required for MCP server
- **Node.js**: For extension development and linting
- **pnpm**: Preferred package manager (workspace configuration)
- **vsce**: VSCode extension packaging tool
- **ESLint**: JavaScript linting and code quality
- **Prettier**: Code formatting and style consistency
- **ruff**: Python linting and formatting

## File Communication Protocol

The system uses file-based communication between MCP server and Cursor extension:

- Trigger files: `/tmp/cursor_enhancer_trigger_*.json`
- Response files: `/tmp/cursor_enhancer_response_*.json`
- MCP response files: `/tmp/mcp_response_*.json`

## Project Structure

```
project-cursor-enhancer/
├── src/                        # Modular source components
│   ├── config/                 # Configuration constants
│   │   ├── constants.py        # Centralized configuration
│   │   └── __init__.py
│   ├── services/               # Business logic services
│   │   ├── cursor_enhancer_service.py
│   │   └── tool_executor.py
│   ├── managers/               # File and response managers
│   │   ├── response_manager.py
│   │   ├── trigger_manager.py
│   │   └── __init__.py
│   ├── protocol/               # MCP protocol handling
│   │   ├── mcp_handler.py
│   │   └── __init__.py
│   └── utils/                  # Shared utilities
│       ├── logging_utils.py
│       ├── file_operations.py
│       └── __init__.py
├── cursor-extension/           # VSCode extension source
│   ├── build.sh               # Comprehensive build script
│   ├── extension.js           # Main extension logic
│   ├── package.json           # Extension configuration
│   ├── pnpm-workspace.yaml    # Workspace configuration
│   ├── src/managers/          # Extension component managers
│   │   ├── popup-manager.js   # Popup interface handler
│   │   └── file-watcher.js    # File communication handler
│   └── dist/                  # Built extension packages
├── scripts/                   # Installation and maintenance
│   ├── install.sh             # Linux installer
│   └── uninstall.sh           # Linux uninstaller
├── documentation/             # Project documentation
│   ├── INSTALLATION.md        # General installation guide
│   └── Installation-Linux.md  # Linux-specific guide
├── cursor_enhancer_mcp.py     # Main MCP server entry point
├── requirements_simple.txt    # Python dependencies
├── .prettierrc               # Code formatting rules
├── eslint.config.js          # JavaScript linting rules
└── CursorEnhancerV2.mdc      # AI behavior rules
```

## Development Workflow

### Quick Development Cycle

```bash
# Full development build and install
cd cursor-extension/
./build.sh dev

# Test changes in Cursor
# Press Ctrl+Shift+R to test extension manually
```

### Release Preparation

```bash
# Lint and format all code
npm run lint:all
prettier --write .

# Build and test
cd cursor-extension/
./build.sh release

# Version bump
./build.sh bump minor
```

## Troubleshooting Commands

```bash
# Check if MCP server is responsive
ps aux | grep cursor_enhancer_mcp

# Monitor file-based communication
watch -n 1 'ls -la /tmp/cursor_enhancer_*'

# Test Cursor extension manually
# In Cursor: Press Ctrl+Shift+R to test popup

# Check extension logs
# In Cursor: Press F12 → Console tab for browser logs

# Rebuild extension after changes
cd cursor-extension/
./build.sh clean && ./build.sh dev

# Test Linux installation with verbose output
./scripts/install.sh

# Test modular imports
python -c "from src.config.constants import FilePatterns; print(f'Patterns: {[attr for attr in dir(FilePatterns) if not attr.startswith(\"_\")]}')"

# Verify no audio dependencies remain
python -c "from src.services.cursor_enhancer_service import CursorEnhancerService; s = CursorEnhancerService(); print('✅ Service created without audio deps')"
```

## Key Features

### Streamlined Interface

- Text input for iterative follow-ups
- Image upload for visual context (PNG, JPG, JPEG, GIF, BMP, WebP)
- Clean popup interface optimized for developer workflow
- No audio complexity - focused on core functionality

### MCP Integration

- Uses `cursor_enhancer_chat` tool for popup activation
- 5-minute timeout for user responses
- File-based communication protocol for reliability
- Global installation works across all Cursor projects

### Linux Optimization

- Comprehensive Ubuntu/Debian support
- Automated installation with apt-get integration
- Optimized for Linux development environments
- Simplified dependency management without audio components

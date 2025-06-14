# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Review Gate V2 is a Cursor IDE enhancement that creates an interactive popup system for extended AI conversations. It leverages the Model Context Protocol (MCP) to enable multi-modal interactions including text, voice commands (speech-to-text), and image uploads within Cursor IDE sessions.

## Core Architecture

### MCP Server (`review_gate_v2_mcp.py`)
- Python-based MCP server that handles communication between Cursor and the popup interface
- Implements speech-to-text using Faster-Whisper for local voice processing
- Manages file-based communication protocol for reliability
- Runs as a standalone process with specific environment variables

### Cursor Extension (`cursor-extension/`)
- VSCode extension that creates the popup interface in Cursor
- Handles multimodal inputs: text, images, and voice recording
- Uses cross-platform file watching to communicate with MCP server
- Built as a `.vsix` package for distribution

### Installation Scripts (`scripts/`)
- Platform-specific installers: `scripts/install.sh` (macOS/Linux), `scripts/install.ps1` and `scripts/install.bat` (Windows)
- Comprehensive uninstall scripts: `scripts/uninstall.sh`, `scripts/uninstall.ps1`, `scripts/uninstall.bat`
- Automated dependency management including Python packages, SoX audio, and package managers
- Global installation in `~/cursor-extensions/review-gate-v2/` or Windows equivalent
- Linux-specific documentation in `documentation/Installation-Linux.md`

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
python review_gate_v2_mcp.py

# Check MCP server logs
tail -f /tmp/review_gate_v2.log

# Test speech functionality (requires SoX)
sox --version
sox -d -r 16000 -c 1 test.wav trim 0 3 && rm test.wav
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
./scripts/install.sh     # macOS/Linux
./scripts/install.ps1    # Windows PowerShell
./scripts/install.bat    # Windows Batch

# Test uninstallation
./scripts/uninstall.sh   # macOS/Linux
./scripts/uninstall.ps1  # Windows PowerShell
./scripts/uninstall.bat  # Windows Batch

# Verify MCP configuration
cat ~/.cursor/mcp.json  # macOS/Linux
cat %USERPROFILE%\.cursor\mcp.json  # Windows
```

## Platform-Specific Considerations

### macOS
- Fully tested and supported
- Uses Homebrew for dependency management
- SoX audio system for speech processing
- Installation path: `~/cursor-extensions/review-gate-v2/`

### Linux
- Comprehensive Ubuntu/Debian support with apt-get package manager
- Automated SoX installation and audio system configuration
- Detailed installation guide in `documentation/Installation-Linux.md`
- Same installation patterns as macOS with Linux-specific optimizations

### Windows
- Limited testing, may need manual adjustments
- Uses Chocolatey for package management when available
- PowerShell and Batch installer variants
- Installation path: `%USERPROFILE%\cursor-extensions\review-gate-v2\`

## Key Configuration Files

### `mcp.json` Structure
```json
{
  "mcpServers": {
    "review-gate-v2": {
      "command": "/path/to/python",
      "args": ["/path/to/review_gate_v2_mcp.py"],
      "env": {
        "PYTHONPATH": "/path/to/extension",
        "PYTHONUNBUFFERED": "1",
        "REVIEW_GATE_MODE": "cursor_integration"
      }
    }
  }
}
```

### `ReviewGateV2.mdc` - The Core Rule
This file contains the AI behavior rules that must be copied to Cursor's settings. It defines:
- Phase 1: Primary task execution
- Phase 2: Mandatory MCP tool activation
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
- `faster-whisper>=1.0.0` - Local speech-to-text processing
- `Pillow>=10.0.0` - Image processing for multimodal inputs
- `typing-extensions>=4.14.0` - Enhanced type annotations
- `asyncio` - Asynchronous I/O support

### System Dependencies
- **SoX**: Audio processing for speech-to-text functionality
- **Python 3.8+**: Required for MCP server
- **Node.js**: For extension development and linting
- **pnpm**: Preferred package manager (workspace configuration)
- **vsce**: VSCode extension packaging tool
- **ESLint**: JavaScript linting and code quality
- **Prettier**: Code formatting and style consistency
- **ruff**: Python linting and formatting

## File Communication Protocol

The system uses file-based communication between MCP server and Cursor extension:
- Trigger files: `/tmp/review_gate_trigger_*.json` (macOS/Linux)
- Response files: `/tmp/review_gate_response_*.json`
- Windows uses system temp directory equivalent

## Speech Processing

Local Faster-Whisper implementation:
- No cloud dependencies for privacy
- Supports WAV format at 16kHz sample rate
- Cross-platform recording using SoX
- Real-time transcription with visual feedback

## Project Structure

```
project-cursor-enhancer/
├── cursor-extension/           # VSCode extension source
│   ├── build.sh               # Comprehensive build script
│   ├── extension.js           # Main extension logic
│   ├── package.json           # Extension configuration
│   ├── pnpm-workspace.yaml    # Workspace configuration
│   └── dist/                  # Built extension packages
├── scripts/                   # Installation and maintenance
│   ├── install.(sh|ps1|bat)   # Platform installers
│   └── uninstall.(sh|ps1|bat) # Platform uninstallers
├── documentation/             # Project documentation
│   ├── INSTALLATION.md        # General installation guide
│   └── Installation-Linux.md  # Linux-specific guide
├── review_gate_v2_mcp.py      # MCP server implementation
├── requirements_simple.txt    # Python dependencies
├── .prettierrc               # Code formatting rules
├── eslint.config.js          # JavaScript linting rules
└── ReviewGateV2.mdc          # AI behavior rules
```

## Development Workflow

### Quick Development Cycle
```bash
# Full development build and install
cd cursor-extension/
./build.sh dev

# Test changes in Cursor
# Press Cmd+Shift+R (macOS) or Ctrl+Shift+R (Windows)
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
ps aux | grep review_gate_v2_mcp

# Monitor file-based communication
watch -n 1 'ls -la /tmp/review_gate_*'

# Test Cursor extension manually
# In Cursor: Press Cmd+Shift+R (macOS) or Ctrl+Shift+R (Windows)

# Check extension logs
# In Cursor: Press F12 → Console tab for browser logs

# Rebuild extension after changes
cd cursor-extension/
./build.sh clean && ./build.sh dev

# Test Linux installation
sudo ./scripts/install.sh --verbose
```
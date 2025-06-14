#!/bin/bash

# Cursor Enhancer - One-Click Installation Script
# Author: Lakshman Turlapati
# This script installs Cursor Enhancer globally for Cursor IDE

set -e # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project root directory (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🚀 Cursor Enhancer - One-Click Installation${NC}"
echo -e "${BLUE}===========================================${NC}"
echo ""

# Detect operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    PACKAGE_MANAGER="apt-get"
    INSTALL_CMD="sudo $PACKAGE_MANAGER install -y"
else
    echo -e "${YELLOW}⚠️ Unsupported operating system: $OSTYPE${NC}"
    echo -e "${YELLOW}💡 This script is designed for Linux Ubuntu systems only${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Detected OS: $OS${NC}"

# Check if Python 3 is available
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    echo -e "${YELLOW}💡 Please install Python 3 and run this script again${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"
fi

# Create global Cursor extensions directory
CURSOR_EXTENSIONS_DIR="$HOME/cursor-extensions"
CURSOR_ENHANCER_DIR="$CURSOR_EXTENSIONS_DIR/cursor-enhancer"

echo -e "${YELLOW}📁 Creating global installation directory...${NC}"
mkdir -p "$CURSOR_ENHANCER_DIR"

# Copy MCP server files
echo -e "${YELLOW}📋 Copying MCP server files...${NC}"
cp "$PROJECT_ROOT/cursor_enhancer_mcp.py" "$CURSOR_ENHANCER_DIR/"
cp "$PROJECT_ROOT/requirements_simple.txt" "$CURSOR_ENHANCER_DIR/"

# Create Python virtual environment
echo -e "${YELLOW}🐍 Creating Python virtual environment...${NC}"
cd "$CURSOR_ENHANCER_DIR"

# Install python3-venv on Linux if needed
if [[ "$OS" == "linux" ]]; then
    if ! dpkg -s python3-venv >/dev/null 2>&1; then
        echo -e "${YELLOW}📦 Installing Python virtual environment support...${NC}"
        sudo apt-get update
        sudo apt-get install -y python3-venv
    fi
fi

python3 -m venv .venv

# Activate virtual environment and install dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_simple.txt
deactivate

echo -e "${GREEN}✅ Python environment created and dependencies installed${NC}"

# Create MCP configuration
CURSOR_MCP_FILE="$HOME/.cursor/mcp.json"
echo -e "${YELLOW}⚙️ Configuring MCP servers...${NC}"
mkdir -p "$HOME/.cursor"

# Backup existing MCP configuration if it exists
if [[ -f "$CURSOR_MCP_FILE" ]]; then
    BACKUP_FILE="$CURSOR_MCP_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}💾 Backing up existing MCP configuration to: $BACKUP_FILE${NC}"
    cp "$CURSOR_MCP_FILE" "$BACKUP_FILE"

    # Check if the existing config is valid JSON
    if ! python3 -m json.tool "$CURSOR_MCP_FILE" >/dev/null 2>&1; then
        echo -e "${RED}⚠️ Existing MCP config has invalid JSON format${NC}"
        echo -e "${YELLOW}💡 Creating new configuration file${NC}"
        EXISTING_SERVERS="{}"
    else
        # Read existing servers
        EXISTING_SERVERS=$(
            python3 - "$CURSOR_MCP_FILE" <<'EOF_p1'
import json
import sys

cursor_mcp_file = sys.argv[1]
try:
    with open(cursor_mcp_file, 'r') as f:
        config = json.load(f)
    servers = config.get('mcpServers', {})
    servers.pop('cursor-enhancer', None)
    print(json.dumps(servers, indent=2))
except (IOError, json.JSONDecodeError):
    print('{}')
EOF_p1
        )

        if [[ "$EXISTING_SERVERS" == "{}" ]]; then
            echo -e "${YELLOW}📝 No existing MCP servers found or failed to parse${NC}"
        else
            echo -e "${GREEN}✅ Found existing MCP servers, merging configurations${NC}"
        fi
    fi
else
    echo -e "${YELLOW}📝 Creating new MCP configuration file${NC}"
    EXISTING_SERVERS="{}"
fi

# Generate merged MCP config
USERNAME=$(whoami)
TEMP_MCP_FILE="/tmp/existing_mcp_servers.$$.json"

# Write existing servers to temporary file
echo "$EXISTING_SERVERS" >"$TEMP_MCP_FILE"

# Create and execute a Python script to handle the JSON processing
if ! python3 - "$TEMP_MCP_FILE" "$CURSOR_ENHANCER_DIR" "$CURSOR_MCP_FILE" <<EOF; then
import json
import os
import sys

temp_mcp_file = sys.argv[1]
cursor_enhancer_dir = sys.argv[2]
cursor_mcp_file = sys.argv[3]

try:
    # Ensure the parent directory for the MCP file exists
    os.makedirs(os.path.dirname(cursor_mcp_file), exist_ok=True)

    with open(temp_mcp_file, 'r') as f:
        try:
            existing_servers = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_servers = {}

    if not isinstance(existing_servers, dict):
        existing_servers = {}

    existing_servers['cursor-enhancer'] = {
        'command': os.path.join(cursor_enhancer_dir, '.venv/bin/python'),
        'args': [os.path.join(cursor_enhancer_dir, 'cursor_enhancer_mcp.py')],
        'env': {
            'PYTHONPATH': cursor_enhancer_dir,
            'PYTHONUNBUFFERED': '1',
            'CURSOR_ENHANCER_MODE': 'cursor_integration'
        }
    }

    config = {'mcpServers': existing_servers}

    with open(cursor_mcp_file, 'w') as f:
        json.dump(config, f, indent=2)

    print('MCP configuration updated successfully')

except Exception as e:
    print(f'Error updating MCP configuration: {e}', file=sys.stderr)
    sys.exit(1)
finally:
    if os.path.exists(temp_mcp_file):
        os.unlink(temp_mcp_file)
EOF
    echo -e "${RED}❌ Failed to update MCP configuration${NC}"
    rm -f "$TEMP_MCP_FILE"
    exit 1
fi

# Validate the generated configuration
if python3 -m json.tool "$CURSOR_MCP_FILE" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ MCP configuration updated successfully at: $CURSOR_MCP_FILE${NC}"

    # Show summary of configured servers
    TOTAL_SERVERS=$(
        python3 - "$CURSOR_MCP_FILE" <<'EOF_p2'
import json
import sys

cursor_mcp_file = sys.argv[1]
try:
    with open(cursor_mcp_file, 'r') as f:
        config = json.load(f)
    servers = config.get('mcpServers', {})
    print(f'Total MCP servers configured: {len(servers)}')
    for name in servers.keys():
        print(f'  • {name}')
except (IOError, json.JSONDecodeError):
    print('Could not read server config.')
EOF_p2
    )
    echo -e "${BLUE}$TOTAL_SERVERS${NC}"
else
    echo -e "${RED}❌ Generated MCP configuration is invalid${NC}"
    if [[ -f "$BACKUP_FILE" ]]; then
        echo -e "${YELLOW}🔄 Restoring from backup...${NC}"
        cp "$BACKUP_FILE" "$CURSOR_MCP_FILE"
        echo -e "${GREEN}✅ Backup restored${NC}"
    else
        echo -e "${RED}❌ No backup available, installation failed${NC}"
        exit 1
    fi
fi

# Test MCP server
echo -e "${YELLOW}🧪 Testing MCP server...${NC}"
cd "$CURSOR_ENHANCER_DIR"
source .venv/bin/activate
TEMP_DIR=$(python3 -c 'import tempfile; print(tempfile.gettempdir())')
timeout 5s python cursor_enhancer_mcp.py >"$TEMP_DIR/mcp_test.log" 2>&1 || true
deactivate

if grep -q "Cursor Enhancer server initialized" "$TEMP_DIR/mcp_test.log"; then
    echo -e "${GREEN}✅ MCP server test successful${NC}"
else
    echo -e "${YELLOW}⚠️ MCP server test inconclusive (may be normal)${NC}"
fi
rm -f "$TEMP_DIR/mcp_test.log"

# Install Cursor extension
EXTENSION_FILE="$PROJECT_ROOT/cursor-extension/dist/cursor-enhancer-3.0.0.vsix"
if [[ -f "$EXTENSION_FILE" ]]; then
    echo -e "${YELLOW}🔌 Installing Cursor extension...${NC}"

    # Copy extension to installation directory
    cp "$EXTENSION_FILE" "$CURSOR_ENHANCER_DIR/"

    echo -e "${BLUE}📋 MANUAL STEP REQUIRED:${NC}"
    echo -e "${YELLOW}Please complete the extension installation manually:${NC}"
    echo -e "1. Open Cursor IDE"
    echo -e "2. Press Ctrl+Shift+P"
    echo -e "3. Type 'Extensions: Install from VSIX'"
    echo -e "4. Select: $CURSOR_ENHANCER_DIR/cursor-enhancer-3.0.0.vsix"
    echo -e "5. Restart Cursor when prompted"
    echo ""

    # Try to open Cursor if available
    if command -v cursor &>/dev/null; then
        echo -e "${YELLOW}🚀 Opening Cursor IDE...${NC}"
        cursor . &
    else
        echo -e "${YELLOW}💡 Please open Cursor IDE manually${NC}"
    fi
else
    echo -e "${RED}❌ Extension file not found: $EXTENSION_FILE${NC}"
    echo -e "${YELLOW}💡 Please install the extension manually from the Cursor Extensions marketplace${NC}"
fi

# Install global rule (optional)
CURSOR_RULES_DIR="$HOME/.config/Cursor/User/rules"

if [[ -f "$PROJECT_ROOT/ReviewGateV2.mdc" ]]; then
    echo -e "${YELLOW}📜 Installing global rule...${NC}"
    mkdir -p "$CURSOR_RULES_DIR"
    cp "$PROJECT_ROOT/CursorEnhancerV2.mdc" "$CURSOR_RULES_DIR/"
    echo -e "${GREEN}✅ Global rule installed${NC}"
fi

# Clean up any existing temp files
echo -e "${YELLOW}🧹 Cleaning up temporary files...${NC}"
TEMP_DIR=$(python3 -c 'import tempfile; print(tempfile.gettempdir())')
rm -f "$TEMP_DIR"/cursor_enhancer_* "$TEMP_DIR"/mcp_response* 2>/dev/null || true

echo ""
echo -e "${GREEN}🎉 Cursor Enhancer Installation Complete!${NC}"
echo -e "${GREEN}=======================================${NC}"
echo ""
echo -e "${BLUE}📍 Installation Summary:${NC}"
echo -e "   • MCP Server: $CURSOR_ENHANCER_DIR"
echo -e "   • MCP Config: $CURSOR_MCP_FILE"
echo -e "   • Extension: $CURSOR_ENHANCER_DIR/cursor-enhancer-3.0.0.vsix"
echo -e "   • Global Rule: $CURSOR_RULES_DIR/CursorEnhancerV2.mdc"
echo ""
echo -e "${BLUE}🧪 Testing Your Installation:${NC}"
echo -e "1. Restart Cursor completely"
echo -e "2. Press ${YELLOW}Ctrl+Shift+R${NC} to test manual trigger"
echo -e "3. Or ask Cursor Agent: ${YELLOW}'Use the cursor_enhancer_chat tool'${NC}"
echo ""
echo -e "${BLUE}📷 Image Upload Features:${NC}"
echo -e "   • Click camera icon in popup"
echo -e "   • Select images (PNG, JPG, etc.)"
echo -e "   • Images are included in response"
echo ""
echo -e "${BLUE}🔧 Troubleshooting:${NC}"
echo -e "   • Logs: ${YELLOW}tail -f $(python3 -c 'import tempfile; print(tempfile.gettempdir())')/cursor_enhancer.log${NC}"
echo -e "   • Browser Console: ${YELLOW}F12 in Cursor${NC}"
echo ""
echo -e "${GREEN}✨ Enjoy your enhanced Cursor workflow! ✨${NC}"

# Final verification
echo -e "${YELLOW}🔍 Final verification...${NC}"
if [[ -f "$CURSOR_ENHANCER_DIR/cursor_enhancer_mcp.py" ]] &&
    [[ -f "$CURSOR_MCP_FILE" ]] &&
    [[ -d "$CURSOR_ENHANCER_DIR/.venv" ]]; then
    echo -e "${GREEN}✅ All components installed successfully${NC}"
    exit 0
else
    echo -e "${RED}❌ Some components may not have installed correctly${NC}"
    echo -e "${YELLOW}💡 Please check the installation manually${NC}"
    exit 1
fi

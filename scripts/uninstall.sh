#!/bin/bash

# Cursor Enhancer - Uninstaller Script
# Author: Lakshman Turlapati

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${RED}🗑️ Cursor Enhancer - Uninstaller${NC}"
echo -e "${RED}==============================${NC}"
echo ""

read -p "$(echo -e ${YELLOW}Are you sure you want to uninstall Cursor Enhancer? [y/N]: ${NC})" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Uninstallation cancelled${NC}"
    exit 0
fi

echo -e "${YELLOW}🧹 Removing Cursor Enhancer...${NC}"

# Remove installation directory
CURSOR_ENHANCER_DIR="$HOME/cursor-extensions/cursor-enhancer"
if [[ -d "$CURSOR_ENHANCER_DIR" ]]; then
    rm -rf "$CURSOR_ENHANCER_DIR"
    echo -e "${GREEN}✅ Removed installation directory${NC}"
fi

# Remove MCP configuration
CURSOR_MCP_FILE="$HOME/.cursor/mcp.json"
if [[ -f "$CURSOR_MCP_FILE" ]]; then
    # Create backup
    cp "$CURSOR_MCP_FILE" "$CURSOR_MCP_FILE.backup"

    # Remove cursor-enhancer entry (simple approach - remove entire config)
    echo '{"mcpServers":{}}' >"$CURSOR_MCP_FILE"
    echo -e "${GREEN}✅ Removed MCP configuration (backup created)${NC}"
fi

# Remove global rule
CURSOR_RULES_DIR="$HOME/.config/Cursor/User/rules"

if [[ -f "$CURSOR_RULES_DIR/CursorEnhancerV2.mdc" ]]; then
    rm "$CURSOR_RULES_DIR/CursorEnhancerV2.mdc"
    echo -e "${GREEN}✅ Removed global rule${NC}"
fi

# Clean up temp files from both old (/tmp) and new (system temp) locations
rm -f /tmp/cursor_enhancer_* /tmp/mcp_response* 2>/dev/null || true
TEMP_DIR=$(python3 -c 'import tempfile; print(tempfile.gettempdir())' 2>/dev/null || echo "/tmp")
rm -f "$TEMP_DIR"/cursor_enhancer_* "$TEMP_DIR"/mcp_response* 2>/dev/null || true
echo -e "${GREEN}✅ Cleaned up temporary files${NC}"

echo ""
echo -e "${YELLOW}📋 Manual Steps Required:${NC}"
echo -e "1. Open Cursor IDE"
echo -e "2. Go to Extensions (Ctrl+Shift+X)"
echo -e "3. Find 'Cursor Enhancer' and uninstall it"
echo -e "4. Restart Cursor"
echo ""
echo -e "${GREEN}✅ Cursor Enhancer uninstallation complete${NC}"
echo -e "${BLUE}💡 Extension must be removed manually from Cursor${NC}"

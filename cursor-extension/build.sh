#!/bin/bash

# Review Gate V2 Extension Build Script
# Provides comprehensive build and development workflow

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🔨 Review Gate V2 Extension Builder${NC}"
echo -e "${BLUE}===================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies
install_deps() {
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"

    if command_exists pnpm; then
        echo -e "${GREEN}✓ Using pnpm${NC}"
        pnpm install
    elif command_exists npm; then
        echo -e "${GREEN}✓ Using npm${NC}"
        npm install
    else
        echo -e "${RED}❌ Neither pnpm nor npm found${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Dependencies installed${NC}"
}

# Function to build extension
build_extension() {
    local BUILD_TYPE=${1:-"release"}

    echo -e "${YELLOW}🏗️  Building extension ($BUILD_TYPE)...${NC}"

    # Create dist directory
    mkdir -p dist

    # Build based on type
    if [ "$BUILD_TYPE" = "dev" ]; then
        if command_exists pnpm; then
            pnpm run build:dev
        else
            npm run build:dev
        fi
    else
        if command_exists pnpm; then
            pnpm run build
        else
            npm run build
        fi
    fi

    echo -e "${GREEN}✅ Extension built successfully${NC}"

    # Show built files
    echo -e "${BLUE}📁 Built files:${NC}"
    ls -la dist/
}

# Function to install in Cursor
install_cursor() {
    echo -e "${YELLOW}🔌 Installing in Cursor...${NC}"

    if command_exists cursor; then
        VSIX_FILE=$(find dist -name "*.vsix" | head -n 1)
        if [ -n "$VSIX_FILE" ]; then
            cursor --install-extension "$VSIX_FILE"
            echo -e "${GREEN}✅ Extension installed in Cursor${NC}"
        else
            echo -e "${RED}❌ No VSIX file found in dist/${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}💡 Cursor CLI not found. Please install manually:${NC}"
        echo -e "   1. Open Cursor"
        echo -e "   2. Press Cmd+Shift+P (or Ctrl+Shift+P)"
        echo -e "   3. Type 'Extensions: Install from VSIX'"
        echo -e "   4. Select: $(find dist -name "*.vsix" | head -n 1)"
    fi
}

# Function to run linting
lint_code() {
    echo -e "${YELLOW}🔍 Running linter...${NC}"

    if command_exists pnpm; then
        pnpm run lint:fix
    else
        npm run lint:fix
    fi

    echo -e "${GREEN}✅ Linting complete${NC}"
}

# Function to clean build artifacts
clean_build() {
    echo -e "${YELLOW}🧹 Cleaning build artifacts...${NC}"

    if command_exists pnpm; then
        pnpm run clean
    else
        npm run clean
    fi

    echo -e "${GREEN}✅ Clean complete${NC}"
}

# Function to bump version
bump_version() {
    local VERSION_TYPE=${1:-"patch"}

    echo -e "${YELLOW}📈 Bumping version ($VERSION_TYPE)...${NC}"

    if command_exists pnpm; then
        pnpm run "version:$VERSION_TYPE"
    else
        npm run "version:$VERSION_TYPE"
    fi

    echo -e "${GREEN}✅ Version bumped${NC}"
}

# Function to show help
show_help() {
    echo -e "${BLUE}Usage: $0 [command] [options]${NC}"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  ${GREEN}install${NC}     Install dependencies"
    echo -e "  ${GREEN}build${NC}       Build extension for release"
    echo -e "  ${GREEN}build-dev${NC}   Build extension for development"
    echo -e "  ${GREEN}dev${NC}         Build and install in Cursor (development)"
    echo -e "  ${GREEN}release${NC}     Build and install in Cursor (release)"
    echo -e "  ${GREEN}lint${NC}        Run linter and fix issues"
    echo -e "  ${GREEN}clean${NC}       Clean build artifacts"
    echo -e "  ${GREEN}bump${NC}        Bump version (patch/minor/major)"
    echo -e "  ${GREEN}help${NC}        Show this help message"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  $0 install"
    echo -e "  $0 build"
    echo -e "  $0 dev"
    echo -e "  $0 bump minor"
    echo ""
}

# Main script logic
case "${1:-help}" in
install)
    install_deps
    ;;
build)
    build_extension "release"
    ;;
build-dev)
    build_extension "dev"
    ;;
dev)
    install_deps
    lint_code
    build_extension "dev"
    install_cursor
    ;;
release)
    install_deps
    lint_code
    build_extension "release"
    install_cursor
    ;;
lint)
    lint_code
    ;;
clean)
    clean_build
    ;;
bump)
    bump_version "${2:-patch}"
    ;;
help | --help | -h)
    show_help
    ;;
*)
    echo -e "${RED}❌ Unknown command: $1${NC}"
    echo ""
    show_help
    exit 1
    ;;
esac

echo ""
echo -e "${GREEN}🎉 Operation completed successfully!${NC}"

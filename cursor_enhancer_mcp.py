#!/usr/bin/env python3
"""
Cursor Enhancer - Advanced MCP Server with Cursor Integration (Refactored)
Author: Lakshman Turlapati
Provides popup chat, quick input, and file picker tools that automatically trigger Cursor extension.

Requirements:
- mcp>=1.9.2 (latest stable version)
- Python 3.8+
"""

import asyncio
import glob
import logging
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

# MCP imports
from mcp.server.stdio import stdio_server

# Import new modular components
from src.config.constants import FilePatterns, TimeoutConfig
from src.managers.response_manager import ResponseManager
from src.managers.trigger_manager import TriggerManager
from src.protocol.mcp_handler import McpProtocolHandler
from src.services.cursor_enhancer_service import CursorEnhancerService
from src.services.tool_executor import ToolExecutor
from src.utils.file_operations import get_temp_path
from src.utils.logging_utils import flush_logger, setup_logger

# Configure logging using centralized utility
logger = setup_logger(__name__)
logger.info(f"🔧 Log file path: {get_temp_path('cursor_enhancer.log')}")


class CursorEnhancerServer:
    """Refactored Cursor Enhancer Server using modular components"""

    def __init__(self):
        # Initialize all components using dependency injection
        self.response_manager = ResponseManager()
        self.trigger_manager = TriggerManager()
        self.cursor_enhancer_service = CursorEnhancerService()
        self.tool_executor = ToolExecutor(self.response_manager, self.trigger_manager)
        self.mcp_handler = McpProtocolHandler(self.tool_executor)

        # Server state
        self.shutdown_requested = False
        self.shutdown_reason = ""

        logger.info("🚀 Cursor Enhancer server initialized by Lakshman Turlapati for Cursor integration")
        flush_logger(logger)

    async def run(self):
        """Run the Cursor Enhancer server with immediate activation capability and shutdown monitoring"""
        logger.info("🚀 Starting Cursor Enhancer MCP Server for IMMEDIATE Cursor integration...")

        async with stdio_server() as (read_stream, write_stream):
            logger.info("✅ Cursor Enhancer server ACTIVE on stdio transport for Cursor")

            # Create server run task
            server_task = asyncio.create_task(
                self.mcp_handler.server.run(read_stream, write_stream, self.mcp_handler.server.create_initialization_options())
            )

            # Create shutdown monitor task
            shutdown_task = asyncio.create_task(self._monitor_shutdown())

            # Create heartbeat task to keep log file fresh for extension status monitoring
            heartbeat_task = asyncio.create_task(self._heartbeat_logger())

            # Wait for either server completion or shutdown request
            done, pending = await asyncio.wait([server_task, shutdown_task, heartbeat_task], return_when=asyncio.FIRST_COMPLETED)

            # Cancel any pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            if self.shutdown_requested:
                logger.info(f"🛑 Cursor Enhancer server shutting down: {self.shutdown_reason}")
            else:
                logger.info("🏁 Cursor Enhancer server completed normally")

    async def _heartbeat_logger(self):
        """Periodically update log file to keep MCP status active in extension"""
        logger.info("💓 Starting heartbeat logger for extension status monitoring")
        heartbeat_count = 0

        while not self.shutdown_requested:
            try:
                # Update log every heartbeat interval
                await asyncio.sleep(TimeoutConfig.HEARTBEAT_INTERVAL)
                heartbeat_count += 1

                # Write heartbeat to log
                logger.info(f"💓 MCP heartbeat #{heartbeat_count} - Server is active and ready")

                # Force log flush to ensure file is updated
                flush_logger(logger)

            except Exception as e:
                logger.error(f"❌ Heartbeat error: {e}")
                await asyncio.sleep(5)

        logger.info("💔 Heartbeat logger stopped")

    async def _monitor_shutdown(self):
        """Monitor for shutdown requests in a separate task"""
        while not self.shutdown_requested:
            await asyncio.sleep(1)  # Check every second

        # Cleanup operations before shutdown
        logger.info("🧹 Performing cleanup operations before shutdown...")

        # Clean up any temporary files using trigger manager
        try:
            self.trigger_manager.cleanup_trigger_files()
        except Exception as e:
            logger.warning(f"⚠️ Cleanup warning: {e}")

        logger.info("✅ Cleanup completed - shutdown ready")
        return True


async def main():
    """Main entry point for Cursor Enhancer with immediate activation"""
    logger.info("🎬 STARTING Cursor Enhancer MCP Server...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: Linux")
    logger.info(f"Working directory: {os.getcwd()}")

    try:
        server = CursorEnhancerServer()
        await server.run()
    except Exception as e:
        logger.error(f"❌ Fatal error in MCP server: {e}")
        import traceback

        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server crashed: {e}")

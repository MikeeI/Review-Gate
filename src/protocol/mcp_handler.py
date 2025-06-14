import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.types import TextContent, Tool


class McpProtocolHandler:
    def __init__(self, tool_executor):
        self.server = Server("cursor-enhancer")
        self.tool_executor = tool_executor
        self.logger = logging.getLogger(__name__)
        self.setup_handlers()

    def setup_handlers(self):
        """Set up MCP request handlers"""

        @self.server.list_tools()
        async def list_tools():
            """List available Cursor Enhancer tools for Cursor Agent"""
            self.logger.info("🔧 Cursor Agent requesting available tools")
            tools = self._get_available_tools()
            self.logger.info(f"✅ Listed {len(tools)} Cursor Enhancer tools for Cursor Agent")
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            """Handle tool calls from Cursor Agent with immediate activation"""
            self.logger.info(f"🎯 CURSOR AGENT CALLED TOOL: {name}")
            self.logger.info(f"📋 Tool arguments: {arguments}")

            # Log that we're processing
            for handler in self.logger.handlers:
                if hasattr(handler, "flush"):
                    handler.flush()

            return await self.tool_executor.execute_tool(name, arguments)

    def _get_available_tools(self) -> list[Tool]:
        """Get list of available tools"""
        return [
            Tool(
                name="cursor_enhancer_chat",
                description="Open Cursor Enhancer chat popup in Cursor for feedback and reviews. Use this when you need user input, feedback, or review from the human user. The popup will appear in Cursor and wait for user response for up to 5 minutes.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to display in the Cursor Enhancer popup - this is what the user will see",
                            "default": "Please provide your review or feedback:",
                        },
                        "title": {
                            "type": "string",
                            "description": "Title for the Cursor Enhancer popup window",
                            "default": "Cursor Enhancer - Enhanced Cursor IDE",
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context about what needs review (code, implementation, etc.)",
                            "default": "",
                        },
                        "urgent": {"type": "boolean", "description": "Whether this is an urgent review request", "default": False},
                    },
                },
            )
        ]

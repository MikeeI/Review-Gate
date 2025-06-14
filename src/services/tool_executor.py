import asyncio
import logging
import time
from datetime import datetime
from typing import Any

from mcp.types import ImageContent, TextContent

from ..config.constants import TimeoutConfig


class ToolExecutor:
    def __init__(self, response_manager, trigger_manager):
        self.response_manager = response_manager
        self.trigger_manager = trigger_manager
        self.logger = logging.getLogger(__name__)
        self._last_attachments = []

    async def execute_tool(self, name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Execute the specified tool with given arguments"""
        await asyncio.sleep(TimeoutConfig.PROCESSING_DELAY)
        self.logger.info(f"⚙️ Processing tool call: {name}")

        try:
            if name == "cursor_enhancer_chat":
                return await self._handle_cursor_enhancer_chat(arguments)
            else:
                self.logger.error(f"❌ Unknown tool: {name}")
                await asyncio.sleep(TimeoutConfig.ERROR_DELAY)
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            self.logger.error(f"💥 Tool call error for {name}: {e}")
            await asyncio.sleep(TimeoutConfig.ERROR_DELAY)
            return [TextContent(type="text", text=f"ERROR: Tool {name} failed: {str(e)}")]

    async def _handle_cursor_enhancer_chat(self, args: dict) -> list[TextContent]:
        """Handle Cursor Enhancer chat popup and wait for user input with 5 minute timeout"""
        message = args.get("message", "Please provide your review or feedback:")
        title = args.get("title", "Cursor Enhancer - Enhanced Cursor IDE")
        context = args.get("context", "")
        urgent = args.get("urgent", False)

        self.logger.info(f"💬 ACTIVATING Cursor Enhancer chat popup IMMEDIATELY for Cursor Agent")
        self.logger.info(f"📝 Title: {title}")
        self.logger.info(f"📄 Message: {message}")

        # Create trigger file for Cursor extension IMMEDIATELY
        trigger_id = f"review_{int(time.time() * 1000)}"  # Use milliseconds for uniqueness

        # Force immediate trigger creation with enhanced debugging
        success = await self.trigger_manager.trigger_cursor_popup_immediately(
            {
                "tool": "cursor_enhancer_chat",
                "message": message,
                "title": title,
                "context": context,
                "urgent": urgent,
                "trigger_id": trigger_id,
                "timestamp": datetime.now().isoformat(),
                "immediate_activation": True,
            }
        )

        if success:
            self.logger.info(f"🔥 POPUP TRIGGERED IMMEDIATELY - waiting for user input (trigger_id: {trigger_id})")

            # Wait for extension acknowledgement first
            ack_received = await self.response_manager.wait_for_extension_acknowledgement(trigger_id, timeout=30)
            if ack_received:
                self.logger.info("📨 Extension acknowledged popup activation")
            else:
                self.logger.warning("⚠️ No extension acknowledgement received - popup may not have opened")

            # Wait for user input from the popup with 5 MINUTE timeout
            self.logger.info("⏳ Waiting for user input for up to 5 minutes...")
            user_input = await self.response_manager.wait_for_user_input(trigger_id, timeout=300)  # 5 MINUTE timeout

            if user_input:
                # Return user input directly to MCP client
                self.logger.info(f"✅ RETURNING USER REVIEW TO MCP CLIENT: {user_input[:100]}...")

                # Check for images in the last response data
                response_content = [TextContent(type="text", text=f"User Response: {user_input}")]

                # If we have stored attachment data, include images
                if hasattr(self, "_last_attachments") and self._last_attachments:
                    for attachment in self._last_attachments:
                        if attachment.get("mimeType", "").startswith("image/"):
                            try:
                                image_content = ImageContent(type="image", data=attachment["base64Data"], mimeType=attachment["mimeType"])
                                response_content.append(image_content)
                                self.logger.info(f"📸 Added image to response: {attachment.get('fileName', 'unknown')}")
                            except Exception as e:
                                self.logger.error(f"❌ Error adding image to response: {e}")

                return response_content
            else:
                response = f"TIMEOUT: No user input received for cursor enhancer within 5 minutes"
                self.logger.warning("⚠️ Cursor Enhancer timed out waiting for user input after 5 minutes")
                return [TextContent(type="text", text=response)]
        else:
            response = f"ERROR: Failed to trigger Cursor Enhancer popup"
            self.logger.error("❌ Failed to trigger Cursor Enhancer popup")
            return [TextContent(type="text", text=response)]

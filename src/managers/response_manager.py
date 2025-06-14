import asyncio
import glob
import json
import logging
import time
from pathlib import Path
from typing import Optional

from ..config.constants import FilePatterns, TimeoutConfig
from ..utils.file_operations import get_temp_path, read_json_file


class ResponseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._last_attachments = []

    async def wait_for_user_input(self, trigger_id: str, timeout: int = None) -> str | None:
        """Wait for user input from the Cursor extension popup with frequent checks and multiple response patterns"""
        if timeout is None:
            timeout = TimeoutConfig.DEFAULT_USER_INPUT

        response_patterns = [
            Path(get_temp_path(f"{FilePatterns.RESPONSE_PREFIX}_{trigger_id}.json")),
            Path(get_temp_path(f"{FilePatterns.RESPONSE_PREFIX}.json")),  # Fallback generic response
            Path(get_temp_path(f"{FilePatterns.MCP_RESPONSE_PREFIX}_{trigger_id}.json")),  # Alternative pattern
            Path(get_temp_path(f"{FilePatterns.MCP_RESPONSE_PREFIX}.json")),  # Generic MCP response
        ]

        self.logger.info(f"👁️ Monitoring for response files: {[str(p) for p in response_patterns]}")
        self.logger.info(f"🔍 Trigger ID: {trigger_id}")

        start_time = time.time()
        check_interval = 0.1  # Check every 100ms for faster response

        while time.time() - start_time < timeout:
            try:
                # Check all possible response file patterns
                for response_file in response_patterns:
                    if response_file.exists():
                        try:
                            file_content = response_file.read_text().strip()
                            self.logger.info(f"📄 Found response file {response_file}: {file_content[:200]}...")

                            # Handle JSON format
                            if file_content.startswith("{"):
                                data = json.loads(file_content)
                                user_input = data.get("user_input", data.get("response", data.get("message", ""))).strip()
                                attachments = data.get("attachments", [])

                                # Also check if trigger_id matches (if specified)
                                response_trigger_id = data.get("trigger_id", "")
                                if response_trigger_id and response_trigger_id != trigger_id:
                                    self.logger.info(f"⚠️ Trigger ID mismatch: expected {trigger_id}, got {response_trigger_id}")
                                    continue

                                # Process attachments if present
                                if attachments:
                                    self.logger.info(f"📎 Found {len(attachments)} attachments")
                                    # Store attachments for use in response
                                    self._last_attachments = attachments
                                    attachment_descriptions = []
                                    for att in attachments:
                                        if att.get("mimeType", "").startswith("image/"):
                                            attachment_descriptions.append(f"Image: {att.get('fileName', 'unknown')}")

                                    if attachment_descriptions:
                                        user_input += f"\n\nAttached: {', '.join(attachment_descriptions)}"
                                else:
                                    self._last_attachments = []

                            # Handle plain text format
                            else:
                                user_input = file_content
                                attachments = []
                                self._last_attachments = []

                            # Clean up response file immediately
                            try:
                                response_file.unlink()
                                self.logger.info(f"🧹 Response file cleaned up: {response_file}")
                            except Exception as cleanup_error:
                                self.logger.warning(f"⚠️ Cleanup error: {cleanup_error}")

                            if user_input:
                                self.logger.info(f"🎉 RECEIVED USER INPUT for trigger {trigger_id}: {user_input[:100]}...")
                                return user_input
                            else:
                                self.logger.warning(f"⚠️ Empty user input in file: {response_file}")

                        except json.JSONDecodeError as e:
                            self.logger.error(f"❌ JSON decode error in {response_file}: {e}")
                        except Exception as e:
                            self.logger.error(f"❌ Error processing response file {response_file}: {e}")

                # Check more frequently for faster response
                await asyncio.sleep(check_interval)

            except Exception as e:
                self.logger.error(f"❌ Error in wait loop: {e}")
                await asyncio.sleep(0.5)

        self.logger.warning(f"⏰ TIMEOUT waiting for user input (trigger_id: {trigger_id})")
        return None

    async def wait_for_extension_acknowledgement(self, trigger_id: str, timeout: int = None) -> bool:
        """Wait for extension acknowledgement that popup was activated"""
        if timeout is None:
            timeout = TimeoutConfig.EXTENSION_ACKNOWLEDGEMENT

        ack_file = Path(get_temp_path(f"review_gate_ack_{trigger_id}.json"))

        self.logger.info(f"🔍 Monitoring for extension acknowledgement: {ack_file}")

        start_time = time.time()
        check_interval = 0.1  # Check every 100ms for fast response

        while time.time() - start_time < timeout:
            try:
                if ack_file.exists():
                    data = json.loads(ack_file.read_text())
                    ack_status = data.get("acknowledged", False)

                    # Clean up acknowledgement file immediately
                    try:
                        ack_file.unlink()
                        self.logger.info(f"🧹 Acknowledgement file cleaned up")
                    except:
                        pass

                    if ack_status:
                        self.logger.info(f"📨 EXTENSION ACKNOWLEDGED popup activation for trigger {trigger_id}")
                        return True

                # Check frequently for faster response
                await asyncio.sleep(check_interval)

            except Exception as e:
                self.logger.error(f"❌ Error reading acknowledgement file: {e}")
                await asyncio.sleep(0.5)

        self.logger.warning(f"⏰ TIMEOUT waiting for extension acknowledgement (trigger_id: {trigger_id})")
        return False

    def get_last_attachments(self):
        """Get the last processed attachments"""
        return self._last_attachments

    def clear_attachments(self):
        """Clear stored attachments"""
        self._last_attachments = []

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from ..config.constants import FilePatterns
from ..utils.file_operations import get_temp_path


class TriggerManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def trigger_cursor_popup_immediately(self, data: dict[str, Any]) -> bool:
        """Create trigger file for Cursor extension with immediate activation and enhanced debugging"""
        try:
            # Add delay before creating trigger to ensure readiness
            await asyncio.sleep(0.1)  # Wait 100ms before trigger creation

            trigger_file = Path(get_temp_path(f"{FilePatterns.TRIGGER_PREFIX}.json"))

            trigger_data = {
                "timestamp": datetime.now().isoformat(),
                "system": "cursor-enhancer",
                "editor": "cursor",
                "data": data,
                "pid": os.getpid(),
                "active_window": True,
                "mcp_integration": True,
                "immediate_activation": True,
            }

            self.logger.info(f"🎯 CREATING trigger file with data: {json.dumps(trigger_data, indent=2)}")

            # Write trigger file with immediate flush
            trigger_file.write_text(json.dumps(trigger_data, indent=2))

            # Verify file was written successfully
            if not trigger_file.exists():
                self.logger.error(f"❌ Failed to create trigger file: {trigger_file}")
                return False

            try:
                file_size = trigger_file.stat().st_size
                if file_size == 0:
                    self.logger.error(f"❌ Trigger file is empty: {trigger_file}")
                    return False
            except FileNotFoundError:
                # File may have been consumed by the extension already - this is OK
                self.logger.info(f"✅ Trigger file was consumed immediately by extension: {trigger_file}")
                file_size = len(json.dumps(trigger_data, indent=2))

            # Force file system sync with retry
            for attempt in range(3):
                try:
                    os.sync()
                    break
                except Exception as sync_error:
                    self.logger.warning(f"⚠️ Sync attempt {attempt + 1} failed: {sync_error}")
                    await asyncio.sleep(0.1)  # Wait 100ms between attempts

            self.logger.info(f"🔥 IMMEDIATE trigger created for Cursor: {trigger_file}")
            self.logger.info(f"📁 Trigger file path: {trigger_file.absolute()}")
            self.logger.info(f"📊 Trigger file size: {file_size} bytes")

            # Create multiple backup trigger files for reliability
            await self._create_backup_triggers(data)

            # Add small delay to allow extension to process
            await asyncio.sleep(0.2)  # Wait 200ms for extension to process

            # Note: Trigger file may have been consumed by extension already, which is good!
            try:
                if trigger_file.exists():
                    self.logger.info(f"✅ Trigger file still exists: {trigger_file}")
                else:
                    self.logger.info(f"✅ Trigger file was consumed by extension: {trigger_file}")
                    self.logger.info(f"🎯 This is expected behavior - extension is working properly")
            except Exception as check_error:
                self.logger.info(f"✅ Cannot check trigger file status (likely consumed): {check_error}")
                self.logger.info(f"🎯 This is expected behavior - extension is working properly")

            # Check if extension might be watching
            log_file = Path(get_temp_path("cursor_enhancer.log"))
            if log_file.exists():
                self.logger.info(f"📝 MCP log file exists: {log_file}")
            else:
                self.logger.warning(f"⚠️ MCP log file missing: {log_file}")

            # Force log flush
            for handler in self.logger.handlers:
                if hasattr(handler, "flush"):
                    handler.flush()

            return True

        except Exception as e:
            self.logger.error(f"❌ CRITICAL: Failed to create Review Gate trigger: {e}")
            import traceback

            self.logger.error(f"🔍 Full traceback: {traceback.format_exc()}")
            # Wait before returning failure
            await asyncio.sleep(1.0)  # Wait 1 second before confirming failure
            return False

    async def _create_backup_triggers(self, data: dict[str, Any]):
        """Create backup trigger files for better reliability"""
        try:
            # Create multiple backup trigger files
            for i in range(3):
                backup_trigger = Path(get_temp_path(f"{FilePatterns.TRIGGER_PREFIX}_{i}.json"))
                backup_data = {
                    "backup_id": i,
                    "timestamp": datetime.now().isoformat(),
                    "system": "cursor-enhancer",
                    "data": data,
                    "mcp_integration": True,
                    "immediate_activation": True,
                }
                backup_trigger.write_text(json.dumps(backup_data, indent=2))

            self.logger.info("🔄 Backup trigger files created for reliability")

        except Exception as e:
            self.logger.warning(f"⚠️ Backup trigger creation failed: {e}")

    def cleanup_trigger_files(self):
        """Clean up any existing trigger files"""
        try:
            # Clean up main trigger file
            main_trigger = Path(get_temp_path(f"{FilePatterns.TRIGGER_PREFIX}.json"))
            if main_trigger.exists():
                main_trigger.unlink()
                self.logger.info("🧹 Main trigger file cleaned up")

            # Clean up backup trigger files
            for i in range(3):
                backup_trigger = Path(get_temp_path(f"{FilePatterns.TRIGGER_PREFIX}_{i}.json"))
                if backup_trigger.exists():
                    backup_trigger.unlink()
                    self.logger.info(f"🧹 Backup trigger file {i} cleaned up")

        except Exception as e:
            self.logger.warning(f"⚠️ Error cleaning up trigger files: {e}")

# Centralized configuration constants
class TimeoutConfig:
    DEFAULT_USER_INPUT = 120  # seconds
    QUICK_REVIEW = 90  # seconds
    EXTENSION_ACKNOWLEDGEMENT = 30  # seconds
    PROCESSING_DELAY = 0.5  # seconds
    ERROR_DELAY = 1.0  # seconds
    HEARTBEAT_INTERVAL = 10  # seconds


class FilePatterns:
    TRIGGER_PREFIX = "cursor_enhancer_trigger"
    RESPONSE_PREFIX = "cursor_enhancer_response"
    MCP_RESPONSE_PREFIX = "mcp_response"

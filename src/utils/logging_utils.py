import logging
import sys
from typing import Optional

from .file_operations import get_temp_path


def setup_logger(name: str = __name__, log_file: str | None = None) -> logging.Logger:
    """Setup logger with file and stderr handlers"""
    if log_file is None:
        log_file = get_temp_path("cursor_enhancer.log")

    # Create logging handlers
    handlers = []

    try:
        # File handler for Unix systems
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        handlers.append(file_handler)
    except Exception as e:
        # If file logging fails, just use stderr
        print(f"Warning: Could not create log file: {e}", file=sys.stderr)

    # Always add stderr handler
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.INFO)
    handlers.append(stderr_handler)

    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add new handlers
    for handler in handlers:
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)

    return logger


def flush_logger(logger: logging.Logger) -> None:
    """Force immediate log flushing"""
    for handler in logger.handlers:
        if hasattr(handler, "flush"):
            handler.flush()


def log_with_flush(logger: logging.Logger, level: str, message: str) -> None:
    """Log message and immediately flush"""
    getattr(logger, level.lower())(message)
    flush_logger(logger)

import json
import os
from pathlib import Path
from typing import Any


def get_temp_path(filename: str) -> str:
    """Get temporary file path for Linux systems"""
    return os.path.join("/tmp", filename)


def write_json_file(file_path: str, data: dict[str, Any]) -> bool:
    """Write JSON data to file with error handling"""
    try:
        Path(file_path).write_text(json.dumps(data, indent=2))
        return True
    except Exception:
        return False


def read_json_file(file_path: str) -> dict[str, Any] | None:
    """Read JSON data from file with error handling"""
    try:
        return json.loads(Path(file_path).read_text())
    except Exception:
        return None

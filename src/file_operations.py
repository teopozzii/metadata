"""File operations utilities."""

from pathlib import Path
import send2trash


def move_to_trash(file_path: Path) -> bool:
    """Move a file to trash. Returns True if successful."""
    try:
        send2trash.send2trash(str(file_path))
        return True
    except Exception:
        return False

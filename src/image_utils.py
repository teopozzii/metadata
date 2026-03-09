"""Utility functions for image processing."""

from pathlib import Path
from PIL import Image
import imagehash

from config import SUPPORTED_EXTENSIONS


def is_supported_image(file_path: Path) -> bool:
    """Check if file is a supported image format."""
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def get_image_hash(image_path: Path) -> str | None:
    """Compute perceptual hash of an image."""
    try:
        with Image.open(image_path) as img:
            return str(imagehash.phash(img))
    except Exception:
        return None


def generate_thumbnail(image_path: Path, max_size: int = 400) -> bytes | None:
    """Generate thumbnail for an image and return as bytes."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            if img.mode == "RGBA":
                img = img.convert("RGB")
            
            from io import BytesIO
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            return buffer.getvalue()
    except Exception:
        return None


def get_images_in_folder(folder_path: Path) -> list[Path]:
    """Get all supported images in a folder (non-recursive)."""
    images = []
    for file_path in folder_path.iterdir():
        if file_path.is_file() and is_supported_image(file_path):
            images.append(file_path)
    return sorted(images, key=lambda p: p.name.lower())

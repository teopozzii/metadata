"""EXIF metadata extraction."""

from pathlib import Path
from typing import TypedDict
import exifread


class ImageMetadata(TypedDict):
    filename: str
    file_path: str
    shot_date: str | None


def extract_exif_date(image_path: Path) -> str | None:
    """Extract creation date from EXIF metadata."""
    try:
        with open(image_path, "rb") as f:
            tags = exifread.process_file(f, details=False)
            
            date_tag = tags.get("EXIF DateTimeOriginal") or tags.get("Image DateTime")
            
            if date_tag:
                return str(date_tag)
            
            return None
    except Exception:
        return None


def scan_folder_for_dates(folder_path: Path) -> list[ImageMetadata]:
    """Scan folder and extract EXIF dates from all images."""
    from src.image_utils import get_images_in_folder
    
    images = get_images_in_folder(folder_path)
    results: list[ImageMetadata] = []
    
    for img_path in images:
        shot_date = extract_exif_date(img_path)
        results.append({
            "filename": img_path.name,
            "file_path": str(img_path),
            "shot_date": shot_date
        })
    
    return results

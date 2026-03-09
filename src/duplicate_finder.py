"""Duplicate image finder logic."""

from pathlib import Path
from typing import TypedDict
import imagehash

from config import DUPLICATE_THRESHOLD
from src.image_utils import get_image_hash, get_images_in_folder


class DuplicatePair(TypedDict):
    file_a: str
    file_b: str
    hash_a: str
    hash_b: str
    distance: int


def find_duplicates(folder_path: Path) -> list[DuplicatePair]:
    """Find duplicate images in a folder using perceptual hashing."""
    images = get_images_in_folder(folder_path)
    
    hashes: dict[str, tuple[Path, imagehash.ImageHash]] = {}
    
    for img_path in images:
        img_hash = get_image_hash(img_path)
        if img_hash:
            hashes[img_path.name] = (img_path, img_hash)
    
    duplicates: list[DuplicatePair] = []
    seen_pairs: set[frozenset[str]] = set()
    
    items = list(hashes.items())
    
    for i, (name1, (path1, hash1)) in enumerate(items):
        for name2, (path2, hash2) in items[i + 1:]:
            hamming_dist = int(hash1 - hash2)
            
            if hamming_dist <= DUPLICATE_THRESHOLD:
                pair = frozenset([name1, name2])
                if pair not in seen_pairs:
                    duplicates.append({
                        "file_a": name1,
                        "file_b": name2,
                        "hash_a": str(path1),
                        "hash_b": str(path2),
                        "distance": hamming_dist
                    })
                    seen_pairs.add(pair)
    
    return duplicates
    
    return duplicates

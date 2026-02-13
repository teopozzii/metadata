#!/usr/bin/env python3
import os
from PIL import Image
import imagehash
from pathlib import Path

# Threshold per similarità (0 = identici, <5 = molto simili)
THRESHOLD = 5

# Directory da scansionare
image_dir = Path(".")

# Raccogli tutti i JPG/JPEG
image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.JPG")) + \
              list(image_dir.glob("*.jpeg")) + list(image_dir.glob("*.JPEG"))

# Calcola hash per ogni immagine
hashes = {}
for img_path in image_files:
    try:
        img = Image.open(img_path)
        hashes[img_path.name] = imagehash.phash(img)
    except Exception as e:
        print(f"Error processing {img_path.name}: {e}")

# Confronta tutte le coppie (O(n²))
duplicates = []
seen = set()

for i, (name1, hash1) in enumerate(hashes.items()):
    for name2, hash2 in list(hashes.items())[i+1:]:
        hamming_dist = hash1 - hash2
        if hamming_dist <= THRESHOLD:
            pair = tuple(sorted([name1, name2]))
            if pair not in seen:
                duplicates.append((name1, name2, hamming_dist))
                seen.add(pair)

# Stampa risultati
if duplicates:
    print(f"Found {len(duplicates)} duplicate pair(s):\n")
    for f1, f2, dist in duplicates:
        print(f"  {f1} ≈ {f2} (distance: {dist})")
else:
    print("No duplicates found.")

"""App configuration."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "metadata-app-secret-key"

THUMBNAIL_SIZE = (400, 400)

DUPLICATE_THRESHOLD = 1

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".tif"}

# Metadata App

A desktop application for working with image metadata on macOS. Find duplicate images and retrieve EXIF shot dates from your photo collection.

## Features

### 🗑️ Remove Duplicates
- Find duplicate and similar images using perceptual hashing
- Interactive side-by-side comparison
- Choose to keep one, both, or skip (skip = keep both)
- Files are moved to Trash (recoverable)

### 📅 Retrieve Shot Date
- Extract EXIF metadata from images
- Gallery view with hover overlay showing filename and date
- Export report to JSON

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

This opens the app in a native macOS window.

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- WebP (.webp)
- TIFF (.tiff, .tif)

## Requirements

- Python 3.11+
- macOS (required for native folder dialogs)

## Project Structure

```
metadata/
├── app.py                 # Main application (Flask + PyWebView)
├── config.py             # Configuration settings
├── src/                  # Source modules
│   ├── __init__.py
│   ├── image_utils.py    # Image processing (hashing, thumbnails)
│   ├── duplicate_finder.py  # Duplicate detection logic
│   ├── exif_extractor.py    # EXIF metadata extraction
│   └── file_operations.py   # File operations (trash)
├── templates/            # HTML templates
│   ├── base.html
│   ├── landing.html
│   ├── duplicates.html
│   └── gallery.html
├── static/               # CSS and JavaScript
│   ├── css/style.css
│   └── js/script.js
└── requirements.txt
```

## Legacy Scripts

The original CLI implementations are preserved for reference:
- `find_dup_pics.py` - Original duplicate finder (terminal-based)
- `pic_dates.sh` - Original date extraction (shell script)

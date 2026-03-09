# Metadata App

A desktop application for working with image metadata. Find duplicate images and retrieve EXIF shot dates from your photo collection.

## Features

### 🗑️ Remove Duplicates
- Find duplicate and similar images using perceptual hashing
- Interactive side-by-side comparison
- Choose to keep one, both, or neither image
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

### Desktop Mode (Default)
```bash
python app.py
```

### Web Mode (for development)
```bash
python app.py --web
```
Then open http://localhost:5000 in your browser.

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- WebP (.webp)
- TIFF (.tiff, .tif)

## Requirements

- Python 3.11+
- macOS (PyWebView native dialogs)

## Project Structure

```
metadata/
├── app.py                 # Main application
├── config.py             # Configuration
├── src/                  # Source modules
│   ├── image_utils.py
│   ├── duplicate_finder.py
│   ├── exif_extractor.py
│   └── file_operations.py
├── templates/            # HTML templates
├── static/               # CSS and JavaScript
└── requirements.txt
```

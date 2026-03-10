#!/usr/bin/env python3
"""Main Flask application with PyWebView desktop wrapper."""

import json
import logging
import os
import subprocess
from pathlib import Path

import webview
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO

from config import BASE_DIR
from src.duplicate_finder import find_duplicates
from src.exif_extractor import scan_folder_for_dates
from src.file_operations import move_to_trash
from src.image_utils import generate_thumbnail, get_images_in_folder

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Api:
    """API exposed to JavaScript via PyWebView."""
    
    def select_folder(self):
        """Open native folder selection dialog using macOS osascript."""
        try:
            result = subprocess.run(
                ['osascript', '-e', 'POSIX path of (choose folder)'],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0 and result.stdout.strip():
                folder = result.stdout.strip()
                logger.debug(f"Folder selected: {folder}")
                return folder
            
            logger.debug("Folder selection cancelled")
            return None
            
        except Exception as e:
            logger.error(f"Error selecting folder: {e}")
            return None


app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)


@app.route("/")
def index():
    """Landing page."""
    return render_template("landing.html")


@app.route("/duplicates/select-folder", methods=["POST"])
def duplicates_select_folder():
    """Handle folder selection for duplicate finder."""
    data = request.get_json()
    folder_path_str = data.get("folder_path", "")
    folder_path = Path(folder_path_str)
    
    logger.debug(f"duplicates_select_folder received: '{folder_path_str}'")
    logger.debug(f"Path exists: {folder_path.exists()}, is_dir: {folder_path.is_dir()}")
    
    if not folder_path.exists() or not folder_path.is_dir():
        logger.error(f"Invalid folder path: {folder_path_str}")
        return jsonify({"error": f"Invalid folder path: {folder_path_str}"}), 400
    
    images = get_images_in_folder(folder_path)
    
    return jsonify({
        "folder_path": str(folder_path),
        "image_count": len(images)
    })


@app.route("/duplicates/scan", methods=["POST"])
def duplicates_scan():
    """Scan folder for duplicates."""
    data = request.get_json()
    folder_path = Path(data.get("folder_path", ""))
    
    if not folder_path.exists():
        return jsonify({"error": "Folder not found"}), 400
    
    duplicates = find_duplicates(folder_path)
    
    return jsonify({
        "duplicates": duplicates,
        "total_pairs": len(duplicates)
    })


@app.route("/duplicates/thumbnail")
def duplicates_thumbnail():
    """Serve thumbnail for an image."""
    file_path = request.args.get("path", "")
    img_path = Path(file_path)
    
    if not img_path.exists():
        return "", 404
    
    thumb_data = generate_thumbnail(img_path)
    if not thumb_data:
        return "", 404
    
    return send_file(
        BytesIO(thumb_data),
        mimetype="image/jpeg"
    )


@app.route("/duplicates/delete", methods=["POST"])
def duplicates_delete():
    """Move a file to trash."""
    data = request.get_json()
    file_path = Path(data.get("file_path", ""))
    
    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404
    
    success = move_to_trash(file_path)
    
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to move file to trash"}), 500


@app.route("/gallery/select-folder", methods=["POST"])
def gallery_select_folder():
    """Handle folder selection for gallery."""
    data = request.get_json()
    folder_path_str = data.get("folder_path", "")
    folder_path = Path(folder_path_str)
    
    logger.debug(f"gallery_select_folder received: '{folder_path_str}'")
    logger.debug(f"Path exists: {folder_path.exists()}, is_dir: {folder_path.is_dir()}")
    
    if not folder_path.exists() or not folder_path.is_dir():
        logger.error(f"Invalid folder path: {folder_path_str}")
        return jsonify({"error": f"Invalid folder path: {folder_path_str}"}), 400
    
    metadata = scan_folder_for_dates(folder_path)
    
    return jsonify({
        "folder_path": str(folder_path),
        "images": metadata
    })


@app.route("/gallery/thumbnail")
def gallery_thumbnail():
    """Serve thumbnail for gallery."""
    file_path = request.args.get("path", "")
    img_path = Path(file_path)
    
    if not img_path.exists():
        return "", 404
    
    thumb_data = generate_thumbnail(img_path, max_size=300)
    if not thumb_data:
        return "", 404
    
    return send_file(
        BytesIO(thumb_data),
        mimetype="image/jpeg"
    )


@app.route("/gallery/export", methods=["POST"])
def gallery_export():
    """Export gallery metadata to JSON file."""
    data = request.get_json()
    folder_path = Path(data.get("folder_path", ""))
    filename = data.get("filename", "shot_dates_report.json")
    
    if not folder_path.exists():
        return jsonify({"error": "Folder not found"}), 400
    
    metadata = scan_folder_for_dates(folder_path)
    
    export_path = folder_path / filename
    
    with open(export_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    return jsonify({
        "success": True,
        "export_path": str(export_path)
    })


def run_desktop():
    """Run the app as a desktop application using PyWebView."""
    api = Api()
    webview.create_window(
        "Metadata App",
        app,
        width=1000,
        height=700,
        resizable=True,
        js_api=api
    )
    webview.start(debug=False)


@app.route("/duplicates")
def duplicates():
    """Duplicate finder page."""
    return render_template("duplicates.html")


@app.route("/gallery")
def gallery():
    """Gallery page."""
    return render_template("gallery.html")


if __name__ == "__main__":
    run_desktop()

#!/usr/bin/env python3
"""Main Flask application with PyWebView desktop wrapper."""

import json
import os
from pathlib import Path

import webview
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO

from config import BASE_DIR
from src.duplicate_finder import find_duplicates
from src.exif_extractor import scan_folder_for_dates
from src.file_operations import move_to_trash
from src.image_utils import generate_thumbnail, get_images_in_folder


class FolderSelectionAPI:
    """API for folder selection dialog."""
    
    def select_folder(self):
        """Open native folder selection dialog."""
        # This will be called from JavaScript
        # PyWebView doesn't have a built-in folder dialog,
        # so we'll handle this via JavaScript in the template
        return ""


api = FolderSelectionAPI()

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
    folder_path = Path(data.get("folder_path", ""))
    
    if not folder_path.exists() or not folder_path.is_dir():
        return jsonify({"error": "Invalid folder path"}), 400
    
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
    folder_path = Path(data.get("folder_path", ""))
    
    if not folder_path.exists() or not folder_path.is_dir():
        return jsonify({"error": "Invalid folder path"}), 400
    
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
    webview.create_window(
        "Metadata App",
        app,
        width=1000,
        height=700,
        resizable=True
    )
    webview.start(debug=False, func=api)


@app.route("/duplicates")
def duplicates():
    """Duplicate finder page."""
    return render_template("duplicates.html")


@app.route("/gallery")
def gallery():
    """Gallery page."""
    return render_template("gallery.html")


@app.route("/select-folder", methods=["POST"])
def select_folder():
    """Handle folder selection via file input."""
    if 'folder' not in request.files:
        return jsonify({"error": "No folder selected"}), 400
    
    file = request.files['folder']
    if not file.filename:
        return jsonify({"error": "No folder selected"}), 400
    
    # Get the folder path from the file path
    folder_path = os.path.dirname(file.filename)
    
    return jsonify({"folder_path": folder_path})


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        app.run(debug=True, port=5000)
    else:
        run_desktop()

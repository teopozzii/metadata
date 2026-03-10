# AGENTS.md - Agent Coding Guidelines

## Project Overview

This is a Python desktop application for working with image metadata on macOS. It provides:
- A desktop GUI for finding and removing duplicate images
- A gallery view for viewing and exporting EXIF shot dates

## Technology Stack

- **Flask**: Web framework for the UI
- **PyWebView**: Desktop wrapper for native window
- **Pillow**: Image processing and thumbnail generation
- **imagehash**: Perceptual hashing for duplicate detection
- **exifread**: EXIF metadata extraction
- **send2trash**: Safe file deletion (moves to Trash)
- **osascript**: Native macOS folder dialog (via Python subprocess)

## Dependencies

Install with: `pip install -r requirements.txt`

---

## Running the Application

```bash
python app.py
```

This opens the app in a native macOS window.

---

## Project Structure

```
metadata/
├── AGENTS.md              # This file
├── README.md              # Project documentation
├── app.py                 # Main Flask application + PyWebView entry
├── config.py              # App configuration
├── requirements.txt       # Python dependencies
├── src/
│   ├── __init__.py
│   ├── image_utils.py     # Image processing (hashing, thumbnails)
│   ├── duplicate_finder.py # Duplicate detection logic
│   ├── exif_extractor.py  # EXIF metadata extraction
│   └── file_operations.py # File operations (trash)
├── templates/
│   ├── base.html          # Base template with styling
│   ├── landing.html       # Landing page
│   ├── duplicates.html   # Duplicate finder UI
│   └── gallery.html      # Gallery view UI
└── static/
    ├── css/
    │   └── style.css     # Deep blue/dark orange theme
    └── js/
        └── script.js     # Client-side JavaScript
```

---

## Code Style Guidelines

### General Principles

- Write clean, readable code with clear variable/function names
- Keep functions focused and reasonably sized (under 100 lines preferred)
- Add docstrings to public functions explaining purpose and parameters
- Handle errors gracefully with informative error messages

### Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use blank lines to separate logical sections within functions
- Two blank lines between top-level definitions (functions, classes)

### Imports

- Use absolute imports with `from module import item` pattern
- Group imports in this order: stdlib, third-party, local
- Separate groups with a blank line
- Sort imports alphabetically within each group

### Naming Conventions

- **Functions/variables**: `snake_case` (e.g., `my_function`, `image_hash`)
- **Classes**: `PascalCase` (e.g., `ImageProcessor`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `THRESHOLD = 5`)
- **Private functions**: prefix with underscore (e.g., `_internal_function`)

### Type Hints

Type hints are recommended for function parameters and return values.

### Error Handling

- Use try/except blocks for operations that may fail
- Catch specific exceptions when possible
- Return JSON errors via `jsonify({"error": "message"})` for API routes

---

## UI/UX Guidelines

### Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Primary Background | Deep Blue | `#1a237e` |
| Secondary Background | Lighter Blue | `#283593` |
| Accent | Dark Orange | `#ff6f00` |
| Accent Hover | Orange | `#ff8f00` |
| Text | White | `#ffffff` |
| Success | Green | `#4caf50` |
| Danger | Red | `#f44336` |

### Template Structure

- Use Jinja2 templates in `templates/` directory
- CSS goes in `static/css/style.css`
- JavaScript goes in `static/js/script.js`
- All templates extend `base.html`

### JavaScript Patterns

- Use vanilla JavaScript (no frameworks)
- Use `fetch()` for API calls
- Folder selection is handled via `window.pywebview.api.select_folder()` which calls a Python function that uses osascript

---

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/duplicates` | GET | Duplicate finder page |
| `/duplicates/select-folder` | POST | Validate folder and get image count |
| `/duplicates/scan` | POST | Find duplicates |
| `/duplicates/thumbnail` | GET | Serve image thumbnail |
| `/duplicates/delete` | POST | Move file to trash |
| `/gallery` | GET | Gallery page |
| `/gallery/select-folder` | POST | Load folder metadata |
| `/gallery/thumbnail` | GET | Serve gallery thumbnail |
| `/gallery/export` | POST | Export report to JSON |

---

## Folder Selection Implementation

The app uses macOS's native folder dialog via osascript:

1. JavaScript calls `window.pywebview.api.select_folder()`
2. Python's `Api.select_folder()` runs: `subprocess.run(['osascript', '-e', 'POSIX path of (choose folder)'])`
3. The result is returned to JavaScript as a Promise

This approach is used instead of tkinter (which may not be available) or PyWebView's JavaScript API (which had compatibility issues).

---

## Testing

Manual testing only:
1. Run `python app.py`
2. Test folder selection in both components
3. Test duplicate detection and deletion
4. Test gallery view and export

For pytest (if tests are added):
```bash
pytest tests/test_file.py::test_function_name
pytest tests/test_file.py -k "test_function_name"
```

---

## Linting

```bash
# Install linting tools
pip install ruff black mypy

# Run ruff (linting)
ruff check .

# Run black (formatting)
black .

# Run mypy (type checking)
mypy .
```

---

## Notes for Agents

- This is a Flask + PyWebView desktop app (macOS only)
- No complex build systems or CI/CD
- All file deletions move files to Trash (recoverable)
- Supported image formats: jpg, jpeg, png, bmp, webp, tiff, tif
- Follow PEP 8 style guidelines
- The app is desktop-only (no web mode)

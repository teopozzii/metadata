# AGENTS.md - Agent Coding Guidelines

## Project Overview

This is a Python desktop application for working with image metadata. It provides:
- A desktop GUI for finding and removing duplicate images
- A gallery view for viewing and exporting EXIF shot dates

## Technology Stack

- **Flask**: Web framework for the UI
- **PyWebView**: Desktop wrapper for native window
- **Pillow**: Image processing and thumbnail generation
- **imagehash**: Perceptual hashing for duplicate detection
- **exifread**: EXIF metadata extraction
- **send2trash**: Safe file deletion (moves to Trash)

## Dependencies

Install with: `pip install -r requirements.txt`

---

## Running the Application

### Desktop Mode (Default)
```bash
python app.py
```

### Web Mode (for development/testing)
```bash
python app.py --web
```
Then open http://localhost:5000 in your browser.

---

## Project Structure

```
metadata/
├── AGENTS.md              # This file
├── README.md              # Project documentation
├── app.py                 # Main Flask application + desktop entry point
├── config.py              # App configuration
├── requirements.txt       # Python dependencies
├── src/
│   ├── __init__.py
│   ├── image_utils.py     # Image processing utilities
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
- Handle folder selection via the provided `openFolderPicker()` function

---

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/duplicates` | GET | Duplicate finder page |
| `/duplicates/select-folder` | POST | Initialize folder scan |
| `/duplicates/scan` | POST | Find duplicates |
| `/duplicates/thumbnail` | GET | Serve image thumbnail |
| `/duplicates/delete` | POST | Move file to trash |
| `/gallery` | GET | Gallery page |
| `/gallery/select-folder` | POST | Load folder metadata |
| `/gallery/thumbnail` | GET | Serve gallery thumbnail |
| `/gallery/export` | POST | Export report to JSON |

---

## Testing

There are currently no automated tests. To test manually:
1. Run `python app.py --web` 
2. Open http://localhost:5000
3. Test each component

For single-component testing via pytest (if tests are added):
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

- This is a simple Flask + PyWebView desktop app
- No complex build systems or CI/CD
- The app uses native file dialogs via PyWebView
- All file deletions move files to Trash (recoverable)
- Supported image formats: jpg, jpeg, png, bmp, webp, tiff, tif
- Follow PEP 8 style guidelines

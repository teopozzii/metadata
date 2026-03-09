# AGENTS.md - Agent Coding Guidelines

## Project Overview

This is a Python project for working with image metadata. It contains scripts to:
- Extract original creation dates from JPG files (`pic_dates.sh`)
- Find duplicate/similar images using perceptual hashing (`find_dup_pics.py`)

## Dependencies

- pillow
- imagehash
- rich
- questionary

Install with: `pip install -r requirements.txt`

---

## Build / Lint / Test Commands

### Running the Scripts

```bash
# Run the duplicate image finder
python find_dup_pics.py

# Run the pic dates extraction script
bash pic_dates.sh
```

### Testing

There are currently no automated tests in this repository. If tests are added:
- Use `pytest` as the test framework
- Place tests in a `tests/` directory

To run a single test with pytest:
```bash
pytest tests/test_file.py::test_function_name
pytest tests/test_file.py -k "test_function_name"
```

### Linting and Code Quality

This project does not currently have formal linting configured. When adding linting:

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

Example:
```python
def function_one():
    """Short description."""
    pass


def function_two():
    """Short description."""
    pass
```

### Imports

- Use absolute imports with `from module import item` pattern
- Group imports in this order: stdlib, third-party, local
- Separate groups with a blank line
- Sort imports alphabetically within each group

Example:
```python
import os
import sys
from pathlib import Path

from PIL import Image
import imagehash
from rich.console import Console

from mypackage import mymodule
```

### Naming Conventions

- **Functions/variables**: `snake_case` (e.g., `my_function`, `image_hash`)
- **Classes**: `PascalCase` (e.g., `ImageProcessor`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `THRESHOLD = 5`)
- **Private functions**: prefix with underscore (e.g., `_internal_function`)
- Use descriptive names: prefer `image_files` over `files` or `imgs`

### Type Hints

Type hints are recommended for function parameters and return values:

```python
def process_image(image_path: Path, threshold: int = 5) -> dict[str, str]:
    """Process a single image.
    
    Args:
        image_path: Path to the image file
        threshold: Similarity threshold (default 5)
    
    Returns:
        Dictionary with processing results
    """
    ...
```

### Error Handling

- Use try/except blocks for operations that may fail
- Catch specific exceptions when possible
- Provide informative error messages that help debugging
- Log errors appropriately (use `rich.console.Console` for user-facing errors)

Example:
```python
try:
    with Image.open(img_path) as img:
        img_hash = imagehash.phash(img)
except PermissionError:
    console.print(f"[red]Permission denied: {img_path}[/red]")
except Exception as e:
    errors.append((img_path.name, str(e)))
```

### Rich Console Usage

When using `rich` for console output:
- Use color codes: `[red]`, `[green]`, `[cyan]`, `[yellow]`, `[bold]`
- Use `console.print()` for output
- Use `track()` for progress bars
- Use `Table` for structured data display
- Use `Panel` for headers/messages

Example:
```python
console.print(f"[bold green]✓ Processed {count} images[/bold green]")
```

### File Path Handling

- Use `pathlib.Path` for all file path operations
- Use `.resolve()` to get absolute paths when needed
- Check file existence before processing

### Questionary Usage

When using `questionary` for interactive menus:
- Use appropriate icons in titles (📂, 📁, ✅, ⚠️, 🔍)
- Handle `None` return (user pressed Ctrl+C)
- Provide clear navigation options

Example:
```python
selection = questionary.select(
    "Choose an option:",
    choices=[
        questionary.Choice(title="📂 Select folder", value="select"),
        questionary.Choice(title="⬆️  Go up", value="up"),
    ]
).ask()
```

---

## File Structure

```
metadata/
├── AGENTS.md              # This file
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── find_dup_pics.py      # Main duplicate finder script
├── pic_dates.sh          # Shell script for date extraction
├── docs/
│   └── ex1.png           # Documentation images
└── .gitignore
```

---

## Common Tasks

### Running the Duplicate Finder

```bash
python find_dup_pics.py
```

The script will:
1. Open an interactive folder navigator
2. Scan selected folder for images (jpg, jpeg, png)
3. Calculate perceptual hashes for all images
4. Compare pairs to find duplicates within threshold
5. Display results in a formatted table

### Adding a New Dependency

1. Install: `pip install <package>`
2. Add to `requirements.txt`
3. Update this AGENTS.md if it introduces new patterns

---

## Notes for Agents

- This is a small, simple Python project - no complex build systems
- No CI/CD pipeline currently configured
- Scripts are intended to be run directly with `python` or `bash`
- Follow PEP 8 style guidelines for any new code
- Test any changes manually since no automated tests exist

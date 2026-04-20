# Contributing to Medium Keyboard Publisher

## Welcome!

Thank you for your interest in contributing to the Medium Keyboard Publisher! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Submitting Changes](#submitting-changes)

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Windows 10/11 (OS-level input requires Windows)
- Basic understanding of Python, PyQt6, and pyautogui

### First Steps

1. Clone the repository
2. Set up your development environment (see below)
3. Run the application to verify everything works

## Development Setup

### 1. Create Virtual Environment

From the workspace root (the folder containing `medium_publisher/`):

```cmd
python -m venv venv
```

### 2. Activate Virtual Environment

```cmd
venv\Scripts\activate
```

### 3. Install Dependencies

```cmd
pip install -r medium_publisher/requirements.txt
```

**Core dependencies**: PyQt6, pyautogui, pynput, Pillow, pywin32, pycryptodome, markdown2, PyYAML, python-dotenv, keyring

### 4. Run Tests

```cmd
python -m pytest medium_publisher/tests/
```

### 5. Run Application

```cmd
python -m medium_publisher.main
```

## Project Structure

```
medium_publisher/
├── ui/                    # PyQt6 desktop GUI
│   ├── main_window.py
│   ├── settings_dialog.py
│   ├── file_selector.py
│   ├── progress_widget.py
│   └── log_widget.py
├── automation/            # OS-level input and typing
│   ├── os_input_controller.py   # pyautogui keyboard/mouse wrapper
│   ├── content_typer.py         # Article typing with formatting
│   ├── human_typing_simulator.py # Typo generation and timing
│   ├── deferred_typo_tracker.py  # Review pass typo tracking
│   └── version_update_typer.py   # Version update via Ctrl+F/select/type
├── navigation/            # Screen recognition and login
│   ├── screen_recognition.py    # pyautogui.locateOnScreen() wrapper
│   ├── login_detector.py        # Detects login state via screen images
│   └── navigation_state_machine.py
├── safety/                # Emergency stop and focus detection
│   ├── emergency_stop.py        # Hotkey + mouse corner + UI stop
│   └── focus_window_detector.py # Detects if browser has focus
├── core/                  # Business logic
│   ├── article_parser.py        # Markdown parsing
│   ├── markdown_processor.py    # Content block generation
│   ├── change_parser.py         # Version update instruction parsing
│   ├── config_manager.py        # YAML configuration
│   ├── models.py                # Data models (ContentBlock, Format, etc.)
│   ├── publishing_workflow.py   # Orchestrates the full workflow
│   ├── session_manager.py       # Session state persistence
│   └── version_diff_detector.py # Detects changes between versions
├── utils/                 # Utilities
│   ├── logger.py
│   ├── validators.py
│   ├── exceptions.py
│   └── error_recovery.py
├── assets/                # Reference PNG images for screen recognition
│   └── medium/
├── config/                # Default configuration
│   └── default_config.yaml
├── tests/                 # Test suite
│   ├── unit/
│   ├── integration/
│   ├── property/
│   └── ui/
├── docs/                  # Documentation
├── main.py                # Entry point
├── build.cmd              # PyInstaller build script
├── create_installer.cmd   # Inno Setup installer script
└── requirements.txt
```

## Coding Standards

### Python Style Guide

We follow **PEP 8** with modifications:

- **Line length**: 100 characters
- **Formatter**: Black
- **Linter**: Ruff
- **Type checker**: mypy (strict mode)

### Code Formatting

```cmd
black medium_publisher/
ruff check medium_publisher/
mypy medium_publisher/
```

### Naming Conventions

- **Functions/Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Private methods**: `_leading_underscore`

### Type Hints

**Always use type hints** for function signatures:

```python
def parse_file(self, file_path: str) -> Article:
    """Parse markdown file.
    
    Args:
        file_path: Path to markdown file
    
    Returns:
        Parsed article object
    
    Raises:
        FileError: If file not found
    """
    pass
```

### Docstrings

Use **Google-style docstrings** for all public methods and classes.

### Error Handling

```python
# Good: Specific exceptions with context
try:
    article = parser.parse_file(path)
except FileNotFoundError:
    logger.error(f"File not found: {path}")
    raise FileError(f"Cannot find article: {path}")

# Bad: Bare except
try:
    article = parser.parse_file(path)
except:  # Don't do this!
    pass
```

### Logging

```python
from medium_publisher.utils.logger import get_logger

logger = get_logger(__name__)

logger.debug("Detailed information for debugging")
logger.info("General information about progress")
logger.warning("Warning about potential issues")
logger.error("Error that needs attention")
```

### Threading

The application uses **QThread** for background typing operations. Never use `async/await` — all I/O is synchronous with `time.sleep()` for delays.

```python
# Good: QThread for background work
class TypingWorker(QThread):
    progress = pyqtSignal(int)
    
    def run(self):
        # Typing happens here (blocking, synchronous)
        self.content_typer.type_article(blocks)

# Bad: async/await (not used in this project)
async def type_article():  # Don't do this!
    await page.keyboard.type(text)
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/              # Unit tests (fast, isolated)
├── integration/       # Integration tests (OS input mocked)
├── property/          # Property-based tests (Hypothesis)
└── ui/               # UI tests (PyQt6)
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from medium_publisher.automation.content_typer import ContentTyper

def test_type_header_level_2():
    """Test that level 2 headers use Ctrl+Alt+1."""
    mock_input = Mock()
    mock_simulator = Mock()
    mock_tracker = Mock()
    mock_config = Mock()
    mock_config.get.return_value = 200
    
    typer = ContentTyper(mock_input, mock_simulator, mock_tracker, mock_config)
    block = ContentBlock(type="header", content="My Header", level=2)
    
    typer.type_header(block)
    
    mock_input.hotkey.assert_any_call("ctrl", "alt", "1")
```

### Test Coverage

- **Minimum**: 80% code coverage
- **Run coverage**:
  ```cmd
  pytest --cov=medium_publisher --cov-report=html medium_publisher/tests/
  ```

## Submitting Changes

### Branch Naming

- **Feature**: `feature/description`
- **Bug fix**: `bugfix/description`
- **Documentation**: `docs/description`

### Commit Messages

Follow **Conventional Commits**:

```
feat(automation): add support for nested list typing
fix(safety): correct emergency stop key release order
docs(troubleshooting): add screen recognition section
```

### PR Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No `async/await` introduced
- [ ] OS-level input goes through OS_Input_Controller
- [ ] Safety checks (emergency stop, focus detection) preserved

---

**Last Updated**: 2025-03-01

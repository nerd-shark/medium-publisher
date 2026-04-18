# Contributing to Medium Article Publisher

## Welcome!

Thank you for your interest in contributing to the Medium Article Publisher! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Project Structure](#project-structure)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Submitting Changes](#submitting-changes)
8. [Documentation](#documentation)
9. [Issue Reporting](#issue-reporting)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what is best for the project
- Show empathy towards other contributors

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Publishing others' private information
- Other conduct that would be inappropriate in a professional setting

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Basic understanding of Python, PyQt6, and Playwright
- Familiarity with markdown and Medium's platform

### First Steps

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/medium-article-publisher.git
   cd medium-article-publisher
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/medium-article-publisher.git
   ```

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows**:
```bash
venv\Scripts\activate
```

**Linux/Mac**:
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### 5. Run Tests

```bash
pytest
```

### 6. Run Application

```bash
python medium_publisher/main.py
```

## Project Structure

```
medium_publisher/
├── ui/                 # PyQt6 user interface
│   ├── main_window.py
│   ├── settings_dialog.py
│   └── ...
├── core/              # Business logic
│   ├── article_parser.py
│   ├── markdown_processor.py
│   └── ...
├── automation/        # Browser automation
│   ├── playwright_controller.py
│   ├── medium_editor.py
│   └── ...
├── utils/             # Utilities
│   ├── logger.py
│   ├── validators.py
│   └── ...
├── config/            # Configuration files
│   ├── default_config.yaml
│   └── selectors.yaml
├── tests/             # Test suite
│   ├── unit/
│   ├── integration/
│   └── ui/
└── docs/              # Documentation
```

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line length**: 100 characters (not 79)
- **Formatter**: Black
- **Linter**: Ruff
- **Type checker**: mypy (strict mode)

### Code Formatting

```bash
# Format code with Black
black medium_publisher/

# Lint with Ruff
ruff check medium_publisher/

# Type check with mypy
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

Use **Google-style docstrings**:

```python
def calculate_time(chars: int, typo_rate: float) -> int:
    """Calculate estimated typing time.
    
    Args:
        chars: Number of characters to type
        typo_rate: Typo rate (0.0-1.0)
    
    Returns:
        Estimated time in seconds
    
    Example:
        >>> calculate_time(1000, 0.05)
        2057
    """
    pass
```

### Error Handling

```python
# Good: Specific exceptions with context
try:
    article = parser.parse_file(path)
except FileNotFoundError:
    logger.error(f"File not found: {path}")
    raise FileError(f"Cannot find article: {path}")
except yaml.YAMLError as e:
    logger.error(f"Invalid YAML: {e}")
    raise ContentError(f"Invalid frontmatter in {path}")

# Bad: Bare except
try:
    article = parser.parse_file(path)
except:  # Don't do this!
    pass
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Detailed information for debugging")
logger.info("General information about progress")
logger.warning("Warning about potential issues")
logger.error("Error that needs attention")
logger.exception("Error with full traceback")
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/              # Unit tests (fast, isolated)
│   ├── test_article_parser.py
│   ├── test_markdown_processor.py
│   └── ...
├── integration/       # Integration tests (slower, dependencies)
│   ├── test_playwright_controller.py
│   ├── test_medium_editor.py
│   └── ...
└── ui/               # UI tests (PyQt6)
    ├── test_main_window.py
    └── ...
```

### Writing Tests

```python
import pytest
from medium_publisher.core.article_parser import ArticleParser

def test_parse_frontmatter():
    """Test frontmatter extraction."""
    parser = ArticleParser()
    content = """---
title: Test Article
tags: [python, testing]
---
Article body"""
    
    frontmatter = parser.extract_frontmatter(content)
    
    assert frontmatter['title'] == 'Test Article'
    assert frontmatter['tags'] == ['python', 'testing']

@pytest.mark.asyncio
async def test_browser_navigation():
    """Test browser navigation."""
    controller = PlaywrightController(headless=True)
    await controller.initialize()
    
    try:
        await controller.navigate("https://medium.com")
        # Assertions here
    finally:
        await controller.close()
```

### Test Coverage

- **Minimum**: 80% code coverage
- **Run coverage**:
  ```bash
  pytest --cov=medium_publisher --cov-report=html
  ```
- **View report**: Open `htmlcov/index.html`

### Mocking

```python
from unittest.mock import Mock, patch, AsyncMock

@patch('medium_publisher.automation.playwright_controller.PlaywrightController')
def test_with_mock(mock_controller):
    """Test with mocked controller."""
    mock_controller.return_value.navigate = AsyncMock()
    
    # Test code here
```

## Submitting Changes

### Branch Naming

- **Feature**: `feature/description`
- **Bug fix**: `bugfix/description`
- **Documentation**: `docs/description`
- **Refactoring**: `refactor/description`

Examples:
- `feature/add-linkedin-support`
- `bugfix/fix-typo-generation`
- `docs/update-api-reference`

### Commit Messages

Follow **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(automation): add support for LinkedIn publishing

Implement LinkedIn API integration for cross-platform publishing.
Includes authentication, content formatting, and error handling.

Closes #123
```

```
fix(typo-simulator): correct QWERTY layout for 'p' key

The adjacent keys for 'p' were incorrect, causing unrealistic typos.
Updated ADJACENT_KEYS map with correct neighbors.

Fixes #456
```

### Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Make changes and commit**:
   ```bash
   git add .
   git commit -m "feat: add my feature"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/my-feature
   ```

5. **Create Pull Request** on GitHub

6. **PR Checklist**:
   - [ ] Code follows style guidelines
   - [ ] All tests pass
   - [ ] New tests added for new features
   - [ ] Documentation updated
   - [ ] Commit messages follow conventions
   - [ ] No merge conflicts

### Code Review

- Be open to feedback
- Respond to comments promptly
- Make requested changes
- Keep discussions professional and constructive

## Documentation

### When to Update Documentation

- Adding new features
- Changing existing behavior
- Fixing bugs that affect usage
- Improving code clarity

### Documentation Types

1. **Code Comments**: Explain complex logic
2. **Docstrings**: Document all public functions/classes
3. **User Documentation**: Update user guides
4. **Developer Documentation**: Update architecture/API docs
5. **README**: Keep README.md current

### Documentation Style

- **Clear and concise**: Avoid jargon
- **Examples**: Include code examples
- **Up-to-date**: Keep in sync with code
- **Complete**: Cover all features

## Issue Reporting

### Before Creating an Issue

1. **Search existing issues**: Check if already reported
2. **Check documentation**: Verify it's not a usage issue
3. **Test with latest version**: Ensure bug still exists

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Windows 10
- Python: 3.11.5
- Version: 1.0.0

**Logs**
```
Relevant log output
```

**Screenshots**
If applicable
```

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## Development Workflow

### Typical Workflow

1. **Pick an issue** from the issue tracker
2. **Comment on issue** to claim it
3. **Create branch** from main
4. **Implement changes** with tests
5. **Run tests** and linters
6. **Update documentation**
7. **Commit changes** with good messages
8. **Push to fork**
9. **Create PR** with description
10. **Address review feedback**
11. **Merge** when approved

### Tips for Success

- **Start small**: Begin with small contributions
- **Ask questions**: Don't hesitate to ask for help
- **Be patient**: Reviews may take time
- **Stay engaged**: Respond to feedback promptly
- **Learn**: Use contributions as learning opportunities

## Getting Help

### Resources

- **Documentation**: Check `docs/` directory
- **Issues**: Search existing issues
- **Discussions**: GitHub Discussions
- **Email**: maintainer@example.com

### Questions

- **Usage questions**: GitHub Discussions
- **Bug reports**: GitHub Issues
- **Feature requests**: GitHub Issues
- **Security issues**: Email maintainer directly

## Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Project README

Thank you for contributing to Medium Article Publisher!

---

**Document Version**: 1.0
**Last Updated**: 2025-03-01
**Maintained By**: Development Team

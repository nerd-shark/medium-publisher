# Medium Article Publisher

A desktop application that automates publishing markdown articles to Medium using browser automation.

## Overview

Medium Article Publisher is a Python-based desktop application that streamlines the process of publishing articles to Medium. It reads markdown files from your local filesystem, parses their content and metadata, and uses browser automation (Playwright) to type the content into Medium's editor with proper formatting.

## Features

- **Markdown Support**: Parse markdown files with YAML frontmatter
- **Browser Automation**: Automated typing into Medium's editor using Playwright
- **Human-Like Typing**: Simulate realistic typing patterns with configurable speed and typos
- **Rate Limiting**: Enforce 35 characters per minute limit to comply with Medium's policies
- **Draft URL Support**: Navigate to existing drafts or create new stories
- **Version Management**: Iteratively update articles through multiple versions
- **Format Preservation**: Convert markdown formatting to Medium's rich text format
- **Batch Publishing**: Publish multiple articles in sequence
- **Desktop UI**: Native PyQt6 interface for easy interaction
- **Secure Credentials**: Store login credentials using OS keychain

## Requirements

- Windows 10/11
- Python 3.11+
- Internet connection
- Valid Medium account

## Installation

### 1. Clone the Repository

```cmd
git clone <repository-url>
cd medium_publisher
```

### 2. Create Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```cmd
playwright install chromium
```

## Project Structure

```
medium_publisher/
├── ui/                     # PyQt6 UI components
│   ├── main_window.py
│   ├── settings_dialog.py
│   ├── progress_widget.py
│   └── file_selector.py
├── core/                   # Core logic
│   ├── article_parser.py
│   ├── markdown_processor.py
│   ├── config_manager.py
│   └── session_manager.py
├── automation/             # Browser automation
│   ├── playwright_controller.py
│   ├── medium_editor.py
│   ├── auth_handler.py
│   └── content_typer.py
├── utils/                  # Utilities
│   ├── logger.py
│   ├── validators.py
│   └── exceptions.py
├── config/                 # Configuration files
│   ├── default_config.yaml
│   └── selectors.yaml
├── tests/                  # Test suite
│   ├── unit/
│   ├── integration/
│   └── ui/
├── main.py                 # Application entry point
└── requirements.txt        # Python dependencies
```

## Usage

### Basic Workflow

1. **Launch Application**
   ```cmd
   python main.py
   ```

2. **Select Markdown File**
   - Click "Select File" button
   - Choose a markdown file with YAML frontmatter

3. **Login to Medium**
   - Click "Login" button
   - Enter credentials in browser
   - Complete 2FA if enabled

4. **Publish Article**
   - Review article metadata
   - Optionally enter draft URL
   - Click "Publish Version"
   - Wait for typing to complete
   - Review in browser
   - Manually insert tables/images at TODO markers

### Markdown Format

Articles should have YAML frontmatter:

```markdown
---
title: "Article Title"
subtitle: "Article Subtitle"
tags:
  - tag1
  - tag2
  - tag3
keywords:
  - keyword1
  - keyword2
status: draft
---

## Introduction

Your article content here...
```

### Configuration

Edit `config/default_config.yaml` to customize:

- Typing speed (10-100ms per character)
- Human-like typing (enabled/disabled)
- Typo frequency (low/medium/high)
- Default publish mode (draft/public)
- Browser visibility (visible/headless)

## Rate Limiting

**IMPORTANT**: The application enforces a hard limit of 35 characters per minute to comply with Medium's policies and avoid detection. Large articles may take significant time to publish.

Example: A 1000-character article with medium typo frequency will take approximately 35-40 minutes to publish.

## Development

### Running Tests

```cmd
REM Run all tests
pytest

REM Run with coverage
pytest --cov=medium_publisher --cov-report=html

REM Run specific test file
pytest tests\unit\test_article_parser.py
```

### Code Quality

```cmd
REM Format code
black medium_publisher

REM Lint code
ruff check medium_publisher

REM Type checking
mypy medium_publisher
```

## Architecture

The application follows a layered architecture:

1. **UI Layer**: PyQt6 desktop interface
2. **Core Layer**: Article parsing and processing logic
3. **Automation Layer**: Playwright browser automation

See `.kiro/specs/medium-article-publisher/design.md` for detailed architecture documentation.

## Security

- Credentials stored securely using OS keychain (keyring library)
- Session cookies encrypted
- No passwords logged
- Input validation and sanitization

## Limitations

- Tables and images require manual insertion (TODO placeholders)
- Rate limited to 35 characters per minute
- Requires stable internet connection
- Medium's UI changes may break selectors

## Troubleshooting

### Browser Not Opening
- Ensure Playwright browsers are installed: `playwright install chromium`
- Check browser visibility setting in config

### Login Fails
- Verify credentials are correct
- Complete 2FA manually when prompted
- Check network connection

### Typing Too Slow
- Rate limit is enforced at 35 chars/min (non-configurable)
- Disable human-like typing to reduce overhead
- Consider publishing shorter articles

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run code quality checks
5. Submit pull request

## License

[Your License Here]

## Support

For issues and questions, please open an issue on the repository.

## Roadmap

- [ ] Image upload automation
- [ ] Scheduling and queuing
- [ ] Article templates
- [ ] Analytics integration
- [ ] Multi-platform support (macOS, Linux)

## Acknowledgments

- Playwright for browser automation
- PyQt6 for desktop UI
- Medium for the publishing platform

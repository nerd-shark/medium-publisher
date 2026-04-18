# Medium Article Publisher - Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Layers](#component-layers)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Technology Stack](#technology-stack)
7. [Module Dependencies](#module-dependencies)

## Overview

The Medium Article Publisher is a desktop application built with a layered architecture that separates concerns between UI, business logic, and browser automation. The application follows SOLID principles and uses dependency injection for testability.

### Key Architectural Principles

1. **Separation of Concerns**: UI, business logic, and automation are in separate layers
2. **Dependency Injection**: Components receive dependencies rather than creating them
3. **Single Responsibility**: Each class has one clear purpose
4. **Interface Segregation**: Small, focused interfaces
5. **Open/Closed**: Open for extension, closed for modification

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Desktop Application                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              PyQt6 UI Layer                            │ │
│  │  - MainWindow (orchestration)                          │ │
│  │  - SettingsDialog (configuration)                      │ │
│  │  - ProgressWidget (feedback)                           │ │
│  │  - LogDisplayWidget (transparency)                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Application Logic Layer                      │ │
│  │  - ArticleParser (markdown parsing)                    │ │
│  │  - MarkdownProcessor (format conversion)               │ │
│  │  - ChangeParser (version instructions)                 │ │
│  │  - ConfigManager (settings)                            │ │
│  │  - SessionManager (state persistence)                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Browser Automation Layer                       │ │
│  │  - PlaywrightController (browser lifecycle)            │ │
│  │  - MediumEditor (editor interactions)                  │ │
│  │  - AuthHandler (authentication)                        │ │
│  │  - ContentTyper (typing with formatting)               │ │
│  │  - RateLimiter (typing rate control)                   │ │
│  │  - HumanTypingSimulator (realistic behavior)           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
              ┌────────────────────────┐
              │   Chromium Browser     │
              │   (Playwright)         │
              └────────────────────────┘
                           ↓
              ┌────────────────────────┐
              │      Medium.com        │
              └────────────────────────┘
```

## Component Layers

### 1. UI Layer (`ui/`)

**Purpose**: User interaction and visual feedback

**Components**:
- `MainWindow`: Primary application window, orchestrates workflows
- `SettingsDialog`: Configuration management UI
- `ProgressWidget`: Real-time progress feedback
- `LogDisplayWidget`: Operation transparency and debugging

**Responsibilities**:
- Capture user input
- Display application state
- Provide visual feedback
- Handle user events
- Delegate to business logic layer

**Design Pattern**: Model-View-Controller (MVC)
- View: PyQt6 widgets
- Controller: MainWindow event handlers
- Model: Core layer classes

### 2. Core Logic Layer (`core/`)

**Purpose**: Business logic and data processing

**Components**:
- `ArticleParser`: Parse markdown files and frontmatter
- `MarkdownProcessor`: Convert markdown to Medium format
- `ChangeParser`: Parse version update instructions
- `ConfigManager`: Application configuration
- `SessionManager`: State persistence

**Responsibilities**:
- Parse and validate input
- Transform data
- Manage application state
- Enforce business rules
- No UI or browser dependencies

**Design Pattern**: Service Layer
- Services operate independently
- Can be tested without UI or browser
- Reusable across different interfaces

### 3. Automation Layer (`automation/`)

**Purpose**: Browser control and Medium interaction

**Components**:
- `PlaywrightController`: Browser lifecycle management
- `MediumEditor`: Medium-specific editor interactions
- `AuthHandler`: Authentication workflows
- `ContentTyper`: Content typing with formatting
- `RateLimiter`: Typing rate enforcement
- `HumanTypingSimulator`: Realistic typing behavior

**Responsibilities**:
- Control browser
- Interact with Medium UI
- Simulate human behavior
- Handle authentication
- Enforce rate limits

**Design Pattern**: Facade + Strategy
- Facade: MediumEditor provides simple interface
- Strategy: Different typing strategies (human vs fast)

### 4. Utility Layer (`utils/`)

**Purpose**: Cross-cutting concerns

**Components**:
- `logger.py`: Logging configuration
- `validators.py`: Input validation
- `exceptions.py`: Custom exceptions

**Responsibilities**:
- Logging
- Validation
- Error handling
- Common utilities

## Data Flow

### Publishing Flow

```
1. User selects markdown file
   ↓
2. ArticleParser.parse_file()
   - Extract frontmatter (title, tags, subtitle)
   - Extract body content
   - Return Article object
   ↓
3. MarkdownProcessor.process()
   - Parse markdown syntax
   - Convert to ContentBlock list
   - Detect tables/images → placeholders
   ↓
4. AuthHandler.login() or restore_session()
   - Check existing session
   - Perform OAuth or email/password login
   - Save session cookies
   ↓
5. MediumEditor.create_new_story() or navigate_to_draft()
   - Navigate to editor
   - Clear existing content (if draft URL)
   ↓
6. ContentTyper.type_text()
   - RateLimiter.wait_if_needed()
   - HumanTypingSimulator.should_make_typo()
   - Type character by character
   - Apply formatting (bold, italic, headers)
   ↓
7. MediumEditor.add_tags() and add_subtitle()
   ↓
8. User reviews and publishes
```

### Version Update Flow

```
1. User selects version (v2, v3, etc.)
   ↓
2. User enters change instructions
   ↓
3. ChangeParser.parse_instructions()
   - Identify sections to modify
   - Extract search markers
   ↓
4. ArticleParser.parse_file() for new version
   ↓
5. MarkdownProcessor.compare_versions()
   - Identify changed sections
   ↓
6. For each change:
   a. MediumEditor.find_section()
   b. MediumEditor.select_section()
   c. MediumEditor.delete_selected_content()
   d. ContentTyper.type_text() (new content)
   ↓
7. User reviews changes
```

## Design Patterns

### 1. Dependency Injection

**Purpose**: Testability and flexibility

**Example**:
```python
class MediumEditor:
    def __init__(self, controller: PlaywrightController, 
                 typer: ContentTyper, config: dict):
        self.controller = controller
        self.typer = typer
        self.config = config
```

**Benefits**:
- Easy to mock dependencies in tests
- Can swap implementations
- Clear dependencies

### 2. Strategy Pattern

**Purpose**: Interchangeable algorithms

**Example**: Human typing vs fast typing
```python
class HumanTypingSimulator:
    def get_typing_delay(self, base_delay: int) -> int:
        # Add variation
        
class FastTypingSimulator:
    def get_typing_delay(self, base_delay: int) -> int:
        # No variation
```

### 3. Facade Pattern

**Purpose**: Simplify complex subsystems

**Example**: MediumEditor hides Playwright complexity
```python
class MediumEditor:
    async def type_content(self, blocks: List[ContentBlock]):
        # Hides complex Playwright interactions
        # Orchestrates ContentTyper, RateLimiter, etc.
```

### 4. Observer Pattern

**Purpose**: Event notification

**Example**: Progress updates
```python
class PublishingWorkflow:
    def __init__(self, progress_callback):
        self.progress_callback = progress_callback
        
    async def publish(self):
        self.progress_callback("Typing title...")
        # ...
        self.progress_callback("Typing content...")
```

### 5. Template Method Pattern

**Purpose**: Define algorithm skeleton

**Example**: Authentication flow
```python
class AuthHandler:
    async def login(self):
        # Template method
        await self._navigate_to_login()
        await self._perform_authentication()
        await self._save_session()
```

## Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.11+ | Application logic |
| UI Framework | PyQt6 | Desktop interface |
| Browser Automation | Playwright | Browser control |
| Markdown Parsing | markdown2 | Markdown to HTML |
| Configuration | PyYAML | Config files |
| Credentials | keyring | Secure storage |
| Testing | pytest | Unit/integration tests |

### Key Libraries

```python
# UI
PyQt6==6.6.0
PyQt6-Qt6==6.6.0

# Browser Automation
playwright==1.40.0

# Markdown Processing
markdown2==2.4.10

# Configuration
PyYAML==6.0.1
python-dotenv==1.0.0

# Security
keyring==24.3.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-qt==4.2.0
pytest-cov==4.1.0
```

## Module Dependencies

### Dependency Graph

```
ui/
├── depends on → core/
├── depends on → automation/
└── depends on → utils/

core/
├── depends on → utils/
└── no dependencies on ui/ or automation/

automation/
├── depends on → core/ (for data models)
├── depends on → utils/
└── no dependencies on ui/

utils/
└── no dependencies (leaf modules)
```

### Import Rules

1. **UI can import**: core, automation, utils
2. **Core can import**: utils only
3. **Automation can import**: core, utils
4. **Utils imports**: nothing (leaf modules)

### Circular Dependency Prevention

- Core layer is independent of UI and automation
- Data models in core/ are shared
- No circular imports between layers

## Configuration Architecture

### Configuration Hierarchy

```
1. Default values (code)
   ↓
2. default_config.yaml (shipped)
   ↓
3. User config file (user's home)
   ↓
4. Environment variables (highest priority)
```

### Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| `default_config.yaml` | `config/` | Default settings |
| `selectors.yaml` | `config/` | CSS selectors |
| `user_config.yaml` | `~/.medium_publisher/` | User overrides |
| `.env` | Project root | Environment vars |

## Error Handling Architecture

### Exception Hierarchy

```
PublishingError (base)
├── AuthenticationError
│   ├── InvalidCredentialsError
│   ├── OAuthTimeoutError
│   └── SessionExpiredError
├── BrowserError
│   ├── SelectorNotFoundError
│   ├── PageLoadTimeoutError
│   └── BrowserCrashError
├── ContentError
│   ├── InvalidMarkdownError
│   ├── MissingFrontmatterError
│   └── UnsupportedFormatError
└── FileError
    ├── FileNotFoundError
    ├── InvalidPathError
    └── PermissionError
```

### Error Handling Strategy

1. **Catch specific exceptions**: Handle known errors
2. **Retry logic**: Up to 3 attempts for transient errors
3. **User feedback**: Clear error messages
4. **Logging**: Detailed logs for debugging
5. **Graceful degradation**: Continue when possible

## Performance Considerations

### Rate Limiting

- **Hard limit**: 35 characters per minute
- **Implementation**: Sliding window algorithm
- **Enforcement**: RateLimiter class
- **Overhead**: Typo simulation adds 20-30% time

### Memory Management

- **Stream large files**: Don't load entirely in memory
- **Clear after use**: Delete ContentBlock objects after typing
- **Browser reuse**: Single browser instance per session
- **Log rotation**: Limit log file size to 10MB

### Async/Await

- **Browser operations**: All async for non-blocking
- **UI updates**: Qt signals for thread safety
- **Concurrent operations**: Where possible (file I/O)

## Security Architecture

### Credential Storage

- **OS keychain**: Use `keyring` library
- **Session cookies**: Encrypted storage
- **No plaintext**: Never store passwords in plaintext
- **Clear on logout**: Remove credentials when user logs out

### Input Validation

- **File paths**: Validate and sanitize
- **Markdown content**: Escape special characters
- **URLs**: Validate format and domain
- **User input**: Sanitize before use

### Browser Security

- **Isolated context**: Each session in separate browser context
- **No persistent storage**: Clear cookies on exit (unless "Remember Me")
- **HTTPS only**: All Medium communication over HTTPS

## Testing Architecture

### Test Structure

```
tests/
├── unit/
│   ├── test_article_parser.py
│   ├── test_markdown_processor.py
│   ├── test_change_parser.py
│   ├── test_rate_limiter.py
│   └── test_human_typing_simulator.py
├── integration/
│   ├── test_playwright_controller.py
│   ├── test_auth_handler.py
│   ├── test_medium_editor.py
│   └── test_end_to_end.py
└── ui/
    ├── test_main_window.py
    └── test_settings_dialog.py
```

### Test Coverage Goals

- **Unit tests**: 80% code coverage minimum
- **Integration tests**: Critical paths covered
- **UI tests**: Button states and workflows
- **End-to-end**: Full publishing flow

### Mocking Strategy

- **Browser**: Mock Playwright for unit tests
- **File system**: Use temporary directories
- **Network**: Mock HTTP requests
- **Time**: Mock time.sleep() for speed

## Deployment Architecture

### Packaging

- **Tool**: PyInstaller
- **Output**: Single executable
- **Includes**: Python runtime, dependencies, Playwright browsers
- **Platform**: Windows 10/11

### Installation

- **Installer**: Windows .msi or .exe
- **Location**: Program Files
- **Shortcuts**: Desktop and Start Menu
- **Uninstaller**: Standard Windows uninstall

### Updates

- **Check on startup**: Query for new version
- **Download**: Automatic download
- **Install**: User-initiated installation
- **Preserve**: User configuration and sessions

## Future Architecture Considerations

### Extensibility Points

1. **Platform abstraction**: Support other platforms (LinkedIn, Dev.to)
2. **Plugin system**: Custom markdown processors
3. **Template system**: Reusable article templates
4. **Scheduling**: Queue and schedule publications
5. **Analytics**: Track published articles and stats

### Scalability

- **Batch processing**: Parallel article processing
- **Cloud deployment**: Web-based version
- **API**: RESTful API for programmatic access
- **Database**: Store article history and metadata

---

**Document Version**: 1.0
**Last Updated**: 2025-03-01
**Maintained By**: Development Team

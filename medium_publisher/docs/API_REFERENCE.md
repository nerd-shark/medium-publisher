# Medium Article Publisher - API Reference

## Table of Contents
1. [Core Layer](#core-layer)
2. [Automation Layer](#automation-layer)
3. [UI Layer](#ui-layer)
4. [Utility Layer](#utility-layer)

## Core Layer

### ArticleParser

**Module**: `core.article_parser`

**Purpose**: Parse markdown files and extract article metadata

#### Class: `ArticleParser`

```python
class ArticleParser:
    """Parse markdown files with YAML frontmatter."""
    
    def __init__(self):
        """Initialize the parser."""
        pass
```

#### Methods

##### `parse_file(file_path: str) -> Article`

Parse a markdown file and return an Article object.

**Parameters**:
- `file_path` (str): Path to markdown file

**Returns**:
- `Article`: Parsed article with metadata and content

**Raises**:
- `FileError`: If file not found or not readable
- `ContentError`: If markdown format invalid

**Example**:
```python
parser = ArticleParser()
article = parser.parse_file("article.md")
print(article.title)  # "My Article Title"
```


##### `extract_frontmatter(content: str) -> dict`

Extract YAML frontmatter from markdown content.

**Parameters**:
- `content` (str): Full markdown content

**Returns**:
- `dict`: Frontmatter key-value pairs

**Raises**:
- `ContentError`: If frontmatter format invalid

**Example**:
```python
content = """---
title: My Article
tags: [python, tutorial]
---
Article body"""
frontmatter = parser.extract_frontmatter(content)
# {'title': 'My Article', 'tags': ['python', 'tutorial']}
```

##### `extract_body(content: str) -> str`

Extract article body (remove frontmatter).

**Parameters**:
- `content` (str): Full markdown content

**Returns**:
- `str`: Article body without frontmatter

##### `validate_article(article: Article) -> bool`

Validate article has required fields.

**Parameters**:
- `article` (Article): Article to validate

**Returns**:
- `bool`: True if valid

**Raises**:
- `ContentError`: If validation fails

#### Data Model: `Article`

```python
@dataclass
class Article:
    """Article data model."""
    title: str
    subtitle: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    status: str = "draft"  # "draft" or "public"
    file_path: str = ""
```

---

### MarkdownProcessor

**Module**: `core.markdown_processor`

**Purpose**: Convert markdown to Medium-compatible format

#### Class: `MarkdownProcessor`

```python
class MarkdownProcessor:
    """Process markdown and convert to ContentBlocks."""
    
    def __init__(self):
        """Initialize the processor."""
        pass
```

#### Methods

##### `process(markdown: str) -> List[ContentBlock]`

Convert markdown to list of content blocks.

**Parameters**:
- `markdown` (str): Markdown content

**Returns**:
- `List[ContentBlock]`: Structured content blocks

**Example**:
```python
processor = MarkdownProcessor()
blocks = processor.process("## Header\n\nParagraph with **bold**")
# [HeaderBlock(level=2, content="Header"), 
#  ParagraphBlock(content="Paragraph with ", formatting=[Bold(5, 9)])]
```

##### `parse_headers(line: str) -> Optional[HeaderBlock]`

Parse markdown headers (##, ###).

**Parameters**:
- `line` (str): Single line of markdown

**Returns**:
- `Optional[HeaderBlock]`: Header block or None

##### `parse_formatting(line: str) -> List[FormattedText]`

Parse inline formatting (bold, italic, code).

**Parameters**:
- `line` (str): Line with formatting

**Returns**:
- `List[FormattedText]`: Formatting spans

##### `parse_code_block(lines: List[str]) -> CodeBlock`

Parse code blocks (```language).

**Parameters**:
- `lines` (List[str]): Code block lines

**Returns**:
- `CodeBlock`: Code block with language

##### `parse_list(lines: List[str]) -> ListBlock`

Parse bullet/numbered lists.

**Parameters**:
- `lines` (List[str]): List lines

**Returns**:
- `ListBlock`: List block with items

##### `detect_table(lines: List[str]) -> Optional[TableBlock]`

Detect markdown tables and return placeholder.

**Parameters**:
- `lines` (List[str]): Potential table lines

**Returns**:
- `Optional[TableBlock]`: Placeholder block or None

##### `detect_image(line: str) -> Optional[ImageBlock]`

Detect markdown images and return placeholder.

**Parameters**:
- `line` (str): Line with potential image

**Returns**:
- `Optional[ImageBlock]`: Placeholder with alt text or None

##### `compare_versions(v1: str, v2: str) -> List[Change]`

Identify changed sections between versions.

**Parameters**:
- `v1` (str): Version 1 markdown
- `v2` (str): Version 2 markdown

**Returns**:
- `List[Change]`: Changed sections

#### Data Models

```python
@dataclass
class ContentBlock:
    """Base content block."""
    type: str  # "paragraph", "header", "code", "list", etc.
    content: str
    formatting: List[Format] = field(default_factory=list)
    level: int = 0  # For headers (2, 3, 4)
    metadata: dict = field(default_factory=dict)

@dataclass
class Format:
    """Inline formatting."""
    type: str  # "bold", "italic", "code", "link"
    start: int
    end: int
    url: str = ""  # For links
```

---

### ChangeParser

**Module**: `core.change_parser`

**Purpose**: Parse user change instructions for version updates

#### Class: `ChangeParser`

```python
class ChangeParser:
    """Parse version update instructions."""
    
    def __init__(self):
        """Initialize the parser."""
        pass
```

#### Methods

##### `parse_instructions(instructions: str) -> List[ChangeInstruction]`

Parse user change instructions.

**Parameters**:
- `instructions` (str): Natural language instructions

**Returns**:
- `List[ChangeInstruction]`: Parsed instructions

**Example**:
```python
parser = ChangeParser()
instructions = "Replace the introduction section with new content"
changes = parser.parse_instructions(instructions)
# [ChangeInstruction(action="replace", section="introduction", ...)]
```

##### `identify_sections(text: str) -> List[str]`

Identify section names in text.

**Parameters**:
- `text` (str): Text with section references

**Returns**:
- `List[str]`: Section names

##### `extract_search_markers(instruction: str) -> Tuple[str, str]`

Extract start/end markers for section search.

**Parameters**:
- `instruction` (str): Single instruction

**Returns**:
- `Tuple[str, str]`: (start_marker, end_marker)

#### Data Model

```python
@dataclass
class ChangeInstruction:
    """Change instruction."""
    action: str  # "replace", "add", "update", "delete"
    section: str  # Section name or identifier
    search_start: str = ""  # Start marker
    search_end: str = ""  # End marker
    new_content: str = ""  # Replacement content
```

---

### ConfigManager

**Module**: `core.config_manager`

**Purpose**: Manage application configuration

#### Class: `ConfigManager`

```python
class ConfigManager:
    """Manage application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize config manager.
        
        Args:
            config_path: Optional path to config file
        """
        pass
```

#### Methods

##### `load_config() -> dict`

Load configuration from file.

**Returns**:
- `dict`: Configuration dictionary

**Raises**:
- `FileError`: If config file not found

##### `save_config(config: dict)`

Save configuration to file.

**Parameters**:
- `config` (dict): Configuration to save

**Raises**:
- `FileError`: If cannot write config

##### `get(key: str, default=None) -> Any`

Get configuration value.

**Parameters**:
- `key` (str): Configuration key (dot notation supported)
- `default`: Default value if key not found

**Returns**:
- `Any`: Configuration value

**Example**:
```python
config = ConfigManager()
speed = config.get("typing.speed_ms", 30)
```

##### `set(key: str, value: Any)`

Set configuration value.

**Parameters**:
- `key` (str): Configuration key
- `value` (Any): Value to set

##### `validate() -> bool`

Validate configuration.

**Returns**:
- `bool`: True if valid

**Raises**:
- `ContentError`: If validation fails

---

### SessionManager

**Module**: `core.session_manager`

**Purpose**: Manage publishing session state

#### Class: `SessionManager`

```python
class SessionManager:
    """Manage session state."""
    
    def __init__(self, session_dir: str):
        """Initialize session manager.
        
        Args:
            session_dir: Directory for session files
        """
        pass
```

#### Methods

##### `start_session() -> str`

Initialize new publishing session.

**Returns**:
- `str`: Session ID

##### `save_state(state: dict)`

Save current state.

**Parameters**:
- `state` (dict): State to save

##### `restore_state() -> dict`

Restore previous state.

**Returns**:
- `dict`: Restored state

##### `clear_session()`

Clear session data.

---

## Automation Layer

### PlaywrightController

**Module**: `automation.playwright_controller`

**Purpose**: Manage Playwright browser instance

#### Class: `PlaywrightController`

```python
class PlaywrightController:
    """Control Playwright browser."""
    
    def __init__(self, headless: bool = False):
        """Initialize controller.
        
        Args:
            headless: Run browser in headless mode
        """
        pass
```

#### Methods

##### `async initialize()`

Initialize browser and context.

**Raises**:
- `BrowserError`: If browser fails to start

##### `async navigate(url: str)`

Navigate to URL.

**Parameters**:
- `url` (str): URL to navigate to

**Raises**:
- `BrowserError`: If navigation fails

##### `async wait_for_selector(selector: str, timeout: int = 30000)`

Wait for element to appear.

**Parameters**:
- `selector` (str): CSS selector
- `timeout` (int): Timeout in milliseconds

**Raises**:
- `BrowserError`: If element not found

##### `async close()`

Close browser.

---

### MediumEditor

**Module**: `automation.medium_editor`

**Purpose**: Interact with Medium's editor

#### Class: `MediumEditor`

```python
class MediumEditor:
    """Medium editor interface."""
    
    def __init__(self, controller: PlaywrightController, 
                 typer: ContentTyper, config: dict):
        """Initialize editor.
        
        Args:
            controller: Playwright controller
            typer: Content typer
            config: Configuration dict
        """
        pass
```

#### Methods

##### `async create_new_story()`

Navigate to new story page.

**Raises**:
- `BrowserError`: If navigation fails

##### `async navigate_to_draft(draft_url: str)`

Navigate to existing draft.

**Parameters**:
- `draft_url` (str): Medium draft URL

**Raises**:
- `BrowserError`: If URL invalid or navigation fails

##### `async validate_draft_url(url: str) -> bool`

Validate URL is a Medium draft/story.

**Parameters**:
- `url` (str): URL to validate

**Returns**:
- `bool`: True if valid Medium URL

##### `async clear_editor_content()`

Clear existing content in editor.

**Raises**:
- `BrowserError`: If clear fails

##### `async type_title(title: str)`

Type article title.

**Parameters**:
- `title` (str): Article title

**Raises**:
- `BrowserError`: If typing fails

##### `async type_content(blocks: List[ContentBlock])`

Type article content with formatting.

**Parameters**:
- `blocks` (List[ContentBlock]): Content blocks

**Raises**:
- `BrowserError`: If typing fails

##### `async find_section(search_text: str) -> bool`

Find section in editor by text search.

**Parameters**:
- `search_text` (str): Text to search for

**Returns**:
- `bool`: True if found

##### `async select_section(start_text: str, end_text: str)`

Select content between markers.

**Parameters**:
- `start_text` (str): Start marker
- `end_text` (str): End marker

**Raises**:
- `BrowserError`: If selection fails

##### `async delete_selected_content()`

Delete currently selected content.

**Raises**:
- `BrowserError`: If deletion fails

##### `async replace_section(search_text: str, new_blocks: List[ContentBlock])`

Find and replace a section.

**Parameters**:
- `search_text` (str): Section to find
- `new_blocks` (List[ContentBlock]): New content

**Raises**:
- `BrowserError`: If replacement fails

##### `async add_tags(tags: List[str])`

Add article tags.

**Parameters**:
- `tags` (List[str]): Tags (max 5)

**Raises**:
- `BrowserError`: If adding tags fails

##### `async add_subtitle(subtitle: str)`

Add article subtitle.

**Parameters**:
- `subtitle` (str): Subtitle text

**Raises**:
- `BrowserError`: If adding subtitle fails

##### `async publish(mode: str = "draft")`

Publish article.

**Parameters**:
- `mode` (str): "draft" or "public"

**Raises**:
- `BrowserError`: If publishing fails

---

### AuthHandler

**Module**: `automation.auth_handler`

**Purpose**: Handle Medium authentication

#### Class: `AuthHandler`

```python
class AuthHandler:
    """Handle authentication."""
    
    def __init__(self, controller: PlaywrightController, config: dict):
        """Initialize auth handler.
        
        Args:
            controller: Playwright controller
            config: Configuration dict
        """
        pass
```

#### Methods

##### `async login(email: Optional[str] = None, password: Optional[str] = None) -> bool`

Login to Medium.

**Parameters**:
- `email` (Optional[str]): Email address
- `password` (Optional[str]): Password

**Returns**:
- `bool`: True if login successful

**Raises**:
- `AuthenticationError`: If login fails

##### `async login_with_oauth() -> bool`

Login via Google OAuth (user-driven).

**Returns**:
- `bool`: True if login successful

**Raises**:
- `AuthenticationError`: If OAuth fails or times out

##### `async check_logged_in() -> bool`

Check if already logged in.

**Returns**:
- `bool`: True if logged in

##### `async wait_for_oauth_completion(timeout: int = 300) -> bool`

Wait for user to complete OAuth flow.

**Parameters**:
- `timeout` (int): Timeout in seconds

**Returns**:
- `bool`: True if completed successfully

**Raises**:
- `AuthenticationError`: If timeout or failure

##### `async detect_login_success() -> bool`

Detect successful login.

**Returns**:
- `bool`: True if login detected

##### `async save_session()`

Save session cookies.

**Raises**:
- `FileError`: If cannot save session

##### `async restore_session() -> bool`

Restore session from cookies.

**Returns**:
- `bool`: True if session restored

##### `async logout()`

Logout from Medium.

---

### ContentTyper

**Module**: `automation.content_typer`

**Purpose**: Type content with formatting and rate limiting

#### Class: `ContentTyper`

```python
class ContentTyper:
    """Type content with formatting."""
    
    def __init__(self, page, config: dict):
        """Initialize typer.
        
        Args:
            page: Playwright page object
            config: Configuration dict
        """
        self.rate_limiter = RateLimiter(max_chars_per_minute=35)
        self.human_simulator = HumanTypingSimulator(
            typo_frequency=config.get("typo_frequency", "low"),
            enabled=config.get("human_typing_enabled", True)
        )
        self.base_delay = config.get("typing_speed_ms", 30)
```

#### Methods

##### `async type_text(text: str)`

Type text with human-like behavior.

**Parameters**:
- `text` (str): Text to type

**Raises**:
- `BrowserError`: If typing fails

##### `async apply_bold(text: str)`

Type and apply bold formatting.

**Parameters**:
- `text` (str): Text to bold

##### `async apply_italic(text: str)`

Type and apply italic formatting.

**Parameters**:
- `text` (str): Text to italicize

##### `async apply_header(text: str, level: int)`

Type and apply header formatting.

**Parameters**:
- `text` (str): Header text
- `level` (int): Header level (2, 3, 4)

##### `async insert_code_block(code: str, language: str = "")`

Insert code block (no typos).

**Parameters**:
- `code` (str): Code content
- `language` (str): Programming language

##### `async insert_link(text: str, url: str)`

Insert link.

**Parameters**:
- `text` (str): Link text
- `url` (str): Link URL

##### `async insert_placeholder(placeholder_type: str, metadata: dict)`

Insert TODO placeholder.

**Parameters**:
- `placeholder_type` (str): "table" or "image"
- `metadata` (dict): Placeholder metadata

---

### RateLimiter

**Module**: `automation.rate_limiter`

**Purpose**: Enforce typing rate limits

#### Class: `RateLimiter`

```python
class RateLimiter:
    """Enforce typing rate limits."""
    
    def __init__(self, max_chars_per_minute: int = 35):
        """Initialize rate limiter.
        
        Args:
            max_chars_per_minute: Maximum characters per minute
        """
        self.max_chars_per_minute = max_chars_per_minute
        self.chars_typed = 0
        self.window_start = None
```

#### Methods

##### `async wait_if_needed(chars_to_type: int)`

Wait if typing would exceed rate limit.

**Parameters**:
- `chars_to_type` (int): Number of characters to type

**Implementation**: Sliding window algorithm

##### `reset_window()`

Reset the rate limit window.

##### `get_estimated_time(total_chars: int, typo_rate: float = 0.0) -> int`

Calculate estimated typing time.

**Parameters**:
- `total_chars` (int): Total characters
- `typo_rate` (float): Typo rate (0.0-1.0)

**Returns**:
- `int`: Estimated time in seconds

**Formula**:
```python
# Base characters
base_chars = total_chars

# Add typo overhead
typos = total_chars * typo_rate
correction_chars = typos * 4  # backspace + retype

# Total characters including corrections
total_with_typos = base_chars + correction_chars

# Time = chars / rate
time_seconds = (total_with_typos / max_chars_per_minute) * 60
```

---

### HumanTypingSimulator

**Module**: `automation.human_typing_simulator`

**Purpose**: Simulate realistic human typing

#### Class: `HumanTypingSimulator`

```python
class HumanTypingSimulator:
    """Simulate human typing behavior."""
    
    def __init__(self, typo_frequency: str = "low", enabled: bool = True):
        """Initialize simulator.
        
        Args:
            typo_frequency: "low" (2%), "medium" (5%), "high" (8%)
            enabled: Whether to simulate typos
        """
        self.enabled = enabled
        self.typo_rate = {"low": 0.02, "medium": 0.05, "high": 0.08}[typo_frequency]
```

#### Methods

##### `should_make_typo() -> bool`

Determine if next character should be a typo.

**Returns**:
- `bool`: True if should make typo

**Implementation**: Random based on typo_rate

##### `generate_typo(intended_char: str) -> str`

Generate realistic typo for character.

**Parameters**:
- `intended_char` (str): Intended character

**Returns**:
- `str`: Typo character (adjacent key)

**Implementation**: Uses QWERTY keyboard layout map

##### `get_correction_delay() -> int`

Get delay before correcting typo.

**Returns**:
- `int`: Delay in milliseconds (1-3 chars worth)

##### `get_typing_delay(base_delay: int) -> int`

Add random variation to typing delay.

**Parameters**:
- `base_delay` (int): Base delay in ms

**Returns**:
- `int`: Varied delay (±20%)

##### `get_thinking_pause() -> int`

Occasionally return longer pause.

**Returns**:
- `int`: Pause duration (100-500ms) or 0

##### `calculate_overhead(text_length: int) -> int`

Calculate extra time for typos.

**Parameters**:
- `text_length` (int): Text length

**Returns**:
- `int`: Extra seconds needed

---

## UI Layer

### MainWindow

**Module**: `ui.main_window`

**Purpose**: Primary application window

#### Class: `MainWindow(QMainWindow)`

```python
class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.setup_ui()
```

#### Methods

##### `select_file()`

Open file selection dialog.

##### `set_draft_url(url: str)`

Set draft URL from input.

**Parameters**:
- `url` (str): Medium draft URL

##### `set_version(version: str)`

Set current version.

**Parameters**:
- `version` (str): Version (v1, v2, v3, etc.)

##### `get_change_instructions() -> str`

Get user's change instructions.

**Returns**:
- `str`: Change instructions

##### `calculate_estimated_time() -> int`

Calculate estimated typing time.

**Returns**:
- `int`: Estimated seconds

##### `login()`

Trigger authentication.

##### `login_with_oauth()`

Trigger OAuth flow.

##### `publish_version()`

Start publishing current version.

##### `apply_changes()`

Apply changes for next version.

##### `update_status(message: str)`

Update status display.

**Parameters**:
- `message` (str): Status message

##### `update_progress(current: int, total: int)`

Update progress bar.

**Parameters**:
- `current` (int): Current progress
- `total` (int): Total items

---

### SettingsDialog

**Module**: `ui.settings_dialog`

**Purpose**: Configuration management UI

#### Class: `SettingsDialog(QDialog)`

```python
class SettingsDialog(QDialog):
    """Settings configuration dialog."""
    
    def __init__(self, config: ConfigManager, parent=None):
        """Initialize settings dialog.
        
        Args:
            config: Configuration manager
            parent: Parent widget
        """
        super().__init__(parent)
        self.config = config
        self.setup_ui()
```

#### Methods

##### `load_settings()`

Load current settings into UI.

##### `save_settings()`

Save settings from UI.

##### `reset_to_defaults()`

Reset all settings to defaults.

---

## Utility Layer

### Logger

**Module**: `utils.logger`

**Purpose**: Logging configuration

#### Functions

##### `setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger`

Set up logger with file and console handlers.

**Parameters**:
- `name` (str): Logger name
- `log_file` (str): Log file path
- `level`: Logging level

**Returns**:
- `logging.Logger`: Configured logger

---

### Validators

**Module**: `utils.validators`

**Purpose**: Input validation

#### Functions

##### `validate_file_path(path: str) -> bool`

Validate file path.

**Parameters**:
- `path` (str): File path

**Returns**:
- `bool`: True if valid

**Raises**:
- `FileError`: If invalid

##### `validate_markdown(content: str) -> bool`

Validate markdown content.

**Parameters**:
- `content` (str): Markdown content

**Returns**:
- `bool`: True if valid

**Raises**:
- `ContentError`: If invalid

##### `validate_draft_url(url: str) -> bool`

Validate Medium draft URL.

**Parameters**:
- `url` (str): URL to validate

**Returns**:
- `bool`: True if valid

**Raises**:
- `ContentError`: If invalid

##### `validate_tags(tags: List[str]) -> bool`

Validate article tags.

**Parameters**:
- `tags` (List[str]): Tags to validate

**Returns**:
- `bool`: True if valid

**Raises**:
- `ContentError`: If invalid (max 5, alphanumeric)

---

### Exceptions

**Module**: `utils.exceptions`

**Purpose**: Custom exceptions

#### Exception Hierarchy

```python
class PublishingError(Exception):
    """Base exception for publishing errors."""
    pass

class AuthenticationError(PublishingError):
    """Authentication failed."""
    pass

class BrowserError(PublishingError):
    """Browser automation error."""
    pass

class ContentError(PublishingError):
    """Content processing error."""
    pass

class FileError(PublishingError):
    """File operation error."""
    pass
```

---

**Document Version**: 1.0
**Last Updated**: 2025-03-01
**Maintained By**: Development Team

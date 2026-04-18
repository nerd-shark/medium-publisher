# Medium Article Publisher - Design

## Overview

The Medium Article Publisher is a desktop application that automates the process of publishing markdown articles to Medium. The application uses browser automation (Playwright) to interact with Medium's web editor, combined with a native desktop UI (PyQt6) for user interaction.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Desktop Application                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              PyQt6 UI Layer                            │ │
│  │  - Main Window                                         │ │
│  │  - File Selection Dialog                               │ │
│  │  - Settings Dialog                                     │ │
│  │  - Progress Display                                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Application Logic Layer                      │ │
│  │  - Article Parser                                      │ │
│  │  - Markdown Processor                                  │ │
│  │  - Configuration Manager                               │ │
│  │  - Session Manager                                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Browser Automation Layer                       │ │
│  │  - Playwright Controller                               │ │
│  │  - Medium Editor Interface                             │ │
│  │  - Authentication Handler                              │ │
│  │  - Content Typer                                       │ │
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

### Component Architecture

```
medium_publisher/
├── ui/
│   ├── __init__.py
│   ├── main_window.py          # Main application window
│   ├── settings_dialog.py      # Settings configuration UI
│   ├── progress_widget.py      # Progress display widget
│   ├── file_selector.py        # File selection dialog
│   └── version_manager.py      # Version selection and change instructions
├── core/
│   ├── __init__.py
│   ├── article_parser.py       # Parse markdown and frontmatter
│   ├── markdown_processor.py   # Convert markdown to Medium format
│   ├── config_manager.py       # Application configuration
│   ├── session_manager.py      # Session state management
│   └── change_parser.py        # Parse user change instructions
├── automation/
│   ├── __init__.py
│   ├── playwright_controller.py # Playwright browser control
│   ├── medium_editor.py        # Medium editor interactions
│   ├── auth_handler.py         # Authentication logic
│   └── content_typer.py        # Content typing with formatting
├── utils/
│   ├── __init__.py
│   ├── logger.py               # Logging configuration
│   ├── validators.py           # Input validation
│   └── exceptions.py           # Custom exceptions
├── config/
│   ├── default_config.yaml     # Default configuration
│   └── selectors.yaml          # Medium CSS selectors
├── main.py                     # Application entry point
└── requirements.txt            # Python dependencies
```

## Component Design

### 1. UI Layer (PyQt6)

#### MainWindow
**Responsibility**: Primary application interface

**Key Methods**:
- `__init__()`: Initialize UI components
- `select_file()`: Open file selection dialog
- `set_draft_url(url)`: Set draft URL from input field
- `set_version(version)`: Set current version (v1, v2, v3, etc.)
- `get_change_instructions()`: Get user's change instructions
- `login()`: Trigger authentication
- `publish_version()`: Start publishing current version
- `apply_changes()`: Apply changes for next version
- `update_status(message)`: Update status display
- `update_progress(current, total)`: Update progress bar

**UI Elements**:
- File path display (QLineEdit, read-only)
- Draft URL input (QLineEdit, optional)
- Version selector (QComboBox: v1, v2, v3, etc.)
- Current version display (QLabel)
- Change instructions input (QTextEdit, multi-line)
- Article info display (QLabel: character count, estimated time)
- Select File button (QPushButton)
- Login button (QPushButton)
- Publish Version button (QPushButton)
- Apply Changes button (QPushButton)
- Settings button (QPushButton)
- Status label (QLabel)
- Progress bar (QProgressBar)
- Log display (QTextEdit, read-only)

#### SettingsDialog
**Responsibility**: Configure application settings

**Settings**:
- Typing speed (slider, 10-100ms)
- Human-like typing (checkbox: enabled/disabled)
- Typo frequency (dropdown: low/medium/high, enabled when human-like typing on)
- Rate limit display (label, non-editable: "35 chars/min")
- Rate limit warning (label: "Large articles may take significant time")
- Default publish mode (radio: draft/public)
- Browser visibility (checkbox: visible/headless)
- Default article directory (file browser)
- Remember login (checkbox)

### 2. Core Layer

#### ArticleParser
**Responsibility**: Parse markdown files and extract metadata

**Key Methods**:
```python
class ArticleParser:
    def parse_file(self, file_path: str) -> Article:
        """Parse markdown file and return Article object"""
        
    def extract_frontmatter(self, content: str) -> dict:
        """Extract YAML frontmatter"""
        
    def extract_body(self, content: str) -> str:
        """Extract article body (remove frontmatter)"""
        
    def validate_article(self, article: Article) -> bool:
        """Validate article has required fields"""
```

**Data Model**:
```python
@dataclass
class Article:
    title: str
    subtitle: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    status: str = "draft"  # draft or public
    file_path: str = ""
```

#### MarkdownProcessor
**Responsibility**: Convert markdown to Medium-compatible format

**Key Methods**:
```python
class MarkdownProcessor:
    def process(self, markdown: str) -> List[ContentBlock]:
        """Convert markdown to list of content blocks"""
        
    def parse_headers(self, line: str) -> Optional[HeaderBlock]:
        """Parse markdown headers (##, ###)"""
        
    def parse_formatting(self, line: str) -> List[FormattedText]:
        """Parse inline formatting (bold, italic, code)"""
        
    def parse_code_block(self, lines: List[str]) -> CodeBlock:
        """Parse code blocks"""
        
    def parse_list(self, lines: List[str]) -> ListBlock:
        """Parse bullet/numbered lists"""
        
    def detect_table(self, lines: List[str]) -> Optional[TableBlock]:
        """Detect markdown tables and return placeholder"""
        
    def detect_image(self, line: str) -> Optional[ImageBlock]:
        """Detect markdown images and return placeholder"""
```

**Data Models**:
```python
@dataclass
class ContentBlock:
    type: str  # paragraph, header, code, list, table_placeholder, image_placeholder
    content: str
    formatting: List[Format] = field(default_factory=list)
    level: int = 0  # for headers (2, 3, 4)
    metadata: dict = field(default_factory=dict)  # for image alt text, table info

@dataclass
class Format:
    type: str  # bold, italic, code, link
    start: int
    end: int
    url: str = ""  # for links
```

#### ConfigManager
**Responsibility**: Manage application configuration

**Key Methods**:
```python
class ConfigManager:
    def load_config(self) -> dict:
        """Load configuration from file"""
        
    def save_config(self, config: dict):
        """Save configuration to file"""
        
    def get(self, key: str, default=None):
        """Get configuration value"""
        
    def set(self, key: str, value):
        """Set configuration value"""
```

**Configuration Structure**:
```yaml
typing:
  speed_ms: 30
  paragraph_delay_ms: 100
  max_chars_per_minute: 35  # HARD LIMIT - not user configurable
  human_typing_enabled: true
  typo_frequency: low  # low (2%), medium (5%), high (8%)
  
publishing:
  default_mode: draft  # draft or public
  auto_add_tags: true
  max_tags: 5
  remember_draft_url: true  # Remember last used draft URL
  
browser:
  headless: false
  timeout_seconds: 30
  
paths:
  last_directory: ""
  articles_directory: ""
  last_draft_url: ""  # Last used draft URL
  
credentials:
  remember_login: false
  # Actual credentials stored in OS keychain
```

#### SessionManager
**Responsibility**: Manage publishing session state

**Key Methods**:
```python
class SessionManager:
    def start_session(self):
        """Initialize new publishing session"""
        
    def save_state(self, state: dict):
        """Save current state"""
        
    def restore_state(self) -> dict:
        """Restore previous state"""
        
    def clear_session(self):
        """Clear session data"""
```

### 3. Automation Layer

#### PlaywrightController
**Responsibility**: Manage Playwright browser instance

**Key Methods**:
```python
class PlaywrightController:
    async def initialize(self, headless: bool = False):
        """Initialize browser and context"""
        
    async def navigate(self, url: str):
        """Navigate to URL"""
        
    async def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wait for element to appear"""
        
    async def close(self):
        """Close browser"""
```

#### MediumEditor
**Responsibility**: Interact with Medium's editor

**Key Methods**:
```python
class MediumEditor:
    async def create_new_story(self):
        """Navigate to new story page"""
        
    async def navigate_to_draft(self, draft_url: str):
        """Navigate to existing draft URL"""
        
    async def validate_draft_url(self, url: str) -> bool:
        """Validate URL is a Medium draft or story"""
        
    async def clear_editor_content(self):
        """Clear existing content in editor (for draft URLs)"""
        
    async def type_title(self, title: str):
        """Type article title"""
        
    async def type_content(self, blocks: List[ContentBlock]):
        """Type article content with formatting"""
        
    async def find_section(self, search_text: str) -> bool:
        """Find section in editor by text search"""
        
    async def select_section(self, start_text: str, end_text: str):
        """Select content between start and end markers"""
        
    async def delete_selected_content(self):
        """Delete currently selected content"""
        
    async def replace_section(self, search_text: str, new_blocks: List[ContentBlock]):
        """Find and replace a section with new content"""
        
    async def add_tags(self, tags: List[str]):
        """Add article tags"""
        
    async def add_subtitle(self, subtitle: str):
        """Add article subtitle"""
        
    async def publish(self, mode: str = "draft"):
        """Publish article (draft or public)"""
```

#### AuthHandler
**Responsibility**: Handle Medium authentication (email/password and Google OAuth)

**Key Methods**:
```python
class AuthHandler:
    async def login(self, email: str = None, password: str = None) -> bool:
        """Login to Medium (email/password or OAuth)"""
        
    async def login_with_oauth(self) -> bool:
        """Login to Medium via Google OAuth (user-driven)"""
        
    async def check_logged_in(self) -> bool:
        """Check if already logged in"""
        
    async def wait_for_oauth_completion(self, timeout: int = 300) -> bool:
        """Wait for user to complete OAuth flow"""
        
    async def detect_login_success(self) -> bool:
        """Detect successful login (any method)"""
        
    async def save_session(self):
        """Save session cookies"""
        
    async def restore_session(self) -> bool:
        """Restore session from cookies"""
        
    async def logout(self):
        """Logout from Medium"""
```

#### ContentTyper
**Responsibility**: Type content with proper formatting and rate limiting

**Key Methods**:
```python
class ContentTyper:
    def __init__(self, config: dict):
        self.rate_limiter = RateLimiter(max_chars_per_minute=35)
        self.human_simulator = HumanTypingSimulator(
            typo_frequency=config.get("typo_frequency", "low"),
            enabled=config.get("human_typing_enabled", True)
        )
        self.base_delay = config.get("typing_speed_ms", 30)
    
    async def type_text(self, text: str):
        """Type text with human-like behavior, rate limiting, and typos"""
        
    async def _type_character(self, char: str):
        """Type single character with possible typo and correction"""
        
    async def apply_bold(self, text: str):
        """Type and apply bold formatting"""
        
    async def apply_italic(self, text: str):
        """Type and apply italic formatting"""
        
    async def apply_header(self, text: str, level: int):
        """Type and apply header formatting"""
        
    async def insert_code_block(self, code: str, language: str = ""):
        """Insert code block (no typos in code)"""
        
    async def insert_link(self, text: str, url: str):
        """Insert link"""
        
    async def insert_placeholder(self, placeholder_type: str, metadata: dict):
        """Insert TODO placeholder for tables/images"""
```

#### RateLimiter
**Responsibility**: Enforce typing rate limits

**Key Methods**:
```python
class RateLimiter:
    def __init__(self, max_chars_per_minute: int = 35):
        """Initialize rate limiter with character limit"""
        self.max_chars_per_minute = max_chars_per_minute
        self.chars_typed = 0
        self.window_start = None
        
    async def wait_if_needed(self, chars_to_type: int):
        """Wait if typing would exceed rate limit"""
        
    def reset_window(self):
        """Reset the rate limit window"""
        
    def get_estimated_time(self, total_chars: int, typo_rate: float = 0.0) -> int:
        """Calculate estimated typing time in seconds (accounting for typos)"""
```

#### HumanTypingSimulator
**Responsibility**: Simulate realistic human typing patterns

**Key Methods**:
```python
class HumanTypingSimulator:
    def __init__(self, typo_frequency: str = "low", enabled: bool = True):
        """Initialize typing simulator
        
        Args:
            typo_frequency: "low" (2%), "medium" (5%), "high" (8%)
            enabled: Whether to simulate typos
        """
        self.enabled = enabled
        self.typo_rate = {"low": 0.02, "medium": 0.05, "high": 0.08}[typo_frequency]
        
    def should_make_typo(self) -> bool:
        """Determine if next character should be a typo"""
        
    def generate_typo(self, intended_char: str) -> str:
        """Generate realistic typo for character (adjacent key)"""
        
    def get_correction_delay(self) -> int:
        """Get delay before correcting typo (1-3 chars)"""
        
    def get_typing_delay(self, base_delay: int) -> int:
        """Add random variation to typing delay (±20%)"""
        
    def get_thinking_pause(self) -> int:
        """Occasionally return longer pause (100-500ms)"""
        
    def calculate_overhead(self, text_length: int) -> int:
        """Calculate extra time needed for typos and corrections"""
```

## Data Flow

### Publishing Flow (Single Version)

```
1. User selects markdown file
   ↓
2. User optionally enters Medium draft URL
   ↓
3. User selects version (v1, v2, v3, etc.)
   ↓
4. ArticleParser parses file for selected version
   ↓
5. MarkdownProcessor converts to ContentBlocks
   - Detects tables → creates "TODO: Insert table here" placeholder
   - Detects images → creates "TODO: Insert image here - [alt]" placeholder
   ↓
6. User clicks "Publish Version"
   ↓
7. AuthHandler checks/performs login
   ↓
8a. If draft URL provided:
    - MediumEditor navigates to draft URL
    - MediumEditor validates URL is Medium draft/story
    - MediumEditor clears existing content (if v1)
   ↓
8b. If no draft URL:
    - MediumEditor creates new story
   ↓
9. ContentTyper types title
   ↓
10. ContentTyper types content blocks (with formatting)
   - Regular text: typed with typos and corrections
   - Code blocks: typed without typos
   - Placeholders: typed as TODO lines
   ↓
11. MediumEditor adds tags and subtitle
   ↓
12. User reviews in browser
   ↓
13. User manually inserts tables/images at TODO markers
   ↓
14. Application pauses and waits for next action
```

### Iterative Version Update Flow

```
1. Version 1 is complete and published to draft
   ↓
2. User selects version 2 from dropdown
   ↓
3. User enters change instructions in text area:
   - "Replace the introduction section with new content"
   - "Add a new section after 'Design Principles'"
   - "Update the conclusion"
   ↓
4. User clicks "Apply Changes"
   ↓
5. ChangeParser parses instructions
   - Identifies sections to modify
   - Extracts search markers
   ↓
6. ArticleParser loads version 2 content
   ↓
7. MarkdownProcessor identifies changed sections
   ↓
8. For each change:
   a. MediumEditor finds section using search text
   b. MediumEditor selects content to replace
   c. MediumEditor deletes selected content
   d. ContentTyper types new content
   ↓
9. User reviews changes in browser
   ↓
10. Repeat for version 3, 4, etc.
   ↓
11. When all versions complete, user publishes final version
```

### Authentication Flow

```
1. User clicks "Login"
   ↓
2. AuthHandler checks for saved session
   ↓
3a. If session exists and valid:
    - Restore session
    - Skip to step 9
   ↓
3b. If no session or invalid:
    - Navigate to Medium login page
    ↓
4. Application displays login options to user:
   - "Enter email/password" (traditional)
   - "Use Google OAuth" (recommended for Google accounts)
   ↓
5a. Traditional Login Path:
    - User enters email and password
    - AuthHandler performs login
    - Handle 2FA if needed
    ↓
5b. Google OAuth Path:
    - Application shows: "Click 'Sign in with Google' in browser"
    - Browser remains visible
    - User clicks "Sign in with Google" on Medium
    - User completes Google OAuth flow
    - User completes Google 2FA if enabled
    - AuthHandler waits for login completion (polls for success)
    ↓
6. AuthHandler detects successful login
   ↓
7. AuthHandler saves session cookies
   ↓
8. Application displays "Logged in successfully"
   ↓
9. Ready to publish articles
```

**OAuth Flow Details**:
```
Google OAuth Flow (User-Driven):
1. App opens Medium login page
2. App displays: "Click 'Sign in with Google' and complete authentication"
3. User clicks "Sign in with Google" button
4. Medium redirects to Google OAuth page
5. User enters Google email (if not already logged in)
6. User enters Google password
7. User completes 2FA if enabled (SMS, authenticator, security key)
8. Google redirects back to Medium
9. App detects successful login by checking for:
   - Presence of user profile elements
   - Absence of login form
   - Valid session cookies
10. App saves session cookies
11. App notifies user: "Login successful"
```

## Error Handling

### Error Categories

1. **File Errors**
   - File not found
   - Invalid markdown format
   - Missing required frontmatter fields
   - Invalid draft URL format
   - Draft URL not accessible
   - **Recovery**: Display error, allow file reselection or URL correction

2. **Authentication Errors**
   - Invalid credentials
   - Network timeout
   - 2FA required
   - OAuth flow cancelled by user
   - OAuth timeout (user didn't complete in time)
   - Session cookies expired
   - **Recovery**: Display error, allow retry, pause for 2FA, restart OAuth flow

3. **Browser Errors**
   - Selector not found (Medium UI changed)
   - Page load timeout
   - Browser crash
   - **Recovery**: Log error, retry up to 3 times, display error message

4. **Content Errors**
   - Unsupported markdown syntax
   - Content too long
   - Invalid characters
   - Tables detected (converted to placeholder)
   - Images detected (converted to placeholder)
   - **Recovery**: Log warning, insert placeholder for tables/images, continue

### Error Handling Strategy

```python
class PublishingError(Exception):
    """Base exception for publishing errors"""
    pass

class AuthenticationError(PublishingError):
    """Authentication failed"""
    pass

class BrowserError(PublishingError):
    """Browser automation error"""
    pass

class ContentError(PublishingError):
    """Content processing error"""
    pass

# Usage
try:
    await medium_editor.type_content(blocks)
except BrowserError as e:
    logger.error(f"Browser error: {e}")
    # Retry logic
    for attempt in range(3):
        try:
            await medium_editor.type_content(blocks)
            break
        except BrowserError:
            if attempt == 2:
                raise
            await asyncio.sleep(2)
```

## Configuration

### CSS Selectors (selectors.yaml)

```yaml
medium:
  login:
    sign_in_button: 'a[href*="sign-in"]'
    google_oauth_button: 'button:has-text("Sign in with Google"), button:has-text("Continue with Google")'
    email_input: 'input[type="email"]'
    password_input: 'input[type="password"]'
    continue_button: 'button:has-text("Continue")'
    
  # Login success detection
  logged_in_indicators:
    user_menu: '[data-testid="user-menu"], button[aria-label*="user menu"]'
    profile_image: 'img[alt*="profile"], [data-testid="profile-image"]'
    new_story_button: 'a[href="/new-story"]'
    
  editor:
    new_story_link: 'a[href="/new-story"]'
    title_field: '[data-testid="storyTitle"]'
    content_area: '[data-testid="storyContent"]'
    publish_button: 'button:has-text("Publish")'
    
  publishing:
    tags_input: 'input[placeholder*="tags"]'
    subtitle_input: 'input[placeholder*="subtitle"]'
    draft_button: 'button:has-text("Save as draft")'
    public_button: 'button:has-text("Publish now")'
    
  draft:
    # Selectors for working with existing drafts
    editor_content: '[contenteditable="true"]'
    clear_all: 'button[aria-label="Clear"]'  # If available
```

### Keyboard Shortcuts (Medium Editor)

```yaml
formatting:
  bold: "Control+B"
  italic: "Control+I"
  code: "Control+Alt+6"
  header_2: "Control+Alt+2"
  header_3: "Control+Alt+3"
  link: "Control+K"
```

## Security Considerations

1. **Credential Storage**
   - Use `keyring` library for OS-level secure storage
   - Never log passwords
   - Clear credentials on logout

2. **Session Management**
   - Store session cookies encrypted
   - Expire sessions after 7 days
   - Clear sessions on application exit (if not "Remember Me")

3. **Input Validation**
   - Sanitize file paths
   - Validate markdown content
   - Escape special characters

## Performance Considerations

1. **Typing Speed and Rate Limiting**
   - Default 30ms per character (human-like)
   - Configurable 10-100ms range
   - Random variation ±20% per character
   - **HARD LIMIT: 35 characters per minute maximum**
   - Rate limiter enforces sliding window
   - Paragraph delays 100ms (natural pauses)
   - Occasional thinking pauses 100-500ms
   - Display estimated time before typing (accounting for typos)

2. **Human Typing Simulation**
   ```python
   # Typo rates:
   # - Low: 2% of characters (1 typo per 50 chars)
   # - Medium: 5% of characters (1 typo per 20 chars)
   # - High: 8% of characters (1 typo per 12.5 chars)
   
   # Typo correction:
   # - Wait 1-3 additional characters before correcting
   # - Use backspace to delete typo
   # - Retype correct character
   # - Adds ~3-5 extra keystrokes per typo
   
   # No typos in:
   # - Code blocks
   # - URLs
   # - TODO placeholders
   
   # Example: 1000 character article with medium typos
   # - Base: 1000 chars
   # - Typos: 50 typos (5%)
   # - Corrections: 50 * 4 = 200 extra keystrokes (backspace + retype)
   # - Total: 1250 keystrokes
   # - Time: 1250 / 35 = 35.7 minutes
   ```

3. **Adjacent Key Typos**
   ```python
   # QWERTY keyboard layout for realistic typos
   ADJACENT_KEYS = {
       'a': ['q', 's', 'w', 'z'],
       'b': ['v', 'g', 'h', 'n'],
       'c': ['x', 'd', 'f', 'v'],
       # ... etc for all keys
   }
   
   # Typo generation:
   # - Select random adjacent key
   # - Type wrong character
   # - Continue typing 1-3 more characters
   # - Backspace to delete typo + extra chars
   # - Retype correctly
   ```

4. **Rate Limiter Implementation**
   ```python
   # Sliding window approach:
   # - Track chars typed in current minute
   # - When limit reached, wait until window slides
   # - Resume typing when capacity available
   # - Account for typos in rate calculation
   ```

5. **Browser Resource Usage**
   - Single browser instance per session
   - Reuse browser for multiple articles
   - Close browser on application exit

6. **Memory Management**
   - Stream large files (don't load entirely in memory)
   - Clear content blocks after typing
   - Limit log file size (rotate at 10MB)

## Testing Strategy

1. **Unit Tests**
   - ArticleParser: Test frontmatter extraction, body parsing
   - MarkdownProcessor: Test markdown conversion
   - ConfigManager: Test config load/save

2. **Integration Tests**
   - End-to-end publishing flow (with test Medium account)
   - Authentication flow
   - Error recovery

3. **UI Tests**
   - Button states (enabled/disabled)
   - Progress updates
   - Error message display

## Future Enhancements

1. **Image Upload**
   - Parse image references in markdown
   - Upload images to Medium
   - Insert images in correct positions

2. **Scheduling**
   - Schedule articles for future publication
   - Queue multiple articles
   - Automatic retry on failure

3. **Templates**
   - Save article templates
   - Quick-fill common metadata
   - Reusable content blocks

4. **Analytics**
   - Track published articles
   - View Medium stats
   - Export publication history

## Technology Stack

- **Language**: Python 3.11+
- **UI Framework**: PyQt6
- **Browser Automation**: Playwright
- **Markdown Parsing**: markdown2 or mistune
- **Configuration**: PyYAML
- **Credential Storage**: keyring
- **Logging**: Python logging module
- **Testing**: pytest, pytest-asyncio, pytest-qt

## Deployment

1. **Package as Executable**
   - Use PyInstaller or cx_Freeze
   - Bundle Python runtime
   - Include Playwright browsers

2. **Installation**
   - Windows installer (.msi or .exe)
   - Install to Program Files
   - Create desktop shortcut
   - Register file associations (.md)

3. **Updates**
   - Check for updates on startup
   - Download and install updates
   - Preserve user configuration

# Medium Article Publisher - API Reference

## Table of Contents
1. [Core Layer](#core-layer)
2. [Input Layer](#input-layer)
3. [Navigation Layer](#navigation-layer)
4. [Safety Layer](#safety-layer)
5. [Data Models](#data-models)
6. [Exceptions](#exceptions)

## Core Layer

### ArticleParser

**Module**: `core.article_parser`

**Purpose**: Parse markdown files and extract article metadata (frontmatter + body).

```python
class ArticleParser:
    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> Article: ...
    def extract_frontmatter(self, content: str) -> dict: ...
    def extract_body(self, content: str) -> str: ...
    def validate_article(self, article: Article) -> bool: ...
```

#### Key Methods

- `parse_file(file_path)` → `Article` — Raises `FileError`, `ContentError`
- `extract_frontmatter(content)` → `dict` — Raises `ContentError`
- `validate_article(article)` → `bool` — Raises `ContentError`

---

### MarkdownProcessor

**Module**: `core.markdown_processor`

**Purpose**: Convert markdown content into structured `ContentBlock` lists with inline formatting.

```python
class MarkdownProcessor:
    def __init__(self):
        pass

    def process(self, markdown: str) -> List[ContentBlock]: ...
    def parse_formatting(self, line: str) -> List[Format]: ...
```

#### Key Methods

- `process(markdown)` → `List[ContentBlock]` — Parses headers, paragraphs, code blocks, lists, inline formatting
- `parse_formatting(line)` → `List[Format]` — Extracts bold, italic, code, link spans

---

### ChangeParser

**Module**: `core.change_parser`

**Purpose**: Parse user change instructions for version update workflows.

```python
class ChangeParser:
    def __init__(self):
        pass

    def parse_instructions(self, instructions: str) -> List[ChangeInstruction]: ...
    def identify_sections(self, text: str) -> List[str]: ...
```

---

### ConfigManager

**Module**: `core.config_manager`

**Purpose**: Load, validate, and provide access to YAML configuration.

```python
class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: Path to YAML config file. Defaults to config/default_config.yaml.
        """
        pass

    def load_config(self) -> dict: ...
    def get(self, key: str, default=None) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def validate(self) -> bool: ...
```

#### Usage

```python
config = ConfigManager("config/default_config.yaml")
base_delay = config.get("typing.base_delay_ms", 150)
confidence = config.get("navigation.screen_confidence", 0.8)
```

---

### SessionManager

**Module**: `core.session_manager`

**Purpose**: Manage publishing session state (progress tracking, resume capability).

```python
class SessionManager:
    def __init__(self, session_dir: str):
        pass

    def start_session(self) -> str: ...
    def save_state(self, state: dict) -> None: ...
    def restore_state(self) -> dict: ...
    def clear_session(self) -> None: ...
```

---

## Input Layer

### ContentTyper

**Module**: `automation.content_typer`

**Purpose**: Orchestrates typing of content blocks with formatting, delegating to OS_Input_Controller and HumanTypingSimulator.

```python
class ContentTyper:
    def __init__(
        self,
        os_input_controller: OS_Input_Controller,
        human_typing_simulator: HumanTypingSimulator,
        deferred_typo_tracker: DeferredTypoTracker,
        config_manager: ConfigManager
    ):
        """All dependencies injected. No Playwright, no browser page object."""
        pass

    def type_block(self, block: ContentBlock) -> None: ...
    def type_text(self, text: str) -> None: ...
    def apply_bold(self, text: str) -> None: ...
    def apply_italic(self, text: str) -> None: ...
    def apply_header(self, text: str, level: int) -> None: ...
    def insert_code_block(self, code: str, language: str = "") -> None: ...
    def insert_link(self, text: str, url: str) -> None: ...
```

#### Key Behavior

- Uses `OS_Input_Controller` for all keystrokes (pyautogui)
- Consults `HumanTypingSimulator` for delay timing and typo decisions
- Tracks deferred typos via `DeferredTypoTracker`
- Reads typing config from `ConfigManager`
- Raises `EmergencyStopError`, `InputControlError`, `FocusLostError`
- Synchronous execution (no async/await)

---

### HumanTypingSimulator

**Module**: `automation.human_typing_simulator`

**Purpose**: Calculate realistic typing delays, decide when to introduce typos, generate typo characters.

```python
class HumanTypingSimulator:
    def __init__(self, config_manager: ConfigManager):
        """Reads typo_frequency, base_delay_ms, variation_percent from config."""
        pass

    def get_typing_delay(self) -> int: ...
    def should_make_typo(self) -> bool: ...
    def generate_typo(self, intended_char: str) -> str: ...
    def get_thinking_pause(self) -> int: ...
    def get_paragraph_pause(self) -> int: ...
```

#### Key Behavior

- Delay = `base_delay_ms ± variation_percent%` (random per keystroke)
- Typo generation uses QWERTY adjacency map
- Thinking pauses occur randomly between words/sentences
- Paragraph pauses occur between content blocks
- No rate limiter class — speed is controlled entirely by `base_delay_ms` and variation

---

### OS_Input_Controller

**Module**: `automation.os_input_controller`

**Purpose**: Send keystrokes and keyboard shortcuts at the OS level via pyautogui.

```python
class OS_Input_Controller:
    def __init__(self, config_manager: ConfigManager):
        pass

    def type_character(self, char: str) -> None: ...
    def type_string(self, text: str, interval: float = 0.0) -> None: ...
    def press_key(self, key: str) -> None: ...
    def hotkey(self, *keys: str) -> None: ...
    def backspace(self, count: int = 1) -> None: ...
```

#### Key Behavior

- Wraps `pyautogui.press()`, `pyautogui.hotkey()`, `pyautogui.typewrite()`
- All input is OS-level (not browser-injected)
- Raises `InputControlError` on failure

---

### DeferredTypoTracker

**Module**: `automation.deferred_typo_tracker`

**Purpose**: Track typos that are not immediately corrected, for batch correction later.

```python
class DeferredTypoTracker:
    def __init__(self):
        pass

    def add_typo(self, typo: DeferredTypo) -> None: ...
    def get_pending_typos(self) -> List[DeferredTypo]: ...
    def clear(self) -> None: ...
    def has_pending(self) -> bool: ...
```

---

### VersionUpdateTyper

**Module**: `automation.version_update_typer`

**Purpose**: Handle version update workflows — find sections, delete content, type replacements.

```python
class VersionUpdateTyper:
    def __init__(
        self,
        content_typer: ContentTyper,
        os_input_controller: OS_Input_Controller,
        config_manager: ConfigManager
    ):
        pass

    def apply_changes(self, changes: List[ChangeInstruction]) -> UpdateResult: ...
    def find_section(self, search_text: str) -> bool: ...
    def replace_section(self, search_text: str, new_blocks: List[ContentBlock]) -> None: ...
    def delete_section(self, search_text: str) -> None: ...
```

---

## Navigation Layer

### NavigationStateMachine

**Module**: `navigation.navigation_state_machine`

**Purpose**: Track and transition between application navigation states using screen recognition.

```python
class NavigationStateMachine:
    def __init__(
        self,
        screen_recognition: ScreenRecognition,
        config_manager: ConfigManager
    ):
        pass

    def get_current_state(self) -> NavigationState: ...
    def wait_for_state(self, target: NavigationState, timeout: int = None) -> bool: ...
    def transition_to(self, target: NavigationState) -> None: ...
```

#### NavigationState Enum

```python
class NavigationState(Enum):
    START = "start"
    LOGGED_OUT_HOME = "logged_out_home"
    SIGN_IN_SCREEN = "sign_in_screen"
    GOOGLE_SIGN_IN = "google_sign_in"
    LOGGED_IN_HOME = "logged_in_home"
    DRAFTS_PAGE = "drafts_page"
    NEW_STORY_EDITOR = "new_story_editor"
```

#### Key Behavior

- Polls screen at `poll_interval_seconds`
- Uses `ScreenRecognition` to identify current state
- Raises `NavigationError` on timeout or invalid transition

---

### ScreenRecognition

**Module**: `navigation.screen_recognition`

**Purpose**: Match reference PNG images against the current screen to identify UI states.

```python
class ScreenRecognition:
    def __init__(self, config_manager: ConfigManager):
        """Loads reference images from assets/medium/ directory."""
        pass

    def find_on_screen(self, reference_image: str, confidence: float = None) -> Optional[Tuple[int, int]]: ...
    def is_visible(self, reference_image: str) -> bool: ...
    def wait_until_visible(self, reference_image: str, timeout: int = 30) -> bool: ...
    def get_screen_state(self) -> NavigationState: ...
```

#### Key Behavior

- Uses pyautogui's `locateOnScreen()` with confidence threshold
- Reference images stored in `assets/medium/`
- Confidence threshold from `navigation.screen_confidence` config
- Returns screen coordinates when found (for click targets)
- Raises `NavigationError` on timeout

---

### LoginDetector

**Module**: `navigation.login_detector`

**Purpose**: Detect whether the user has completed login by monitoring screen state.

```python
class LoginDetector:
    def __init__(
        self,
        screen_recognition: ScreenRecognition,
        config_manager: ConfigManager
    ):
        pass

    def is_logged_in(self) -> bool: ...
    def wait_for_login(self, timeout: int = None) -> bool: ...
```

#### Key Behavior

- Does NOT perform login — user completes OAuth manually in their browser
- Monitors screen for logged-in indicators (reference images)
- Timeout from `navigation.login_timeout_seconds`
- Raises `NavigationError` if login not detected within timeout

---

## Safety Layer

### EmergencyStop

**Module**: `safety.emergency_stop`

**Purpose**: Monitor keyboard for emergency stop hotkey via pynput.

```python
class EmergencyStop:
    def __init__(self, config_manager: ConfigManager):
        """Reads emergency_stop_hotkey from config."""
        pass

    def start_monitoring(self) -> None: ...
    def stop_monitoring(self) -> None: ...
    def is_triggered(self) -> bool: ...
    def reset(self) -> None: ...
```

#### Key Behavior

- Uses pynput keyboard listener (runs in background thread)
- Default hotkey: Ctrl+Shift+Escape
- When triggered, raises `EmergencyStopError` in the typing thread
- Must be started before typing begins

---

### FocusWindowDetector

**Module**: `safety.focus_window_detector`

**Purpose**: Verify the target window (browser) has focus before sending keystrokes.

```python
class FocusWindowDetector:
    def __init__(self, config_manager: ConfigManager):
        pass

    def check_focus(self) -> bool: ...
    def wait_for_focus(self, timeout: int = 10) -> bool: ...
```

#### Key Behavior

- Checks active window title/handle matches expected target
- Raises `FocusLostError` if focus lost during typing (when `focus_check_enabled` is true)
- Prevents keystrokes from being sent to wrong application

---

## Data Models

### Article

```python
@dataclass
class Article:
    title: str
    subtitle: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    status: str = "draft"
    file_path: str = ""
```

### ContentBlock

```python
@dataclass
class ContentBlock:
    type: str  # "paragraph", "header", "code", "list", "blockquote"
    content: str
    formatting: List[Format] = field(default_factory=list)
    level: int = 0  # For headers (2, 3, 4)
    metadata: dict = field(default_factory=dict)
```

### Format

```python
@dataclass
class Format:
    type: str  # "bold", "italic", "code", "link"
    start: int
    end: int
    url: str = ""  # For links only
```

### DeferredTypo

```python
@dataclass
class DeferredTypo:
    block_index: int
    char_index: int
    wrong_char: str
    correct_char: str
```

### UpdateResult

```python
@dataclass
class UpdateResult:
    success: bool
    message: str
    changes_applied: List[str]
```

---

## Exceptions

### Exception Hierarchy

```python
class PublishingError(Exception):
    """Base exception for all publishing errors."""
    pass

class ContentError(PublishingError):
    """Content processing or validation error."""
    pass

class FileError(PublishingError):
    """File operation error (read/write/not found)."""
    pass

class EmergencyStopError(PublishingError):
    """User triggered emergency stop hotkey."""
    pass

class NavigationError(PublishingError):
    """Screen recognition or navigation timeout error."""
    pass

class InputControlError(PublishingError):
    """OS-level input (pyautogui) failure."""
    pass

class FocusLostError(PublishingError):
    """Target window lost focus during typing."""
    pass
```

---

## Launch

```cmd
python -m medium_publisher.main
```

Runs the application from workspace root. The main module initializes the Qt application, wires up dependencies, and shows the main window.

---

**Document Version**: 2.0
**Last Updated**: 2025-06-01
**Architecture**: OS-level input (pyautogui/pynput) with screen recognition

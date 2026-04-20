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

The Medium Article Publisher is a desktop application that types markdown articles into Medium's web editor using OS-level keyboard and mouse events. It uses screen recognition (image matching) to detect page state and navigate through login flows, then simulates human typing with realistic delays, typos, and corrections.

### Key Architectural Principles

1. **Separation of Concerns**: UI, business logic, automation, navigation, and safety are in separate layers
2. **Dependency Injection**: Components receive dependencies rather than creating them
3. **Single Responsibility**: Each class has one clear purpose
4. **OS-Level Input**: No browser automation libraries — all interaction happens through pyautogui/pynput
5. **Screen Recognition over DOM**: Page state is detected by matching reference PNG images, not by querying the DOM

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Desktop Application                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              PyQt6 UI Layer                            │ │
│  │  - MainWindow (orchestration)                          │ │
│  │  - FileSelector (article picker)                       │ │
│  │  - SettingsDialog (configuration)                      │ │
│  │  - ProgressWidget (feedback)                           │ │
│  │  - LogWidget (transparency)                            │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Core Logic Layer                             │ │
│  │  - ArticleParser (markdown + YAML frontmatter)         │ │
│  │  - MarkdownProcessor (→ ContentBlock list)             │ │
│  │  - PublishingWorkflow (QThread orchestrator)            │ │
│  │  - ConfigManager (hierarchical YAML config)            │ │
│  │  - SessionManager (state persistence)                  │ │
│  │  - ChangeParser (version update instructions)          │ │
│  │  - VersionDiffDetector (diff between versions)         │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Automation Layer (OS-Level Input)              │ │
│  │  - OSInputController (pyautogui keyboard/mouse)        │ │
│  │  - HumanTypingSimulator (delays, typos, corrections)   │ │
│  │  - ContentTyper (types blocks with formatting)         │ │
│  │  - DeferredTypoTracker (records typos for review)      │ │
│  │  - VersionUpdateTyper (applies version changes)        │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Navigation Layer (Screen Recognition)          │ │
│  │  - ScreenRecognition (pyautogui.locateOnScreen)        │ │
│  │  - NavigationStateMachine (FSM for login flow)         │ │
│  │  - LoginDetector (page state via reference images)     │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Safety Layer                              │ │
│  │  - EmergencyStop (hotkey + mouse corner failsafe)      │ │
│  │  - FocusWindowDetector (pause when focus lost)         │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
              ┌────────────────────────┐
              │   Default Browser      │
              │   (opened via          │
              │    webbrowser module)   │
              └────────────────────────┘
                           ↓
              ┌────────────────────────┐
              │      Medium.com        │
              └────────────────────────┘
```

## Component Layers

### 1. UI Layer (`ui/`)

**Purpose**: User interaction and visual feedback

**Modules**:
- `main_window.py` — Primary application window, workflow orchestration
- `file_selector.py` — File picker for markdown articles
- `settings_dialog.py` — Configuration management UI
- `progress_widget.py` — Real-time progress feedback
- `log_widget.py` — Operation log display

**Responsibilities**:
- Capture user input (file selection, settings, start/stop)
- Display application state and progress
- Provide visual feedback during typing
- Delegate to core layer via signals/slots
- Keep responsive via QThread-based workflows

### 2. Core Logic Layer (`core/`)

**Purpose**: Business logic, data processing, and workflow orchestration

**Modules**:
- `article_parser.py` — Parses markdown files with YAML frontmatter into Article objects
- `markdown_processor.py` — Converts parsed markdown into a list of ContentBlock objects (paragraphs, headers, code blocks, lists, etc.)
- `publishing_workflow.py` — QThread-based orchestrator that coordinates the full pipeline: open browser → navigate → login → type content
- `config_manager.py` — Hierarchical YAML configuration with defaults, user overrides, and environment variables
- `session_manager.py` — Persists state between runs (last file, window position, etc.)
- `change_parser.py` — Parses version update instructions (what to add/remove/modify)
- `version_diff_detector.py` — Detects differences between article versions

**Responsibilities**:
- Parse and validate markdown input
- Transform markdown into typed content blocks
- Orchestrate the full publishing pipeline
- Manage application configuration
- No direct UI or OS input dependencies (testable in isolation)

### 3. Automation Layer (`automation/`)

**Purpose**: OS-level keyboard and mouse control with human-like behavior

**Modules**:
- `os_input_controller.py` — Wraps pyautogui for keyboard/mouse operations (keypress, hotkey, click, type)
- `human_typing_simulator.py` — Generates realistic typing delays, introduces typos, and simulates corrections (backspace + retype)
- `content_typer.py` — Types ContentBlock objects with appropriate formatting (headers via Ctrl+Alt+1, bold via Ctrl+B, etc.)
- `deferred_typo_tracker.py` — Records typos that weren't fixed inline, for a review pass after typing completes
- `version_update_typer.py` — Applies version changes to an existing draft (find section, select, delete, retype)

**Responsibilities**:
- Send OS-level keyboard events (character-by-character)
- Send OS-level mouse clicks (for navigation buttons)
- Simulate human typing patterns (variable delays, occasional typos)
- Apply Medium-specific keyboard shortcuts for formatting
- Track and fix deferred typos in a review pass

**Key Design Decision**: All input goes through pyautogui/pynput, not through any browser API. This means the app types into whatever window has focus — the safety layer ensures that's the correct window.

### 4. Navigation Layer (`navigation/`)

**Purpose**: Detect page state and navigate through login flows using screen recognition

**Modules**:
- `screen_recognition.py` — Wraps `pyautogui.locateOnScreen()` to find reference PNG images on screen with configurable confidence threshold
- `navigation_state_machine.py` — Finite state machine that drives the login flow (detect state → click appropriate button → wait → detect next state)
- `login_detector.py` — Determines current page state (Medium homepage, Google OAuth page, editor, etc.) by matching reference images

**Responsibilities**:
- Open Medium.com via `webbrowser.open()`
- Detect current page state by matching reference screenshots
- Navigate through Google OAuth login by clicking detected UI elements
- Transition through states until the editor is reached
- Handle timeouts and retry logic

**Reference Images**: Stored in `assets/medium/` as PNG files. Each image represents a UI element or page state (e.g., "Sign in with Google" button, account selector, editor toolbar).

### 5. Safety Layer (`safety/`)

**Purpose**: Protect against runaway automation

**Modules**:
- `emergency_stop.py` — Global hotkey listener (Ctrl+Shift+Escape) and mouse-to-corner failsafe. Immediately halts all automation and releases held modifier keys.
- `focus_window_detector.py` — Monitors which window has focus. Pauses typing if the browser loses focus, resumes when focus returns.

**Responsibilities**:
- Provide multiple independent stop mechanisms
- Release all held modifier keys on emergency stop
- Pause automation when target window loses focus
- Prevent typing into wrong applications

## Data Flow

### Publishing Flow

```
1. User selects markdown file in UI
   ↓
2. ArticleParser.parse_file()
   - Extract YAML frontmatter (title, subtitle, tags)
   - Extract body content
   - Return Article object
   ↓
3. MarkdownProcessor.process()
   - Parse markdown syntax
   - Convert to list of ContentBlock objects
   - Each block has: type, content, formatting metadata
   - Tables/images → placeholder blocks
   ↓
4. PublishingWorkflow.run() [in QThread]
   ↓
5. webbrowser.open("https://medium.com/new-story")
   - Opens default browser
   ↓
6. NavigationStateMachine.navigate_to_editor()
   - ScreenRecognition detects page state
   - LoginDetector identifies: homepage? OAuth page? editor?
   - Clicks through login flow using detected button positions
   - Waits for each transition (with timeout)
   ↓
7. ContentTyper.type_blocks(content_blocks)
   - For each ContentBlock:
     a. Apply formatting prefix (header shortcut, quote shortcut, etc.)
     b. OSInputController types text character-by-character
     c. HumanTypingSimulator adds delays and occasional typos
     d. DeferredTypoTracker records unfixed typos
   ↓
8. DeferredTypoTracker.fix_deferred_typos()
   - Review pass: navigate to each deferred typo and fix it
   ↓
9. UI shows completion notification
   - Lists any placeholders (images, tables) for manual insertion
```

### Version Update Flow

```
1. User selects new version file
   ↓
2. ChangeParser.parse_instructions()
   - Identify sections to modify
   - Extract search markers and replacement content
   ↓
3. VersionDiffDetector.detect_changes()
   - Compare old version to new version
   - Produce list of change operations
   ↓
4. VersionUpdateTyper.apply_changes()
   - For each change:
     a. Use Ctrl+F to find section marker
     b. Select the section content
     c. Delete selected content
     d. Type new content via ContentTyper
   ↓
5. User reviews changes in Medium
```

## Design Patterns

### 1. State Machine (Navigation)

**Purpose**: Manage complex login flow with clear state transitions

```python
class NavigationStateMachine:
    states = [INITIAL, MEDIUM_HOME, SIGN_IN_PAGE, GOOGLE_OAUTH, 
              ACCOUNT_SELECTOR, TWO_FACTOR, EDITOR_READY]
    
    def advance(self):
        current = self.detect_state()  # Screen recognition
        action = self.transitions[current]
        action.execute()  # Click detected button
        self.wait_for_transition()
```

### 2. Strategy Pattern (Typing Behavior)

**Purpose**: Swap between human-like and fast typing

```python
class HumanTypingSimulator:
    def get_delay(self, base_delay: int) -> int:
        # Gaussian variation + occasional long pauses
        
    def should_make_typo(self) -> bool:
        # Probabilistic typo generation
        
    def get_typo_char(self, intended: str) -> str:
        # Adjacent key on keyboard layout
```

### 3. Observer Pattern (Progress Updates)

**Purpose**: Keep UI responsive during long typing operations

```python
class PublishingWorkflow(QThread):
    progress_updated = pyqtSignal(int, str)  # percent, message
    typing_complete = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def run(self):
        self.progress_updated.emit(10, "Opening browser...")
        # ...
        self.progress_updated.emit(50, "Typing content...")
```

### 4. Facade Pattern (OS Input)

**Purpose**: Simplify pyautogui/pynput interactions behind a clean interface

```python
class OSInputController:
    def type_character(self, char: str): ...
    def hotkey(self, *keys): ...
    def click_at(self, x: int, y: int): ...
    def release_all_modifiers(self): ...
```

### 5. Template Method (Content Typing)

**Purpose**: Different block types share the same typing skeleton but vary in formatting

```python
class ContentTyper:
    def type_block(self, block: ContentBlock):
        self._apply_prefix_formatting(block)  # Header shortcut, quote, etc.
        self._type_content(block)              # Character-by-character
        self._apply_inline_formatting(block)   # Bold, italic, links
        self._finalize_block(block)            # Enter key, separator
```

## Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.11+ | Application logic |
| UI Framework | PyQt6 | Desktop interface |
| Keyboard/Mouse | pyautogui + pynput | OS-level input events |
| Screen Recognition | pyautogui.locateOnScreen() + Pillow | Detect page state via image matching |
| Browser Opening | webbrowser (stdlib) | Open Medium in default browser |
| Markdown Parsing | markdown2 | Markdown to structured content |
| Configuration | PyYAML | Hierarchical config files |
| Credentials | keyring | Secure OS credential storage |
| Encryption | pycryptodome | Session data encryption |
| Windows API | pywin32 | Window focus detection |
| Environment | python-dotenv | Environment variable loading |

### Dependencies (requirements.txt)

```
PyQt6
pyautogui
pynput
Pillow
pywin32
pycryptodome
markdown2
PyYAML
python-dotenv
keyring
```

### What's NOT in the Stack

- ❌ Playwright — No browser automation library
- ❌ Selenium — No WebDriver
- ❌ Chromium — No bundled browser
- ❌ async/await — Synchronous code with QThread for concurrency
- ❌ Any DOM manipulation — All interaction is OS-level

## Module Dependencies

### Dependency Graph

```
ui/
├── depends on → core/ (workflow, config, parser)
└── depends on → safety/ (emergency stop binding)

core/
├── depends on → automation/ (content typer, OS input)
├── depends on → navigation/ (state machine, screen recognition)
└── depends on → safety/ (focus detection, emergency stop)

automation/
├── depends on → safety/ (checks before typing)
└── no dependencies on ui/ or navigation/

navigation/
├── depends on → automation/ (OS input for clicking)
└── no dependencies on ui/ or core/

safety/
└── no dependencies (leaf layer — standalone monitors)
```

### Import Rules

1. **UI** can import: core, safety
2. **Core** can import: automation, navigation, safety
3. **Automation** can import: safety
4. **Navigation** can import: automation
5. **Safety** imports: nothing (leaf layer, standalone)

### Circular Dependency Prevention

- Safety layer is fully independent (can halt anything without importing it)
- Navigation uses automation for clicking but doesn't know about content
- Core orchestrates everything but automation/navigation don't depend on core

## Configuration Architecture

### Configuration Hierarchy (highest priority wins)

```
1. Code defaults (lowest)
   ↓
2. default_config.yaml (medium_publisher/config/)
   ↓
3. User config (~/.medium_publisher/config.yaml)
   ↓
4. Environment variables (highest priority)
```

### Configuration Sections

| Section | Contents |
|---------|----------|
| `typing` | Base delay, variation, typo frequency, deferred ratio |
| `publishing` | Default mode, batch settings |
| `safety` | Emergency hotkey, countdown, failsafe settings |
| `navigation` | Google email, confidence threshold, timeouts |
| `ui` | Always on top, remember position, theme |
| `assets` | Reference image paths |

### Key Files

| File | Location | Purpose |
|------|----------|---------|
| `default_config.yaml` | `medium_publisher/config/` | Shipped defaults |
| `config.yaml` | `~/.medium_publisher/` | User overrides |
| `*.png` | `medium_publisher/assets/medium/` | Screen recognition reference images |

## Error Handling Architecture

### Exception Hierarchy

```
PublishingError (base)
├── NavigationError
│   ├── ScreenRecognitionTimeout
│   ├── LoginFlowFailed
│   └── UnexpectedPageState
├── TypingError
│   ├── FocusLostError
│   ├── EmergencyStopTriggered
│   └── FormattingError
├── ContentError
│   ├── InvalidMarkdownError
│   ├── MissingFrontmatterError
│   └── UnsupportedFormatError
└── ConfigError
    ├── MissingConfigError
    └── InvalidConfigError
```

### Error Handling Strategy

1. **Emergency stop**: Immediately halt, release all keys, save progress
2. **Focus lost**: Pause and wait for focus to return
3. **Screen recognition timeout**: Retry with lower confidence, then prompt user
4. **Typing errors**: Log and continue (typos are self-correcting by design)
5. **User feedback**: Clear error messages in the log widget

## Performance Considerations

### Typing Speed

- **Base rate**: ~60 WPM (200ms between keystrokes)
- **Variation**: ±30% Gaussian distribution around base delay
- **Typo overhead**: ~20-30% additional time for typo/correction cycles
- **Formatting overhead**: Keyboard shortcuts add ~100ms per formatted span

### Threading Model

- **Main thread**: PyQt6 event loop (UI responsive at all times)
- **Worker thread**: QThread runs PublishingWorkflow (typing, navigation)
- **Communication**: pyqtSignal/pyqtSlot for thread-safe UI updates
- **No async/await**: Synchronous code in worker thread, sleeps for delays

### Memory

- ContentBlock list is generated once and consumed sequentially
- Reference images loaded on demand for screen recognition
- Log rotation at 10MB prevents unbounded growth

## Security Architecture

### Credential Storage

- **OS keychain**: `keyring` library for stored credentials
- **Session data**: Encrypted with pycryptodome
- **No plaintext passwords**: Ever

### Input Safety

- **Focus detection**: Only types when correct window is focused
- **Emergency stop**: Multiple independent halt mechanisms
- **Key release**: All modifier keys released on stop/error/exit
- **No network access**: App doesn't make HTTP requests (browser handles all Medium communication)

## Testing Architecture

### Test Structure

```
tests/
├── unit/
│   ├── test_article_parser.py
│   ├── test_markdown_processor.py
│   ├── test_change_parser.py
│   ├── test_human_typing_simulator.py
│   ├── test_config_manager.py
│   └── test_version_diff_detector.py
├── integration/
│   ├── test_content_typer.py
│   ├── test_navigation_state_machine.py
│   └── test_publishing_workflow.py
└── ui/
    ├── test_main_window.py
    └── test_settings_dialog.py
```

### Mocking Strategy

- **OS input**: Mock pyautogui/pynput for unit tests (no actual keypresses)
- **Screen recognition**: Mock locateOnScreen with predetermined results
- **File system**: Use temporary directories
- **Time**: Mock sleep() for fast test execution

---

**Document Version**: 2.0
**Last Updated**: 2025-06-01
**Maintained By**: Development Team

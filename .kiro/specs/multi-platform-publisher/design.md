# Multi-Platform Article Publisher - Design

## Overview

This design extends the Medium Article Publisher to support multiple publishing platforms through a platform abstraction layer. The architecture uses the Strategy Pattern to enable platform-specific implementations while maintaining a unified user interface and workflow.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Desktop Application                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              PyQt6 UI Layer                            │ │
│  │  - Main Window (with Platform Selector)               │ │
│  │  - Platform Settings Dialog                           │ │
│  │  - File Selection Dialog                              │ │
│  │  - Progress Display                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Application Logic Layer                      │ │
│  │  - Article Parser (platform-agnostic)                 │ │
│  │  - Markdown Processor (platform-agnostic)             │ │
│  │  - Configuration Manager (multi-platform)             │ │
│  │  - Session Manager (multi-platform)                   │ │
│  │  - Publishing Workflow (platform-agnostic)            │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Platform Abstraction Layer                     │ │
│  │  - PlatformInterface (Abstract Base Class)            │ │
│  │  - PlatformFactory (Creates platform instances)       │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌──────────────────────┬──────────────────────────────────┐ │
│  │  Medium Platform     │  Substack Platform               │ │
│  │  - MediumAuth        │  - SubstackAuth                  │ │
│  │  - MediumEditor      │  - SubstackEditor                │ │
│  │  - MediumTyper       │  - SubstackTyper                 │ │
│  └──────────────────────┴──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
              ┌────────────────────────┐
              │   Chromium Browser     │
              │   (Playwright)         │
              └────────────────────────┘
                           ↓
              ┌────────────┬────────────┐
              │ Medium.com │Substack.com│
              └────────────┴────────────┘
```

### Component Architecture

```
medium_publisher/
├── ui/
│   ├── main_window.py          # Updated with platform selector
│   ├── platform_settings.py    # New: Platform-specific settings
│   ├── settings_dialog.py      # Updated for multi-platform
│   └── ...
├── core/
│   ├── article_parser.py       # Unchanged (platform-agnostic)
│   ├── markdown_processor.py   # Unchanged (platform-agnostic)
│   ├── config_manager.py       # Updated for multi-platform config
│   ├── session_manager.py      # Updated for multi-platform sessions
│   ├── publishing_workflow.py  # Updated to use PlatformInterface
│   └── ...
├── platforms/
│   ├── __init__.py
│   ├── platform_interface.py   # New: Abstract base class
│   ├── platform_factory.py     # New: Factory for creating platforms
│   ├── medium/
│   │   ├── __init__.py
│   │   ├── medium_platform.py  # New: Refactored from MediumEditor
│   │   ├── medium_auth.py      # Refactored from AuthHandler
│   │   ├── medium_typer.py     # Refactored from ContentTyper
│   │   └── medium_selectors.yaml
│   └── substack/
│       ├── __init__.py
│       ├── substack_platform.py # New: Substack implementation
│       ├── substack_auth.py     # New: Substack authentication
│       ├── substack_typer.py    # New: Substack content typing
│       └── substack_selectors.yaml
├── automation/
│   ├── playwright_controller.py # Unchanged (platform-agnostic)
│   ├── rate_limiter.py          # Unchanged (platform-agnostic)
│   └── human_typing_simulator.py # Unchanged (platform-agnostic)
└── ...
```

## Platform Abstraction Layer

### PlatformInterface (Abstract Base Class)

```python
from abc import ABC, abstractmethod
from typing import Optional, List
from ..core.models import Article, ContentBlock

class PlatformInterface(ABC):
    """Abstract interface for publishing platforms."""
    
    def __init__(self, playwright_controller, config: dict):
        """
        Initialize platform.
        
        Args:
            playwright_controller: Playwright controller instance
            config: Platform-specific configuration
        """
        self.playwright_controller = playwright_controller
        self.config = config
    
    @abstractmethod
    async def authenticate(self) -> bool:
        """
        Authenticate with platform.
        
        Returns:
            True if authentication successful
        """
        pass
    
    @abstractmethod
    async def check_logged_in(self) -> bool:
        """
        Check if currently logged in.
        
        Returns:
            True if logged in
        """
        pass
    
    @abstractmethod
    async def restore_session(self) -> bool:
        """
        Restore session from saved cookies.
        
        Returns:
            True if session restored
        """
        pass
    
    @abstractmethod
    async def save_session(self):
        """Save session cookies."""
        pass
    
    @abstractmethod
    async def logout(self):
        """Logout from platform."""
        pass
    
    @abstractmethod
    async def create_new_story(self):
        """Navigate to new story/post page."""
        pass
    
    @abstractmethod
    async def navigate_to_draft(self, draft_url: str):
        """
        Navigate to existing draft.
        
        Args:
            draft_url: Platform-specific draft URL
        """
        pass
    
    @abstractmethod
    async def validate_draft_url(self, url: str) -> bool:
        """
        Validate draft URL format.
        
        Args:
            url: Draft URL to validate
            
        Returns:
            True if valid for this platform
        """
        pass
    
    @abstractmethod
    async def clear_editor_content(self):
        """Clear existing content in editor."""
        pass
    
    @abstractmethod
    async def type_title(self, title: str):
        """
        Type article title.
        
        Args:
            title: Article title
        """
        pass
    
    @abstractmethod
    async def type_content(self, blocks: List[ContentBlock]) -> List[str]:
        """
        Type article content.
        
        Args:
            blocks: Content blocks to type
            
        Returns:
            List of placeholder strings found
        """
        pass
    
    @abstractmethod
    async def add_metadata(self, article: Article):
        """
        Add platform-specific metadata.
        
        Args:
            article: Article with metadata
        """
        pass
    
    @abstractmethod
    async def publish(self, mode: str) -> Optional[str]:
        """
        Publish article.
        
        Args:
            mode: Publishing mode (platform-specific)
            
        Returns:
            Draft/published URL
        """
        pass
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """
        Get platform name.
        
        Returns:
            Platform name (e.g., "Medium", "Substack")
        """
        pass
    
    @abstractmethod
    def get_supported_publish_modes(self) -> List[str]:
        """
        Get supported publishing modes.
        
        Returns:
            List of mode names (e.g., ["draft", "public"])
        """
        pass
```

### PlatformFactory

```python
from typing import Dict, Type
from .platform_interface import PlatformInterface
from .medium.medium_platform import MediumPlatform
from .substack.substack_platform import SubstackPlatform

class PlatformFactory:
    """Factory for creating platform instances."""
    
    _platforms: Dict[str, Type[PlatformInterface]] = {
        "medium": MediumPlatform,
        "substack": SubstackPlatform,
    }
    
    @classmethod
    def create_platform(
        cls,
        platform_name: str,
        playwright_controller,
        config: dict
    ) -> PlatformInterface:
        """
        Create platform instance.
        
        Args:
            platform_name: Platform name ("medium", "substack")
            playwright_controller: Playwright controller
            config: Platform-specific configuration
            
        Returns:
            Platform instance
            
        Raises:
            ValueError: If platform not supported
        """
        platform_class = cls._platforms.get(platform_name.lower())
        if not platform_class:
            raise ValueError(f"Unsupported platform: {platform_name}")
        
        return platform_class(playwright_controller, config)
    
    @classmethod
    def get_supported_platforms(cls) -> List[str]:
        """
        Get list of supported platforms.
        
        Returns:
            List of platform names
        """
        return list(cls._platforms.keys())
    
    @classmethod
    def register_platform(cls, name: str, platform_class: Type[PlatformInterface]):
        """
        Register a new platform.
        
        Args:
            name: Platform name
            platform_class: Platform class
        """
        cls._platforms[name.lower()] = platform_class
```

## Platform Implementations

### Medium Platform

**File**: `platforms/medium/medium_platform.py`

```python
class MediumPlatform(PlatformInterface):
    """Medium platform implementation."""
    
    def __init__(self, playwright_controller, config: dict):
        super().__init__(playwright_controller, config)
        self.auth_handler = MediumAuth(playwright_controller, config)
        self.typer = MediumTyper(playwright_controller.page, config)
        self.selectors = self._load_selectors()
    
    def get_platform_name(self) -> str:
        return "Medium"
    
    def get_supported_publish_modes(self) -> List[str]:
        return ["draft", "public"]
    
    async def authenticate(self) -> bool:
        return await self.auth_handler.login()
    
    # ... implement all abstract methods
```

### Substack Platform

**File**: `platforms/substack/substack_platform.py`

```python
class SubstackPlatform(PlatformInterface):
    """Substack platform implementation."""
    
    def __init__(self, playwright_controller, config: dict):
        super().__init__(playwright_controller, config)
        self.auth_handler = SubstackAuth(playwright_controller, config)
        self.typer = SubstackTyper(playwright_controller.page, config)
        self.selectors = self._load_selectors()
    
    def get_platform_name(self) -> str:
        return "Substack"
    
    def get_supported_publish_modes(self) -> List[str]:
        return ["draft", "send"]
    
    async def authenticate(self) -> bool:
        return await self.auth_handler.login()
    
    # ... implement all abstract methods
```

## Configuration Structure

### Multi-Platform Configuration

```yaml
# config/default_config.yaml

# Global settings (platform-agnostic)
typing:
  speed_ms: 30
  paragraph_delay_ms: 100
  max_chars_per_minute: 35
  human_typing_enabled: true
  typo_frequency: low

browser:
  headless: false
  timeout_seconds: 30

paths:
  last_directory: ""
  articles_directory: ""

# Platform selection
platform:
  selected: "medium"  # Current platform
  last_used: "medium"

# Platform-specific configurations
platforms:
  medium:
    publishing:
      default_mode: draft
      auto_add_tags: true
      max_tags: 5
      remember_draft_url: true
    credentials:
      remember_login: false
    paths:
      last_draft_url: ""
      session_cookies: "~/.medium_publisher/medium_session_cookies.json"
  
  substack:
    publishing:
      default_mode: draft
      auto_add_categories: true
      remember_draft_url: true
    credentials:
      remember_login: false
    paths:
      last_draft_url: ""
      session_cookies: "~/.medium_publisher/substack_session_cookies.json"
      custom_domain: ""  # Optional custom domain
```

## UI Changes

### Main Window Updates

**New UI Elements**:
- Platform selector dropdown (above file selection)
- Platform-specific status indicator
- Platform-specific draft URL validation

**Updated Methods**:
```python
class MainWindow(QMainWindow):
    def __init__(self, config_manager: ConfigManager):
        # ... existing code ...
        self.current_platform: str = "medium"
        self.platform_factory = PlatformFactory()
        
    def _create_platform_selection_group(self) -> QGroupBox:
        """Create platform selection group."""
        group = QGroupBox("Publishing Platform")
        layout = QHBoxLayout()
        
        layout.addWidget(QLabel("Platform:"))
        
        self.platform_selector = QComboBox()
        self.platform_selector.addItems(
            self.platform_factory.get_supported_platforms()
        )
        self.platform_selector.currentTextChanged.connect(self.set_platform)
        layout.addWidget(self.platform_selector)
        
        self.platform_status_label = QLabel("Not configured")
        layout.addWidget(self.platform_status_label)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def set_platform(self, platform: str):
        """Set current platform."""
        self.current_platform = platform
        self.config.set("platform.selected", platform)
        
        # Update UI for platform-specific options
        self._update_platform_ui()
        
        # Clear platform-specific state
        self.draft_url_input.clear()
        
        # Check authentication status
        self._check_platform_authentication()
```

## Publishing Workflow Updates

### Updated PublishingWorkflow

```python
class PublishingWorkflow:
    """Platform-agnostic publishing workflow."""
    
    def __init__(
        self,
        platform_name: str,
        config: Dict[str, Any],
        session_manager: SessionManager,
        progress_callback: Optional[Callable] = None
    ):
        self.platform_name = platform_name
        self.config = config
        self.session_manager = session_manager
        self.progress_callback = progress_callback
        
        # Platform instance (created during workflow)
        self.platform: Optional[PlatformInterface] = None
    
    async def publish_article(
        self,
        article_path: str,
        version: str = "v1",
        draft_url: Optional[str] = None,
        publish_mode: str = "draft"
    ) -> PublishingResult:
        """Publish article using selected platform."""
        
        try:
            # Initialize browser and platform
            await self._initialize_platform()
            
            # Validate publish mode for platform
            if publish_mode not in self.platform.get_supported_publish_modes():
                raise PublishingError(
                    f"Publish mode '{publish_mode}' not supported by "
                    f"{self.platform.get_platform_name()}"
                )
            
            # Rest of workflow uses platform interface
            # ... existing workflow code ...
            
        except Exception as e:
            logger.exception(f"Publishing failed on {self.platform_name}: {e}")
            raise
    
    async def _initialize_platform(self):
        """Initialize platform instance."""
        # Create Playwright controller
        self.playwright_controller = PlaywrightController(...)
        await self.playwright_controller.initialize()
        
        # Create platform instance
        platform_config = self.config.get(f"platforms.{self.platform_name}", {})
        self.platform = PlatformFactory.create_platform(
            self.platform_name,
            self.playwright_controller,
            platform_config
        )
```

## Migration Strategy

### Phase 1: Create Abstraction Layer
1. Create `platforms/` directory structure
2. Implement `PlatformInterface` abstract class
3. Implement `PlatformFactory`
4. Add platform configuration structure

### Phase 2: Refactor Medium Implementation
1. Create `platforms/medium/` directory
2. Move `MediumEditor` → `MediumPlatform`
3. Move `AuthHandler` → `MediumAuth`
4. Move `ContentTyper` → `MediumTyper`
5. Update imports throughout codebase
6. Test Medium functionality (ensure no regression)

### Phase 3: Implement Substack Platform
1. Create `platforms/substack/` directory
2. Implement `SubstackPlatform`
3. Implement `SubstackAuth`
4. Implement `SubstackTyper`
5. Create `substack_selectors.yaml`
6. Test Substack functionality

### Phase 4: Update UI and Workflow
1. Add platform selector to UI
2. Update `PublishingWorkflow` to use `PlatformInterface`
3. Update `ConfigManager` for multi-platform config
4. Update `SessionManager` for multi-platform sessions
5. Add platform-specific settings dialog

### Phase 5: Testing and Documentation
1. Test both platforms independently
2. Test platform switching
3. Test multi-platform sessions
4. Update user documentation
5. Update developer documentation

## Substack-Specific Implementation Notes

### Substack Editor Differences

**Editor Type**: Substack uses a markdown-native editor (not WYSIWYG like Medium)

**Implications**:
- May be able to paste markdown directly instead of typing
- Keyboard shortcuts different from Medium
- Formatting applied differently

### Substack Authentication

**Method**: Email/password only (no OAuth)

**Flow**:
1. Navigate to substack.com/sign-in
2. Enter email
3. Enter password
4. Handle 2FA if enabled
5. Save session cookies

### Substack Selectors (Preliminary)

```yaml
substack:
  login:
    sign_in_button: 'a[href*="sign-in"]'
    email_input: 'input[type="email"]'
    password_input: 'input[type="password"]'
    submit_button: 'button[type="submit"]'
  
  logged_in_indicators:
    user_menu: '[data-testid="user-menu"]'
    new_post_button: 'a[href*="/publish"]'
  
  editor:
    new_post_link: 'a[href*="/publish"]'
    title_field: 'textarea[placeholder*="Title"]'
    content_area: 'div[contenteditable="true"]'
    publish_button: 'button:has-text("Publish")'
  
  publishing:
    category_input: 'input[placeholder*="category"]'
    draft_button: 'button:has-text("Save draft")'
    send_button: 'button:has-text("Publish now")'
```

## Testing Strategy

### Platform Interface Tests
- Test abstract interface contract
- Test factory creation
- Test platform registration

### Platform-Specific Tests
- Test Medium platform (existing tests)
- Test Substack platform (new tests)
- Test authentication for each platform
- Test content typing for each platform
- Test publishing for each platform

### Integration Tests
- Test platform switching
- Test multi-platform sessions
- Test configuration management
- Test UI updates

### Regression Tests
- Ensure existing Medium functionality works
- Ensure no performance degradation
- Ensure backward compatibility

## Future Enhancements

### Additional Platforms
- Dev.to
- Hashnode
- Ghost
- WordPress

### Platform-Specific Features
- Medium: Image upload, series/collections
- Substack: Email scheduling, subscriber management
- Cross-posting: Publish to multiple platforms simultaneously

## Technology Stack

- **Language**: Python 3.11+
- **UI Framework**: PyQt6
- **Browser Automation**: Playwright
- **Markdown Parsing**: markdown2 or mistune
- **Configuration**: PyYAML
- **Credential Storage**: keyring
- **Logging**: Python logging module
- **Testing**: pytest, pytest-asyncio, pytest-qt
- **Design Pattern**: Strategy Pattern for platform abstraction

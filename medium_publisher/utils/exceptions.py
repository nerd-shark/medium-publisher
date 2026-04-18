"""
Custom exceptions for Medium Article Publisher.

This module defines the exception hierarchy for the application,
providing specific error types for different failure scenarios.
"""


class PublishingError(Exception):
    """
    Base exception for all publishing-related errors.
    
    All custom exceptions in the application inherit from this base class,
    allowing for broad exception handling when needed.
    
    Attributes:
        message: Human-readable error message
        details: Optional dictionary with additional error context
    """
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize PublishingError.
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class AuthenticationError(PublishingError):
    """
    Exception raised when authentication with Medium fails.
    
    This includes login failures, session expiration, invalid credentials,
    and 2FA issues.
    
    Examples:
        - Invalid email or password
        - Session cookies expired
        - 2FA code required but not provided
        - Account locked or suspended
    """
    pass


class BrowserError(PublishingError):
    """
    Exception raised when browser automation encounters an error.
    
    This includes browser crashes, page load failures, selector not found,
    timeout errors, and other Playwright-related issues.
    
    Examples:
        - Browser process crashed
        - Page load timeout
        - CSS selector not found (Medium UI changed)
        - Network connection lost
        - JavaScript execution failed
    """
    pass


class ContentError(PublishingError):
    """
    Exception raised when content processing fails.
    
    This includes markdown parsing errors, invalid formatting,
    unsupported syntax, and content validation failures.
    
    Examples:
        - Malformed markdown syntax
        - Invalid frontmatter YAML
        - Content exceeds size limits
        - Unsupported markdown features
        - Invalid characters in content
    """
    pass


class FileError(PublishingError):
    """
    Exception raised when file operations fail.
    
    This includes file not found, permission denied, invalid file format,
    and I/O errors.
    
    Examples:
        - File not found at specified path
        - Permission denied reading file
        - File is not a valid markdown file
        - File is empty or corrupted
        - Directory does not exist
    """
    pass


class EmergencyStopError(PublishingError):
    """
    Exception raised when the emergency stop is triggered.
    
    This halts all OS-level keyboard and mouse automation immediately.
    All held modifier keys are released before this exception propagates.
    
    Examples:
        - User pressed the emergency stop hotkey (Ctrl+Shift+Escape)
        - User moved mouse to screen corner (pyautogui failsafe)
        - User clicked the Emergency Stop button in the UI
    """
    pass


class NavigationError(PublishingError):
    """
    Exception raised when screen navigation or login detection fails.
    
    This includes failures in the navigation state machine, screen
    recognition timeouts, and login flow errors.
    
    Examples:
        - No reference image matched the current screen within timeout
        - Login timeout exceeded (5 minutes)
        - Page load timeout exceeded (30 seconds)
        - Unexpected navigation state transition
    """
    pass


class InputControlError(PublishingError):
    """
    Exception raised when OS-level input control operations fail.
    
    This includes pyautogui/pynput failures for keyboard and mouse events.
    
    Examples:
        - Failed to type character via pyautogui
        - Failed to click at screen coordinates
        - Image not found on screen for click_image
        - Key combination failed to execute
    """
    pass


class FocusLostError(PublishingError):
    """
    Exception raised when the target window loses focus during typing.
    
    Typing is paused when the active window changes away from the
    expected browser/editor window.
    
    Examples:
        - User switched to another application during typing
        - A system notification stole focus
        - The browser window was minimized or closed
    """
    pass

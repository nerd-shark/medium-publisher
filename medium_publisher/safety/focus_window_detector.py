"""
Focus window detector for OS-level input automation.

Monitors the active window to detect focus changes during typing,
pausing automation if the user switches away from the target window.
"""

from typing import Optional

from medium_publisher.utils.exceptions import FocusLostError
from medium_publisher.utils.logger import get_logger

logger = get_logger("safety.focus_window_detector")

# Platform-specific window detection
try:
    import win32gui  # type: ignore[import-untyped]
    _HAS_WIN32 = True
except ImportError:
    _HAS_WIN32 = False
    logger.debug("win32gui not available; window detection will use fallback")


class FocusWindowDetector:
    """Monitors the active window to detect focus changes during typing.

    Uses win32gui on Windows for native window title detection.
    Falls back to a no-op implementation on unsupported platforms.
    """

    def __init__(self) -> None:
        """Initialize with platform-specific window detection."""
        self._target_title: Optional[str] = None
        logger.info(
            "FocusWindowDetector initialized (win32gui available: %s)",
            _HAS_WIN32,
        )

    def get_active_window_title(self) -> str:
        """Return the title of the currently focused window.

        Returns:
            Window title string, or empty string if detection fails.
        """
        if _HAS_WIN32:
            try:
                hwnd = win32gui.GetForegroundWindow()
                title = win32gui.GetWindowText(hwnd)
                return title
            except Exception as e:
                logger.error("Failed to get active window title: %s", e)
                return ""
        return ""

    def capture_target_window(self) -> None:
        """Capture the current window title as the expected target.

        Should be called just before typing begins so the detector
        knows which window to monitor.
        """
        self._target_title = self.get_active_window_title()
        logger.info("Target window captured: '%s'", self._target_title)

    def is_target_focused(self) -> bool:
        """Check if the target window still has focus.

        Returns:
            True if the target window is focused or if no target has been
            captured yet. False if focus has shifted to a different window.
        """
        if self._target_title is None:
            return True

        current_title = self.get_active_window_title()
        if not current_title:
            # Cannot determine — assume focused to avoid false positives
            return True

        focused = current_title == self._target_title
        if not focused:
            logger.warning(
                "Focus lost: expected '%s', got '%s'",
                self._target_title,
                current_title,
            )
        return focused

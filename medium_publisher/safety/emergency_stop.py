"""
Emergency stop mechanism for OS-level input automation.

Provides immediate halt of all keyboard and mouse automation via
configurable hotkey, mouse-to-corner failsafe, or programmatic trigger.
"""

import threading
from typing import Optional

import pyautogui
from pynput.keyboard import GlobalHotKeys

from medium_publisher.utils.exceptions import EmergencyStopError
from medium_publisher.utils.logger import get_logger

logger = get_logger("safety.emergency_stop")


class EmergencyStop:
    """Safety mechanism for immediately halting all automation.

    Uses pynput GlobalHotKeys in a background thread for hotkey detection
    and pyautogui FAILSAFE for mouse-to-corner detection. When triggered,
    all held modifier keys are released and a stopped flag is set.

    Attributes:
        hotkey: Key combination string for emergency stop trigger.
    """

    def __init__(self, hotkey: str = "ctrl+shift+escape") -> None:
        """Initialize EmergencyStop.

        Args:
            hotkey: Key combination string (e.g. 'ctrl+shift+escape').
        """
        self._hotkey = hotkey
        self._stopped = False
        self._paused = False
        self._lock = threading.Lock()
        self._listener: Optional[GlobalHotKeys] = None
        self._monitoring = False

        # Enable pyautogui failsafe (mouse-to-corner detection)
        pyautogui.FAILSAFE = True

        logger.info("EmergencyStop initialized with hotkey: %s", hotkey)

    def _build_hotkey_str(self) -> str:
        """Convert hotkey config string to pynput GlobalHotKeys format.

        Converts 'ctrl+shift+escape' to '<ctrl>+<shift>+<esc>'.

        Returns:
            Formatted hotkey string for pynput GlobalHotKeys.
        """
        key_map = {
            "ctrl": "<ctrl>",
            "shift": "<shift>",
            "alt": "<alt>",
            "escape": "<esc>",
            "esc": "<esc>",
            "enter": "<enter>",
            "tab": "<tab>",
            "space": "<space>",
        }
        parts = self._hotkey.lower().split("+")
        mapped = [key_map.get(p.strip(), p.strip()) for p in parts]
        return "+".join(mapped)

    def start_monitoring(self) -> None:
        """Start listening for hotkey via pynput GlobalHotKeys in a background thread."""
        if self._monitoring:
            logger.warning("Monitoring already active")
            return

        hotkey_str = self._build_hotkey_str()
        logger.info("Starting hotkey monitoring: %s", hotkey_str)

        self._listener = GlobalHotKeys({hotkey_str: self._on_hotkey})
        self._listener.daemon = True
        self._listener.start()
        self._monitoring = True
        logger.info("Emergency stop monitoring started")

    def stop_monitoring(self) -> None:
        """Stop the pynput listener thread."""
        if self._listener is not None:
            self._listener.stop()
            self._listener = None
        self._monitoring = False
        logger.info("Emergency stop monitoring stopped")

    def _on_hotkey(self) -> None:
        """Callback when emergency stop hotkey is pressed."""
        logger.warning("Emergency stop hotkey detected!")
        self.trigger()

    def trigger(self) -> None:
        """Trigger emergency stop.

        Sets the stopped flag and releases all held modifier keys.
        This should halt all pending input events within 100ms.
        """
        with self._lock:
            self._stopped = True
            self._paused = False
        logger.warning("EMERGENCY STOP TRIGGERED")
        self.release_all_keys()

    def reset(self) -> None:
        """Reset stopped state to allow automation to resume."""
        with self._lock:
            self._stopped = False
            self._paused = False
        logger.info("Emergency stop reset")

    def is_stopped(self) -> bool:
        """Check if emergency stop has been triggered.

        Returns:
            True if stopped or paused.
        """
        with self._lock:
            return self._stopped or self._paused

    @property
    def is_paused(self) -> bool:
        """Check if automation is in paused state (vs fully stopped).

        Returns:
            True if paused but not fully stopped.
        """
        with self._lock:
            return self._paused and not self._stopped

    def pause(self) -> None:
        """Pause automation (stop after current word)."""
        with self._lock:
            self._paused = True
        logger.info("Automation paused")

    def resume(self) -> None:
        """Resume automation from paused state."""
        with self._lock:
            if self._stopped:
                logger.warning("Cannot resume: emergency stop is active. Call reset() first.")
                return
            self._paused = False
        logger.info("Automation resumed")

    def release_all_keys(self) -> None:
        """Release all held modifier keys (Ctrl, Shift, Alt).

        Called on trigger to ensure no modifier keys remain held,
        preventing stuck-key scenarios.
        """
        modifier_keys = ["ctrl", "shift", "alt", "win"]
        for key in modifier_keys:
            try:
                pyautogui.keyUp(key)
            except Exception as e:
                logger.error("Failed to release key '%s': %s", key, e)
        logger.info("All modifier keys released")

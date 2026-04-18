"""
OS-level input controller for keyboard and mouse automation.

Generates real operating system keyboard and mouse events via pyautogui,
with safety checks for emergency stop and focus window detection before
every action.
"""

import time
from typing import Optional, Tuple

import pyautogui

from medium_publisher.safety.emergency_stop import EmergencyStop
from medium_publisher.safety.focus_window_detector import FocusWindowDetector
from medium_publisher.utils.exceptions import (
    EmergencyStopError,
    FocusLostError,
    InputControlError,
)
from medium_publisher.utils.logger import get_logger

logger = get_logger("automation.os_input_controller")


class OS_Input_Controller:
    """Generates real OS-level keyboard and mouse events via pyautogui.

    Every method that produces input checks the emergency stop and focus
    window state before executing. If the emergency stop has been triggered,
    ``EmergencyStopError`` is raised. If the target window has lost focus,
    ``FocusLostError`` is raised.

    Args:
        emergency_stop: Injected EmergencyStop for halt-state checks.
        focus_detector: Injected FocusWindowDetector for window-focus checks.
    """

    def __init__(
        self,
        emergency_stop: EmergencyStop,
        focus_detector: FocusWindowDetector,
    ) -> None:
        self._emergency_stop = emergency_stop
        self._focus_detector = focus_detector
        logger.info("OS_Input_Controller initialized")

    def _check_safety(self) -> None:
        """Check emergency stop and focus window before any action.

        Raises:
            EmergencyStopError: If the emergency stop has been triggered.
            FocusLostError: If the target window has lost focus.
        """
        if self._emergency_stop.is_stopped():
            logger.warning("Action blocked: emergency stop is active")
            raise EmergencyStopError("Emergency stop is active")
        if not self._focus_detector.is_target_focused():
            logger.warning("Action blocked: target window lost focus")
            raise FocusLostError("Target window lost focus")

    # ------------------------------------------------------------------
    # Keyboard methods
    # ------------------------------------------------------------------

    def type_character(self, char: str) -> None:
        """Type a single character.

        Args:
            char: The character to type.

        Raises:
            EmergencyStopError: If stopped.
            FocusLostError: If focus lost.
            InputControlError: If pyautogui fails.
        """
        self._check_safety()
        try:
            pyautogui.write(char, interval=0)
        except Exception as exc:
            logger.error("Failed to type character '%s': %s", char, exc)
            raise InputControlError(
                f"Failed to type character '{char}'", details={"error": str(exc)}
            ) from exc

    def type_text(self, text: str, delay_ms: int = 200) -> None:
        """Type a string character-by-character with configurable delay.

        Args:
            text: The text to type.
            delay_ms: Delay between keystrokes in milliseconds.

        Raises:
            EmergencyStopError: If stopped.
            FocusLostError: If focus lost.
            InputControlError: If pyautogui fails.
        """
        interval = delay_ms / 1000.0
        for char in text:
            self._check_safety()
            try:
                pyautogui.write(char, interval=0)
            except Exception as exc:
                logger.error("Failed to type text at char '%s': %s", char, exc)
                raise InputControlError(
                    f"Failed to type text", details={"char": char, "error": str(exc)}
                ) from exc
            time.sleep(interval)

    def press_key(self, key: str) -> None:
        """Press and release a single key (e.g. 'enter', 'backspace').

        Args:
            key: The key name recognised by pyautogui.

        Raises:
            EmergencyStopError: If stopped.
            FocusLostError: If focus lost.
            InputControlError: If pyautogui fails.
        """
        self._check_safety()
        try:
            pyautogui.press(key)
        except Exception as exc:
            logger.error("Failed to press key '%s': %s", key, exc)
            raise InputControlError(
                f"Failed to press key '{key}'", details={"error": str(exc)}
            ) from exc

    def hotkey(self, *keys: str) -> None:
        """Press a key combination (e.g. ``hotkey('ctrl', 'alt', '1')``).

        Args:
            *keys: Key names to press simultaneously.

        Raises:
            EmergencyStopError: If stopped.
            FocusLostError: If focus lost.
            InputControlError: If pyautogui fails.
        """
        self._check_safety()
        try:
            pyautogui.hotkey(*keys)
        except Exception as exc:
            logger.error("Failed to execute hotkey %s: %s", keys, exc)
            raise InputControlError(
                f"Failed to execute hotkey {keys}", details={"error": str(exc)}
            ) from exc

    def select_text_backwards(self, char_count: int) -> None:
        """Select text backwards using Shift+Left arrow.

        Args:
            char_count: Number of characters to select.

        Raises:
            EmergencyStopError: If stopped.
            FocusLostError: If focus lost.
            InputControlError: If pyautogui fails.
        """
        self._check_safety()
        try:
            for _ in range(char_count):
                pyautogui.hotkey("shift", "left")
        except Exception as exc:
            logger.error("Failed to select text backwards: %s", exc)
            raise InputControlError(
                "Failed to select text backwards", details={"error": str(exc)}
            ) from exc

    # ------------------------------------------------------------------
    # Mouse methods
    # ------------------------------------------------------------------

    def click_at(self, x: int, y: int) -> None:
        """Move mouse to (x, y) and click.

        Args:
            x: Horizontal screen coordinate.
            y: Vertical screen coordinate.

        Raises:
            EmergencyStopError: If stopped.
            FocusLostError: If focus lost.
            InputControlError: If pyautogui fails.
        """
        self._check_safety()
        try:
            pyautogui.click(x, y)
        except Exception as exc:
            logger.error("Failed to click at (%d, %d): %s", x, y, exc)
            raise InputControlError(
                f"Failed to click at ({x}, {y})", details={"error": str(exc)}
            ) from exc

    def click_image(self, image_path: str, confidence: float = 0.8) -> bool:
        """Locate an image on screen and click its centre.

        Args:
            image_path: Path to the reference image file.
            confidence: Matching confidence threshold (0.0–1.0).

        Returns:
            True if the image was found and clicked, False otherwise.

        Raises:
            EmergencyStopError: If stopped.
            FocusLostError: If focus lost.
        """
        self._check_safety()
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location is not None:
                centre = pyautogui.center(location)
                pyautogui.click(centre)
                logger.info("Clicked image '%s' at %s", image_path, centre)
                return True
            logger.info("Image '%s' not found on screen", image_path)
            return False
        except Exception as exc:
            logger.error("Error during click_image for '%s': %s", image_path, exc)
            return False

    def scroll(self, clicks: int) -> None:
        """Scroll the mouse wheel.

        Args:
            clicks: Number of scroll increments. Positive = up, negative = down.

        Raises:
            EmergencyStopError: If stopped.
            FocusLostError: If focus lost.
            InputControlError: If pyautogui fails.
        """
        self._check_safety()
        try:
            pyautogui.scroll(clicks)
        except Exception as exc:
            logger.error("Failed to scroll %d clicks: %s", clicks, exc)
            raise InputControlError(
                f"Failed to scroll {clicks} clicks", details={"error": str(exc)}
            ) from exc

    # ------------------------------------------------------------------
    # Safety helpers
    # ------------------------------------------------------------------

    def release_all_keys(self) -> None:
        """Release all held modifier keys (Ctrl, Shift, Alt, Win).

        Delegates to pyautogui.keyUp for each modifier. Errors are logged
        but not raised so this method is safe to call during cleanup.
        """
        modifier_keys = ["ctrl", "shift", "alt", "win"]
        for key in modifier_keys:
            try:
                pyautogui.keyUp(key)
            except Exception as exc:
                logger.error("Failed to release key '%s': %s", key, exc)
        logger.info("All modifier keys released via OS_Input_Controller")

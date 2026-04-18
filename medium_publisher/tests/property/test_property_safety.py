"""
Property-based tests for the Safety Layer.

Tests Properties 19 and 20 from the design document:
- Property 19: Emergency stop releases all held modifier keys
- Property 20: Focus window change pauses typing
"""

import threading
from unittest.mock import patch, MagicMock, call

import pytest
from hypothesis import given, strategies as st, settings

from medium_publisher.safety.emergency_stop import EmergencyStop
from medium_publisher.safety.focus_window_detector import FocusWindowDetector


class TestProperty19EmergencyStopReleasesKeys:
    """Property 19: Emergency stop releases all held modifier keys.

    When trigger() is called, release_all_keys() must be invoked,
    ensuring no modifier keys remain held.

    **Validates: Requirements 6.4**
    """

    @given(hotkey=st.sampled_from([
        "ctrl+shift+escape",
        "ctrl+alt+delete",
        "ctrl+shift+q",
    ]))
    @settings(max_examples=20)
    @patch("medium_publisher.safety.emergency_stop.pyautogui")
    @patch("medium_publisher.safety.emergency_stop.GlobalHotKeys")
    def test_trigger_always_releases_all_modifier_keys(
        self, mock_hotkeys_cls: MagicMock, mock_pyautogui: MagicMock, hotkey: str
    ) -> None:
        """For any hotkey config, trigger() must call keyUp for all modifiers."""
        es = EmergencyStop(hotkey=hotkey)
        mock_pyautogui.reset_mock()

        es.trigger()

        assert es.is_stopped() is True
        expected_keys = {"ctrl", "shift", "alt", "win"}
        released_keys = {
            c.args[0] for c in mock_pyautogui.keyUp.call_args_list
        }
        assert expected_keys == released_keys

    @given(trigger_count=st.integers(min_value=1, max_value=5))
    @settings(max_examples=10)
    @patch("medium_publisher.safety.emergency_stop.pyautogui")
    @patch("medium_publisher.safety.emergency_stop.GlobalHotKeys")
    def test_multiple_triggers_always_release_keys(
        self, mock_hotkeys_cls: MagicMock, mock_pyautogui: MagicMock, trigger_count: int
    ) -> None:
        """Triggering multiple times always releases keys each time."""
        es = EmergencyStop()
        mock_pyautogui.reset_mock()

        for _ in range(trigger_count):
            es.trigger()

        # Each trigger should release 4 modifier keys
        assert mock_pyautogui.keyUp.call_count == trigger_count * 4


class TestProperty20FocusWindowChangePausesTyping:
    """Property 20: Focus window change pauses typing.

    When is_target_focused() returns False, typing should be paused.

    **Validates: Requirements 6.9**
    """

    @given(
        target_title=st.text(min_size=1, max_size=100).filter(lambda s: s.strip()),
        other_title=st.text(min_size=1, max_size=100).filter(lambda s: s.strip()),
    )
    @settings(max_examples=50)
    def test_different_window_title_returns_not_focused(
        self, target_title: str, other_title: str
    ) -> None:
        """For any two distinct window titles, is_target_focused returns False
        when the active window differs from the captured target."""
        if target_title == other_title:
            return  # Skip when titles happen to match

        detector = FocusWindowDetector()

        with patch.object(detector, "get_active_window_title") as mock_get:
            # Capture target
            mock_get.return_value = target_title
            detector.capture_target_window()

            # Simulate focus change
            mock_get.return_value = other_title
            assert detector.is_target_focused() is False

    @given(title=st.text(min_size=1, max_size=100).filter(lambda s: s.strip()))
    @settings(max_examples=50)
    def test_same_window_title_returns_focused(self, title: str) -> None:
        """For any window title, is_target_focused returns True when
        the active window matches the captured target."""
        detector = FocusWindowDetector()

        with patch.object(detector, "get_active_window_title") as mock_get:
            mock_get.return_value = title
            detector.capture_target_window()
            assert detector.is_target_focused() is True

    @given(title=st.text(min_size=1, max_size=100).filter(lambda s: s.strip()))
    @settings(max_examples=20)
    def test_no_target_captured_always_returns_focused(self, title: str) -> None:
        """When no target has been captured, is_target_focused always returns True."""
        detector = FocusWindowDetector()
        # Don't capture target
        with patch.object(detector, "get_active_window_title") as mock_get:
            mock_get.return_value = title
            assert detector.is_target_focused() is True

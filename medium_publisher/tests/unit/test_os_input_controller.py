"""
Unit tests for OS_Input_Controller.

Mocks pyautogui and pynput calls, verifies correct key sequences,
emergency stop checks, and focus window integration.

Requirements: 4.1, 4.2
"""

from unittest.mock import patch, MagicMock, call

import pytest

from medium_publisher.automation.os_input_controller import OS_Input_Controller
from medium_publisher.utils.exceptions import (
    EmergencyStopError,
    FocusLostError,
    InputControlError,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_pyautogui():
    """Patch pyautogui inside the os_input_controller module."""
    with patch("medium_publisher.automation.os_input_controller.pyautogui") as mock:
        yield mock


@pytest.fixture
def emergency_stop():
    """Create a mock EmergencyStop."""
    es = MagicMock()
    es.is_stopped.return_value = False
    return es


@pytest.fixture
def focus_detector():
    """Create a mock FocusWindowDetector."""
    fd = MagicMock()
    fd.is_target_focused.return_value = True
    return fd


@pytest.fixture
def controller(mock_pyautogui, emergency_stop, focus_detector):
    """Create an OS_Input_Controller with mocked dependencies."""
    return OS_Input_Controller(emergency_stop, focus_detector)


# ---------------------------------------------------------------------------
# Emergency stop checks — every action must check before executing
# ---------------------------------------------------------------------------

class TestEmergencyStopBeforeAction:
    """Verify EmergencyStopError is raised when stopped, for every action."""

    def _stopped_controller(self, mock_pyautogui):
        es = MagicMock()
        es.is_stopped.return_value = True
        fd = MagicMock()
        fd.is_target_focused.return_value = True
        return OS_Input_Controller(es, fd)

    def test_type_character_raises(self, mock_pyautogui):
        ctrl = self._stopped_controller(mock_pyautogui)
        with pytest.raises(EmergencyStopError):
            ctrl.type_character("a")

    def test_type_text_raises(self, mock_pyautogui):
        ctrl = self._stopped_controller(mock_pyautogui)
        with pytest.raises(EmergencyStopError):
            ctrl.type_text("hello")

    def test_press_key_raises(self, mock_pyautogui):
        ctrl = self._stopped_controller(mock_pyautogui)
        with pytest.raises(EmergencyStopError):
            ctrl.press_key("enter")

    def test_hotkey_raises(self, mock_pyautogui):
        ctrl = self._stopped_controller(mock_pyautogui)
        with pytest.raises(EmergencyStopError):
            ctrl.hotkey("ctrl", "b")

    def test_click_at_raises(self, mock_pyautogui):
        ctrl = self._stopped_controller(mock_pyautogui)
        with pytest.raises(EmergencyStopError):
            ctrl.click_at(100, 200)

    def test_click_image_raises(self, mock_pyautogui):
        ctrl = self._stopped_controller(mock_pyautogui)
        with pytest.raises(EmergencyStopError):
            ctrl.click_image("test.png")

    def test_scroll_raises(self, mock_pyautogui):
        ctrl = self._stopped_controller(mock_pyautogui)
        with pytest.raises(EmergencyStopError):
            ctrl.scroll(3)


# ---------------------------------------------------------------------------
# Focus window checks — every action must check focus before executing
# ---------------------------------------------------------------------------

class TestFocusLostBeforeAction:
    """Verify FocusLostError is raised when target window loses focus."""

    def _unfocused_controller(self, mock_pyautogui):
        es = MagicMock()
        es.is_stopped.return_value = False
        fd = MagicMock()
        fd.is_target_focused.return_value = False
        return OS_Input_Controller(es, fd)

    def test_type_character_raises(self, mock_pyautogui):
        ctrl = self._unfocused_controller(mock_pyautogui)
        with pytest.raises(FocusLostError):
            ctrl.type_character("a")

    def test_type_text_raises(self, mock_pyautogui):
        ctrl = self._unfocused_controller(mock_pyautogui)
        with pytest.raises(FocusLostError):
            ctrl.type_text("hello")

    def test_press_key_raises(self, mock_pyautogui):
        ctrl = self._unfocused_controller(mock_pyautogui)
        with pytest.raises(FocusLostError):
            ctrl.press_key("enter")

    def test_hotkey_raises(self, mock_pyautogui):
        ctrl = self._unfocused_controller(mock_pyautogui)
        with pytest.raises(FocusLostError):
            ctrl.hotkey("ctrl", "b")

    def test_click_at_raises(self, mock_pyautogui):
        ctrl = self._unfocused_controller(mock_pyautogui)
        with pytest.raises(FocusLostError):
            ctrl.click_at(100, 200)

    def test_click_image_raises(self, mock_pyautogui):
        ctrl = self._unfocused_controller(mock_pyautogui)
        with pytest.raises(FocusLostError):
            ctrl.click_image("test.png")

    def test_scroll_raises(self, mock_pyautogui):
        ctrl = self._unfocused_controller(mock_pyautogui)
        with pytest.raises(FocusLostError):
            ctrl.scroll(3)


# ---------------------------------------------------------------------------
# Keyboard action tests
# ---------------------------------------------------------------------------

class TestTypeCharacter:
    """Test type_character delegates to pyautogui.write."""

    def test_delegates_to_pyautogui_write(self, controller, mock_pyautogui):
        controller.type_character("a")
        mock_pyautogui.write.assert_called_once_with("a", interval=0)

    def test_pyautogui_error_raises_input_control_error(self, controller, mock_pyautogui):
        mock_pyautogui.write.side_effect = Exception("fail")
        with pytest.raises(InputControlError):
            controller.type_character("x")


class TestTypeText:
    """Test type_text types each character with delay."""

    @patch("medium_publisher.automation.os_input_controller.time")
    def test_types_each_character(self, mock_time, controller, mock_pyautogui):
        controller.type_text("ab", delay_ms=100)
        assert mock_pyautogui.write.call_count == 2
        mock_pyautogui.write.assert_any_call("a", interval=0)
        mock_pyautogui.write.assert_any_call("b", interval=0)

    @patch("medium_publisher.automation.os_input_controller.time")
    def test_sleeps_between_characters(self, mock_time, controller, mock_pyautogui):
        controller.type_text("ab", delay_ms=200)
        assert mock_time.sleep.call_count == 2
        mock_time.sleep.assert_called_with(0.2)

    @patch("medium_publisher.automation.os_input_controller.time")
    def test_checks_safety_per_character(self, mock_time, controller, emergency_stop, mock_pyautogui):
        controller.type_text("abc", delay_ms=0)
        # is_stopped called once per character + once per is_target_focused
        assert emergency_stop.is_stopped.call_count == 3


class TestPressKey:
    """Test press_key delegates to pyautogui.press."""

    def test_delegates_to_pyautogui_press(self, controller, mock_pyautogui):
        controller.press_key("enter")
        mock_pyautogui.press.assert_called_once_with("enter")

    def test_pyautogui_error_raises_input_control_error(self, controller, mock_pyautogui):
        mock_pyautogui.press.side_effect = Exception("fail")
        with pytest.raises(InputControlError):
            controller.press_key("enter")


class TestHotkey:
    """Test hotkey delegates to pyautogui.hotkey."""

    def test_delegates_to_pyautogui_hotkey(self, controller, mock_pyautogui):
        controller.hotkey("ctrl", "alt", "1")
        mock_pyautogui.hotkey.assert_called_once_with("ctrl", "alt", "1")

    def test_pyautogui_error_raises_input_control_error(self, controller, mock_pyautogui):
        mock_pyautogui.hotkey.side_effect = Exception("fail")
        with pytest.raises(InputControlError):
            controller.hotkey("ctrl", "b")


class TestSelectTextBackwards:
    """Test select_text_backwards uses Shift+Left arrow."""

    def test_calls_shift_left_n_times(self, controller, mock_pyautogui):
        controller.select_text_backwards(3)
        assert mock_pyautogui.hotkey.call_count == 3
        mock_pyautogui.hotkey.assert_called_with("shift", "left")


# ---------------------------------------------------------------------------
# Mouse action tests
# ---------------------------------------------------------------------------

class TestClickAt:
    """Test click_at delegates to pyautogui.click."""

    def test_delegates_to_pyautogui_click(self, controller, mock_pyautogui):
        controller.click_at(100, 200)
        mock_pyautogui.click.assert_called_once_with(100, 200)

    def test_pyautogui_error_raises_input_control_error(self, controller, mock_pyautogui):
        mock_pyautogui.click.side_effect = Exception("fail")
        with pytest.raises(InputControlError):
            controller.click_at(50, 50)


class TestClickImage:
    """Test click_image locates and clicks image on screen."""

    def test_found_and_clicked(self, controller, mock_pyautogui):
        mock_pyautogui.locateOnScreen.return_value = (10, 20, 100, 50)
        mock_pyautogui.center.return_value = (60, 45)
        result = controller.click_image("btn.png", confidence=0.9)
        assert result is True
        mock_pyautogui.locateOnScreen.assert_called_once_with("btn.png", confidence=0.9)
        mock_pyautogui.click.assert_called_once_with((60, 45))

    def test_not_found_returns_false(self, controller, mock_pyautogui):
        mock_pyautogui.locateOnScreen.return_value = None
        result = controller.click_image("missing.png")
        assert result is False
        mock_pyautogui.click.assert_not_called()

    def test_exception_returns_false(self, controller, mock_pyautogui):
        mock_pyautogui.locateOnScreen.side_effect = Exception("screen error")
        result = controller.click_image("err.png")
        assert result is False


class TestScroll:
    """Test scroll delegates to pyautogui.scroll."""

    def test_delegates_to_pyautogui_scroll(self, controller, mock_pyautogui):
        controller.scroll(5)
        mock_pyautogui.scroll.assert_called_once_with(5)

    def test_negative_scroll(self, controller, mock_pyautogui):
        controller.scroll(-3)
        mock_pyautogui.scroll.assert_called_once_with(-3)

    def test_pyautogui_error_raises_input_control_error(self, controller, mock_pyautogui):
        mock_pyautogui.scroll.side_effect = Exception("fail")
        with pytest.raises(InputControlError):
            controller.scroll(1)


# ---------------------------------------------------------------------------
# release_all_keys
# ---------------------------------------------------------------------------

class TestReleaseAllKeys:
    """Test release_all_keys delegates to pyautogui.keyUp."""

    def test_releases_four_modifiers(self, controller, mock_pyautogui):
        mock_pyautogui.reset_mock()
        controller.release_all_keys()
        assert mock_pyautogui.keyUp.call_count == 4
        released = {c.args[0] for c in mock_pyautogui.keyUp.call_args_list}
        assert released == {"ctrl", "shift", "alt", "win"}

    def test_handles_keyup_exception_gracefully(self, controller, mock_pyautogui):
        mock_pyautogui.keyUp.side_effect = Exception("key error")
        # Should not raise
        controller.release_all_keys()

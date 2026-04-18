"""
Unit tests for EmergencyStop.

Tests trigger/reset/pause/resume state transitions, key release on trigger,
and hotkey monitoring lifecycle.

Requirements: 6.1–6.7
"""

import threading
from unittest.mock import patch, MagicMock, call

import pytest

from medium_publisher.safety.emergency_stop import EmergencyStop


@pytest.fixture
def mock_pyautogui():
    """Mock pyautogui for all tests."""
    with patch("medium_publisher.safety.emergency_stop.pyautogui") as mock:
        yield mock


@pytest.fixture
def mock_hotkeys():
    """Mock pynput GlobalHotKeys for all tests."""
    with patch("medium_publisher.safety.emergency_stop.GlobalHotKeys") as mock:
        yield mock


@pytest.fixture
def es(mock_pyautogui, mock_hotkeys):
    """Create an EmergencyStop instance with mocked dependencies."""
    return EmergencyStop()


class TestEmergencyStopInit:
    """Test EmergencyStop initialization."""

    def test_default_hotkey(self, mock_pyautogui, mock_hotkeys):
        es = EmergencyStop()
        assert es._hotkey == "ctrl+shift+escape"

    def test_custom_hotkey(self, mock_pyautogui, mock_hotkeys):
        es = EmergencyStop(hotkey="ctrl+alt+q")
        assert es._hotkey == "ctrl+alt+q"

    def test_failsafe_enabled(self, mock_pyautogui, mock_hotkeys):
        EmergencyStop()
        assert mock_pyautogui.FAILSAFE is True

    def test_initial_state_not_stopped(self, es):
        assert es.is_stopped() is False

    def test_initial_state_not_paused(self, es):
        assert es.is_paused is False


class TestTriggerResetCycle:
    """Test trigger and reset state transitions."""

    def test_trigger_sets_stopped(self, es, mock_pyautogui):
        es.trigger()
        assert es.is_stopped() is True

    def test_trigger_clears_paused(self, es, mock_pyautogui):
        es.pause()
        es.trigger()
        assert es.is_paused is False

    def test_reset_clears_stopped(self, es, mock_pyautogui):
        es.trigger()
        es.reset()
        assert es.is_stopped() is False

    def test_reset_clears_paused(self, es, mock_pyautogui):
        es.pause()
        es.reset()
        assert es.is_paused is False

    def test_trigger_releases_all_keys(self, es, mock_pyautogui):
        mock_pyautogui.reset_mock()
        es.trigger()
        released = {c.args[0] for c in mock_pyautogui.keyUp.call_args_list}
        assert released == {"ctrl", "shift", "alt", "win"}


class TestPauseResume:
    """Test pause and resume state transitions."""

    def test_pause_sets_paused(self, es):
        es.pause()
        assert es.is_paused is True

    def test_pause_makes_is_stopped_true(self, es):
        es.pause()
        assert es.is_stopped() is True

    def test_resume_clears_paused(self, es):
        es.pause()
        es.resume()
        assert es.is_paused is False

    def test_resume_clears_is_stopped(self, es):
        es.pause()
        es.resume()
        assert es.is_stopped() is False

    def test_resume_does_not_clear_stopped_state(self, es, mock_pyautogui):
        """Cannot resume from a full emergency stop — must reset first."""
        es.trigger()
        es.resume()
        assert es.is_stopped() is True

    def test_pause_resume_cycle(self, es):
        es.pause()
        assert es.is_paused is True
        es.resume()
        assert es.is_paused is False
        assert es.is_stopped() is False


class TestMonitoring:
    """Test hotkey monitoring lifecycle."""

    def test_start_monitoring_creates_listener(self, es, mock_hotkeys):
        es.start_monitoring()
        mock_hotkeys.assert_called_once()
        assert es._monitoring is True

    def test_start_monitoring_starts_listener(self, es, mock_hotkeys):
        es.start_monitoring()
        mock_hotkeys.return_value.start.assert_called_once()

    def test_stop_monitoring_stops_listener(self, es, mock_hotkeys):
        es.start_monitoring()
        es.stop_monitoring()
        mock_hotkeys.return_value.stop.assert_called_once()
        assert es._monitoring is False

    def test_double_start_monitoring_is_noop(self, es, mock_hotkeys):
        es.start_monitoring()
        es.start_monitoring()
        assert mock_hotkeys.call_count == 1

    def test_stop_without_start_is_safe(self, es, mock_hotkeys):
        es.stop_monitoring()
        assert es._monitoring is False


class TestHotkeyMapping:
    """Test hotkey string conversion for pynput."""

    def test_default_hotkey_mapping(self, es):
        result = es._build_hotkey_str()
        assert result == "<ctrl>+<shift>+<esc>"

    def test_custom_hotkey_mapping(self, mock_pyautogui, mock_hotkeys):
        es = EmergencyStop(hotkey="ctrl+alt+q")
        result = es._build_hotkey_str()
        assert result == "<ctrl>+<alt>+q"

    def test_hotkey_callback_triggers_stop(self, es, mock_pyautogui):
        es._on_hotkey()
        assert es.is_stopped() is True


class TestReleaseAllKeys:
    """Test release_all_keys behavior."""

    def test_releases_four_modifiers(self, es, mock_pyautogui):
        mock_pyautogui.reset_mock()
        es.release_all_keys()
        assert mock_pyautogui.keyUp.call_count == 4

    def test_handles_keyup_exception(self, es, mock_pyautogui):
        mock_pyautogui.keyUp.side_effect = Exception("key error")
        # Should not raise
        es.release_all_keys()


class TestThreadSafety:
    """Test thread safety of state transitions."""

    def test_concurrent_trigger_and_check(self, mock_pyautogui, mock_hotkeys):
        es = EmergencyStop()
        results = []

        def trigger_and_check():
            es.trigger()
            results.append(es.is_stopped())

        threads = [threading.Thread(target=trigger_and_check) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(results)

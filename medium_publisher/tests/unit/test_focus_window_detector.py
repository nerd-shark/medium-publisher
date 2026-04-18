"""
Unit tests for FocusWindowDetector.

Tests window title detection, target capture, and focus comparison logic.

Requirements: 6.9
"""

from unittest.mock import patch, MagicMock

import pytest

from medium_publisher.safety.focus_window_detector import FocusWindowDetector


@pytest.fixture
def detector():
    """Create a FocusWindowDetector instance."""
    return FocusWindowDetector()


class TestGetActiveWindowTitle:
    """Test get_active_window_title with mocked win32gui."""

    @patch("medium_publisher.safety.focus_window_detector._HAS_WIN32", True)
    @patch("medium_publisher.safety.focus_window_detector.win32gui")
    def test_returns_window_title(self, mock_win32gui):
        mock_win32gui.GetForegroundWindow.return_value = 12345
        mock_win32gui.GetWindowText.return_value = "Google Chrome"
        detector = FocusWindowDetector()
        assert detector.get_active_window_title() == "Google Chrome"

    @patch("medium_publisher.safety.focus_window_detector._HAS_WIN32", True)
    @patch("medium_publisher.safety.focus_window_detector.win32gui")
    def test_returns_empty_on_exception(self, mock_win32gui):
        mock_win32gui.GetForegroundWindow.side_effect = Exception("fail")
        detector = FocusWindowDetector()
        assert detector.get_active_window_title() == ""

    @patch("medium_publisher.safety.focus_window_detector._HAS_WIN32", False)
    def test_returns_empty_without_win32(self):
        detector = FocusWindowDetector()
        assert detector.get_active_window_title() == ""


class TestCaptureTargetWindow:
    """Test capture_target_window."""

    def test_captures_current_title(self, detector):
        with patch.object(detector, "get_active_window_title", return_value="Medium Editor"):
            detector.capture_target_window()
            assert detector._target_title == "Medium Editor"

    def test_captures_empty_title(self, detector):
        with patch.object(detector, "get_active_window_title", return_value=""):
            detector.capture_target_window()
            assert detector._target_title == ""


class TestIsTargetFocused:
    """Test is_target_focused comparison logic."""

    def test_returns_true_when_no_target_captured(self, detector):
        assert detector.is_target_focused() is True

    def test_returns_true_when_same_window(self, detector):
        with patch.object(detector, "get_active_window_title") as mock_get:
            mock_get.return_value = "Medium - New Story"
            detector.capture_target_window()
            assert detector.is_target_focused() is True

    def test_returns_false_when_different_window(self, detector):
        with patch.object(detector, "get_active_window_title") as mock_get:
            mock_get.return_value = "Medium - New Story"
            detector.capture_target_window()
            mock_get.return_value = "Visual Studio Code"
            assert detector.is_target_focused() is False

    def test_returns_true_when_active_title_empty(self, detector):
        """When we can't determine the active window, assume focused."""
        with patch.object(detector, "get_active_window_title") as mock_get:
            mock_get.return_value = "Medium Editor"
            detector.capture_target_window()
            mock_get.return_value = ""
            assert detector.is_target_focused() is True

    def test_exact_match_required(self, detector):
        with patch.object(detector, "get_active_window_title") as mock_get:
            mock_get.return_value = "Medium - New Story"
            detector.capture_target_window()
            mock_get.return_value = "Medium - New Story (Draft)"
            assert detector.is_target_focused() is False

    def test_case_sensitive_comparison(self, detector):
        with patch.object(detector, "get_active_window_title") as mock_get:
            mock_get.return_value = "Medium Editor"
            detector.capture_target_window()
            mock_get.return_value = "medium editor"
            assert detector.is_target_focused() is False

    def test_recapture_updates_target(self, detector):
        with patch.object(detector, "get_active_window_title") as mock_get:
            mock_get.return_value = "Window A"
            detector.capture_target_window()
            mock_get.return_value = "Window B"
            detector.capture_target_window()
            assert detector._target_title == "Window B"
            assert detector.is_target_focused() is True

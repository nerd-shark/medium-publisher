"""Unit tests for the Navigation layer.

Tests ScreenRecognition, LoginDetector, and NavigationStateMachine.

Requirements: 3.1–3.19
"""

import time
from pathlib import Path
from unittest.mock import patch, MagicMock, call, PropertyMock

import pytest

from medium_publisher.core.models import NavigationState
from medium_publisher.navigation.screen_recognition import ScreenRecognition
from medium_publisher.navigation.login_detector import LoginDetector, STATE_IMAGES
from medium_publisher.navigation.navigation_state_machine import (
    NavigationStateMachine,
    MEDIUM_URL,
)
from medium_publisher.utils.exceptions import NavigationError


# ---------------------------------------------------------------------------
# ScreenRecognition tests
# ---------------------------------------------------------------------------

class TestScreenRecognition:
    """Tests for ScreenRecognition class."""

    @patch("medium_publisher.navigation.screen_recognition.pyautogui")
    def test_find_on_screen_returns_centre(self, mock_pyautogui):
        mock_box = MagicMock()
        mock_pyautogui.locateOnScreen.return_value = mock_box
        mock_centre = MagicMock()
        mock_centre.x = 100
        mock_centre.y = 200
        mock_pyautogui.center.return_value = mock_centre

        sr = ScreenRecognition(assets_dir=Path("/fake/assets"), confidence=0.8)
        result = sr.find_on_screen("test.png")

        assert result == (100, 200)
        mock_pyautogui.locateOnScreen.assert_called_once()

    @patch("medium_publisher.navigation.screen_recognition.pyautogui")
    def test_find_on_screen_returns_none_when_not_found(self, mock_pyautogui):
        mock_pyautogui.locateOnScreen.return_value = None

        sr = ScreenRecognition(assets_dir=Path("/fake/assets"))
        result = sr.find_on_screen("missing.png")

        assert result is None

    @patch("medium_publisher.navigation.screen_recognition.pyautogui")
    def test_find_on_screen_returns_none_on_exception(self, mock_pyautogui):
        mock_pyautogui.locateOnScreen.side_effect = Exception("screen error")

        sr = ScreenRecognition(assets_dir=Path("/fake/assets"))
        result = sr.find_on_screen("error.png")

        assert result is None

    @patch("medium_publisher.navigation.screen_recognition.pyautogui")
    def test_is_visible_true(self, mock_pyautogui):
        mock_box = MagicMock()
        mock_pyautogui.locateOnScreen.return_value = mock_box
        mock_pyautogui.center.return_value = MagicMock(x=50, y=50)

        sr = ScreenRecognition(assets_dir=Path("/fake/assets"))
        assert sr.is_visible("test.png") is True

    @patch("medium_publisher.navigation.screen_recognition.pyautogui")
    def test_is_visible_false(self, mock_pyautogui):
        mock_pyautogui.locateOnScreen.return_value = None

        sr = ScreenRecognition(assets_dir=Path("/fake/assets"))
        assert sr.is_visible("test.png") is False

    @patch("medium_publisher.navigation.screen_recognition.time")
    @patch("medium_publisher.navigation.screen_recognition.pyautogui")
    def test_wait_for_returns_coords_when_found(self, mock_pyautogui, mock_time):
        mock_time.monotonic.side_effect = [0, 1, 2]  # start, first poll, second poll
        mock_time.sleep = MagicMock()
        mock_box = MagicMock()
        mock_pyautogui.locateOnScreen.side_effect = [None, mock_box]
        mock_pyautogui.center.return_value = MagicMock(x=300, y=400)

        sr = ScreenRecognition(assets_dir=Path("/fake/assets"))
        result = sr.wait_for("test.png", timeout_seconds=10, poll_interval=1.0)

        assert result == (300, 400)

    @patch("medium_publisher.navigation.screen_recognition.time")
    @patch("medium_publisher.navigation.screen_recognition.pyautogui")
    def test_wait_for_returns_none_on_timeout(self, mock_pyautogui, mock_time):
        mock_time.monotonic.side_effect = [0, 5, 15, 35]
        mock_time.sleep = MagicMock()
        mock_pyautogui.locateOnScreen.return_value = None

        sr = ScreenRecognition(assets_dir=Path("/fake/assets"))
        result = sr.wait_for("test.png", timeout_seconds=30, poll_interval=2.0)

        assert result is None

    def test_set_confidence(self):
        sr = ScreenRecognition(assets_dir=Path("/fake/assets"), confidence=0.5)
        sr.set_confidence(0.95)
        assert sr._confidence == 0.95

    @patch("medium_publisher.navigation.screen_recognition.pyautogui")
    def test_capture_reference(self, mock_pyautogui, tmp_path):
        mock_screenshot = MagicMock()
        mock_pyautogui.screenshot.return_value = mock_screenshot

        sr = ScreenRecognition(assets_dir=tmp_path)
        sr.capture_reference("new_ref.png", (0, 0, 100, 100))

        mock_pyautogui.screenshot.assert_called_once_with(region=(0, 0, 100, 100))
        mock_screenshot.save.assert_called_once()

    def test_default_assets_dir(self):
        sr = ScreenRecognition()
        expected = Path(__file__).parent.parent.parent / "navigation" / ".." / "assets" / "medium"
        # Just verify it ends with assets/medium
        assert sr._assets_dir.name == "medium"
        assert sr._assets_dir.parent.name == "assets"


# ---------------------------------------------------------------------------
# LoginDetector tests
# ---------------------------------------------------------------------------

class TestLoginDetector:
    """Tests for LoginDetector class."""

    def test_detect_logged_out_home(self):
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name == "home-page-logged-out.png"

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.LOGGED_OUT_HOME

    def test_detect_sign_in_screen(self):
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name == "sign-in-screen.png"

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.SIGN_IN_SCREEN

    def test_detect_google_sign_in(self):
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name == "google-sign-in.png"

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.GOOGLE_SIGN_IN

    def test_detect_logged_in_home(self):
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name == "medium-logged-in.png"

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.LOGGED_IN_HOME

    def test_detect_drafts_page(self):
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name == "medium-drafts-page.png"

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.DRAFTS_PAGE

    def test_detect_new_story_editor(self):
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name == "medium-new-story-page.png"

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.NEW_STORY_EDITOR

    def test_detect_error_when_no_match(self):
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.return_value = False

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.ERROR

    def test_first_match_wins(self):
        """When multiple images match, the first in iteration order wins."""
        mock_screen = MagicMock(spec=ScreenRecognition)
        # Both logged-out home and sign-in visible
        mock_screen.is_visible.side_effect = lambda name: name in (
            "home-page-logged-out.png", "sign-in-screen.png"
        )

        detector = LoginDetector(mock_screen)
        result = detector.detect_state()
        # home-page-logged-out.png comes first in STATE_IMAGES
        assert result == NavigationState.LOGGED_OUT_HOME

    def test_detect_google_sign_in_alt(self):
        """Alt Google sign-in image also resolves to GOOGLE_SIGN_IN."""
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name == "google-sign-in-alt.png"

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.GOOGLE_SIGN_IN


# ---------------------------------------------------------------------------
# NavigationStateMachine tests
# ---------------------------------------------------------------------------

class TestNavigationStateMachine:
    """Tests for NavigationStateMachine class."""

    @pytest.fixture
    def mock_deps(self):
        """Create mocked dependencies for NavigationStateMachine."""
        screen = MagicMock(spec=ScreenRecognition)
        controller = MagicMock()
        config = MagicMock()
        config.get.side_effect = lambda key, default=None: {
            "navigation.poll_interval_seconds": 0.01,
            "navigation.login_timeout_seconds": 0.5,
            "navigation.page_load_timeout_seconds": 0.1,
            "navigation.google_account_email": "test@gmail.com",
        }.get(key, default)
        return screen, controller, config

    def test_detect_current_state_delegates_to_detector(self, mock_deps):
        screen, controller, config = mock_deps
        screen.is_visible.side_effect = lambda name: name == "medium-logged-in.png"

        nsm = NavigationStateMachine(screen, controller, config)
        state = nsm.detect_current_state()

        assert state == NavigationState.LOGGED_IN_HOME

    @patch("medium_publisher.navigation.navigation_state_machine.webbrowser")
    @patch("medium_publisher.navigation.navigation_state_machine.time")
    def test_navigate_to_editor_success(self, mock_time, mock_webbrowser, mock_deps):
        screen, controller, config = mock_deps

        # Track call count to simulate state progression
        detect_call_count = [0]

        def is_visible_side_effect(image_name):
            """First round: logged-in home. Second round: new story editor."""
            count = detect_call_count[0]
            detect_call_count[0] += 1
            if count < 7:
                # First detect_state (7 images): match logged-in home
                return image_name == "medium-logged-in.png"
            else:
                # Second detect_state: match new story editor
                return image_name == "medium-new-story-page.png"

        screen.is_visible.side_effect = is_visible_side_effect
        screen.find_on_screen.return_value = (500, 300)
        mock_time.monotonic.side_effect = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06]
        mock_time.sleep = MagicMock()

        nsm = NavigationStateMachine(screen, controller, config)
        result = nsm.navigate_to_editor()

        assert result is True
        mock_webbrowser.open.assert_called()

    @patch("medium_publisher.navigation.navigation_state_machine.webbrowser")
    @patch("medium_publisher.navigation.navigation_state_machine.time")
    def test_navigate_to_editor_with_draft_url(self, mock_time, mock_webbrowser, mock_deps):
        screen, controller, config = mock_deps
        # Detect new story editor immediately (7 images checked)
        screen.is_visible.side_effect = [
            False, False, False, False, False, False, True,
        ]
        mock_time.monotonic.side_effect = [0, 0.01, 0.02]
        mock_time.sleep = MagicMock()

        nsm = NavigationStateMachine(screen, controller, config)
        draft_url = "https://medium.com/p/abc123/edit"
        result = nsm.navigate_to_editor(draft_url=draft_url)

        assert result is True
        mock_webbrowser.open.assert_any_call(draft_url)

    @patch("medium_publisher.navigation.navigation_state_machine.webbrowser")
    @patch("medium_publisher.navigation.navigation_state_machine.time")
    def test_navigate_to_editor_timeout(self, mock_time, mock_webbrowser, mock_deps):
        screen, controller, config = mock_deps
        # Never match any image
        screen.is_visible.return_value = False
        # Simulate time passing beyond timeout
        call_count = [0]
        def advancing_time():
            call_count[0] += 1
            return call_count[0] * 0.2
        mock_time.monotonic.side_effect = advancing_time
        mock_time.sleep = MagicMock()

        nsm = NavigationStateMachine(screen, controller, config)

        with pytest.raises(NavigationError, match="Login timeout exceeded"):
            nsm.navigate_to_editor()


class TestStateHandlers:
    """Tests for individual state transition handlers."""

    @pytest.fixture
    def nsm(self):
        screen = MagicMock(spec=ScreenRecognition)
        controller = MagicMock()
        config = MagicMock()
        config.get.side_effect = lambda key, default=None: {
            "navigation.poll_interval_seconds": 0.01,
            "navigation.login_timeout_seconds": 0.5,
            "navigation.page_load_timeout_seconds": 0.1,
            "navigation.google_account_email": "test@gmail.com",
        }.get(key, default)
        return NavigationStateMachine(screen, controller, config)

    def test_handle_logged_out_home_clicks(self, nsm):
        nsm._screen.find_on_screen.return_value = (100, 200)
        nsm._handle_logged_out_home()
        nsm._input.click_at.assert_called_once_with(100, 200)

    def test_handle_sign_in_screen_clicks(self, nsm):
        nsm._screen.find_on_screen.return_value = (150, 250)
        nsm._handle_sign_in_screen()
        nsm._input.click_at.assert_called_once_with(150, 250)

    def test_handle_google_sign_in_clicks_and_sets_2fa(self, nsm):
        nsm._screen.find_on_screen.return_value = (200, 300)
        nsm._handle_google_sign_in()
        nsm._input.click_at.assert_called_once_with(200, 300)
        assert nsm._current_state == NavigationState.WAITING_2FA

    def test_handle_google_sign_in_falls_back_to_alt(self, nsm):
        """When primary google-sign-in.png not found, tries alt variant."""
        nsm._screen.find_on_screen.side_effect = (
            lambda name: (300, 400) if name == "google-sign-in-alt.png" else None
        )
        nsm._handle_google_sign_in()
        nsm._input.click_at.assert_called_once_with(300, 400)
        assert nsm._current_state == NavigationState.WAITING_2FA

    @patch("medium_publisher.navigation.navigation_state_machine.time")
    def test_handle_waiting_2fa_success(self, mock_time, nsm):
        mock_time.monotonic.side_effect = [0, 0.01, 0.02]
        mock_time.sleep = MagicMock()
        # Simulate 2FA completing — detector finds logged-in state
        nsm._detector = MagicMock()
        nsm._detector.detect_state.side_effect = [
            NavigationState.ERROR,
            NavigationState.LOGGED_IN_HOME,
        ]

        nsm._handle_waiting_2fa()
        assert nsm._current_state == NavigationState.LOGGED_IN_HOME

    @patch("medium_publisher.navigation.navigation_state_machine.time")
    def test_handle_waiting_2fa_timeout(self, mock_time, nsm):
        call_count = [0]
        def advancing_time():
            call_count[0] += 1
            return call_count[0] * 0.2
        mock_time.monotonic.side_effect = advancing_time
        mock_time.sleep = MagicMock()
        nsm._detector = MagicMock()
        nsm._detector.detect_state.return_value = NavigationState.ERROR

        with pytest.raises(NavigationError, match="2FA timeout exceeded"):
            nsm._handle_waiting_2fa()

    @patch("medium_publisher.navigation.navigation_state_machine.webbrowser")
    def test_handle_logged_in_home_with_draft_url(self, mock_webbrowser, nsm):
        nsm._handle_logged_in_home(draft_url="https://medium.com/p/abc/edit")
        mock_webbrowser.open.assert_called_once_with("https://medium.com/p/abc/edit")

    def test_handle_logged_in_home_without_draft_url(self, nsm):
        nsm._screen.find_on_screen.return_value = (400, 500)
        nsm._handle_logged_in_home(draft_url=None)
        nsm._input.click_at.assert_called_once_with(400, 500)

    @patch("medium_publisher.navigation.navigation_state_machine.webbrowser")
    def test_handle_drafts_page_with_draft_url(self, mock_webbrowser, nsm):
        nsm._handle_drafts_page(draft_url="https://medium.com/p/xyz/edit")
        mock_webbrowser.open.assert_called_once_with("https://medium.com/p/xyz/edit")

    @patch("medium_publisher.navigation.navigation_state_machine.webbrowser")
    def test_handle_drafts_page_without_draft_url(self, mock_webbrowser, nsm):
        nsm._handle_drafts_page(draft_url=None)
        mock_webbrowser.open.assert_called_once_with(f"{MEDIUM_URL}/new-story")


class TestErrorStateHandling:
    """Tests for error state scenarios."""

    @pytest.fixture
    def mock_deps(self):
        screen = MagicMock(spec=ScreenRecognition)
        controller = MagicMock()
        config = MagicMock()
        config.get.side_effect = lambda key, default=None: {
            "navigation.poll_interval_seconds": 0.01,
            "navigation.login_timeout_seconds": 0.1,
            "navigation.page_load_timeout_seconds": 0.05,
            "navigation.google_account_email": "test@gmail.com",
        }.get(key, default)
        return screen, controller, config

    def test_error_state_when_no_image_matches(self, mock_deps):
        screen, controller, config = mock_deps
        screen.is_visible.return_value = False

        nsm = NavigationStateMachine(screen, controller, config)
        state = nsm.detect_current_state()

        assert state == NavigationState.ERROR

    def test_handle_logged_out_home_no_coords(self, mock_deps):
        """When find_on_screen returns None, click_at is not called."""
        screen, controller, config = mock_deps
        screen.find_on_screen.return_value = None

        nsm = NavigationStateMachine(screen, controller, config)
        nsm._handle_logged_out_home()

        controller.click_at.assert_not_called()

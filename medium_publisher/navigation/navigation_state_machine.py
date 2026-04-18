"""Navigation state machine for Medium Keyboard Publisher.

Drives the full navigation flow from opening Medium.com through login
detection to reaching the new-story editor, using screen recognition
and OS-level input control.

Requirements: 3.1–3.19
"""

import time
import webbrowser
from typing import Optional

from medium_publisher.automation.os_input_controller import OS_Input_Controller
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.core.models import NavigationState
from medium_publisher.navigation.login_detector import LoginDetector
from medium_publisher.navigation.screen_recognition import ScreenRecognition
from medium_publisher.utils.exceptions import NavigationError
from medium_publisher.utils.logger import get_logger

logger = get_logger("navigation.state_machine")

MEDIUM_URL = "https://medium.com"


class NavigationStateMachine:
    """Drives navigation through Medium's login and editor flow.

    Uses a finite state machine pattern: detect current screen state via
    LoginDetector, then execute the appropriate action to transition to
    the next state until the editor is reached.

    Args:
        screen_recognition: For locating UI elements on screen.
        input_controller: For clicking buttons and typing.
        config: For reading navigation settings.
    """

    # Reference image → state mapping (used by LoginDetector)
    STATE_IMAGES = {
        "home-page-logged-out.png": NavigationState.LOGGED_OUT_HOME,
        "sign-in-screen.png": NavigationState.SIGN_IN_SCREEN,
        "google-sign-in.png": NavigationState.GOOGLE_SIGN_IN,
        "google-sign-in-alt.png": NavigationState.GOOGLE_SIGN_IN,
        "medium-logged-in.png": NavigationState.LOGGED_IN_HOME,
        "medium-drafts-page.png": NavigationState.DRAFTS_PAGE,
        "medium-new-story-page.png": NavigationState.NEW_STORY_EDITOR,
    }

    def __init__(
        self,
        screen_recognition: ScreenRecognition,
        input_controller: OS_Input_Controller,
        config: ConfigManager,
    ) -> None:
        self._screen = screen_recognition
        self._input = input_controller
        self._config = config
        self._detector = LoginDetector(screen_recognition)
        self._current_state = NavigationState.START

        self._poll_interval = config.get("navigation.poll_interval_seconds", 2)
        self._login_timeout = config.get("navigation.login_timeout_seconds", 300)
        self._page_load_timeout = config.get("navigation.page_load_timeout_seconds", 30)
        self._google_email = config.get(
            "navigation.google_account_email", "diverdan326@gmail.com"
        )

        logger.info("NavigationStateMachine initialized")

    def detect_current_state(self) -> NavigationState:
        """Check all 6 reference images to determine the current page state.

        Returns:
            The detected NavigationState.
        """
        state = self._detector.detect_state()
        self._current_state = state
        return state

    def navigate_to_editor(self, draft_url: Optional[str] = None) -> bool:
        """Execute the full navigation flow from START to READY.

        Opens Medium.com, detects the current state, and transitions
        through the login flow until the editor is reached.

        Args:
            draft_url: Optional Medium draft URL to navigate to instead
                       of creating a new story.

        Returns:
            True if the editor is ready, False on timeout/error.

        Raises:
            NavigationError: On unrecoverable navigation failures.
        """
        logger.info("Starting navigation flow (draft_url=%s)", draft_url)
        self._current_state = NavigationState.START

        # Open Medium in default browser
        self._open_medium(draft_url)

        # Wait for initial page load then detect state
        logger.info("Waiting for page to load...")
        time.sleep(3)  # Brief initial wait for browser to open

        deadline = time.monotonic() + self._login_timeout
        while time.monotonic() < deadline:
            self._current_state = self.detect_current_state()
            logger.info("Current state: %s", self._current_state.value)

            if self._current_state == NavigationState.READY:
                logger.info("Navigation complete — editor is ready")
                return True

            if self._current_state == NavigationState.NEW_STORY_EDITOR:
                self._current_state = NavigationState.READY
                logger.info("Editor detected — navigation complete")
                return True

            if self._current_state == NavigationState.ERROR:
                logger.warning("No reference image matched, retrying...")
                time.sleep(self._poll_interval)
                continue

            # Execute state handler
            try:
                self._transition(self._current_state, draft_url)
            except NavigationError:
                raise
            except Exception as exc:
                logger.error("State transition error: %s", exc)
                raise NavigationError(
                    f"Navigation failed in state {self._current_state.value}",
                    details={"error": str(exc)},
                ) from exc

            time.sleep(self._poll_interval)

        logger.error("Navigation timed out after %d seconds", self._login_timeout)
        raise NavigationError(
            "Login timeout exceeded",
            details={"timeout_seconds": self._login_timeout},
        )

    def _open_medium(self, draft_url: Optional[str] = None) -> None:
        """Open Medium.com (or draft URL) in the default browser."""
        url = draft_url if draft_url else MEDIUM_URL
        logger.info("Opening %s in default browser", url)
        webbrowser.open(url)

    def _transition(
        self, current: NavigationState, draft_url: Optional[str] = None
    ) -> None:
        """Execute the action for the current state.

        Args:
            current: The current NavigationState.
            draft_url: Optional draft URL for logged-in handlers.
        """
        handlers = {
            NavigationState.LOGGED_OUT_HOME: self._handle_logged_out_home,
            NavigationState.SIGN_IN_SCREEN: self._handle_sign_in_screen,
            NavigationState.GOOGLE_SIGN_IN: self._handle_google_sign_in,
            NavigationState.WAITING_2FA: self._handle_waiting_2fa,
            NavigationState.LOGGED_IN_HOME: lambda: self._handle_logged_in_home(draft_url),
            NavigationState.DRAFTS_PAGE: lambda: self._handle_drafts_page(draft_url),
        }
        handler = handlers.get(current)
        if handler:
            old_state = current.value
            handler()
            logger.info("Transitioned from %s", old_state)

    def _handle_logged_out_home(self) -> None:
        """Click the 'Sign in' button on the logged-out homepage."""
        logger.info("Handling LOGGED_OUT_HOME — clicking 'Sign in'")
        coords = self._screen.find_on_screen("home-page-logged-out.png")
        if coords:
            self._input.click_at(coords[0], coords[1])

    def _handle_sign_in_screen(self) -> None:
        """Click the 'Sign in with Google' button."""
        logger.info("Handling SIGN_IN_SCREEN — clicking 'Sign in with Google'")
        coords = self._screen.find_on_screen("sign-in-screen.png")
        if coords:
            self._input.click_at(coords[0], coords[1])

    def _handle_google_sign_in(self) -> None:
        """Click the configured Google account on the OAuth chooser.

        Tries both google-sign-in.png and google-sign-in-alt.png since
        Google's account chooser can appear in different layouts.
        """
        logger.info(
            "Handling GOOGLE_SIGN_IN — selecting account %s", self._google_email
        )
        # Try primary image first, then alt variant
        coords = self._screen.find_on_screen("google-sign-in.png")
        if not coords:
            coords = self._screen.find_on_screen("google-sign-in-alt.png")
        if coords:
            self._input.click_at(coords[0], coords[1])
        # After clicking, we may need 2FA — transition to WAITING_2FA
        self._current_state = NavigationState.WAITING_2FA

    def _handle_waiting_2fa(self) -> None:
        """Wait for the user to complete 2FA authentication.

        Polls every poll_interval seconds for up to login_timeout seconds.
        """
        logger.info(
            "Handling WAITING_2FA — waiting for user to complete 2FA (timeout=%ds)",
            self._login_timeout,
        )
        deadline = time.monotonic() + self._login_timeout
        while time.monotonic() < deadline:
            state = self._detector.detect_state()
            if state in (
                NavigationState.LOGGED_IN_HOME,
                NavigationState.NEW_STORY_EDITOR,
                NavigationState.DRAFTS_PAGE,
            ):
                logger.info("2FA complete — detected %s", state.value)
                self._current_state = state
                return
            time.sleep(self._poll_interval)

        raise NavigationError(
            "2FA timeout exceeded",
            details={"timeout_seconds": self._login_timeout},
        )

    def _handle_logged_in_home(self, draft_url: Optional[str] = None) -> None:
        """Click 'Write' button or navigate to draft URL."""
        if draft_url:
            logger.info("Handling LOGGED_IN_HOME — navigating to draft URL")
            webbrowser.open(draft_url)
        else:
            logger.info("Handling LOGGED_IN_HOME — clicking 'Write'")
            coords = self._screen.find_on_screen("medium-logged-in.png")
            if coords:
                self._input.click_at(coords[0], coords[1])

    def _handle_drafts_page(self, draft_url: Optional[str] = None) -> None:
        """Navigate to new story or specific draft from the drafts page."""
        if draft_url:
            logger.info("Handling DRAFTS_PAGE — navigating to draft URL")
            webbrowser.open(draft_url)
        else:
            logger.info("Handling DRAFTS_PAGE — navigating to new story")
            webbrowser.open(f"{MEDIUM_URL}/new-story")

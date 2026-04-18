"""Login detector for Medium Keyboard Publisher.

Uses ScreenRecognition to check reference images and determine
the current page state, mapping matches to NavigationState enum values.

Some states have multiple reference image variants (e.g. Google sign-in
can appear in two different layouts). All variants for a state are checked.

Requirements: 3.3, 3.4
"""

from typing import Dict, List, Tuple

from medium_publisher.core.models import NavigationState
from medium_publisher.navigation.screen_recognition import ScreenRecognition
from medium_publisher.utils.logger import get_logger

logger = get_logger("navigation.login_detector")

# Reference image → NavigationState mapping.
# A state can have multiple image variants — any match triggers the state.
STATE_IMAGES: Dict[str, NavigationState] = {
    "home-page-logged-out.png": NavigationState.LOGGED_OUT_HOME,
    "sign-in-screen.png": NavigationState.SIGN_IN_SCREEN,
    "google-sign-in.png": NavigationState.GOOGLE_SIGN_IN,
    "google-sign-in-alt.png": NavigationState.GOOGLE_SIGN_IN,
    "medium-logged-in.png": NavigationState.LOGGED_IN_HOME,
    "medium-drafts-page.png": NavigationState.DRAFTS_PAGE,
    "medium-new-story-page.png": NavigationState.NEW_STORY_EDITOR,
}

# Images grouped by state for quick lookup (preserves check order).
_STATE_IMAGE_GROUPS: List[Tuple[NavigationState, List[str]]] = []
_seen_states: List[NavigationState] = []
for _img, _state in STATE_IMAGES.items():
    if _state not in _seen_states:
        _seen_states.append(_state)
        _STATE_IMAGE_GROUPS.append((_state, []))
    for _s, _imgs in _STATE_IMAGE_GROUPS:
        if _s == _state:
            _imgs.append(_img)
            break


class LoginDetector:
    """Detects the current Medium page state using screen recognition.

    Checks all reference images against the current screen and returns
    the NavigationState corresponding to the first match. States with
    multiple image variants (e.g. Google sign-in) match if *any* variant
    is visible.

    Args:
        screen_recognition: Injected ScreenRecognition instance.
    """

    def __init__(self, screen_recognition: ScreenRecognition) -> None:
        self._screen = screen_recognition
        logger.info("LoginDetector initialized")

    def detect_state(self) -> NavigationState:
        """Check all reference images and return the current NavigationState.

        Iterates through states in order. For each state, checks all image
        variants. Returns the NavigationState for the first visible image,
        or ERROR if none match.

        Returns:
            The detected NavigationState.
        """
        for state, image_names in _STATE_IMAGE_GROUPS:
            for image_name in image_names:
                if self._screen.is_visible(image_name):
                    logger.info(
                        "Detected state: %s (matched '%s')",
                        state.value,
                        image_name,
                    )
                    return state

        logger.warning("No reference image matched — returning ERROR state")
        return NavigationState.ERROR

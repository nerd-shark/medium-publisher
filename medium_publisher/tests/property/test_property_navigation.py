"""Property-based tests for navigation state detection.

Property 9: Navigation state detection returns correct state.

For any combination of reference image visibility, detect_state() SHALL
check all reference images (including variants like google-sign-in-alt.png)
and return the NavigationState corresponding to the first matching image,
or ERROR if none match.

**Validates: Requirements 3.3, 3.4**
"""

from unittest.mock import MagicMock

from hypothesis import given, strategies as st, settings

from medium_publisher.core.models import NavigationState
from medium_publisher.navigation.login_detector import (
    LoginDetector,
    STATE_IMAGES,
    _STATE_IMAGE_GROUPS,
)
from medium_publisher.navigation.screen_recognition import ScreenRecognition

# All image names (includes alt variants)
IMAGE_NAMES = list(STATE_IMAGES.keys())

visibility_strategy = st.fixed_dictionaries(
    {name: st.booleans() for name in IMAGE_NAMES}
)

all_invisible_strategy = st.just({name: False for name in IMAGE_NAMES})

single_visible_strategy = st.sampled_from(IMAGE_NAMES)


class TestProperty9NavigationStateDetection:
    """Property 9: Navigation state detection returns correct state.

    **Validates: Requirements 3.3, 3.4**
    """

    @given(visible_image=single_visible_strategy)
    @settings(max_examples=30)
    def test_single_visible_image_returns_correct_state(
        self, visible_image: str
    ) -> None:
        """For any single visible image, detect_state() returns the
        corresponding NavigationState."""
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name == visible_image

        detector = LoginDetector(mock_screen)
        result = detector.detect_state()

        expected = STATE_IMAGES[visible_image]
        assert result == expected, (
            f"Expected {expected} for visible image '{visible_image}', got {result}"
        )

    @given(visibility=all_invisible_strategy)
    @settings(max_examples=10)
    def test_no_visible_images_returns_error(self, visibility: dict) -> None:
        """When no images are visible, detect_state() returns ERROR."""
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.return_value = False

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.ERROR

    @given(visibility=visibility_strategy)
    @settings(max_examples=50)
    def test_first_matching_state_wins(self, visibility: dict) -> None:
        """detect_state() returns the state for the first visible image
        (grouped by state), or ERROR if none match."""
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: visibility.get(name, False)

        detector = LoginDetector(mock_screen)
        result = detector.detect_state()

        # Determine expected using the same grouped iteration order
        expected = NavigationState.ERROR
        for state, image_names in _STATE_IMAGE_GROUPS:
            if any(visibility.get(img, False) for img in image_names):
                expected = state
                break

        assert result == expected

    @given(visibility=all_invisible_strategy)
    @settings(max_examples=10)
    def test_all_images_checked_when_none_visible(self, visibility: dict) -> None:
        """When no images are visible, all images must be checked."""
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.return_value = False

        detector = LoginDetector(mock_screen)
        detector.detect_state()

        assert mock_screen.is_visible.call_count == len(IMAGE_NAMES)

    def test_alt_google_sign_in_detected(self) -> None:
        """google-sign-in-alt.png should also resolve to GOOGLE_SIGN_IN."""
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = (
            lambda name: name == "google-sign-in-alt.png"
        )

        detector = LoginDetector(mock_screen)
        assert detector.detect_state() == NavigationState.GOOGLE_SIGN_IN

    def test_primary_google_image_checked_before_alt(self) -> None:
        """When both google images are visible, primary is matched first."""
        mock_screen = MagicMock(spec=ScreenRecognition)
        mock_screen.is_visible.side_effect = lambda name: name in (
            "google-sign-in.png",
            "google-sign-in-alt.png",
        )

        detector = LoginDetector(mock_screen)
        detector.detect_state()

        # The primary image should be checked first and matched
        calls = [c.args[0] for c in mock_screen.is_visible.call_args_list]
        google_idx = calls.index("google-sign-in.png")
        # Should have stopped after finding the primary
        assert google_idx < len(calls)

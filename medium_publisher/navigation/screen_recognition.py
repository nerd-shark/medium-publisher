"""Screen recognition for Medium Keyboard Publisher.

Wraps pyautogui's locateOnScreen() to find UI elements by matching
reference screenshot images with configurable confidence threshold.

Requirements: 3.2, 3.3, 3.14, 3.17, 3.18
"""

import time
from pathlib import Path
from typing import Optional, Tuple

import pyautogui

from medium_publisher.utils.logger import get_logger

logger = get_logger("navigation.screen_recognition")


class ScreenRecognition:
    """Finds UI elements on screen by matching reference images.

    Uses pyautogui's locateOnScreen() with a configurable confidence
    threshold to locate pre-captured reference screenshots.

    Args:
        assets_dir: Path to directory containing reference images.
        confidence: Matching confidence threshold (0.0–1.0).
    """

    def __init__(
        self,
        assets_dir: Optional[Path] = None,
        confidence: float = 0.8,
    ) -> None:
        if assets_dir is None:
            package_root = Path(__file__).parent.parent
            assets_dir = package_root / "assets" / "medium"
        self._assets_dir = Path(assets_dir)
        self._confidence = confidence
        logger.info(
            "ScreenRecognition initialized (assets=%s, confidence=%.2f)",
            self._assets_dir,
            self._confidence,
        )

    def find_on_screen(self, image_name: str) -> Optional[Tuple[int, int]]:
        """Locate image on screen and return its centre coordinates.

        Args:
            image_name: Filename of the reference image (e.g. 'sign-in-screen.png').

        Returns:
            (x, y) centre coordinates if found, None otherwise.
        """
        image_path = self._assets_dir / image_name
        try:
            location = pyautogui.locateOnScreen(
                str(image_path), confidence=self._confidence
            )
            if location is not None:
                centre = pyautogui.center(location)
                logger.debug("Found '%s' at (%d, %d)", image_name, centre.x, centre.y)
                return (centre.x, centre.y)
            logger.debug("Image '%s' not found on screen", image_name)
            return None
        except Exception as exc:
            logger.error("Error locating '%s': %s", image_name, exc)
            return None

    def is_visible(self, image_name: str) -> bool:
        """Check if a reference image is currently visible on screen.

        Args:
            image_name: Filename of the reference image.

        Returns:
            True if the image is visible, False otherwise.
        """
        return self.find_on_screen(image_name) is not None

    def wait_for(
        self,
        image_name: str,
        timeout_seconds: float = 30,
        poll_interval: float = 2.0,
    ) -> Optional[Tuple[int, int]]:
        """Poll for an image to appear on screen.

        Args:
            image_name: Filename of the reference image.
            timeout_seconds: Maximum seconds to wait before giving up.
            poll_interval: Seconds between each poll attempt.

        Returns:
            (x, y) centre coordinates if found within timeout, None otherwise.
        """
        logger.info(
            "Waiting for '%s' (timeout=%ds, poll=%.1fs)",
            image_name,
            timeout_seconds,
            poll_interval,
        )
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            result = self.find_on_screen(image_name)
            if result is not None:
                logger.info("'%s' appeared on screen", image_name)
                return result
            time.sleep(poll_interval)
        logger.warning("Timed out waiting for '%s'", image_name)
        return None

    def capture_reference(
        self, image_name: str, region: Tuple[int, int, int, int]
    ) -> None:
        """Capture a new reference image from a screen region.

        Args:
            image_name: Filename to save the captured image as.
            region: (left, top, width, height) screen region to capture.
        """
        image_path = self._assets_dir / image_name
        self._assets_dir.mkdir(parents=True, exist_ok=True)
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(str(image_path))
        logger.info("Captured reference image '%s' from region %s", image_name, region)

    def set_confidence(self, confidence: float) -> None:
        """Update the matching confidence threshold.

        Args:
            confidence: New confidence value (0.0–1.0).
        """
        self._confidence = confidence
        logger.info("Screen recognition confidence set to %.2f", confidence)

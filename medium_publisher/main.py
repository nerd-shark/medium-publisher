"""
Medium Keyboard Publisher — Main Entry Point

Initializes all components with dependency injection and launches the
PyQt6 application. Registers safety hooks for abnormal exit cleanup.

Requirements: 6.1, 6.2, NFR-2.1
"""

import atexit
import sys
from pathlib import Path

import pyautogui
from PyQt6.QtWidgets import QApplication, QMessageBox

from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.safety.emergency_stop import EmergencyStop
from medium_publisher.safety.focus_window_detector import FocusWindowDetector
from medium_publisher.automation.os_input_controller import OS_Input_Controller
from medium_publisher.navigation.screen_recognition import ScreenRecognition
from medium_publisher.navigation.navigation_state_machine import NavigationStateMachine
from medium_publisher.automation.deferred_typo_tracker import DeferredTypoTracker
from medium_publisher.automation.human_typing_simulator import HumanTypingSimulator
from medium_publisher.automation.content_typer import ContentTyper
from medium_publisher.core.change_parser import ChangeParser
from medium_publisher.core.markdown_processor import MarkdownProcessor
from medium_publisher.core.publishing_workflow import PublishingWorkflow
from medium_publisher.core.session_manager import SessionManager
from medium_publisher.core.version_diff_detector import VersionDiffDetector
from medium_publisher.automation.version_update_typer import VersionUpdateTyper
from medium_publisher.ui.main_window import MainWindow
from medium_publisher.utils.logger import get_logger

logger = get_logger("main")


def _release_keys_on_exit() -> None:
    """Release all modifier keys on abnormal exit (atexit hook)."""
    try:
        for key in ("ctrl", "shift", "alt", "win"):
            pyautogui.keyUp(key)
        logger.info("atexit: all modifier keys released")
    except Exception as exc:
        # Best-effort — don't raise during interpreter shutdown
        try:
            logger.error("atexit: failed to release keys: %s", exc)
        except Exception:
            pass


def exception_hook(exc_type, exc_value, exc_traceback):
    """Global exception handler — log unhandled exceptions."""
    logger.critical(
        "Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback)
    )
    error_msg = f"{exc_type.__name__}: {exc_value}"
    if QApplication.instance():
        QMessageBox.critical(
            None,
            "Critical Error",
            f"An unexpected error occurred:\n\n{error_msg}\n\n"
            "Please check the log file for details.",
        )
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


def main() -> int:
    """Initialize components via dependency injection and run the app."""
    sys.excepthook = exception_hook

    logger.info("=" * 60)
    logger.info("Medium Keyboard Publisher starting")
    logger.info("=" * 60)

    try:
        # --- pyautogui safety ---
        pyautogui.FAILSAFE = True

        # --- Configuration ---
        config = ConfigManager()
        config.load_config()
        logger.info("Configuration loaded")

        # --- Safety layer ---
        hotkey = config.get("safety.emergency_stop_hotkey", "ctrl+shift+escape")
        emergency_stop = EmergencyStop(hotkey=hotkey)
        focus_detector = FocusWindowDetector()

        # --- OS input ---
        input_controller = OS_Input_Controller(emergency_stop, focus_detector)

        # Register key-release atexit hook (uses pyautogui directly)
        atexit.register(_release_keys_on_exit)

        # --- Screen recognition & navigation ---
        assets_dir = Path(config.get(
            "assets.reference_images_dir",
            str(Path(__file__).parent / "assets" / "medium"),
        ))
        confidence = config.get("navigation.screen_confidence", 0.8)
        screen_recognition = ScreenRecognition(
            assets_dir=assets_dir, confidence=confidence
        )
        nav_state_machine = NavigationStateMachine(
            screen_recognition, input_controller, config
        )

        # --- Typing simulation ---
        typo_tracker = DeferredTypoTracker()
        typing_simulator = HumanTypingSimulator(
            typo_frequency=config.get("typing.typo_frequency", "low"),
            enabled=config.get("typing.human_typing_enabled", True),
        )
        content_typer = ContentTyper(
            input_controller, typing_simulator, typo_tracker, config
        )

        # --- Session ---
        session_manager = SessionManager()

        # --- Change detection & version update ---
        markdown_processor = MarkdownProcessor()
        change_parser = ChangeParser()
        version_diff_detector = VersionDiffDetector(markdown_processor)
        version_update_typer = VersionUpdateTyper(
            input_controller, content_typer, change_parser, config
        )

        # --- Publishing workflow ---
        publishing_workflow = PublishingWorkflow(
            config=config,
            emergency_stop=emergency_stop,
            nav_state_machine=nav_state_machine,
            content_typer=content_typer,
            typo_tracker=typo_tracker,
            session_manager=session_manager,
            version_update_typer=version_update_typer,
            version_diff_detector=version_diff_detector,
        )

        # --- Start emergency-stop monitoring ---
        emergency_stop.start_monitoring()
        logger.info("Emergency stop monitoring active (hotkey=%s)", hotkey)

        # --- Qt application ---
        app = QApplication(sys.argv)
        app.setApplicationName("Medium Keyboard Publisher")
        app.setOrganizationName("Medium Publisher")
        app.setApplicationVersion("0.2.0")

        window = MainWindow(config)
        window.set_emergency_stop(emergency_stop)
        window.show()
        logger.info("Main window displayed")

        # Store references on window for workflow access
        window._input_controller = input_controller
        window._content_typer = content_typer
        window._nav_state_machine = nav_state_machine
        window.set_session_manager(session_manager)
        window._typo_tracker = typo_tracker
        window._screen_recognition = screen_recognition
        window._focus_detector = focus_detector
        window._publishing_workflow = publishing_workflow

        logger.info("Starting application event loop")
        exit_code = app.exec()

        # --- Cleanup ---
        emergency_stop.stop_monitoring()
        input_controller.release_all_keys()
        logger.info("Application exited with code %d", exit_code)
        return exit_code

    except Exception:
        logger.exception("Failed to start application")
        QMessageBox.critical(
            None,
            "Startup Error",
            "Failed to start application. Check the log file for details.",
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())

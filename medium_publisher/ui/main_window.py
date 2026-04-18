"""Main window UI for Medium Keyboard Publisher.

Reworked for OS-level keyboard/mouse automation via pyautogui/pynput.
Removes all Playwright/Selenium-specific controls.
"""

import re
from pathlib import Path
from typing import List, Optional

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from medium_publisher.core.article_parser import ArticleParser
from medium_publisher.core.change_parser import ChangeInstruction, ChangeParser
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.core.markdown_processor import MarkdownProcessor
from medium_publisher.core.publishing_workflow import TypingWorker, VersionUpdateWorker
from medium_publisher.core.session_manager import SessionManager
from medium_publisher.core.version_diff_detector import VersionDiffDetector
from medium_publisher.ui.file_selector import FileSelector
from medium_publisher.ui.progress_widget import ProgressWidget
from medium_publisher.ui.settings_dialog import SettingsDialog
from medium_publisher.utils.logger import get_logger
from medium_publisher.utils.validators import validate_version_filename

logger = get_logger(__name__)

# Medium draft URL pattern
MEDIUM_DRAFT_URL_PATTERN = re.compile(
    r"^https?://([\w-]+\.)?medium\.com/.+"
)


class MainWindow(QMainWindow):
    """Main application window for Medium Keyboard Publisher.

    Provides controls for file selection, typing automation, emergency stop,
    pause/resume, countdown display, draft URL input, batch file selection,
    and always-on-top toggle.
    """

    # Signals for thread-safe UI updates from worker threads
    status_changed = pyqtSignal(str)
    countdown_tick = pyqtSignal(int)
    typing_finished = pyqtSignal(bool, str)  # success, message

    def __init__(self, config: ConfigManager) -> None:
        super().__init__()
        self.config = config
        self._article_parser = ArticleParser()
        self._markdown_processor = MarkdownProcessor()
        self._file_selector = FileSelector(parent=self, config=config)

        # State
        self._selected_file: Optional[Path] = None
        self._selected_files: list[Path] = []
        self._is_typing = False
        self._is_paused = False
        self._countdown_remaining = 0
        self._countdown_timer: Optional[QTimer] = None

        # Emergency stop reference (injected later via set_emergency_stop)
        self._emergency_stop = None

        # Session manager reference (injected later via set_session_manager)
        self._session_manager: Optional[SessionManager] = None

        self._init_ui()
        self._setup_shortcuts()
        self._connect_signals()
        self._update_button_states()

        # Apply always-on-top from config
        if self.config.get("ui.always_on_top", True):
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        logger.info("MainWindow initialized")

    # --- Public API -----------------------------------------------------------

    def set_emergency_stop(self, emergency_stop) -> None:
        """Inject the EmergencyStop instance after construction."""
        self._emergency_stop = emergency_stop

    def set_session_manager(self, session_manager: SessionManager) -> None:
        """Inject the SessionManager and restore any persisted session state.

        Called after construction by the entry point once all dependencies
        are wired.  Triggers ``_restore_session_state()`` so the UI is
        pre-populated with the last known draft URL and version.
        """
        self._session_manager = session_manager
        self._restore_session_state()

    @property
    def selected_file(self) -> Optional[Path]:
        return self._selected_file

    @property
    def selected_files(self) -> list[Path]:
        return list(self._selected_files)

    @property
    def is_typing(self) -> bool:
        return self._is_typing

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    def get_draft_url(self) -> Optional[str]:
        """Return the draft URL if valid, else None."""
        url = self.draft_url_input.text().strip()
        if not url:
            return None
        return url if self.validate_draft_url(url) else None

    @staticmethod
    def validate_draft_url(url: str) -> bool:
        """Return True if *url* looks like a Medium draft/story URL."""
        if not url:
            return False
        return bool(MEDIUM_DRAFT_URL_PATTERN.match(url))

    # --- UI construction ------------------------------------------------------

    def _init_ui(self) -> None:
        self.setWindowTitle("Medium Keyboard Publisher")
        self.setMinimumSize(700, 520)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        root.addWidget(self._build_file_group())
        root.addWidget(self._build_draft_url_group())
        root.addWidget(self._build_version_update_group())
        root.addWidget(self._build_article_info_group())
        root.addWidget(self._build_countdown_group())
        root.addWidget(self._build_actions_group())

        # Progress widget
        self.progress_widget = ProgressWidget(self)
        root.addWidget(self.progress_widget)

        # Always-on-top toggle
        self.always_on_top_cb = QCheckBox("Always on top")
        self.always_on_top_cb.setChecked(self.config.get("ui.always_on_top", True))
        self.always_on_top_cb.toggled.connect(self._on_always_on_top_toggled)
        root.addWidget(self.always_on_top_cb)

        self.statusBar().showMessage("Ready")

        # Set initial version state (v1 = standard workflow)
        self._on_version_changed("v1")

    def _build_file_group(self) -> QGroupBox:
        group = QGroupBox("Article File")
        layout = QVBoxLayout()
        row = QHBoxLayout()

        self.file_path_label = QLineEdit()
        self.file_path_label.setReadOnly(True)
        self.file_path_label.setPlaceholderText("No file selected")
        row.addWidget(self.file_path_label)

        self.select_file_btn = QPushButton("Select File")
        self.select_file_btn.clicked.connect(self._on_select_file)
        row.addWidget(self.select_file_btn)

        self.select_batch_btn = QPushButton("Select Batch")
        self.select_batch_btn.clicked.connect(self._on_select_batch)
        row.addWidget(self.select_batch_btn)

        layout.addLayout(row)
        group.setLayout(layout)
        return group

    def _build_draft_url_group(self) -> QGroupBox:
        group = QGroupBox("Medium Draft URL (Optional)")
        layout = QVBoxLayout()

        self.draft_url_input = QLineEdit()
        self.draft_url_input.setPlaceholderText("https://medium.com/p/<id>/edit")
        self.draft_url_input.textChanged.connect(self._on_draft_url_changed)
        layout.addWidget(self.draft_url_input)

        self.draft_url_status = QLabel("")
        self.draft_url_status.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.draft_url_status)

        group.setLayout(layout)
        return group

    def _build_version_update_group(self) -> QGroupBox:
        """Build the Version Update group box.

        Contains:
        - Version Selector: QComboBox with v1-v5 options
        - Previous Version Selector: file picker (QLineEdit + Browse button)
        - Change Instructions Area: QTextEdit for natural language instructions
        - Apply Changes button
        - Draft URL display (from session state)
        - Detected changes summary label
        """
        group = QGroupBox("Version Update")
        outer = QVBoxLayout()

        # --- Version selector row ---
        form = QFormLayout()
        self._version_selector = QComboBox()
        self._version_selector.addItems(["v1", "v2", "v3", "v4", "v5"])
        form.addRow("Version:", self._version_selector)
        outer.addLayout(form)

        # --- Previous version file picker ---
        self._prev_version_label = QLabel("Previous Version:")
        outer.addWidget(self._prev_version_label)

        prev_row = QHBoxLayout()
        self._prev_version_edit = QLineEdit()
        self._prev_version_edit.setReadOnly(True)
        self._prev_version_edit.setPlaceholderText("Select previous version file for diff...")
        prev_row.addWidget(self._prev_version_edit)

        self._browse_prev_btn = QPushButton("Browse...")
        self._browse_prev_btn.clicked.connect(self._on_browse_previous_version)
        prev_row.addWidget(self._browse_prev_btn)

        self._prev_version_row_widget = QWidget()
        self._prev_version_row_widget.setLayout(prev_row)
        outer.addWidget(self._prev_version_row_widget)

        # --- Change instructions area ---
        self._instructions_label = QLabel("Change Instructions:")
        outer.addWidget(self._instructions_label)

        self._change_instructions_area = QTextEdit()
        self._change_instructions_area.setPlaceholderText(
            "Describe changes in natural language, e.g.:\n"
            "Replace the introduction with a shorter version.\n"
            "Delete the 'Old Section' heading and its content.\n"
            "Add a new 'Conclusion' section at the end."
        )
        self._change_instructions_area.setMaximumHeight(120)
        outer.addWidget(self._change_instructions_area)

        # --- Draft URL display (from session state) ---
        self._draft_url_label = QLabel("Draft URL:")
        outer.addWidget(self._draft_url_label)

        self._draft_url_edit = QLineEdit()
        self._draft_url_edit.setPlaceholderText("https://medium.com/p/<id>/edit")
        outer.addWidget(self._draft_url_edit)

        # --- Detected changes summary ---
        self._changes_summary_label = QLabel("")
        self._changes_summary_label.setWordWrap(True)
        self._changes_summary_label.setStyleSheet("color: gray; font-size: 10px;")
        outer.addWidget(self._changes_summary_label)

        # --- Apply Changes button ---
        self._apply_changes_btn = QPushButton("Apply Changes")
        self._apply_changes_btn.setEnabled(False)
        self._apply_changes_btn.clicked.connect(self._on_apply_changes)
        outer.addWidget(self._apply_changes_btn)

        # --- New Session button ---
        self._new_session_btn = QPushButton("New Session")
        self._new_session_btn.setToolTip("Clear current session and start fresh")
        self._new_session_btn.clicked.connect(self._on_new_session)
        outer.addWidget(self._new_session_btn)

        # Connect version selector signal and set initial state
        self._version_selector.currentTextChanged.connect(self._on_version_changed)

        group.setLayout(outer)
        return group

    def _on_browse_previous_version(self) -> None:
        """Open file dialog for selecting previous version file."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Previous Version File",
            "",
            "Markdown Files (*.md);;All Files (*)",
        )
        if path:
            self._prev_version_edit.setText(path)

    def _on_version_changed(self, version: str) -> None:
        """Show/hide version update controls based on selection.

        v1: Hide version update controls, show standard typing workflow.
        v2+: Show version update controls (previous version picker,
             change instructions area, Apply Changes button).
        """
        is_v1 = version == "v1"

        # Version update controls — hidden for v1, shown for v2+
        version_update_widgets = [
            self._prev_version_label,
            self._prev_version_row_widget,
            self._instructions_label,
            self._change_instructions_area,
            self._draft_url_label,
            self._draft_url_edit,
            self._changes_summary_label,
            self._apply_changes_btn,
        ]
        for widget in version_update_widgets:
            widget.setVisible(not is_v1)

        # Standard typing workflow controls — shown for v1, hidden for v2+
        standard_workflow_widgets = [
            self.start_btn,
            self.pause_resume_btn,
        ]
        for widget in standard_workflow_widgets:
            widget.setVisible(is_v1)

        logger.info(
            "Version changed to %s — %s",
            version,
            "standard workflow" if is_v1 else "version update workflow",
        )

    # --- Version update workflow handlers ------------------------------------

    def _restore_session_state(self) -> None:
        """Restore draft URL and version selector from persisted session.

        Called automatically when a ``SessionManager`` is injected via
        ``set_session_manager()``.  If no session exists on disk the UI
        is left at its defaults.

        Requirements: 8.4, 8.5
        """
        if self._session_manager is None:
            return

        try:
            state = self._session_manager.restore_state()
        except Exception:
            logger.warning("Failed to restore session state", exc_info=True)
            return

        if not state:
            logger.info("No previous session to restore")
            return

        # Restore draft URL
        draft_url = state.get("draft_url")
        if draft_url:
            self._draft_url_edit.setText(draft_url)
            logger.info("Restored draft URL from session: %s", draft_url)

        # Restore version selector
        current_version = state.get("current_version")
        if current_version:
            idx = self._version_selector.findText(current_version)
            if idx >= 0:
                self._version_selector.setCurrentIndex(idx)
                logger.info("Restored version selector to %s", current_version)

        logger.info("Session state restored successfully")

    def _on_new_session(self) -> None:
        """Clear the current session and reset all version-update fields.

        Requirement: 8.6
        """
        reply = QMessageBox.question(
            self,
            "New Session",
            "This will clear the current session state, including the draft URL "
            "and version selection.\n\nAre you sure?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # Clear persisted session
        if self._session_manager is not None:
            self._session_manager.clear_session()

        # Reset UI fields
        self._draft_url_edit.clear()
        self._version_selector.setCurrentIndex(0)  # back to v1
        self._change_instructions_area.clear()
        self._prev_version_edit.clear()
        self._changes_summary_label.clear()

        self.statusBar().showMessage("Session cleared — ready for a fresh start")
        logger.info("User cleared session via New Session action")

    def _on_apply_changes(self) -> None:
        """Validate inputs, detect/parse changes, show confirmation, start workflow."""
        version = self._version_selector.currentText()
        draft_url = self._draft_url_edit.text().strip()

        # Validate draft URL
        if not draft_url:
            QMessageBox.warning(self, "Missing Draft URL", "Please enter a Medium draft URL.")
            return

        prev_file = self._prev_version_edit.text().strip()
        instructions_text = self._change_instructions_area.toPlainText().strip()

        # Must have at least one input source
        if not prev_file and not instructions_text:
            QMessageBox.warning(
                self,
                "No Changes Specified",
                "Please provide either a previous version file for diff comparison "
                "or enter change instructions.",
            )
            return

        # Validate that a current article file is selected
        if not self._selected_file:
            QMessageBox.warning(self, "No File Selected", "Please select an article file first.")
            return

        instructions: list[ChangeInstruction] = []

        try:
            if prev_file:
                # Diff-based detection
                detector = VersionDiffDetector(self._markdown_processor)
                instructions = detector.detect_changes(prev_file, str(self._selected_file))
            elif instructions_text:
                # Manual instruction parsing
                parser = ChangeParser()
                instructions = parser.parse_instructions(instructions_text)
        except Exception as exc:
            QMessageBox.critical(
                self, "Error Detecting Changes", f"Failed to detect changes:\n\n{exc}"
            )
            return

        if not instructions:
            QMessageBox.information(
                self, "No Changes", "No changes were detected or parsed from the input."
            )
            return

        # Build confirmation summary
        summary_lines = [f"Detected {len(instructions)} change(s):\n"]
        for i, inst in enumerate(instructions, 1):
            section = inst.section or "(unknown)"
            summary_lines.append(f"  {i}. {inst.action.value.upper()} — {section}")

        summary = "\n".join(summary_lines)
        self._changes_summary_label.setText(summary)

        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Confirm Changes",
            f"{summary}\n\nProceed with applying these changes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # Read article content for the worker
        try:
            article_content = self._selected_file.read_text(encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(
                self, "File Read Error", f"Cannot read article file:\n\n{exc}"
            )
            return

        # Disable controls and show countdown
        self._set_version_update_controls_enabled(False)
        self._is_typing = True
        self._update_button_states()
        self.progress_widget.start_publishing()

        # Store worker params for use after countdown
        self._pending_vu_instructions = instructions
        self._pending_vu_article_content = article_content
        self._pending_vu_draft_url = draft_url
        self._pending_vu_version = version

        # Start countdown, then launch worker
        self._start_version_update_countdown()

    def _start_version_update_countdown(self) -> None:
        """Run countdown (3, 2, 1) then start the VersionUpdateWorker."""
        duration = int(self.config.get("safety.countdown_seconds", 3))
        self._countdown_remaining = duration
        self.countdown_tick.emit(self._countdown_remaining)

        self._countdown_timer = QTimer(self)
        self._countdown_timer.setInterval(1000)
        self._countdown_timer.timeout.connect(self._tick_version_update_countdown)
        self._countdown_timer.start()

    def _tick_version_update_countdown(self) -> None:
        """Tick the version update countdown and launch worker when done."""
        self._countdown_remaining -= 1
        self.countdown_tick.emit(self._countdown_remaining)
        if self._countdown_remaining <= 0:
            self._countdown_timer.stop()
            self._launch_version_update_worker()

    def _launch_version_update_worker(self) -> None:
        """Create and start the VersionUpdateWorker thread."""
        workflow = getattr(self, "_publishing_workflow", None)
        if workflow is None:
            QMessageBox.critical(
                self, "Configuration Error", "Publishing workflow not configured."
            )
            self._on_version_update_finished(False, "Publishing workflow not configured.")
            return

        self._version_update_worker = VersionUpdateWorker(
            workflow=workflow,
            instructions=self._pending_vu_instructions,
            article_content=self._pending_vu_article_content,
            draft_url=self._pending_vu_draft_url,
            version=self._pending_vu_version,
        )
        self._version_update_worker.status_update.connect(self.update_status)
        self._version_update_worker.instruction_progress.connect(self.update_progress)
        self._version_update_worker.finished_signal.connect(self._on_version_update_finished)
        self._version_update_worker.start()

        logger.info("VersionUpdateWorker started for %s", self._pending_vu_version)

    @pyqtSlot(bool, str)
    def _on_version_update_finished(self, success: bool, message: str) -> None:
        """Handle VersionUpdateWorker completion."""
        self._is_typing = False
        self._is_paused = False
        self._set_version_update_controls_enabled(True)
        self._update_button_states()
        self.progress_widget.finish_publishing(success)

        if success:
            QMessageBox.information(self, "Version Update Complete", message)
        else:
            QMessageBox.warning(self, "Version Update Stopped", message)

        logger.info("Version update finished: success=%s, message=%s", success, message)

    def _set_version_update_controls_enabled(self, enabled: bool) -> None:
        """Enable or disable all version update input controls."""
        self._version_selector.setEnabled(enabled)
        self._prev_version_edit.setEnabled(enabled)
        self._browse_prev_btn.setEnabled(enabled)
        self._change_instructions_area.setEnabled(enabled)
        self._draft_url_edit.setEnabled(enabled)
        self._apply_changes_btn.setEnabled(enabled)
        self.select_file_btn.setEnabled(enabled)
        self.select_batch_btn.setEnabled(enabled)
        self.settings_btn.setEnabled(enabled)

    def _build_article_info_group(self) -> QGroupBox:
        group = QGroupBox("Article Information")
        layout = QVBoxLayout()
        self.article_info_label = QLabel("No article loaded")
        self.article_info_label.setWordWrap(True)
        layout.addWidget(self.article_info_label)
        group.setLayout(layout)
        return group

    def _build_countdown_group(self) -> QGroupBox:
        group = QGroupBox("Countdown")
        layout = QVBoxLayout()
        self.countdown_label = QLabel("")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        layout.addWidget(self.countdown_label)
        group.setLayout(layout)
        return group

    def _build_actions_group(self) -> QGroupBox:
        group = QGroupBox("Actions")
        outer = QVBoxLayout()

        # Skip navigation checkbox
        self._skip_nav_checkbox = QCheckBox("Skip Navigation (editor already open)")
        self._skip_nav_checkbox.setChecked(True)
        self._skip_nav_checkbox.setToolTip(
            "Check this if you already have the Medium editor open and focused.\n"
            "The app will skip screen recognition and start typing immediately after countdown."
        )
        outer.addWidget(self._skip_nav_checkbox)

        # Action buttons row
        layout = QHBoxLayout()

        self.start_btn = QPushButton("Start Typing")
        self.start_btn.clicked.connect(self._on_start_typing)
        layout.addWidget(self.start_btn)

        self.pause_resume_btn = QPushButton("Pause")
        self.pause_resume_btn.clicked.connect(self._on_pause_resume)
        layout.addWidget(self.pause_resume_btn)

        self.emergency_stop_btn = QPushButton("Emergency Stop")
        self.emergency_stop_btn.setStyleSheet("background-color: #cc0000; color: white; font-weight: bold;")
        self.emergency_stop_btn.clicked.connect(self._on_emergency_stop)
        layout.addWidget(self.emergency_stop_btn)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self._on_open_settings)
        layout.addWidget(self.settings_btn)

        outer.addLayout(layout)
        group.setLayout(outer)
        return group

    # --- Shortcuts & signals --------------------------------------------------

    def _setup_shortcuts(self) -> None:
        QShortcut(QKeySequence.StandardKey.Open, self).activated.connect(self._on_select_file)
        QShortcut(QKeySequence("Ctrl+Shift+S"), self).activated.connect(self._on_emergency_stop)

    def _connect_signals(self) -> None:
        self.status_changed.connect(self._apply_status)
        self.countdown_tick.connect(self._apply_countdown)
        self.typing_finished.connect(self._apply_typing_finished)

    # --- Slot implementations -------------------------------------------------

    @pyqtSlot(str)
    def _apply_status(self, message: str) -> None:
        self.statusBar().showMessage(message)

    @pyqtSlot(int)
    def _apply_countdown(self, remaining: int) -> None:
        if remaining > 0:
            self.countdown_label.setText(str(remaining))
        else:
            self.countdown_label.setText("Go!")
            QTimer.singleShot(500, lambda: self.countdown_label.setText(""))

    @pyqtSlot(bool, str)
    def _apply_typing_finished(self, success: bool, message: str) -> None:
        self._is_typing = False
        self._is_paused = False
        self._update_button_states()
        if success:
            QMessageBox.information(self, "Complete", message)
        else:
            QMessageBox.warning(self, "Stopped", message)

    # --- Button handlers ------------------------------------------------------

    def _on_select_file(self) -> None:
        path = self._file_selector.select_file()
        if path:
            self._selected_file = path
            self._selected_files = []
            self.file_path_label.setText(str(path))
            self._load_article_info()
            self._update_button_states()

    def _on_select_batch(self) -> None:
        paths = self._file_selector.select_multiple_files()
        if paths:
            self._selected_files = paths
            self._selected_file = None
            self.file_path_label.setText(f"{len(paths)} files selected")
            self.article_info_label.setText(
                f"Batch: {len(paths)} articles\n"
                + "\n".join(f"  {p.name}" for p in paths[:5])
                + ("\n  ..." if len(paths) > 5 else "")
            )
            self._update_button_states()

    def _on_draft_url_changed(self, text: str) -> None:
        if not text.strip():
            self.draft_url_status.setText("Leave empty to create a new story")
            self.draft_url_status.setStyleSheet("color: gray; font-size: 10px;")
        elif self.validate_draft_url(text.strip()):
            self.draft_url_status.setText("Valid Medium URL")
            self.draft_url_status.setStyleSheet("color: green; font-size: 10px;")
        else:
            self.draft_url_status.setText("Invalid URL — expected https://medium.com/...")
            self.draft_url_status.setStyleSheet("color: red; font-size: 10px;")

    def _on_start_typing(self) -> None:
        """Start the countdown, then begin typing."""
        if self._is_typing:
            return
        self._is_typing = True
        self._is_paused = False
        self._update_button_states()
        self.start_countdown()

    def _on_pause_resume(self) -> None:
        if not self._is_typing:
            return
        if self._is_paused:
            # Resume
            self._is_paused = False
            self.pause_resume_btn.setText("Pause")
            if self._emergency_stop:
                self._emergency_stop.resume()
            self.status_changed.emit("Resumed")
        else:
            # Pause
            self._is_paused = True
            self.pause_resume_btn.setText("Resume")
            if self._emergency_stop:
                self._emergency_stop.pause()
            self.status_changed.emit("Paused")
        self._update_button_states()

    def _on_emergency_stop(self) -> None:
        if self._emergency_stop:
            self._emergency_stop.trigger()
        self._is_typing = False
        self._is_paused = False
        # Cancel countdown if running
        if self._countdown_timer and self._countdown_timer.isActive():
            self._countdown_timer.stop()
        self.countdown_label.setText("")
        self._update_button_states()
        self.status_changed.emit("EMERGENCY STOP")

    def _on_open_settings(self) -> None:
        dialog = SettingsDialog(self.config, self)
        if dialog.exec() == SettingsDialog.DialogCode.Accepted:
            self.status_changed.emit("Settings saved")

    def _on_always_on_top_toggled(self, checked: bool) -> None:
        self.config.set("ui.always_on_top", checked)
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()  # Required after changing window flags

    # --- Countdown ------------------------------------------------------------

    def start_countdown(self) -> None:
        """Run the pre-typing countdown (3, 2, 1, Go!)."""
        duration = int(self.config.get("safety.countdown_seconds", 3))
        self._countdown_remaining = duration
        self.countdown_tick.emit(self._countdown_remaining)

        self._countdown_timer = QTimer(self)
        self._countdown_timer.setInterval(1000)
        self._countdown_timer.timeout.connect(self._tick_countdown)
        self._countdown_timer.start()

    def _tick_countdown(self) -> None:
        self._countdown_remaining -= 1
        self.countdown_tick.emit(self._countdown_remaining)
        if self._countdown_remaining <= 0:
            self._countdown_timer.stop()
            self._launch_typing_worker()

    def _launch_typing_worker(self) -> None:
        """Create and start the TypingWorker thread."""
        workflow = getattr(self, "_publishing_workflow", None)
        if workflow is None:
            QMessageBox.critical(
                self, "Configuration Error", "Publishing workflow not configured."
            )
            self._is_typing = False
            self._update_button_states()
            return

        if not self._selected_file:
            QMessageBox.warning(self, "No File", "Please select an article file first.")
            self._is_typing = False
            self._update_button_states()
            return

        # Reset emergency stop from any previous run
        if self._emergency_stop:
            self._emergency_stop.reset()

        # When skipping navigation, disable focus detection since the user
        # is responsible for keeping the browser focused.
        if hasattr(self, '_focus_detector') and self._focus_detector:
            self._focus_detector._target_title = None

        # Set skip navigation on the workflow
        workflow._skip_navigation = self._skip_nav_checkbox.isChecked()

        draft_url = self.draft_url_input.text().strip() or None

        self._typing_worker = TypingWorker(
            workflow=workflow,
            file_paths=[str(self._selected_file)],
            draft_url=draft_url,
        )
        self._typing_worker.status_update.connect(self.update_status)
        self._typing_worker.block_progress.connect(self.update_progress)
        self._typing_worker.finished_signal.connect(self._on_typing_finished)
        self._typing_worker.start()

        logger.info("TypingWorker started for %s", self._selected_file.name)

    @pyqtSlot(bool, str)
    def _on_typing_finished(self, success: bool, message: str) -> None:
        """Handle TypingWorker completion."""
        self._is_typing = False
        self._is_paused = False
        self._update_button_states()
        self.progress_widget.finish_publishing(success)

        if success:
            QMessageBox.information(self, "Typing Complete", message)
        else:
            QMessageBox.warning(self, "Typing Stopped", message)

        logger.info("Typing finished: success=%s, message=%s", success, message)

    # --- Helpers --------------------------------------------------------------

    def _load_article_info(self) -> None:
        if not self._selected_file:
            return
        try:
            article = self._article_parser.parse_file(str(self._selected_file))
            blocks = self._markdown_processor.process(article.content)
            char_count = sum(len(b.content) for b in blocks)
            base_delay = self.config.get("typing.base_delay_ms", 200)
            est_seconds = (char_count * base_delay) / 1000
            est_minutes = est_seconds / 60
            self.article_info_label.setText(
                f"Title: {article.title}\n"
                f"Characters: {char_count:,}\n"
                f"Blocks: {len(blocks)}\n"
                f"Est. time: {est_minutes:.1f} min\n"
                f"Tags: {', '.join(article.tags[:5])}"
            )
        except Exception as exc:
            self.article_info_label.setText(f"Error: {exc}")

    def _update_button_states(self) -> None:
        """Enable/disable buttons based on current state."""
        has_file = self._selected_file is not None or len(self._selected_files) > 0

        self.start_btn.setEnabled(has_file and not self._is_typing)
        self.pause_resume_btn.setEnabled(self._is_typing)
        self.emergency_stop_btn.setEnabled(True)  # Always available
        self.select_file_btn.setEnabled(not self._is_typing)
        self.select_batch_btn.setEnabled(not self._is_typing)
        self.draft_url_input.setEnabled(not self._is_typing)
        self.settings_btn.setEnabled(not self._is_typing)

    def update_status(self, message: str) -> None:
        """Thread-safe status update."""
        self.status_changed.emit(message)

    def update_progress(self, current: int, total: int) -> None:
        """Update the progress widget percentage."""
        if total > 0:
            self.progress_widget.update_progress(int((current / total) * 100))

    def _auto_discover_versions(self, selected_file: Path) -> List[Path]:
        """Discover version files in the parent versions/ directory.

        Scans for files matching ``v{N}-{article-name}.md`` pattern,
        sorts by version number ascending.

        Args:
            selected_file: The currently selected version file.

        Returns:
            Sorted list of discovered version file paths.
        """
        versions_dir = selected_file.parent
        if not versions_dir.is_dir():
            return []

        discovered: List[tuple[int, Path]] = []
        for child in versions_dir.iterdir():
            if not child.is_file() or child.suffix != ".md":
                continue
            result = validate_version_filename(child.name)
            if result is not None:
                version_number, _ = result
                discovered.append((version_number, child))

        discovered.sort(key=lambda item: item[0])
        return [path for _, path in discovered]

    def _suggest_previous_version(self, selected_file: Path) -> Optional[Path]:
        """Suggest v{N-1} as the previous version based on selected file name.

        Parses the version number from the filename, decrements it,
        and checks if that file exists in the same directory.

        Args:
            selected_file: The currently selected version file.

        Returns:
            Path to suggested previous version, or None if not found.
        """
        result = validate_version_filename(selected_file.name)
        if result is None:
            return None

        version_number, article_name = result
        if version_number <= 1:
            return None

        previous_filename = f"v{version_number - 1}-{article_name}.md"
        previous_path = selected_file.parent / previous_filename
        if previous_path.is_file():
            return previous_path
        return None

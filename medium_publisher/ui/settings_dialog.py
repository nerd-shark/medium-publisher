"""Settings dialog for Medium Keyboard Publisher.

Provides configuration for typing speed, typo behaviour, safety controls,
navigation, and UI preferences. Removes all Playwright/browser settings.
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.utils.logger import get_logger

logger = get_logger(__name__)


class SettingsDialog(QDialog):
    """Settings dialog for application configuration.

    Sections:
    - Typing: base delay, variation, typo frequency, immediate/deferred ratio
    - Safety: emergency stop hotkey, countdown duration
    - Navigation: Google account email, screen recognition confidence
    - Paths: default article directory
    - UI: always-on-top, remember window position
    """

    def __init__(self, config: ConfigManager, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.config = config
        self._init_ui()
        self._load_settings()
        logger.info("SettingsDialog initialized")

    # --- UI construction ------------------------------------------------------

    def _init_ui(self) -> None:
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(520)

        layout = QVBoxLayout()
        layout.addWidget(self._build_typing_group())
        layout.addWidget(self._build_safety_group())
        layout.addWidget(self._build_navigation_group())
        layout.addWidget(self._build_paths_group())
        layout.addWidget(self._build_ui_group())

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_settings)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _build_typing_group(self) -> QGroupBox:
        group = QGroupBox("Typing")
        form = QFormLayout()

        self.base_delay_spin = QSpinBox()
        self.base_delay_spin.setRange(50, 1000)
        self.base_delay_spin.setSuffix(" ms")
        form.addRow("Base delay per keystroke:", self.base_delay_spin)

        self.variation_spin = QSpinBox()
        self.variation_spin.setRange(0, 100)
        self.variation_spin.setSuffix(" %")
        form.addRow("Speed variation (±):", self.variation_spin)

        self.typo_freq_combo = QComboBox()
        self.typo_freq_combo.addItems(["low", "medium", "high"])
        form.addRow("Typo frequency:", self.typo_freq_combo)

        self.immediate_ratio_spin = QDoubleSpinBox()
        self.immediate_ratio_spin.setRange(0.0, 1.0)
        self.immediate_ratio_spin.setSingleStep(0.05)
        self.immediate_ratio_spin.setDecimals(2)
        form.addRow("Immediate correction ratio:", self.immediate_ratio_spin)

        group.setLayout(form)
        return group

    def _build_safety_group(self) -> QGroupBox:
        group = QGroupBox("Safety")
        form = QFormLayout()

        self.hotkey_input = QLineEdit()
        self.hotkey_input.setPlaceholderText("ctrl+shift+escape")
        form.addRow("Emergency stop hotkey:", self.hotkey_input)

        self.countdown_spin = QSpinBox()
        self.countdown_spin.setRange(1, 10)
        self.countdown_spin.setSuffix(" s")
        form.addRow("Countdown duration:", self.countdown_spin)

        group.setLayout(form)
        return group

    def _build_navigation_group(self) -> QGroupBox:
        group = QGroupBox("Navigation")
        form = QFormLayout()

        self.google_email_input = QLineEdit()
        self.google_email_input.setPlaceholderText("user@gmail.com")
        form.addRow("Google account email:", self.google_email_input)

        self.confidence_spin = QDoubleSpinBox()
        self.confidence_spin.setRange(0.1, 1.0)
        self.confidence_spin.setSingleStep(0.05)
        self.confidence_spin.setDecimals(2)
        form.addRow("Screen recognition confidence:", self.confidence_spin)

        group.setLayout(form)
        return group

    def _build_paths_group(self) -> QGroupBox:
        group = QGroupBox("Paths")
        form = QFormLayout()

        self.directory_label = QLabel("(Not set)")
        self.directory_label.setWordWrap(True)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._select_directory)

        row = QHBoxLayout()
        row.addWidget(self.directory_label, 1)
        row.addWidget(browse_btn)
        form.addRow("Default article directory:", row)

        group.setLayout(form)
        return group

    def _build_ui_group(self) -> QGroupBox:
        group = QGroupBox("UI")
        form = QFormLayout()

        self.always_on_top_cb = QCheckBox("Keep window on top")
        form.addRow("", self.always_on_top_cb)

        self.remember_position_cb = QCheckBox("Remember window position")
        form.addRow("", self.remember_position_cb)

        group.setLayout(form)
        return group

    # --- Load / Save ----------------------------------------------------------

    def _load_settings(self) -> None:
        self.base_delay_spin.setValue(int(self.config.get("typing.base_delay_ms", 200)))
        self.variation_spin.setValue(int(self.config.get("typing.variation_percent", 30)))

        typo = self.config.get("typing.typo_frequency", "low")
        idx = self.typo_freq_combo.findText(typo)
        if idx >= 0:
            self.typo_freq_combo.setCurrentIndex(idx)

        self.immediate_ratio_spin.setValue(
            float(self.config.get("typing.immediate_correction_ratio", 0.70))
        )

        self.hotkey_input.setText(
            self.config.get("safety.emergency_stop_hotkey", "ctrl+shift+escape")
        )
        self.countdown_spin.setValue(int(self.config.get("safety.countdown_seconds", 3)))

        self.google_email_input.setText(
            self.config.get("navigation.google_account_email", "")
        )
        self.confidence_spin.setValue(
            float(self.config.get("navigation.screen_confidence", 0.8))
        )

        articles_dir = self.config.get("paths.articles_directory", "")
        self.directory_label.setText(articles_dir or "(Not set)")

        self.always_on_top_cb.setChecked(self.config.get("ui.always_on_top", True))
        self.remember_position_cb.setChecked(
            self.config.get("ui.remember_window_position", True)
        )
        logger.info("Settings loaded")

    def _save_settings(self) -> None:
        self.config.set("typing.base_delay_ms", self.base_delay_spin.value())
        self.config.set("typing.variation_percent", self.variation_spin.value())
        self.config.set("typing.typo_frequency", self.typo_freq_combo.currentText())
        self.config.set("typing.immediate_correction_ratio", self.immediate_ratio_spin.value())

        self.config.set("safety.emergency_stop_hotkey", self.hotkey_input.text().strip())
        self.config.set("safety.countdown_seconds", self.countdown_spin.value())

        self.config.set("navigation.google_account_email", self.google_email_input.text().strip())
        self.config.set("navigation.screen_confidence", self.confidence_spin.value())

        articles_dir = self.directory_label.text()
        if articles_dir != "(Not set)":
            self.config.set("paths.articles_directory", articles_dir)

        self.config.set("ui.always_on_top", self.always_on_top_cb.isChecked())
        self.config.set("ui.remember_window_position", self.remember_position_cb.isChecked())

        self.config.save_config()
        logger.info("Settings saved")
        self.accept()

    def _select_directory(self) -> None:
        current = self.directory_label.text()
        if current == "(Not set)":
            current = str(Path.home())
        directory = QFileDialog.getExistingDirectory(
            self, "Select Default Article Directory", current,
            QFileDialog.Option.ShowDirsOnly,
        )
        if directory:
            self.directory_label.setText(directory)

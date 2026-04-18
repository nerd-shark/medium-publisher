"""Unit tests for reworked UI components.

Tests button state management, countdown display, draft URL validation,
multi-file selection, and progress/batch tracking.

Requirements: 14.1–14.10
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import Qt

# Ensure package is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.ui.main_window import MainWindow
from medium_publisher.ui.progress_widget import ProgressWidget
from medium_publisher.ui.settings_dialog import SettingsDialog


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def config(tmp_path):
    """Create a ConfigManager with a minimal default config."""
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    default_cfg = cfg_dir / "default_config.yaml"
    default_cfg.write_text(
        "typing:\n"
        "  base_delay_ms: 200\n"
        "  variation_percent: 30\n"
        "  typo_frequency: low\n"
        "  immediate_correction_ratio: 0.70\n"
        "safety:\n"
        "  emergency_stop_hotkey: ctrl+shift+escape\n"
        "  countdown_seconds: 3\n"
        "navigation:\n"
        "  screen_confidence: 0.8\n"
        "  google_account_email: test@gmail.com\n"
        "ui:\n"
        "  always_on_top: false\n"
        "  remember_window_position: true\n"
    )
    cm = ConfigManager(config_dir=cfg_dir)
    cm.load_config()
    return cm


# ---------------------------------------------------------------------------
# MainWindow — button state management
# ---------------------------------------------------------------------------

class TestMainWindowButtonStates:
    """Test that buttons are enabled/disabled correctly based on state."""

    def test_start_disabled_when_no_file(self, qtbot, config):
        win = MainWindow(config)
        qtbot.addWidget(win)
        assert not win.start_btn.isEnabled()

    def test_start_enabled_after_file_selected(self, qtbot, config, tmp_path):
        win = MainWindow(config)
        qtbot.addWidget(win)

        md = tmp_path / "article.md"
        md.write_text("---\ntitle: Test\ntags: []\n---\nHello world\n")

        # Simulate file selection
        win._selected_file = md
        win._update_button_states()
        assert win.start_btn.isEnabled()

    def test_pause_disabled_when_not_typing(self, qtbot, config):
        win = MainWindow(config)
        qtbot.addWidget(win)
        assert not win.pause_resume_btn.isEnabled()

    def test_pause_enabled_when_typing(self, qtbot, config, tmp_path):
        win = MainWindow(config)
        qtbot.addWidget(win)

        md = tmp_path / "article.md"
        md.write_text("---\ntitle: T\ntags: []\n---\nBody\n")
        win._selected_file = md
        win._is_typing = True
        win._update_button_states()
        assert win.pause_resume_btn.isEnabled()
        assert not win.start_btn.isEnabled()

    def test_emergency_stop_always_enabled(self, qtbot, config):
        win = MainWindow(config)
        qtbot.addWidget(win)
        assert win.emergency_stop_btn.isEnabled()

    def test_file_buttons_disabled_during_typing(self, qtbot, config, tmp_path):
        win = MainWindow(config)
        qtbot.addWidget(win)
        md = tmp_path / "a.md"
        md.write_text("---\ntitle: T\ntags: []\n---\nBody\n")
        win._selected_file = md
        win._is_typing = True
        win._update_button_states()
        assert not win.select_file_btn.isEnabled()
        assert not win.select_batch_btn.isEnabled()
        assert not win.settings_btn.isEnabled()


# ---------------------------------------------------------------------------
# MainWindow — countdown display
# ---------------------------------------------------------------------------

class TestCountdownDisplay:
    """Test the pre-typing countdown (3, 2, 1, Go!)."""

    def test_countdown_starts_at_configured_value(self, qtbot, config):
        config.set("safety.countdown_seconds", 3)
        win = MainWindow(config)
        qtbot.addWidget(win)

        win._selected_file = Path("dummy.md")
        win.start_countdown()

        assert win.countdown_label.text() == "3"

    def test_countdown_ticks_down(self, qtbot, config):
        config.set("safety.countdown_seconds", 2)
        win = MainWindow(config)
        qtbot.addWidget(win)

        win.start_countdown()
        # Simulate one tick
        win._tick_countdown()
        assert win._countdown_remaining == 1

    def test_countdown_reaches_zero(self, qtbot, config):
        config.set("safety.countdown_seconds", 1)
        win = MainWindow(config)
        qtbot.addWidget(win)

        win.start_countdown()
        win._tick_countdown()
        # Should have emitted 0 and stopped
        assert win._countdown_remaining == 0


# ---------------------------------------------------------------------------
# MainWindow — draft URL validation
# ---------------------------------------------------------------------------

class TestDraftUrlValidation:
    """Test draft URL validation in the UI."""

    def test_valid_medium_url(self, qtbot, config):
        assert MainWindow.validate_draft_url("https://medium.com/p/abc123/edit")

    def test_valid_publication_url(self, qtbot, config):
        assert MainWindow.validate_draft_url("https://pub.medium.com/my-article-abc123")

    def test_invalid_url_rejected(self, qtbot, config):
        assert not MainWindow.validate_draft_url("https://example.com/article")

    def test_empty_url_rejected(self, qtbot, config):
        assert not MainWindow.validate_draft_url("")

    def test_url_status_label_updates(self, qtbot, config):
        win = MainWindow(config)
        qtbot.addWidget(win)

        win.draft_url_input.setText("https://medium.com/p/123/edit")
        assert "Valid" in win.draft_url_status.text()

        win.draft_url_input.setText("https://bad.com/nope")
        assert "Invalid" in win.draft_url_status.text()

        win.draft_url_input.setText("")
        assert "empty" in win.draft_url_status.text().lower() or "Leave" in win.draft_url_status.text()


# ---------------------------------------------------------------------------
# MainWindow — batch file selection
# ---------------------------------------------------------------------------

class TestBatchFileSelection:
    """Test multi-file selection updates UI correctly."""

    def test_batch_selection_updates_label(self, qtbot, config, tmp_path):
        win = MainWindow(config)
        qtbot.addWidget(win)

        files = []
        for i in range(3):
            f = tmp_path / f"article_{i}.md"
            f.write_text(f"---\ntitle: Art {i}\ntags: []\n---\nBody {i}\n")
            files.append(f)

        # Simulate batch selection
        win._selected_files = files
        win._selected_file = None
        win.file_path_label.setText(f"{len(files)} files selected")
        win._update_button_states()

        assert "3 files" in win.file_path_label.text()
        assert win.start_btn.isEnabled()

    def test_single_file_clears_batch(self, qtbot, config, tmp_path):
        win = MainWindow(config)
        qtbot.addWidget(win)

        f = tmp_path / "single.md"
        f.write_text("---\ntitle: T\ntags: []\n---\nBody\n")

        win._selected_files = [f, f]
        win._selected_file = f
        win._selected_files = []
        win._update_button_states()

        assert win.start_btn.isEnabled()
        assert len(win.selected_files) == 0


# ---------------------------------------------------------------------------
# ProgressWidget — per-block and batch tracking
# ---------------------------------------------------------------------------

class TestProgressWidget:
    """Test per-block progress and batch tracking."""

    def test_block_progress_updates(self, qtbot):
        pw = ProgressWidget()
        qtbot.addWidget(pw)

        pw.start_publishing(total_articles=1, estimated_seconds=60)
        pw.update_block_progress(3, 10)

        assert "3" in pw.block_label.text()
        assert "10" in pw.block_label.text()
        assert pw.progress_bar.value() == 30

    def test_batch_progress_label(self, qtbot):
        pw = ProgressWidget()
        qtbot.addWidget(pw)

        pw.start_publishing(total_articles=5)
        pw.update_batch_progress(2, 5)

        assert "2" in pw.batch_label.text()
        assert "5" in pw.batch_label.text()

    def test_single_article_hides_batch_label(self, qtbot):
        pw = ProgressWidget()
        qtbot.addWidget(pw)

        pw.start_publishing(total_articles=1)
        assert pw.batch_label.text() == ""

    def test_finish_sets_100_percent(self, qtbot):
        pw = ProgressWidget()
        qtbot.addWidget(pw)

        pw.start_publishing()
        pw.finish_publishing(success=True)
        assert pw.progress_bar.value() == 100
        assert "Complete" in pw.status_label.text()

    def test_reset_clears_all(self, qtbot):
        pw = ProgressWidget()
        qtbot.addWidget(pw)

        pw.start_publishing(total_articles=3, estimated_seconds=120)
        pw.update_block_progress(5, 10)
        pw.reset()

        assert pw.progress_bar.value() == 0
        assert pw.status_label.text() == "Ready"
        assert pw.batch_label.text() == ""


# ---------------------------------------------------------------------------
# SettingsDialog — loads and saves config values
# ---------------------------------------------------------------------------

class TestSettingsDialog:
    """Test that SettingsDialog loads/saves config correctly."""

    def test_loads_typing_settings(self, qtbot, config):
        dlg = SettingsDialog(config)
        qtbot.addWidget(dlg)

        assert dlg.base_delay_spin.value() == 200
        assert dlg.variation_spin.value() == 30
        assert dlg.typo_freq_combo.currentText() == "low"
        assert dlg.immediate_ratio_spin.value() == pytest.approx(0.70)

    def test_loads_safety_settings(self, qtbot, config):
        dlg = SettingsDialog(config)
        qtbot.addWidget(dlg)

        assert dlg.hotkey_input.text() == "ctrl+shift+escape"
        assert dlg.countdown_spin.value() == 3

    def test_loads_navigation_settings(self, qtbot, config):
        dlg = SettingsDialog(config)
        qtbot.addWidget(dlg)

        assert dlg.google_email_input.text() == "test@gmail.com"
        assert dlg.confidence_spin.value() == pytest.approx(0.8)

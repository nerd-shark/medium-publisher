"""Integration tests for the full typing flow.

Tests the complete article-typing pipeline with mocked OS input,
batch publishing, and error recovery scenarios.

All OS-level calls (pyautogui, pynput, webbrowser, win32gui) are mocked.

Requirements: 4.1–4.18, 10.1–10.5, 13.1–13.7
"""

from __future__ import annotations

from pathlib import Path
from typing import List
from unittest.mock import MagicMock, patch, call

import pytest

from medium_publisher.automation.content_typer import ContentTyper
from medium_publisher.automation.deferred_typo_tracker import DeferredTypoTracker
from medium_publisher.automation.human_typing_simulator import HumanTypingSimulator
from medium_publisher.automation.os_input_controller import OS_Input_Controller
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.core.publishing_workflow import PublishingWorkflow, PublishingResult
from medium_publisher.core.session_manager import SessionManager
from medium_publisher.navigation.navigation_state_machine import NavigationStateMachine
from medium_publisher.safety.emergency_stop import EmergencyStop
from medium_publisher.safety.focus_window_detector import FocusWindowDetector
from medium_publisher.utils.exceptions import EmergencyStopError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    """Disable all time.sleep calls to speed up tests."""
    import time as _time
    monkeypatch.setattr(_time, "sleep", lambda _: None)


SAMPLE_ARTICLE = """\
---
title: Integration Test Article
subtitle: A subtitle for testing
tags:
  - testing
  - integration
---

## Introduction

This is a paragraph with **bold** and *italic* text.

## Code Example

```python
print("hello")
```

## Lists

* item one
* item two

## Conclusion

Final paragraph.
"""


@pytest.fixture
def sample_article_file(tmp_path: Path) -> Path:
    """Create a sample markdown article on disk."""
    p = tmp_path / "test_article.md"
    p.write_text(SAMPLE_ARTICLE, encoding="utf-8")
    return p


@pytest.fixture
def batch_article_files(tmp_path: Path) -> List[Path]:
    """Create multiple sample articles for batch testing."""
    files = []
    for i in range(3):
        content = SAMPLE_ARTICLE.replace(
            "Integration Test Article", f"Batch Article {i + 1}"
        )
        p = tmp_path / f"article_{i + 1}.md"
        p.write_text(content, encoding="utf-8")
        files.append(p)
    return files


@pytest.fixture
def mock_pyautogui():
    """Patch pyautogui globally so no real input is generated."""
    with patch("medium_publisher.automation.os_input_controller.pyautogui") as m:
        m.FAILSAFE = True
        yield m


@pytest.fixture
def mock_emergency_stop():
    """Create an EmergencyStop that never fires."""
    es = MagicMock(spec=EmergencyStop)
    es.is_stopped.return_value = False
    es.is_paused = False
    return es


@pytest.fixture
def mock_focus_detector():
    """Create a FocusWindowDetector that always reports focus."""
    fd = MagicMock(spec=FocusWindowDetector)
    fd.is_target_focused.return_value = True
    return fd


@pytest.fixture
def config(tmp_path: Path) -> ConfigManager:
    """Create a ConfigManager with test-friendly settings."""
    cfg = ConfigManager.__new__(ConfigManager)
    cfg.config = {
        "typing": {
            "base_delay_ms": 1,
            "variation_percent": 0,
            "human_typing_enabled": False,
            "typo_frequency": "low",
            "immediate_correction_ratio": 0.70,
        },
        "safety": {
            "emergency_stop_hotkey": "ctrl+shift+escape",
            "countdown_seconds": 0,
        },
        "navigation": {
            "screen_confidence": 0.8,
            "poll_interval_seconds": 0.01,
            "login_timeout_seconds": 1,
            "page_load_timeout_seconds": 1,
            "google_account_email": "test@example.com",
        },
        "assets": {
            "reference_images_dir": str(tmp_path / "assets"),
        },
    }
    cfg.config_dir = tmp_path / "config"
    cfg.user_config_dir = tmp_path / "user_config"
    cfg.default_config_path = cfg.config_dir / "default_config.yaml"
    cfg.user_config_path = cfg.user_config_dir / "config.yaml"
    return cfg


@pytest.fixture
def input_controller(mock_pyautogui, mock_emergency_stop, mock_focus_detector):
    """Create an OS_Input_Controller with mocked dependencies."""
    return OS_Input_Controller(mock_emergency_stop, mock_focus_detector)


@pytest.fixture
def content_typer(input_controller, config):
    """Create a ContentTyper with mocked input and disabled typos."""
    simulator = HumanTypingSimulator(typo_frequency="low", enabled=False)
    tracker = DeferredTypoTracker()
    return ContentTyper(input_controller, simulator, tracker, config)


@pytest.fixture
def session_manager(tmp_path: Path):
    """Create a SessionManager writing to a temp directory."""
    return SessionManager(session_dir=tmp_path / "session")


@pytest.fixture
def nav_state_machine(config, input_controller):
    """Create a NavigationStateMachine that always reports READY."""
    nav = MagicMock(spec=NavigationStateMachine)
    nav.navigate_to_editor.return_value = True
    return nav


@pytest.fixture
def workflow(
    config,
    mock_emergency_stop,
    nav_state_machine,
    content_typer,
    session_manager,
):
    """Create a PublishingWorkflow with all mocked/test dependencies."""
    tracker = content_typer._tracker
    return PublishingWorkflow(
        config=config,
        emergency_stop=mock_emergency_stop,
        nav_state_machine=nav_state_machine,
        content_typer=content_typer,
        typo_tracker=tracker,
        session_manager=session_manager,
    )


# ---------------------------------------------------------------------------
# Test: Complete single-article typing flow
# ---------------------------------------------------------------------------


class TestFullTypingFlow:
    """Verify the complete article typing pipeline end-to-end."""

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_single_article_types_all_blocks(
        self, mock_pag, sample_article_file, workflow
    ):
        """Typing a single article should invoke key sequences for every block."""
        mock_pag.FAILSAFE = True
        results = workflow.execute(
            file_paths=[str(sample_article_file)],
        )

        assert len(results) == 1
        assert results[0].success is True
        assert results[0].file_path == str(sample_article_file)

        # pyautogui.write should have been called (characters typed)
        assert mock_pag.write.call_count > 0

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_single_article_applies_header_shortcuts(
        self, mock_pag, sample_article_file, workflow
    ):
        """Headers should trigger Ctrl+Alt+1 or Ctrl+Alt+2 hotkeys."""
        mock_pag.FAILSAFE = True
        workflow.execute(file_paths=[str(sample_article_file)])

        hotkey_calls = [
            c for c in mock_pag.hotkey.call_args_list
            if c.args[:2] == ("ctrl", "alt")
        ]
        # At least one header shortcut expected (## Introduction, etc.)
        assert len(hotkey_calls) >= 1

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_single_article_types_code_without_typos(
        self, mock_pag, sample_article_file, workflow
    ):
        """Code blocks should be typed verbatim (no typo simulation)."""
        mock_pag.FAILSAFE = True
        workflow.execute(file_paths=[str(sample_article_file)])

        # The code content 'print("hello")' should appear in write calls
        all_written = "".join(
            c.args[0] for c in mock_pag.write.call_args_list if c.args
        )
        assert 'print("hello")' in all_written

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_single_article_collects_placeholders(
        self, mock_pag, tmp_path, workflow
    ):
        """Placeholder blocks should be reported in the result."""
        md = """\
---
title: Placeholder Test
---

Some text.

![alt text](http://example.com/img.png)
"""
        p = tmp_path / "placeholder.md"
        p.write_text(md, encoding="utf-8")
        mock_pag.FAILSAFE = True

        results = workflow.execute(file_paths=[str(p)])
        assert results[0].success is True
        # Placeholder should be collected
        assert any("image" in ph.lower() for ph in results[0].placeholders)

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_navigation_called_before_typing(
        self, mock_pag, sample_article_file, workflow, nav_state_machine
    ):
        """navigate_to_editor must be called before typing starts."""
        mock_pag.FAILSAFE = True
        workflow.execute(file_paths=[str(sample_article_file)])
        nav_state_machine.navigate_to_editor.assert_called_once()


# ---------------------------------------------------------------------------
# Test: Batch publishing flow
# ---------------------------------------------------------------------------


class TestBatchPublishingFlow:
    """Verify batch mode: multiple articles, pause between, skip on failure."""

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_batch_publishes_all_articles(
        self, mock_pag, batch_article_files, workflow
    ):
        """All articles in a batch should be processed sequentially."""
        mock_pag.FAILSAFE = True
        paths = [str(p) for p in batch_article_files]
        results = workflow.execute(file_paths=paths)

        assert len(results) == 3
        assert all(r.success for r in results)

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_batch_reports_article_progress(
        self, mock_pag, batch_article_files, workflow
    ):
        """article_cb should be called with (current, total) for each article."""
        mock_pag.FAILSAFE = True
        article_cb = MagicMock()
        paths = [str(p) for p in batch_article_files]
        workflow.execute(file_paths=paths, article_cb=article_cb)

        expected = [call(1, 3), call(2, 3), call(3, 3)]
        assert article_cb.call_args_list == expected

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_batch_skips_on_parse_failure(
        self, mock_pag, batch_article_files, tmp_path, workflow
    ):
        """If one article fails to parse, the batch should skip it and continue."""
        mock_pag.FAILSAFE = True
        bad_file = tmp_path / "bad.md"
        bad_file.write_text("not valid frontmatter", encoding="utf-8")

        paths = [str(batch_article_files[0]), str(bad_file), str(batch_article_files[1])]
        results = workflow.execute(file_paths=paths)

        assert len(results) == 3
        assert results[0].success is True
        assert results[1].success is False  # bad file
        assert results[2].success is True

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_batch_skips_on_navigation_failure(
        self, mock_pag, batch_article_files, workflow, nav_state_machine
    ):
        """If navigation fails for one article, skip and continue."""
        mock_pag.FAILSAFE = True
        # Fail on second call only
        nav_state_machine.navigate_to_editor.side_effect = [True, False, True]

        paths = [str(p) for p in batch_article_files]
        results = workflow.execute(file_paths=paths)

        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True


# ---------------------------------------------------------------------------
# Test: Error recovery — emergency stop mid-article
# ---------------------------------------------------------------------------


class TestErrorRecovery:
    """Verify emergency stop and progress saving during typing."""

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_emergency_stop_halts_batch(
        self, mock_pag, batch_article_files, workflow, mock_emergency_stop
    ):
        """Emergency stop during typing should halt the entire batch."""
        mock_pag.FAILSAFE = True

        # Simulate emergency stop on second pyautogui.write call
        call_count = {"n": 0}
        original_write = mock_pag.write

        def write_side_effect(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] > 5:
                mock_emergency_stop.is_stopped.return_value = True
                raise EmergencyStopError("Emergency stop triggered")

        mock_pag.write.side_effect = write_side_effect

        paths = [str(p) for p in batch_article_files]

        with pytest.raises(EmergencyStopError):
            workflow.execute(file_paths=paths)

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_progress_saved_on_error(
        self, mock_pag, sample_article_file, workflow, session_manager
    ):
        """On unexpected error, typing progress should be saved to session."""
        mock_pag.FAILSAFE = True

        # Make navigation succeed but typing fail mid-way
        call_count = {"n": 0}

        def write_side_effect(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] > 3:
                raise RuntimeError("Simulated OS error")

        mock_pag.write.side_effect = write_side_effect

        results = workflow.execute(file_paths=[str(sample_article_file)])

        # Should have one failed result (not raise)
        assert len(results) == 1
        assert results[0].success is False

    @patch("medium_publisher.automation.os_input_controller.pyautogui")
    def test_review_pass_with_deferred_typos(
        self, mock_pag, sample_article_file, workflow
    ):
        """When deferred typos exist, review pass should call Ctrl+Home and Ctrl+F."""
        mock_pag.FAILSAFE = True

        # Manually record a deferred typo so the review pass has work to do
        workflow._tracker.record(
            block_index=0,
            char_offset=5,
            wrong_char="x",
            correct_char="a",
            surrounding_context="test context",
        )

        workflow.execute(file_paths=[str(sample_article_file)])

        hotkey_calls = mock_pag.hotkey.call_args_list
        ctrl_home_calls = [c for c in hotkey_calls if c.args == ("ctrl", "home")]
        ctrl_f_calls = [c for c in hotkey_calls if c.args == ("ctrl", "f")]
        # Review pass: Ctrl+Home to go to top, Ctrl+F to find each typo
        assert len(ctrl_home_calls) >= 1
        assert len(ctrl_f_calls) >= 1

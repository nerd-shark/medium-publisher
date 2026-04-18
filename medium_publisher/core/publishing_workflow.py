"""
Publishing workflow orchestration for Medium Keyboard Publisher.

Coordinates the full publishing flow: file selection → parse → countdown →
navigate to editor → type article → review pass → completion notification.
Supports batch mode with sequential processing.

Runs typing in a QThread to keep the UI responsive.

Requirements: 1.1–1.7, 8.1–8.4, 10.1–10.5, 13.1–13.7
"""

from __future__ import annotations

import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional

from PyQt6.QtCore import QThread, pyqtSignal

from medium_publisher.automation.content_typer import ContentTyper
from medium_publisher.automation.deferred_typo_tracker import DeferredTypoTracker
from medium_publisher.automation.version_update_typer import VersionUpdateTyper
from medium_publisher.core.article_parser import ArticleParser
from medium_publisher.core.change_parser import ChangeInstruction
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.core.markdown_processor import MarkdownProcessor
from medium_publisher.core.models import ContentBlock, UpdateResult
from medium_publisher.core.session_manager import SessionManager
from medium_publisher.core.version_diff_detector import VersionDiffDetector
from medium_publisher.navigation.navigation_state_machine import NavigationStateMachine
from medium_publisher.safety.emergency_stop import EmergencyStop
from medium_publisher.utils.exceptions import (
    ContentError,
    EmergencyStopError,
    FileError,
    FocusLostError,
    NavigationError,
    PublishingError,
)
from medium_publisher.utils.logger import get_logger

logger = get_logger("core.publishing_workflow")


@dataclass
class PublishingResult:
    """Result of a single article publishing attempt."""

    success: bool
    message: str
    file_path: str = ""
    placeholders: List[str] = field(default_factory=list)


class TypingWorker(QThread):
    """Runs the typing workflow in a background thread.

    Signals:
        status_update(str): Emitted with status messages.
        block_progress(int, int): Emitted with (current_block, total_blocks).
        article_progress(int, int): Emitted with (current_article, total_articles).
        finished_signal(bool, str): Emitted when workflow completes (success, message).
        placeholders_found(list): Emitted with placeholder strings after typing.
    """

    status_update = pyqtSignal(str)
    block_progress = pyqtSignal(int, int)
    article_progress = pyqtSignal(int, int)
    finished_signal = pyqtSignal(bool, str)
    placeholders_found = pyqtSignal(list)

    def __init__(
        self,
        workflow: "PublishingWorkflow",
        file_paths: List[str],
        draft_url: Optional[str] = None,
    ) -> None:
        super().__init__()
        self._workflow = workflow
        self._file_paths = file_paths
        self._draft_url = draft_url

    def run(self) -> None:  # noqa: D401 – Qt override
        """Execute the publishing workflow (called by QThread.start)."""
        try:
            results = self._workflow.execute(
                file_paths=self._file_paths,
                draft_url=self._draft_url,
                status_cb=self.status_update.emit,
                block_cb=lambda c, t: self.block_progress.emit(c, t),
                article_cb=lambda c, t: self.article_progress.emit(c, t),
                placeholders_cb=lambda p: self.placeholders_found.emit(p),
            )
            # Summarise
            ok = sum(1 for r in results if r.success)
            fail = len(results) - ok
            if fail == 0:
                self.finished_signal.emit(True, f"All {ok} article(s) typed successfully.")
            else:
                self.finished_signal.emit(
                    False,
                    f"{ok} succeeded, {fail} failed. Check log for details.",
                )
        except EmergencyStopError:
            self.finished_signal.emit(False, "Emergency stop triggered.")
        except Exception as exc:
            logger.exception("TypingWorker unhandled error")
            self.finished_signal.emit(False, f"Error: {exc}")


class VersionUpdateWorker(QThread):
    """Runs the version update workflow in a background thread.

    Signals:
        status_update(str): Emitted with status messages.
        instruction_progress(int, int): Emitted with (current_instruction, total).
        finished_signal(bool, str): Emitted when workflow completes (success, message).
    """

    status_update = pyqtSignal(str)
    instruction_progress = pyqtSignal(int, int)
    finished_signal = pyqtSignal(bool, str)

    def __init__(
        self,
        workflow: "PublishingWorkflow",
        instructions: List[ChangeInstruction],
        article_content: str,
        draft_url: str,
        version: str,
    ) -> None:
        super().__init__()
        self._workflow = workflow
        self._instructions = instructions
        self._article_content = article_content
        self._draft_url = draft_url
        self._version = version

    def run(self) -> None:  # noqa: D401 – Qt override
        """Execute version update workflow (called by QThread.start)."""
        try:
            result = self._workflow.execute_version_update(
                instructions=self._instructions,
                article_content=self._article_content,
                draft_url=self._draft_url,
                version=self._version,
                status_cb=self.status_update.emit,
                progress_cb=lambda c, t: self.instruction_progress.emit(c, t),
            )
            summary = (
                f"Version {self._version} complete: "
                f"{result.applied_count} applied, "
                f"{result.skipped_count} skipped, "
                f"{result.failed_count} failed"
            )
            self.finished_signal.emit(result.success, summary)
        except EmergencyStopError:
            self.finished_signal.emit(False, "Emergency stop triggered.")
        except Exception as exc:
            logger.exception("VersionUpdateWorker unhandled error")
            self.finished_signal.emit(False, f"Error: {exc}")


class PublishingWorkflow:
    """Orchestrates the full article-typing pipeline.

    All heavy dependencies are injected so the class is testable with mocks.
    """

    def __init__(
        self,
        config: ConfigManager,
        emergency_stop: EmergencyStop,
        nav_state_machine: NavigationStateMachine,
        content_typer: ContentTyper,
        typo_tracker: DeferredTypoTracker,
        session_manager: SessionManager,
        version_update_typer: Optional[VersionUpdateTyper] = None,
        version_diff_detector: Optional[VersionDiffDetector] = None,
    ) -> None:
        self._config = config
        self._emergency_stop = emergency_stop
        self._nav = nav_state_machine
        self._typer = content_typer
        self._tracker = typo_tracker
        self._session = session_manager
        self._version_update_typer = version_update_typer
        self._version_diff_detector = version_diff_detector
        self._parser = ArticleParser()
        self._md = MarkdownProcessor()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def version_diff_detector(self) -> Optional[VersionDiffDetector]:
        """Access the injected VersionDiffDetector (may be None)."""
        return self._version_diff_detector

    @property
    def version_update_typer(self) -> Optional[VersionUpdateTyper]:
        """Access the injected VersionUpdateTyper (may be None)."""
        return self._version_update_typer

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def execute(
        self,
        file_paths: List[str],
        draft_url: Optional[str] = None,
        status_cb: Optional[Callable[[str], None]] = None,
        block_cb: Optional[Callable[[int, int], None]] = None,
        article_cb: Optional[Callable[[int, int], None]] = None,
        placeholders_cb: Optional[Callable[[List[str]], None]] = None,
    ) -> List[PublishingResult]:
        """Run the publishing workflow for one or more articles.

        Args:
            file_paths: Markdown file paths to publish.
            draft_url: Optional Medium draft URL (used for first article).
            status_cb: Status message callback.
            block_cb: Block progress callback (current, total).
            article_cb: Article progress callback (current, total).
            placeholders_cb: Callback with list of placeholder strings.

        Returns:
            List of PublishingResult, one per article.
        """
        results: List[PublishingResult] = []
        total = len(file_paths)

        self._session.start_session()
        self._session.set_batch_articles(file_paths)

        for idx, fpath in enumerate(file_paths):
            if article_cb:
                article_cb(idx + 1, total)
            self._session.set_current_batch_index(idx)

            result = self._publish_single(
                fpath,
                draft_url=draft_url if idx == 0 else None,
                status_cb=status_cb,
                block_cb=block_cb,
                placeholders_cb=placeholders_cb,
            )
            results.append(result)

            if not result.success:
                logger.warning("Article failed: %s — skipping", fpath)
                if status_cb:
                    status_cb(f"Skipped failed article: {Path(fpath).name}")

            # Pause between articles in batch mode
            if idx < total - 1:
                if status_cb:
                    status_cb("Pausing before next article...")
                time.sleep(2)

        self._session.clear_session()
        return results

    # ------------------------------------------------------------------
    # Version update workflow
    # ------------------------------------------------------------------

    def execute_version_update(
        self,
        instructions: List[ChangeInstruction],
        article_content: str,
        draft_url: str,
        version: str,
        status_cb: Optional[Callable[[str], None]] = None,
        progress_cb: Optional[Callable[[int, int], None]] = None,
    ) -> UpdateResult:
        """Execute the version update workflow end-to-end.

        1. Save session state (version, draft URL).
        2. Navigate to draft URL via NavigationStateMachine.
        3. Delegate to VersionUpdateTyper.apply_changes().
        4. Mark version complete in SessionManager.
        5. Return summary of applied/skipped changes.

        Args:
            instructions: Parsed change instructions.
            article_content: Full markdown content of the new version.
            draft_url: Medium draft URL to navigate to.
            version: Version identifier (e.g., "v2").
            status_cb: Status message callback.
            progress_cb: Progress callback (current_instruction, total).

        Returns:
            UpdateResult with applied/skipped/failed counts.

        Raises:
            PublishingError: If VersionUpdateTyper is not configured.
            NavigationError: If navigation to the editor fails.
            EmergencyStopError: Re-raised after saving progress.
            FocusLostError: Re-raised after pausing workflow.
        """
        if self._version_update_typer is None:
            raise PublishingError(
                "VersionUpdateTyper not configured",
                details={"hint": "Inject version_update_typer into PublishingWorkflow"},
            )

        total = len(instructions)
        logger.info(
            "execute_version_update: version=%s, instructions=%d, draft_url=%s",
            version, total, draft_url,
        )

        # 1. Save session state
        if status_cb:
            status_cb(f"Saving session state for {version}...")
        self._session.save_state({
            "current_version": version,
            "draft_url": draft_url,
            "version_update_in_progress": True,
            "last_applied_instruction_index": 0,
            "version_update_instructions_total": total,
        })

        # 2. Navigate to draft URL
        if status_cb:
            status_cb("Navigating to Medium editor...")
        if not self._nav.navigate_to_editor(draft_url=draft_url):
            self._session.save_state({"version_update_in_progress": False})
            return UpdateResult(
                success=False,
                total_instructions=total,
                failed_count=total,
                failed_sections=[("navigation", "Failed to reach Medium editor")],
            )

        # 3. Delegate to VersionUpdateTyper
        try:
            if status_cb:
                status_cb(f"Applying {total} change(s) for {version}...")
            result = self._version_update_typer.apply_changes(
                instructions=instructions,
                article_content=article_content,
                status_cb=status_cb,
            )

            # 4. Mark version complete
            self._session.mark_version_complete(version)
            self._session.save_state({"version_update_in_progress": False})

            if status_cb:
                status_cb(
                    f"Version {version} complete: "
                    f"{result.applied_count} applied, "
                    f"{result.skipped_count} skipped, "
                    f"{result.failed_count} failed"
                )

            logger.info(
                "Version update %s complete: applied=%d, skipped=%d, failed=%d",
                version, result.applied_count, result.skipped_count, result.failed_count,
            )
            return result

        except EmergencyStopError:
            logger.warning("Emergency stop during version update %s", version)
            self._version_update_typer._input.release_all_keys()
            self._session.save_state({
                "version_update_in_progress": True,
                "emergency_stopped": True,
            })
            raise

        except FocusLostError:
            logger.warning("Focus lost during version update %s", version)
            self._session.save_state({
                "version_update_in_progress": True,
                "paused": True,
            })
            if status_cb:
                status_cb("Workflow paused — target window lost focus. Please refocus the editor.")
            raise

    # ------------------------------------------------------------------
    # Single-article pipeline
    # ------------------------------------------------------------------

    def _publish_single(
        self,
        file_path: str,
        draft_url: Optional[str],
        status_cb: Optional[Callable[[str], None]],
        block_cb: Optional[Callable[[int, int], None]],
        placeholders_cb: Optional[Callable[[List[str]], None]],
    ) -> PublishingResult:
        """Publish a single article end-to-end."""
        try:
            # 1. Parse
            if status_cb:
                status_cb(f"Parsing {Path(file_path).name}...")
            article = self._parser.parse_file(file_path)
            blocks = self._md.process(article.content)
            self._session.set_article_path(file_path)
            logger.info("Parsed %d blocks from %s", len(blocks), file_path)

            # 2. Navigate to editor (skip if flag is set)
            if getattr(self, '_skip_navigation', False):
                if status_cb:
                    status_cb("Skipping navigation — assuming editor is focused...")
                logger.info("Navigation skipped — _skip_navigation is True")
            else:
                if status_cb:
                    status_cb("Navigating to Medium editor...")
                if not self._nav.navigate_to_editor(draft_url=draft_url):
                    return PublishingResult(
                        success=False,
                        message="Failed to reach Medium editor",
                        file_path=file_path,
                    )

            # 3. Type article
            if status_cb:
                status_cb("Typing article...")
            placeholders = self._type_article_with_progress(
                article.title,
                article.subtitle,
                blocks,
                block_cb,
            )

            if placeholders_cb and placeholders:
                placeholders_cb(placeholders)

            # 4. Completion
            if status_cb:
                status_cb("Article typed successfully")
            self._session.set_review_pass_completed(True)

            return PublishingResult(
                success=True,
                message="Article typed successfully",
                file_path=file_path,
                placeholders=placeholders,
            )

        except EmergencyStopError:
            logger.warning("Emergency stop during article: %s", file_path)
            self._save_progress_on_error()
            raise  # Propagate to stop the entire batch

        except (FileError, ContentError) as exc:
            logger.error("Content/file error for %s: %s", file_path, exc)
            return PublishingResult(
                success=False, message=str(exc), file_path=file_path
            )

        except NavigationError as exc:
            logger.error("Navigation error for %s: %s", file_path, exc)
            return PublishingResult(
                success=False, message=str(exc), file_path=file_path
            )

        except Exception as exc:
            logger.exception("Unexpected error for %s", file_path)
            self._emergency_stop.trigger()
            self._save_progress_on_error()
            return PublishingResult(
                success=False,
                message=f"Unexpected error: {exc}",
                file_path=file_path,
            )

    # ------------------------------------------------------------------
    # Typing helpers
    # ------------------------------------------------------------------

    def _type_article_with_progress(
        self,
        title: str,
        subtitle: str,
        blocks: List[ContentBlock],
        block_cb: Optional[Callable[[int, int], None]],
    ) -> List[str]:
        """Type article blocks and return placeholder list."""
        total = len(blocks)
        placeholders: List[str] = []

        # Title (first block or explicit)
        self._typer.type_title(title)
        if subtitle:
            self._typer.type_subtitle(subtitle)

        for idx, block in enumerate(blocks):
            if block_cb:
                block_cb(idx + 1, total)
            self._session.set_last_typed_block_index(idx)

            # Collect placeholders
            if block.type in ("table_placeholder", "image_placeholder"):
                alt = block.metadata.get("alt_text", block.metadata.get("caption", ""))
                tag = "image" if block.type == "image_placeholder" else "table"
                placeholders.append(f"[{tag}: {alt}]" if alt else f"[{tag}]")

            self._typer._type_block(block)

        # Review pass
        self._typer.perform_review_pass()

        return placeholders

    def _save_progress_on_error(self) -> None:
        """Persist current typing progress for manual recovery."""
        try:
            typos = [
                {
                    "block_index": t.block_index,
                    "char_offset": t.char_offset,
                    "wrong_char": t.wrong_char,
                    "correct_char": t.correct_char,
                    "surrounding_context": t.surrounding_context,
                }
                for t in self._tracker.get_all()
            ]
            self._session.set_deferred_typos(typos)
            logger.info("Typing progress saved for recovery")
        except Exception as exc:
            logger.error("Failed to save progress: %s", exc)

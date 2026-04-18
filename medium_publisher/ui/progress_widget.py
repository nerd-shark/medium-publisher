"""Progress widget for Medium Keyboard Publisher.

Displays per-ContentBlock progress, estimated time remaining (with typo
overhead), and batch progress (Article N of M).
"""

from datetime import datetime, timedelta
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ProgressWidget(QWidget):
    """Widget showing typing progress, time estimates, and batch status."""

    cancel_requested = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        # Tracking state
        self._start_time: Optional[datetime] = None
        self._total_blocks = 0
        self._current_block = 0
        self._total_articles = 1
        self._current_article = 0
        self._estimated_total_seconds = 0

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("Progress")
        glayout = QVBoxLayout()

        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        glayout.addWidget(self.status_label)

        # Batch progress
        self.batch_label = QLabel("")
        self.batch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        glayout.addWidget(self.batch_label)

        # Block progress
        self.block_label = QLabel("Block: - / -")
        self.block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        glayout.addWidget(self.block_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        glayout.addWidget(self.progress_bar)

        # Time row
        time_row = QHBoxLayout()
        self.elapsed_label = QLabel("Elapsed: 00:00:00")
        time_row.addWidget(self.elapsed_label)
        time_row.addStretch()
        self.remaining_label = QLabel("Remaining: --:--:--")
        time_row.addWidget(self.remaining_label)
        glayout.addLayout(time_row)

        # Cancel
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_requested.emit)
        glayout.addWidget(self.cancel_button)

        group.setLayout(glayout)
        layout.addWidget(group)
        self.setLayout(layout)

    # --- Public API -----------------------------------------------------------

    def start_publishing(
        self,
        total_articles: int = 1,
        estimated_seconds: int = 0,
    ) -> None:
        self._start_time = datetime.now()
        self._current_article = 0
        self._total_articles = total_articles
        self._estimated_total_seconds = estimated_seconds
        self._total_blocks = 0
        self._current_block = 0
        self.cancel_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.update_status("Starting...")
        self._update_batch_label()
        self._update_block_label()

    def update_status(self, status: str) -> None:
        self.status_label.setText(status)

    def update_block_progress(self, current_block: int, total_blocks: int) -> None:
        """Update per-ContentBlock progress."""
        self._current_block = current_block
        self._total_blocks = total_blocks
        self._update_block_label()
        if total_blocks > 0:
            pct = int((current_block / total_blocks) * 100)
            self.progress_bar.setValue(pct)
        self._update_time_labels()

    def update_batch_progress(self, current_article: int, total_articles: int) -> None:
        """Update batch progress (Article N of M)."""
        self._current_article = current_article
        self._total_articles = total_articles
        self._update_batch_label()

    def update_progress(self, percentage: int) -> None:
        self.progress_bar.setValue(percentage)
        self._update_time_labels()

    def update_article_count(self, current: int, total: int) -> None:
        self.update_batch_progress(current, total)

    def finish_publishing(self, success: bool = True) -> None:
        self.cancel_button.setEnabled(False)
        self.progress_bar.setValue(100)
        self.update_status("Complete" if success else "Cancelled")
        self._update_time_labels()

    def reset(self) -> None:
        self._start_time = None
        self._total_blocks = 0
        self._current_block = 0
        self._total_articles = 1
        self._current_article = 0
        self._estimated_total_seconds = 0
        self.status_label.setText("Ready")
        self.batch_label.setText("")
        self.block_label.setText("Block: - / -")
        self.progress_bar.setValue(0)
        self.elapsed_label.setText("Elapsed: 00:00:00")
        self.remaining_label.setText("Remaining: --:--:--")
        self.cancel_button.setEnabled(False)

    # --- Internal helpers -----------------------------------------------------

    def _update_batch_label(self) -> None:
        if self._total_articles > 1:
            self.batch_label.setText(
                f"Article {self._current_article} of {self._total_articles}"
            )
        else:
            self.batch_label.setText("")

    def _update_block_label(self) -> None:
        if self._total_blocks > 0:
            self.block_label.setText(
                f"Block: {self._current_block} / {self._total_blocks}"
            )
        else:
            self.block_label.setText("Block: - / -")

    def _update_time_labels(self) -> None:
        if self._start_time is None:
            self.elapsed_label.setText("Elapsed: 00:00:00")
            self.remaining_label.setText("Remaining: --:--:--")
            return

        elapsed = datetime.now() - self._start_time
        self.elapsed_label.setText(f"Elapsed: {self._fmt(elapsed)}")

        pct = self.progress_bar.value()
        if pct > 0:
            elapsed_s = elapsed.total_seconds()
            est_total = elapsed_s / (pct / 100.0)
            remaining_s = max(0, est_total - elapsed_s)
            self.remaining_label.setText(
                f"Remaining: {self._fmt(timedelta(seconds=int(remaining_s)))}"
            )
        elif self._estimated_total_seconds > 0:
            self.remaining_label.setText(
                f"Remaining: ~{self._fmt(timedelta(seconds=self._estimated_total_seconds))}"
            )
        else:
            self.remaining_label.setText("Remaining: --:--:--")

    @staticmethod
    def _fmt(td: timedelta) -> str:
        total = int(td.total_seconds())
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

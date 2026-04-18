"""
Log display widget for Medium Article Publisher UI.

Provides a QTextEdit widget that displays application logs
with color coding for different log levels.
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat
from PyQt6.QtCore import Qt, pyqtSignal


class LogDisplayWidget(QWidget):
    """
    Widget for displaying application logs in the UI.
    
    Features:
    - Color-coded log levels
    - Auto-scroll to latest log
    - Clear log button
    - Maximum line limit to prevent memory issues
    """
    
    # Signal emitted when logs are cleared
    logs_cleared = pyqtSignal()
    
    # Color scheme for log levels
    LOG_COLORS = {
        logging.DEBUG: QColor(128, 128, 128),      # Gray
        logging.INFO: QColor(0, 0, 0),             # Black
        logging.WARNING: QColor(255, 140, 0),      # Orange
        logging.ERROR: QColor(255, 0, 0),          # Red
        logging.CRITICAL: QColor(139, 0, 0)        # Dark Red
    }
    
    def __init__(self, parent=None):
        """
        Initialize log display widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.max_lines = 1000  # Instance variable for maximum lines
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Log text display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.log_text)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("Clear Logs")
        self.clear_button.clicked.connect(self.clear_logs)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def append_log(self, message: str, level: int = logging.INFO):
        """
        Append a log message to the display.
        
        Args:
            message: Log message text
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # Get color for log level
        color = self.LOG_COLORS.get(level, QColor(0, 0, 0))
        
        # Create text format with color
        text_format = QTextCharFormat()
        text_format.setForeground(color)
        
        # Move cursor to end
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Insert text with format
        cursor.insertText(message + "\n", text_format)
        
        # Auto-scroll to bottom
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    
    def clear_logs(self):
        """Clear all logs from the display."""
        self.log_text.clear()
        self.logs_cleared.emit()
    
    def get_text(self) -> str:
        """
        Get all log text.
        
        Returns:
            Complete log text
        """
        return self.log_text.toPlainText()
    
    def set_max_lines(self, max_lines: int):
        """
        Set maximum number of log lines to keep.
        
        Args:
            max_lines: Maximum number of lines
        """
        self.max_lines = max(100, max_lines)  # Minimum 100 lines


class QtLogHandler(logging.Handler):
    """
    Custom logging handler that sends logs to LogDisplayWidget.
    
    This handler integrates Python's logging system with the Qt UI,
    allowing logs to be displayed in real-time in the application.
    """
    
    def __init__(self, log_widget: LogDisplayWidget):
        """
        Initialize Qt log handler.
        
        Args:
            log_widget: LogDisplayWidget instance to send logs to
        """
        super().__init__()
        self.log_widget = log_widget
    
    def emit(self, record: logging.LogRecord):
        """
        Emit a log record to the widget.
        
        Args:
            record: Log record to emit
        """
        try:
            msg = self.format(record)
            self.log_widget.append_log(msg, record.levelno)
        except Exception:
            self.handleError(record)

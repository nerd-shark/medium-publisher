"""
Logging utility module for Medium Article Publisher.

Provides centralized logging configuration with file rotation,
multiple log levels, and UI integration support.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
from datetime import datetime


class LoggerConfig:
    """Configuration for application logging."""
    
    # Log directory (user's home directory)
    LOG_DIR = Path.home() / ".medium_publisher" / "logs"
    
    # Log file settings
    LOG_FILE = "medium_publisher.log"
    MAX_BYTES = 10 * 1024 * 1024  # 10MB per file
    BACKUP_COUNT = 5  # Keep 5 backup files
    
    # Log format
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Default log level
    DEFAULT_LEVEL = logging.INFO


class MediumPublisherLogger:
    """
    Centralized logger for Medium Article Publisher.
    
    Features:
    - File logging with rotation (10MB max, 5 backups)
    - Console logging for development
    - Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - UI integration support via custom handler
    """
    
    _instance: Optional['MediumPublisherLogger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Singleton pattern to ensure single logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logger (only once)."""
        if not self._initialized:
            self._setup_logging()
            MediumPublisherLogger._initialized = True
    
    def _setup_logging(self):
        """Set up logging configuration with file rotation and console output."""
        # Create log directory if it doesn't exist
        LoggerConfig.LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create root logger
        self.logger = logging.getLogger("medium_publisher")
        self.logger.setLevel(LoggerConfig.DEFAULT_LEVEL)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        
        # File handler with rotation
        log_file_path = LoggerConfig.LOG_DIR / LoggerConfig.LOG_FILE
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=LoggerConfig.MAX_BYTES,
            backupCount=LoggerConfig.BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            LoggerConfig.LOG_FORMAT,
            datefmt=LoggerConfig.DATE_FORMAT
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler for development
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            LoggerConfig.LOG_FORMAT,
            datefmt=LoggerConfig.DATE_FORMAT
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # UI handler placeholder (will be set by UI)
        self.ui_handler: Optional[logging.Handler] = None
        
        self.logger.info("Logging system initialized")
        self.logger.info(f"Log file: {log_file_path}")
    
    def get_logger(self, name: str = "medium_publisher") -> logging.Logger:
        """
        Get a logger instance.
        
        Args:
            name: Logger name (default: "medium_publisher")
            
        Returns:
            Logger instance
        """
        # Ensure all loggers are children of medium_publisher for proper propagation
        if name != "medium_publisher" and not name.startswith("medium_publisher."):
            name = f"medium_publisher.{name}"
        return logging.getLogger(name)
    
    def set_level(self, level: int):
        """
        Set logging level.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger.setLevel(level)
        self.logger.info(f"Log level set to {logging.getLevelName(level)}")
    
    def add_ui_handler(self, handler: logging.Handler):
        """
        Add UI handler for displaying logs in the application.
        
        Args:
            handler: Custom logging handler for UI integration
        """
        if self.ui_handler:
            self.logger.removeHandler(self.ui_handler)
        
        self.ui_handler = handler
        self.ui_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            LoggerConfig.LOG_FORMAT,
            datefmt=LoggerConfig.DATE_FORMAT
        )
        self.ui_handler.setFormatter(formatter)
        self.logger.addHandler(self.ui_handler)
        self.logger.info("UI handler added to logger")
    
    def remove_ui_handler(self):
        """Remove UI handler from logger."""
        if self.ui_handler:
            self.logger.removeHandler(self.ui_handler)
            self.ui_handler = None
            self.logger.info("UI handler removed from logger")
    
    def get_log_file_path(self) -> Path:
        """
        Get the path to the current log file.
        
        Returns:
            Path to log file
        """
        return LoggerConfig.LOG_DIR / LoggerConfig.LOG_FILE
    
    def get_log_directory(self) -> Path:
        """
        Get the log directory path.
        
        Returns:
            Path to log directory
        """
        return LoggerConfig.LOG_DIR


# Convenience functions for quick logging
def get_logger(name: str = "medium_publisher") -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    logger_instance = MediumPublisherLogger()
    return logger_instance.get_logger(name)


def setup_logging(level: int = logging.INFO):
    """
    Set up logging system.
    
    Args:
        level: Logging level (default: INFO)
    """
    logger_instance = MediumPublisherLogger()
    logger_instance.set_level(level)

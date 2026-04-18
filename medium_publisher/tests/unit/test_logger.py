"""
Unit tests for logging infrastructure.
"""

import logging
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from medium_publisher.utils.logger import (
    MediumPublisherLogger,
    LoggerConfig,
    get_logger,
    setup_logging
)


class TestLoggerConfig:
    """Tests for LoggerConfig."""
    
    def test_log_directory_path(self):
        """Test log directory is in user home."""
        assert LoggerConfig.LOG_DIR == Path.home() / ".medium_publisher" / "logs"
    
    def test_log_file_name(self):
        """Test log file name."""
        assert LoggerConfig.LOG_FILE == "medium_publisher.log"
    
    def test_max_bytes(self):
        """Test max bytes is 10MB."""
        assert LoggerConfig.MAX_BYTES == 10 * 1024 * 1024
    
    def test_backup_count(self):
        """Test backup count is 5."""
        assert LoggerConfig.BACKUP_COUNT == 5
    
    def test_default_level(self):
        """Test default log level is INFO."""
        assert LoggerConfig.DEFAULT_LEVEL == logging.INFO


class TestMediumPublisherLogger:
    """Tests for MediumPublisherLogger."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton instance before each test."""
        MediumPublisherLogger._instance = None
        MediumPublisherLogger._initialized = False
        yield
        MediumPublisherLogger._instance = None
        MediumPublisherLogger._initialized = False
    
    def test_singleton_pattern(self):
        """Test logger uses singleton pattern."""
        logger1 = MediumPublisherLogger()
        logger2 = MediumPublisherLogger()
        assert logger1 is logger2
    
    def test_initialization_creates_log_directory(self):
        """Test initialization creates log directory."""
        logger_instance = MediumPublisherLogger()
        log_dir = logger_instance.get_log_directory()
        
        # Verify log directory exists after initialization
        assert log_dir.exists()
        assert log_dir.is_dir()
    
    def test_get_logger_returns_logger(self):
        """Test get_logger returns a logger instance."""
        logger_instance = MediumPublisherLogger()
        logger = logger_instance.get_logger()
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_with_custom_name(self):
        """Test get_logger with custom name."""
        logger_instance = MediumPublisherLogger()
        logger = logger_instance.get_logger("custom_logger")
        assert logger.name == "custom_logger"
    
    def test_set_level_changes_log_level(self):
        """Test set_level changes logging level."""
        logger_instance = MediumPublisherLogger()
        logger_instance.set_level(logging.DEBUG)
        assert logger_instance.logger.level == logging.DEBUG

    
    def test_add_ui_handler(self):
        """Test adding UI handler."""
        logger_instance = MediumPublisherLogger()
        mock_handler = Mock(spec=logging.Handler)
        mock_handler.level = logging.DEBUG
        mock_handler.setLevel = Mock()
        mock_handler.setFormatter = Mock()
        
        logger_instance.add_ui_handler(mock_handler)
        
        assert logger_instance.ui_handler == mock_handler
        assert mock_handler in logger_instance.logger.handlers
    
    def test_remove_ui_handler(self):
        """Test removing UI handler."""
        logger_instance = MediumPublisherLogger()
        mock_handler = Mock(spec=logging.Handler)
        mock_handler.level = logging.DEBUG
        mock_handler.setLevel = Mock()
        mock_handler.setFormatter = Mock()
        
        logger_instance.add_ui_handler(mock_handler)
        logger_instance.remove_ui_handler()
        
        assert logger_instance.ui_handler is None
        assert mock_handler not in logger_instance.logger.handlers
    
    def test_replace_ui_handler(self):
        """Test replacing existing UI handler."""
        logger_instance = MediumPublisherLogger()
        handler1 = Mock(spec=logging.Handler)
        handler1.level = logging.DEBUG
        handler1.setLevel = Mock()
        handler1.setFormatter = Mock()
        handler2 = Mock(spec=logging.Handler)
        handler2.level = logging.DEBUG
        handler2.setLevel = Mock()
        handler2.setFormatter = Mock()
        
        logger_instance.add_ui_handler(handler1)
        logger_instance.add_ui_handler(handler2)
        
        assert logger_instance.ui_handler == handler2
        assert handler1 not in logger_instance.logger.handlers
        assert handler2 in logger_instance.logger.handlers
    
    def test_get_log_file_path(self):
        """Test get_log_file_path returns correct path."""
        logger_instance = MediumPublisherLogger()
        expected_path = LoggerConfig.LOG_DIR / LoggerConfig.LOG_FILE
        assert logger_instance.get_log_file_path() == expected_path
    
    def test_get_log_directory(self):
        """Test get_log_directory returns correct directory."""
        logger_instance = MediumPublisherLogger()
        assert logger_instance.get_log_directory() == LoggerConfig.LOG_DIR


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton instance before each test."""
        MediumPublisherLogger._instance = None
        MediumPublisherLogger._initialized = False
        yield
        MediumPublisherLogger._instance = None
        MediumPublisherLogger._initialized = False
    
    def test_get_logger_function(self):
        """Test get_logger convenience function."""
        logger = get_logger()
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_with_name(self):
        """Test get_logger with custom name."""
        logger = get_logger("test_logger")
        assert logger.name == "test_logger"
    
    def test_setup_logging_function(self):
        """Test setup_logging convenience function."""
        setup_logging(logging.DEBUG)
        logger_instance = MediumPublisherLogger()
        assert logger_instance.logger.level == logging.DEBUG


class TestLoggingIntegration:
    """Integration tests for logging system."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton instance before each test."""
        MediumPublisherLogger._instance = None
        MediumPublisherLogger._initialized = False
        yield
        MediumPublisherLogger._instance = None
        MediumPublisherLogger._initialized = False
    
    def test_log_messages_at_different_levels(self):
        """Test logging messages at different levels."""
        logger = get_logger()
        
        # Should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    
    def test_logger_with_exception(self):
        """Test logging with exception info."""
        logger = get_logger()
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("Exception occurred")

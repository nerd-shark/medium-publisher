"""
File Selector Dialog for Medium Article Publisher.

This module provides a file selection dialog that filters for markdown files,
remembers the last directory, and validates file selection.
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import QFileDialog, QWidget

from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.utils.logger import get_logger
from medium_publisher.utils.exceptions import FileError


logger = get_logger(__name__)


class FileSelector:
    """
    File selector dialog for markdown files.
    
    Features:
    - Filters for .md files
    - Remembers last directory
    - Validates file selection
    - Integrates with ConfigManager
    """
    
    def __init__(self, parent: Optional[QWidget] = None, config: Optional[ConfigManager] = None):
        """
        Initialize file selector.
        
        Args:
            parent: Parent widget for dialog
            config: Configuration manager instance
        """
        self.parent = parent
        self.config = config or ConfigManager()
        self.last_directory = self._get_last_directory()
        
        logger.info(f"FileSelector initialized - last_directory: {self.last_directory}")
    
    def _get_last_directory(self) -> Path:
        """
        Get last used directory from config.
        
        Returns:
            Path to last directory or home directory
        """
        last_dir = self.config.get("paths.last_directory", "")
        
        if last_dir and Path(last_dir).exists():
            return Path(last_dir)
        
        # Fallback to articles directory if configured
        articles_dir = self.config.get("paths.articles_directory", "")
        if articles_dir and Path(articles_dir).exists():
            return Path(articles_dir)
        
        # Final fallback to home directory
        return Path.home()
    
    def _save_last_directory(self, directory: Path) -> None:
        """
        Save last used directory to config.
        
        Args:
            directory: Directory path to save
        """
        self.config.set("paths.last_directory", str(directory))
        self.config.save_config()
        self.last_directory = directory
        
        logger.info(f"Last directory saved - directory: {directory}")
    
    def select_file(self) -> Optional[Path]:
        """
        Open file selection dialog and return selected file.
        
        Returns:
            Path to selected file or None if cancelled
            
        Raises:
            FileError: If selected file is invalid
        """
        logger.info(f"Opening file selection dialog - directory: {self.last_directory}")
        
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Select Markdown Article",
            str(self.last_directory),
            "Markdown Files (*.md);;All Files (*.*)"
        )
        
        # User cancelled
        if not file_path:
            logger.info("File selection cancelled")
            return None
        
        # Validate and return
        selected_path = Path(file_path)
        self._validate_file(selected_path)
        
        # Save directory for next time
        self._save_last_directory(selected_path.parent)
        
        logger.info(f"File selected - file_path: {selected_path}")
        return selected_path
    
    def select_multiple_files(self) -> list[Path]:
        """
        Open file selection dialog for multiple files.
        
        Returns:
            List of selected file paths (empty if cancelled)
            
        Raises:
            FileError: If any selected file is invalid
        """
        logger.info(f"Opening multi-file selection dialog - directory: {self.last_directory}")
        
        # Open file dialog with multi-selection
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.parent,
            "Select Markdown Articles (Multiple)",
            str(self.last_directory),
            "Markdown Files (*.md);;All Files (*.*)"
        )
        
        # User cancelled
        if not file_paths:
            logger.info("Multi-file selection cancelled")
            return []
        
        # Validate all files
        selected_paths = []
        for file_path in file_paths:
            path = Path(file_path)
            self._validate_file(path)
            selected_paths.append(path)
        
        # Save directory from first file
        if selected_paths:
            self._save_last_directory(selected_paths[0].parent)
        
        logger.info(f"Multiple files selected - count: {len(selected_paths)}")
        return selected_paths
    
    def _validate_file(self, file_path: Path) -> None:
        """
        Validate selected file.
        
        Args:
            file_path: Path to validate
            
        Raises:
            FileError: If file is invalid
        """
        # Check file exists
        if not file_path.exists():
            error_msg = f"File does not exist: {file_path}"
            logger.error(f"File validation failed - error: {error_msg}")
            raise FileError(error_msg)
        
        # Check is file (not directory)
        if not file_path.is_file():
            error_msg = f"Path is not a file: {file_path}"
            logger.error(f"File validation failed - error: {error_msg}")
            raise FileError(error_msg)
        
        # Check has .md extension
        if file_path.suffix.lower() != ".md":
            error_msg = f"File is not a markdown file (.md): {file_path}"
            logger.error(f"File validation failed - error: {error_msg}")
            raise FileError(error_msg)
        
        # Check file is readable
        if not file_path.stat().st_size > 0:
            error_msg = f"File is empty: {file_path}"
            logger.error(f"File validation failed - error: {error_msg}")
            raise FileError(error_msg)
        
        logger.info(f"File validation passed - file_path: {file_path}")
    
    def get_last_directory(self) -> Path:
        """
        Get the last used directory.
        
        Returns:
            Path to last directory
        """
        return self.last_directory
    
    def set_last_directory(self, directory: Path) -> None:
        """
        Set the last used directory.
        
        Args:
            directory: Directory path to set
        """
        if directory.exists() and directory.is_dir():
            self._save_last_directory(directory)
        else:
            logger.warning(f"Invalid directory - directory: {directory}")

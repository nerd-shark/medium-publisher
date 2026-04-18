"""
Tests for File Selector Dialog.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from PyQt6.QtWidgets import QWidget, QApplication

from medium_publisher.ui.file_selector import FileSelector
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.utils.exceptions import FileError


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def mock_config():
    """Create mock config manager."""
    config = Mock(spec=ConfigManager)
    config.get.return_value = ""
    return config


@pytest.fixture
def file_selector(mock_config, qapp):
    """Create file selector instance."""
    return FileSelector(config=mock_config)


@pytest.fixture
def temp_md_file(tmp_path):
    """Create temporary markdown file."""
    file_path = tmp_path / "test.md"
    file_path.write_text("# Test Article\n\nContent here.")
    return file_path


@pytest.fixture
def temp_empty_file(tmp_path):
    """Create temporary empty file."""
    file_path = tmp_path / "empty.md"
    file_path.touch()
    return file_path


class TestFileSelectorInitialization:
    """Test file selector initialization."""
    
    def test_init_with_config(self, mock_config, qapp):
        """Test initialization with config."""
        selector = FileSelector(config=mock_config)
        
        assert selector.config == mock_config
        assert selector.parent is None
        assert isinstance(selector.last_directory, Path)
    
    def test_init_with_parent(self, mock_config, qapp):
        """Test initialization with parent widget."""
        parent = QWidget()
        selector = FileSelector(parent=parent, config=mock_config)
        
        assert selector.parent == parent
    
    def test_init_without_config(self, qapp):
        """Test initialization without config creates default."""
        selector = FileSelector()
        
        assert isinstance(selector.config, ConfigManager)
    
    def test_get_last_directory_from_config(self, mock_config, tmp_path):
        """Test getting last directory from config."""
        mock_config.get.return_value = str(tmp_path)
        
        selector = FileSelector(config=mock_config)
        
        assert selector.last_directory == tmp_path
    
    def test_get_last_directory_fallback_to_articles(self, mock_config, tmp_path):
        """Test fallback to articles directory."""
        articles_dir = tmp_path / "articles"
        articles_dir.mkdir()
        
        def get_side_effect(key, default=""):
            if key == "paths.last_directory":
                return ""
            elif key == "paths.articles_directory":
                return str(articles_dir)
            return default
        
        mock_config.get.side_effect = get_side_effect
        
        selector = FileSelector(config=mock_config)
        
        assert selector.last_directory == articles_dir
    
    def test_get_last_directory_fallback_to_home(self, mock_config):
        """Test fallback to home directory."""
        mock_config.get.return_value = ""
        
        selector = FileSelector(config=mock_config)
        
        assert selector.last_directory == Path.home()


class TestFileSelection:
    """Test file selection functionality."""
    
    @patch('medium_publisher.ui.file_selector.QFileDialog.getOpenFileName')
    def test_select_file_success(self, mock_dialog, file_selector, temp_md_file):
        """Test successful file selection."""
        mock_dialog.return_value = (str(temp_md_file), "")
        
        result = file_selector.select_file()
        
        assert result == temp_md_file
        mock_dialog.assert_called_once()
    
    @patch('medium_publisher.ui.file_selector.QFileDialog.getOpenFileName')
    def test_select_file_cancelled(self, mock_dialog, file_selector):
        """Test file selection cancelled."""
        mock_dialog.return_value = ("", "")
        
        result = file_selector.select_file()
        
        assert result is None
    
    @patch('medium_publisher.ui.file_selector.QFileDialog.getOpenFileName')
    def test_select_file_saves_directory(self, mock_dialog, file_selector, temp_md_file):
        """Test file selection saves last directory."""
        mock_dialog.return_value = (str(temp_md_file), "")
        
        file_selector.select_file()
        
        file_selector.config.set.assert_called_with(
            "paths.last_directory",
            str(temp_md_file.parent)
        )
        file_selector.config.save_config.assert_called_once()
    
    @patch('medium_publisher.ui.file_selector.QFileDialog.getOpenFileName')
    def test_select_file_dialog_parameters(self, mock_dialog, file_selector, tmp_path):
        """Test file dialog called with correct parameters."""
        file_selector.last_directory = tmp_path
        mock_dialog.return_value = ("", "")
        
        file_selector.select_file()
        
        args = mock_dialog.call_args[0]
        assert args[0] == file_selector.parent
        assert args[1] == "Select Markdown Article"
        assert args[2] == str(tmp_path)
        assert "Markdown Files (*.md)" in args[3]


class TestFileValidation:
    """Test file validation."""
    
    def test_validate_file_success(self, file_selector, temp_md_file):
        """Test validation of valid file."""
        # Should not raise
        file_selector._validate_file(temp_md_file)
    
    def test_validate_file_not_exists(self, file_selector, tmp_path):
        """Test validation fails for non-existent file."""
        non_existent = tmp_path / "nonexistent.md"
        
        with pytest.raises(FileError, match="does not exist"):
            file_selector._validate_file(non_existent)
    
    def test_validate_file_is_directory(self, file_selector, tmp_path):
        """Test validation fails for directory."""
        with pytest.raises(FileError, match="not a file"):
            file_selector._validate_file(tmp_path)
    
    def test_validate_file_wrong_extension(self, file_selector, tmp_path):
        """Test validation fails for non-markdown file."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("content")
        
        with pytest.raises(FileError, match="not a markdown file"):
            file_selector._validate_file(txt_file)
    
    def test_validate_file_empty(self, file_selector, temp_empty_file):
        """Test validation fails for empty file."""
        with pytest.raises(FileError, match="empty"):
            file_selector._validate_file(temp_empty_file)
    
    def test_validate_file_case_insensitive_extension(self, file_selector, tmp_path):
        """Test validation accepts .MD extension."""
        md_file = tmp_path / "test.MD"
        md_file.write_text("# Content")
        
        # Should not raise
        file_selector._validate_file(md_file)


class TestDirectoryManagement:
    """Test directory management."""
    
    def test_get_last_directory(self, file_selector, tmp_path):
        """Test getting last directory."""
        file_selector.last_directory = tmp_path
        
        result = file_selector.get_last_directory()
        
        assert result == tmp_path
    
    def test_set_last_directory(self, file_selector, tmp_path):
        """Test setting last directory."""
        file_selector.set_last_directory(tmp_path)
        
        assert file_selector.last_directory == tmp_path
        file_selector.config.set.assert_called_with(
            "paths.last_directory",
            str(tmp_path)
        )
        file_selector.config.save_config.assert_called_once()
    
    def test_set_last_directory_invalid(self, file_selector, tmp_path):
        """Test setting invalid directory is ignored."""
        non_existent = tmp_path / "nonexistent"
        original_dir = file_selector.last_directory
        
        file_selector.set_last_directory(non_existent)
        
        # Should not change
        assert file_selector.last_directory == original_dir
        file_selector.config.set.assert_not_called()
    
    def test_save_last_directory(self, file_selector, tmp_path):
        """Test saving last directory."""
        file_selector._save_last_directory(tmp_path)
        
        assert file_selector.last_directory == tmp_path
        file_selector.config.set.assert_called_with(
            "paths.last_directory",
            str(tmp_path)
        )
        file_selector.config.save_config.assert_called_once()


class TestIntegration:
    """Test integration scenarios."""
    
    @patch('medium_publisher.ui.file_selector.QFileDialog.getOpenFileName')
    def test_full_selection_workflow(self, mock_dialog, mock_config, temp_md_file):
        """Test complete file selection workflow."""
        # Setup
        mock_config.get.return_value = str(temp_md_file.parent)
        selector = FileSelector(config=mock_config)
        mock_dialog.return_value = (str(temp_md_file), "")
        
        # Select file
        result = selector.select_file()
        
        # Verify
        assert result == temp_md_file
        assert selector.last_directory == temp_md_file.parent
        mock_config.set.assert_called()
        mock_config.save_config.assert_called()
    
    @patch('medium_publisher.ui.file_selector.QFileDialog.getOpenFileName')
    def test_selection_with_validation_error(self, mock_dialog, file_selector, tmp_path):
        """Test selection with validation error."""
        # Select non-existent file
        non_existent = tmp_path / "nonexistent.md"
        mock_dialog.return_value = (str(non_existent), "")
        
        with pytest.raises(FileError):
            file_selector.select_file()
    
    def test_multiple_selections(self, mock_config, tmp_path):
        """Test multiple file selections update directory."""
        # Create files in different directories
        dir1 = tmp_path / "dir1"
        dir1.mkdir()
        file1 = dir1 / "test1.md"
        file1.write_text("# Test 1")
        
        dir2 = tmp_path / "dir2"
        dir2.mkdir()
        file2 = dir2 / "test2.md"
        file2.write_text("# Test 2")
        
        selector = FileSelector(config=mock_config)
        
        # First selection
        with patch('medium_publisher.ui.file_selector.QFileDialog.getOpenFileName') as mock_dialog:
            mock_dialog.return_value = (str(file1), "")
            selector.select_file()
            assert selector.last_directory == dir1
        
        # Second selection
        with patch('medium_publisher.ui.file_selector.QFileDialog.getOpenFileName') as mock_dialog:
            mock_dialog.return_value = (str(file2), "")
            selector.select_file()
            assert selector.last_directory == dir2

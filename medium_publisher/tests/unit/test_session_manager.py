"""Tests for SessionManager class."""

import pytest
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

from medium_publisher.core.session_manager import SessionManager
from medium_publisher.utils.exceptions import FileError


@pytest.fixture
def temp_session_dir(tmp_path):
    """Create temporary session directory."""
    session_dir = tmp_path / "test_session"
    return session_dir


@pytest.fixture
def session_manager(temp_session_dir):
    """Create SessionManager with temporary directory."""
    return SessionManager(session_dir=temp_session_dir)


class TestSessionManagerInitialization:
    """Test SessionManager initialization."""
    
    def test_init_creates_session_dir(self, temp_session_dir):
        """Test initialization creates session directory."""
        manager = SessionManager(session_dir=temp_session_dir)
        assert temp_session_dir.exists()
        assert manager.session_dir == temp_session_dir
        assert manager.session_file == temp_session_dir / "session_state.json"
    
    def test_init_default_session_dir(self):
        """Test initialization with default session directory."""
        manager = SessionManager()
        expected_dir = Path.home() / ".medium_publisher"
        assert manager.session_dir == expected_dir
    
    def test_init_creates_nested_dirs(self, tmp_path):
        """Test initialization creates nested directories."""
        nested_dir = tmp_path / "level1" / "level2" / "session"
        manager = SessionManager(session_dir=nested_dir)
        assert nested_dir.exists()
    
    def test_init_handles_existing_dir(self, temp_session_dir):
        """Test initialization with existing directory."""
        temp_session_dir.mkdir(parents=True)
        manager = SessionManager(session_dir=temp_session_dir)
        assert temp_session_dir.exists()


class TestStartSession:
    """Test start_session method."""
    
    def test_start_session_creates_state(self, session_manager):
        """Test start_session creates initial state."""
        session_manager.start_session()
        
        state = session_manager.get_current_state()
        assert "session_id" in state
        assert "started_at" in state
        assert state["current_version"] is None
        assert state["article_path"] is None
        assert state["draft_url"] is None
        assert state["versions_completed"] == []
        assert state["last_operation"] is None
    
    def test_start_session_creates_file(self, session_manager):
        """Test start_session creates session file."""
        session_manager.start_session()
        assert session_manager.session_file.exists()
    
    def test_start_session_has_timestamp(self, session_manager):
        """Test start_session includes valid timestamp."""
        session_manager.start_session()
        
        state = session_manager.get_current_state()
        # Verify ISO format timestamp
        datetime.fromisoformat(state["session_id"])
        datetime.fromisoformat(state["started_at"])
    
    def test_start_session_clears_previous(self, session_manager):
        """Test start_session clears previous state."""
        # Create initial session
        session_manager.start_session()
        session_manager.update_version("v1")
        
        # Start new session
        session_manager.start_session()
        
        state = session_manager.get_current_state()
        assert state["current_version"] is None


class TestSaveState:
    """Test save_state method."""
    
    def test_save_state_updates_memory(self, session_manager):
        """Test save_state updates in-memory state."""
        session_manager.start_session()
        session_manager.save_state({"current_version": "v1"})
        
        state = session_manager.get_current_state()
        assert state["current_version"] == "v1"
    
    def test_save_state_writes_file(self, session_manager):
        """Test save_state writes to file."""
        session_manager.start_session()
        session_manager.save_state({"current_version": "v2"})
        
        # Read file directly
        with open(session_manager.session_file, 'r') as f:
            data = json.load(f)
        
        assert data["current_version"] == "v2"
    
    def test_save_state_adds_timestamp(self, session_manager):
        """Test save_state adds last_updated timestamp."""
        session_manager.start_session()
        session_manager.save_state({"test": "value"})
        
        state = session_manager.get_current_state()
        assert "last_updated" in state
        datetime.fromisoformat(state["last_updated"])
    
    def test_save_state_atomic_write(self, session_manager, temp_session_dir):
        """Test save_state uses atomic write."""
        session_manager.start_session()
        
        # Save state
        session_manager.save_state({"current_version": "v1"})
        
        # Verify temp file doesn't exist
        temp_file = temp_session_dir / "session_state.tmp"
        assert not temp_file.exists()
        
        # Verify final file exists
        assert session_manager.session_file.exists()
    
    def test_save_state_handles_error(self, session_manager):
        """Test save_state handles write errors."""
        session_manager.start_session()
        
        # Mock open to raise exception
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            with pytest.raises(FileError):
                session_manager.save_state({"test": "value"})


class TestRestoreState:
    """Test restore_state method."""
    
    def test_restore_state_loads_file(self, session_manager):
        """Test restore_state loads from file."""
        # Create and save session
        session_manager.start_session()
        session_manager.save_state({"current_version": "v3"})
        
        # Create new manager and restore
        new_manager = SessionManager(session_dir=session_manager.session_dir)
        state = new_manager.restore_state()
        
        assert state["current_version"] == "v3"
    
    def test_restore_state_no_file(self, session_manager):
        """Test restore_state with no session file."""
        state = session_manager.restore_state()
        assert state == {}
    
    def test_restore_state_invalid_json(self, session_manager):
        """Test restore_state with invalid JSON."""
        # Create invalid JSON file
        session_manager.session_file.parent.mkdir(parents=True, exist_ok=True)
        with open(session_manager.session_file, 'w') as f:
            f.write("invalid json {")
        
        with pytest.raises(FileError):
            session_manager.restore_state()
    
    def test_restore_state_updates_memory(self, session_manager):
        """Test restore_state updates in-memory state."""
        # Create and save session
        session_manager.start_session()
        session_manager.save_state({"current_version": "v2"})
        
        # Create new manager and restore
        new_manager = SessionManager(session_dir=session_manager.session_dir)
        new_manager.restore_state()
        
        state = new_manager.get_current_state()
        assert state["current_version"] == "v2"


class TestClearSession:
    """Test clear_session method."""
    
    def test_clear_session_removes_file(self, session_manager):
        """Test clear_session removes session file."""
        session_manager.start_session()
        assert session_manager.session_file.exists()
        
        session_manager.clear_session()
        assert not session_manager.session_file.exists()
    
    def test_clear_session_clears_memory(self, session_manager):
        """Test clear_session clears in-memory state."""
        session_manager.start_session()
        session_manager.save_state({"current_version": "v1"})
        
        session_manager.clear_session()
        
        state = session_manager.get_current_state()
        assert state == {}
    
    def test_clear_session_no_file(self, session_manager):
        """Test clear_session when no file exists."""
        # Should not raise error
        session_manager.clear_session()
        assert not session_manager.session_file.exists()


class TestVersionManagement:
    """Test version-related methods."""
    
    def test_update_version(self, session_manager):
        """Test update_version updates current version."""
        session_manager.start_session()
        session_manager.update_version("v2")
        
        state = session_manager.get_current_state()
        assert state["current_version"] == "v2"
    
    def test_mark_version_complete(self, session_manager):
        """Test mark_version_complete adds to list."""
        session_manager.start_session()
        session_manager.mark_version_complete("v1")
        
        state = session_manager.get_current_state()
        assert "v1" in state["versions_completed"]
    
    def test_mark_version_complete_no_duplicates(self, session_manager):
        """Test mark_version_complete doesn't add duplicates."""
        session_manager.start_session()
        session_manager.mark_version_complete("v1")
        session_manager.mark_version_complete("v1")
        
        state = session_manager.get_current_state()
        assert state["versions_completed"].count("v1") == 1
    
    def test_mark_multiple_versions_complete(self, session_manager):
        """Test marking multiple versions complete."""
        session_manager.start_session()
        session_manager.mark_version_complete("v1")
        session_manager.mark_version_complete("v2")
        session_manager.mark_version_complete("v3")
        
        state = session_manager.get_current_state()
        assert state["versions_completed"] == ["v1", "v2", "v3"]


class TestProgressTracking:
    """Test progress tracking methods."""
    
    def test_update_progress(self, session_manager):
        """Test update_progress updates progress dict."""
        session_manager.start_session()
        session_manager.update_progress(2, 5, "typing content")
        
        state = session_manager.get_current_state()
        assert state["progress"]["current_article"] == 2
        assert state["progress"]["total_articles"] == 5
        assert state["progress"]["current_step"] == "typing content"
    
    def test_update_progress_no_step(self, session_manager):
        """Test update_progress without step description."""
        session_manager.start_session()
        session_manager.update_progress(1, 3)
        
        state = session_manager.get_current_state()
        assert state["progress"]["current_article"] == 1
        assert state["progress"]["total_articles"] == 3
        assert state["progress"]["current_step"] is None


class TestArticleMetadata:
    """Test article metadata methods."""
    
    def test_set_article_path(self, session_manager):
        """Test set_article_path updates path."""
        session_manager.start_session()
        session_manager.set_article_path("/path/to/article.md")
        
        state = session_manager.get_current_state()
        assert state["article_path"] == "/path/to/article.md"
    
    def test_set_draft_url(self, session_manager):
        """Test set_draft_url updates URL."""
        session_manager.start_session()
        session_manager.set_draft_url("https://medium.com/draft/123")
        
        state = session_manager.get_current_state()
        assert state["draft_url"] == "https://medium.com/draft/123"
    
    def test_set_draft_url_none(self, session_manager):
        """Test set_draft_url with None."""
        session_manager.start_session()
        session_manager.set_draft_url(None)
        
        state = session_manager.get_current_state()
        assert state["draft_url"] is None
    
    def test_set_last_operation(self, session_manager):
        """Test set_last_operation updates operation."""
        session_manager.start_session()
        session_manager.set_last_operation("typing title")
        
        state = session_manager.get_current_state()
        assert state["last_operation"] == "typing title"


class TestGetCurrentState:
    """Test get_current_state method."""
    
    def test_get_current_state_returns_copy(self, session_manager):
        """Test get_current_state returns copy, not reference."""
        session_manager.start_session()
        
        state1 = session_manager.get_current_state()
        state1["test"] = "modified"
        
        state2 = session_manager.get_current_state()
        assert "test" not in state2


class TestIntegration:
    """Test integration scenarios."""
    
    def test_full_session_lifecycle(self, session_manager):
        """Test complete session lifecycle."""
        # Start session
        session_manager.start_session()
        
        # Update various fields
        session_manager.set_article_path("/path/to/article.md")
        session_manager.set_draft_url("https://medium.com/draft/123")
        session_manager.update_version("v1")
        session_manager.update_progress(1, 3, "typing content")
        session_manager.set_last_operation("typing")
        
        # Mark version complete
        session_manager.mark_version_complete("v1")
        
        # Verify state
        state = session_manager.get_current_state()
        assert state["article_path"] == "/path/to/article.md"
        assert state["draft_url"] == "https://medium.com/draft/123"
        assert state["current_version"] == "v1"
        assert state["versions_completed"] == ["v1"]
        assert state["progress"]["current_article"] == 1
        assert state["last_operation"] == "typing"
        
        # Clear session
        session_manager.clear_session()
        assert not session_manager.session_file.exists()
    
    def test_session_persistence_across_restarts(self, session_manager):
        """Test session persists across application restarts."""
        # Create session
        session_manager.start_session()
        session_manager.set_article_path("/path/to/article.md")
        session_manager.update_version("v2")
        session_manager.mark_version_complete("v1")
        session_manager.update_progress(2, 5, "typing")
        
        # Simulate restart - create new manager
        new_manager = SessionManager(session_dir=session_manager.session_dir)
        restored_state = new_manager.restore_state()
        
        # Verify all data restored
        assert restored_state["article_path"] == "/path/to/article.md"
        assert restored_state["current_version"] == "v2"
        assert restored_state["versions_completed"] == ["v1"]
        assert restored_state["progress"]["current_article"] == 2
        assert restored_state["progress"]["total_articles"] == 5
    
    def test_iterative_version_workflow(self, session_manager):
        """Test iterative version update workflow."""
        session_manager.start_session()
        session_manager.set_article_path("/article.md")
        
        # Version 1
        session_manager.update_version("v1")
        session_manager.set_last_operation("typing v1 content")
        session_manager.mark_version_complete("v1")
        
        # Version 2
        session_manager.update_version("v2")
        session_manager.set_last_operation("updating sections for v2")
        session_manager.mark_version_complete("v2")
        
        # Version 3
        session_manager.update_version("v3")
        session_manager.set_last_operation("final edits for v3")
        session_manager.mark_version_complete("v3")
        
        # Verify progression
        state = session_manager.get_current_state()
        assert state["current_version"] == "v3"
        assert state["versions_completed"] == ["v1", "v2", "v3"]

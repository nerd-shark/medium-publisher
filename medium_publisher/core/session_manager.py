"""Session state management for Medium Article Publisher.

This module provides session state persistence across application restarts,
supporting iterative version updates, error recovery, typing progress tracking,
and deferred typo state serialization.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from medium_publisher.utils.logger import get_logger
from medium_publisher.utils.exceptions import FileError


class SessionManager:
    """Manages publishing session state with persistence.
    
    Handles session lifecycle, state persistence, and restoration across
    application restarts. Supports iterative version updates by maintaining
    current version context.
    
    Attributes:
        session_file: Path to session state JSON file
        logger: Logger instance for session operations
        _current_state: In-memory session state dictionary
    """
    
    def __init__(self, session_dir: Optional[Path] = None):
        """Initialize SessionManager with session directory.
        
        Args:
            session_dir: Directory for session files. Defaults to
                ~/.medium_publisher/ if not provided.
        """
        self.logger = get_logger(__name__)
        
        # Default session directory
        if session_dir is None:
            session_dir = Path.home() / ".medium_publisher"
        
        self.session_dir = Path(session_dir)
        self.session_file = self.session_dir / "session_state.json"
        self._current_state: Dict[str, Any] = {}
        
        # Create session directory if it doesn't exist
        self._ensure_session_dir()
    
    def _ensure_session_dir(self) -> None:
        """Ensure session directory exists."""
        try:
            self.session_dir.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Session directory ready: {self.session_dir}")
        except Exception as e:
            self.logger.error(f"Failed to create session directory: {e}")
            raise FileError(f"Cannot create session directory: {e}")
    
    def start_session(self) -> None:
        """Initialize new publishing session.
        
        Creates a new session with timestamp and empty state. Clears any
        existing session state.
        
        Raises:
            FileError: If session initialization fails
        """
        self.logger.info("Starting new publishing session")
        
        self._current_state = {
            "session_id": datetime.now().isoformat(),
            "started_at": datetime.now().isoformat(),
            "current_version": None,
            "article_path": None,
            "draft_url": None,
            "versions_completed": [],
            "last_operation": None,
            "progress": {
                "current_article": 0,
                "total_articles": 0,
                "current_step": None
            },
            "last_typed_block_index": 0,
            "deferred_typos": [],
            "review_pass_completed": False,
            "batch_articles": [],
            "current_batch_index": 0,
        }
        
        # Save initial state
        self.save_state(self._current_state)
        self.logger.info(f"Session started: {self._current_state['session_id']}")
    
    def save_state(self, state: Dict[str, Any]) -> None:
        """Save current session state to disk.
        
        Persists session state as JSON file for recovery across restarts.
        Updates in-memory state and writes to session file atomically.
        
        Args:
            state: Session state dictionary to save
            
        Raises:
            FileError: If state cannot be saved
        """
        try:
            # Update in-memory state
            self._current_state.update(state)
            
            # Add timestamp
            self._current_state["last_updated"] = datetime.now().isoformat()
            
            # Write to file atomically (write to temp, then rename)
            temp_file = self.session_file.with_suffix(".tmp")
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self._current_state, f, indent=2)
            
            # Atomic rename
            temp_file.replace(self.session_file)
            
            self.logger.debug(f"Session state saved: {len(self._current_state)} keys")
            
        except Exception as e:
            self.logger.error(f"Failed to save session state: {e}")
            raise FileError(f"Cannot save session state: {e}")
    
    def restore_state(self) -> Dict[str, Any]:
        """Restore previous session state from disk.
        
        Loads session state from JSON file if it exists. Returns empty
        dictionary if no session file found.
        
        Returns:
            Dictionary containing restored session state, or empty dict
            if no session exists
            
        Raises:
            FileError: If session file exists but cannot be read
        """
        if not self.session_file.exists():
            self.logger.info("No previous session found")
            return {}
        
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                self._current_state = json.load(f)
            
            self.logger.info(
                f"Session restored: {self._current_state.get('session_id', 'unknown')}"
            )
            self.logger.debug(f"Restored state: {len(self._current_state)} keys")
            
            return self._current_state.copy()
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid session file format: {e}")
            raise FileError(f"Cannot parse session file: {e}")
        except Exception as e:
            self.logger.error(f"Failed to restore session state: {e}")
            raise FileError(f"Cannot restore session state: {e}")
    
    def clear_session(self) -> None:
        """Clear session data from memory and disk.
        
        Removes session file and clears in-memory state. Used when
        publishing completes or user explicitly clears session.
        """
        self.logger.info("Clearing session data")
        
        # Clear in-memory state
        self._current_state = {}
        
        # Remove session file if it exists
        if self.session_file.exists():
            try:
                self.session_file.unlink()
                self.logger.debug("Session file deleted")
            except Exception as e:
                self.logger.warning(f"Failed to delete session file: {e}")
        
        self.logger.info("Session cleared")
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current in-memory session state.
        
        Returns:
            Copy of current session state dictionary
        """
        return self._current_state.copy()
    
    def update_version(self, version: str) -> None:
        """Update current version in session state.
        
        Args:
            version: Version identifier (e.g., "v1", "v2")
        """
        self.save_state({"current_version": version})
        self.logger.info(f"Version updated: {version}")
    
    def mark_version_complete(self, version: str) -> None:
        """Mark a version as completed.
        
        Args:
            version: Version identifier that was completed
        """
        versions = self._current_state.get("versions_completed", [])
        if version not in versions:
            versions.append(version)
            self.save_state({"versions_completed": versions})
            self.logger.info(f"Version marked complete: {version}")
    
    def update_progress(self, current: int, total: int, step: Optional[str] = None) -> None:
        """Update publishing progress.
        
        Args:
            current: Current article number
            total: Total number of articles
            step: Optional description of current step
        """
        progress = {
            "current_article": current,
            "total_articles": total,
            "current_step": step
        }
        self.save_state({"progress": progress})
        self.logger.debug(f"Progress updated: {current}/{total}")
    
    def set_article_path(self, path: str) -> None:
        """Set current article file path.
        
        Args:
            path: Path to markdown article file
        """
        self.save_state({"article_path": path})
        self.logger.debug(f"Article path set: {path}")
    
    def set_draft_url(self, url: Optional[str]) -> None:
        """Set Medium draft URL.
        
        Args:
            url: Medium draft URL or None
        """
        self.save_state({"draft_url": url})
        self.logger.debug(f"Draft URL set: {url}")
    
    def set_last_operation(self, operation: str) -> None:
        """Set last operation performed.
        
        Args:
            operation: Description of last operation
        """
        self.save_state({"last_operation": operation})
        self.logger.debug(f"Last operation: {operation}")

    def set_last_typed_block_index(self, index: int) -> None:
        """Set the index of the last successfully typed ContentBlock.
        
        Args:
            index: Block index for recovery after errors.
        """
        self.save_state({"last_typed_block_index": index})
        self.logger.debug(f"Last typed block index: {index}")

    def set_deferred_typos(self, typos: List[Dict[str, Any]]) -> None:
        """Set the list of deferred typos for session persistence.
        
        Each typo dict should have: block_index, char_offset, wrong_char,
        correct_char, surrounding_context.
        
        Args:
            typos: List of DeferredTypo dicts to serialize.
        """
        self.save_state({"deferred_typos": typos})
        self.logger.debug(f"Deferred typos saved: {len(typos)} typos")

    def get_deferred_typos(self) -> List[Dict[str, Any]]:
        """Get the list of deferred typos from session state.
        
        Returns:
            List of DeferredTypo dicts, or empty list if none.
        """
        return self._current_state.get("deferred_typos", [])

    def set_review_pass_completed(self, completed: bool) -> None:
        """Set whether the review pass has been completed.
        
        Args:
            completed: True if review pass finished.
        """
        self.save_state({"review_pass_completed": completed})
        self.logger.debug(f"Review pass completed: {completed}")

    def set_batch_articles(self, file_paths: List[str]) -> None:
        """Set the list of article file paths for batch publishing.
        
        Args:
            file_paths: List of markdown file paths.
        """
        self.save_state({"batch_articles": file_paths})
        self.logger.debug(f"Batch articles set: {len(file_paths)} files")

    def set_current_batch_index(self, index: int) -> None:
        """Set the current article index in batch publishing.
        
        Args:
            index: Current article index (0-based).
        """
        self.save_state({"current_batch_index": index})
        self.logger.debug(f"Current batch index: {index}")

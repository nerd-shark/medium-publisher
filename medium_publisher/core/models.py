"""
Data models for Medium Article Publisher.

This module defines the core data structures for representing articles,
content blocks, and formatting information.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path


@dataclass
class Format:
    """
    Represents inline formatting for text content.
    
    Attributes:
        type: Format type (bold, italic, code, link)
        start: Starting character index
        end: Ending character index
        url: URL for link format (optional)
    """
    type: str  # bold, italic, code, link
    start: int
    end: int
    url: str = ""
    
    def validate(self) -> bool:
        """
        Validate format data.
        
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValueError: If validation fails
        """
        # Validate type
        valid_types = ["bold", "italic", "code", "link"]
        if self.type not in valid_types:
            raise ValueError(
                f"Invalid format type '{self.type}'. "
                f"Must be one of: {', '.join(valid_types)}"
            )
        
        # Validate indices
        if self.start < 0:
            raise ValueError(f"Format start index must be >= 0, got {self.start}")
        
        if self.end <= self.start:
            raise ValueError(
                f"Format end index ({self.end}) must be > start index ({self.start})"
            )
        
        # Validate URL for link type
        if self.type == "link" and not self.url:
            raise ValueError("Format type 'link' requires a URL")
        
        return True


@dataclass
class ContentBlock:
    """
    Represents a block of content in an article.
    
    Attributes:
        type: Block type (paragraph, header, code, list, table_placeholder, image_placeholder)
        content: Text content of the block
        formatting: List of Format objects for inline formatting
        level: Header level (2, 3, 4) for header blocks
        metadata: Additional metadata (image alt text, table info, etc.)
    """
    type: str
    content: str
    formatting: List[Format] = field(default_factory=list)
    level: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> bool:
        """
        Validate content block data.
        
        Returns:
            True if valid, False otherwise
            
        raises:
            ValueError: If validation fails
        """
        # Validate type
        valid_types = [
            "paragraph",
            "header",
            "code",
            "list",
            "table_placeholder",
            "image_placeholder"
        ]
        if self.type not in valid_types:
            raise ValueError(
                f"Invalid block type '{self.type}'. "
                f"Must be one of: {', '.join(valid_types)}"
            )
        
        # Validate content
        if not self.content:
            raise ValueError("ContentBlock content cannot be empty")
        
        # Validate header level
        if self.type == "header":
            if self.level not in [2, 3, 4]:
                raise ValueError(
                    f"Header level must be 2, 3, or 4, got {self.level}"
                )
        
        # Validate formatting
        for fmt in self.formatting:
            fmt.validate()
            # Ensure format indices are within content bounds
            if fmt.end > len(self.content):
                raise ValueError(
                    f"Format end index ({fmt.end}) exceeds content length "
                    f"({len(self.content)})"
                )
        
        # Validate image placeholder has alt text
        if self.type == "image_placeholder":
            if "alt_text" not in self.metadata:
                raise ValueError(
                    "Image placeholder requires 'alt_text' in metadata"
                )
        
        return True


@dataclass
class Article:
    """
    Represents a complete article with metadata and content.
    
    Attributes:
        title: Article title
        subtitle: Article subtitle (optional)
        content: Raw markdown content
        tags: List of article tags (max 5)
        keywords: List of SEO keywords
        status: Publication status (draft or public)
        file_path: Path to source markdown file
    """
    title: str
    subtitle: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    status: str = "draft"
    file_path: str = ""
    
    def validate(self) -> bool:
        """
        Validate article data.
        
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValueError: If validation fails
        """
        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Article title cannot be empty")
        
        if len(self.title) > 200:
            raise ValueError(
                f"Article title too long ({len(self.title)} chars). "
                "Maximum 200 characters"
            )
        
        # Validate status
        valid_statuses = ["draft", "public"]
        # Also accept version-prefixed statuses like "v1-draft", "v2-public"
        normalized_status = self.status
        if normalized_status and "-" in normalized_status:
            # Strip version prefix (e.g., "v1-draft" → "draft")
            parts = normalized_status.split("-", 1)
            if parts[0].startswith("v") and parts[0][1:].isdigit():
                normalized_status = parts[1]
        if normalized_status not in valid_statuses:
            raise ValueError(
                f"Invalid status '{self.status}'. "
                f"Must be one of: {', '.join(valid_statuses)} "
                f"(optionally prefixed with version, e.g., 'v1-draft')"
            )
        
        # Validate tags
        if len(self.tags) > 5:
            raise ValueError(
                f"Too many tags ({len(self.tags)}). Maximum 5 tags allowed"
            )
        
        # Validate tag format (alphanumeric, hyphens, spaces only)
        import re
        tag_pattern = re.compile(r'^[a-zA-Z0-9\s\-]+$')
        for tag in self.tags:
            if not tag_pattern.match(tag):
                raise ValueError(
                    f"Invalid tag '{tag}'. "
                    "Tags must contain only alphanumeric characters, hyphens, and spaces"
                )
        
        # Validate file path if provided
        if self.file_path:
            path = Path(self.file_path)
            if not path.suffix == ".md":
                raise ValueError(
                    f"Invalid file extension '{path.suffix}'. "
                    "Must be .md (markdown)"
                )
        
        return True
    
    def has_required_fields(self) -> bool:
        """
        Check if article has all required fields.
        
        Returns:
            True if all required fields are present
        """
        return bool(self.title and self.content)


@dataclass
class DeferredTypo:
    """A typo left uncorrected during typing, to be fixed in review pass.

    Attributes:
        block_index: Which ContentBlock the typo is in.
        char_offset: Character offset within the block's typed text.
        wrong_char: The incorrect character that was typed.
        correct_char: The character that should have been typed.
        surrounding_context: ~20 chars of surrounding text for Ctrl+F search.
    """
    block_index: int
    char_offset: int
    wrong_char: str
    correct_char: str
    surrounding_context: str


@dataclass
class TypingProgress:
    """Tracks typing progress for UI display and recovery.

    Attributes:
        total_blocks: Total number of ContentBlocks in the article.
        current_block: Index of the block currently being typed.
        total_chars: Total character count across all blocks.
        typed_chars: Number of characters typed so far.
        deferred_typo_count: Number of deferred typos pending correction.
        review_pass_started: Whether the review pass has begun.
        review_pass_completed: Whether the review pass has finished.
        estimated_remaining_seconds: Estimated seconds remaining.
    """
    total_blocks: int
    current_block: int
    total_chars: int
    typed_chars: int
    deferred_typo_count: int
    review_pass_started: bool = False
    review_pass_completed: bool = False
    estimated_remaining_seconds: float = 0.0


class NavigationState(Enum):
    """States in the Medium navigation flow."""
    START = "start"
    LOGGED_OUT_HOME = "logged_out_home"
    SIGN_IN_SCREEN = "sign_in_screen"
    GOOGLE_SIGN_IN = "google_sign_in"
    WAITING_2FA = "waiting_2fa"
    LOGGED_IN_HOME = "logged_in_home"
    DRAFTS_PAGE = "drafts_page"
    NEW_STORY_EDITOR = "new_story_editor"
    ERROR = "error"
    READY = "ready"


@dataclass
class UpdateResult:
    """Result of a version update workflow execution.

    Attributes:
        success: True if at least one instruction was applied.
        total_instructions: Total number of instructions processed.
        applied_count: Number of instructions successfully applied.
        skipped_count: Number of instructions skipped (section not found).
        failed_count: Number of instructions that failed during execution.
        applied_sections: List of section names that were updated.
        skipped_sections: List of section names that were skipped with reasons.
        failed_sections: List of section names that failed with error details.
    """
    success: bool
    total_instructions: int
    applied_count: int = 0
    skipped_count: int = 0
    failed_count: int = 0
    applied_sections: List[str] = field(default_factory=list)
    skipped_sections: List[Tuple[str, str]] = field(default_factory=list)  # (section, reason)
    failed_sections: List[Tuple[str, str]] = field(default_factory=list)   # (section, error)


@dataclass
class VersionFileInfo:
    """Metadata about a discovered version file.

    Attributes:
        path: Full path to the version file.
        version_number: Extracted version number (1, 2, 3, ...).
        article_name: Article name portion of the filename.
        filename: Just the filename (e.g., "v2-my-article.md").
    """
    path: Path
    version_number: int
    article_name: str
    filename: str

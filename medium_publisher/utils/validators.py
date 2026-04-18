"""
Input validation utilities for Medium Article Publisher.

This module provides validation functions for all user inputs,
ensuring data integrity and providing user-friendly error messages.
"""

import re
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from .exceptions import FileError, ContentError


class ValidationResult:
    """
    Result of a validation operation.
    
    Attributes:
        is_valid: Whether the validation passed
        error_message: User-friendly error message if validation failed
        details: Optional dictionary with additional error context
    """
    
    def __init__(self, is_valid: bool, error_message: str = "", details: dict = None):
        """
        Initialize ValidationResult.
        
        Args:
            is_valid: Whether the validation passed
            error_message: User-friendly error message if validation failed
            details: Optional dictionary with additional error context
        """
        self.is_valid = is_valid
        self.error_message = error_message
        self.details = details or {}
    
    def __bool__(self) -> bool:
        """Allow using ValidationResult in boolean context."""
        return self.is_valid
    
    def __str__(self) -> str:
        """Return string representation."""
        if self.is_valid:
            return "Validation passed"
        return self.error_message


def validate_file_path(file_path: str) -> ValidationResult:
    """
    Validate a file path for markdown article.
    
    Checks:
    - Path is not empty
    - File exists
    - Path points to a file (not directory)
    - File has .md extension
    - File is not empty (size > 0)
    - File is readable
    
    Args:
        file_path: Path to validate
        
    Returns:
        ValidationResult with is_valid and error_message
        
    Examples:
        >>> result = validate_file_path("article.md")
        >>> if not result:
        ...     print(result.error_message)
    """
    # Check if path is empty
    if not file_path or not file_path.strip():
        return ValidationResult(
            False,
            "File path cannot be empty",
            {"path": file_path}
        )
    
    try:
        path = Path(file_path)
    except Exception as e:
        return ValidationResult(
            False,
            f"Invalid file path: {str(e)}",
            {"path": file_path, "error": str(e)}
        )
    
    # Check if file exists
    if not path.exists():
        return ValidationResult(
            False,
            f"File not found: {file_path}",
            {"path": str(path)}
        )
    
    # Check if path is a file (not directory)
    if not path.is_file():
        return ValidationResult(
            False,
            f"Path is not a file: {file_path}",
            {"path": str(path)}
        )
    
    # Check file extension (case-insensitive)
    if path.suffix.lower() != '.md':
        return ValidationResult(
            False,
            f"File must have .md extension, got: {path.suffix}",
            {"path": str(path), "extension": path.suffix}
        )
    
    # Check if file is not empty
    if path.stat().st_size == 0:
        return ValidationResult(
            False,
            f"File is empty: {file_path}",
            {"path": str(path), "size": 0}
        )
    
    # Check if file is readable
    try:
        with open(path, 'r', encoding='utf-8') as f:
            f.read(1)  # Try to read first character
    except PermissionError:
        return ValidationResult(
            False,
            f"Permission denied reading file: {file_path}",
            {"path": str(path)}
        )
    except UnicodeDecodeError:
        return ValidationResult(
            False,
            f"File is not valid UTF-8 text: {file_path}",
            {"path": str(path)}
        )
    except Exception as e:
        return ValidationResult(
            False,
            f"Cannot read file: {str(e)}",
            {"path": str(path), "error": str(e)}
        )
    
    return ValidationResult(True)


def validate_markdown_content(content: str) -> ValidationResult:
    """
    Validate markdown content structure.
    
    Checks:
    - Content is not empty
    - Content is valid UTF-8
    - Content length is reasonable (< 500KB)
    - No null bytes in content
    
    Args:
        content: Markdown content to validate
        
    Returns:
        ValidationResult with is_valid and error_message
    """
    # Check if content is empty
    if not content or not content.strip():
        return ValidationResult(
            False,
            "Markdown content cannot be empty"
        )
    
    # Check content length (500KB limit)
    max_size = 500 * 1024  # 500KB
    if len(content.encode('utf-8')) > max_size:
        return ValidationResult(
            False,
            f"Content too large (max {max_size // 1024}KB)",
            {"size": len(content.encode('utf-8'))}
        )
    
    # Check for null bytes
    if '\x00' in content:
        return ValidationResult(
            False,
            "Content contains null bytes (invalid text file)"
        )
    
    return ValidationResult(True)


def validate_frontmatter(frontmatter: dict) -> ValidationResult:
    """
    Validate article frontmatter metadata.
    
    Checks:
    - Title is present and not empty
    - Title length is reasonable (< 200 chars)
    - Subtitle length is reasonable (< 300 chars) if present
    - Tags are valid if present
    
    Args:
        frontmatter: Dictionary with frontmatter data
        
    Returns:
        ValidationResult with is_valid and error_message
    """
    # Check if frontmatter is a dictionary
    if not isinstance(frontmatter, dict):
        return ValidationResult(
            False,
            "Frontmatter must be a dictionary",
            {"type": type(frontmatter).__name__}
        )
    
    # Check for required title field
    if 'title' not in frontmatter:
        return ValidationResult(
            False,
            "Frontmatter must include 'title' field"
        )
    
    title = frontmatter.get('title', '')
    
    # Check title is not empty
    if not title or not str(title).strip():
        return ValidationResult(
            False,
            "Title cannot be empty"
        )
    
    # Check title length
    if len(str(title)) > 200:
        return ValidationResult(
            False,
            f"Title too long (max 200 characters, got {len(str(title))})",
            {"title_length": len(str(title))}
        )
    
    # Check subtitle length if present
    subtitle = frontmatter.get('subtitle', '')
    if subtitle and len(str(subtitle)) > 300:
        return ValidationResult(
            False,
            f"Subtitle too long (max 300 characters, got {len(str(subtitle))})",
            {"subtitle_length": len(str(subtitle))}
        )
    
    # Validate tags if present
    if 'tags' in frontmatter:
        tags = frontmatter['tags']
        if tags:  # Only validate if tags list is not empty
            tag_result = validate_tags(tags)
            if not tag_result:
                return tag_result
    
    return ValidationResult(True)


def validate_tags(tags: List[str]) -> ValidationResult:
    """
    Validate article tags.
    
    Checks:
    - Tags is a list
    - Maximum 5 tags (Medium's limit)
    - Each tag is alphanumeric with hyphens/spaces only
    - Each tag is not empty
    - Each tag length is reasonable (< 50 chars)
    
    Args:
        tags: List of tag strings
        
    Returns:
        ValidationResult with is_valid and error_message
    """
    # Check if tags is a list
    if not isinstance(tags, list):
        return ValidationResult(
            False,
            "Tags must be a list",
            {"type": type(tags).__name__}
        )
    
    # Check maximum number of tags
    if len(tags) > 5:
        return ValidationResult(
            False,
            f"Maximum 5 tags allowed (got {len(tags)})",
            {"tag_count": len(tags)}
        )
    
    # Validate each tag
    for i, tag in enumerate(tags):
        # Check tag is a string
        if not isinstance(tag, str):
            return ValidationResult(
                False,
                f"Tag {i+1} must be a string, got {type(tag).__name__}",
                {"tag_index": i, "tag_type": type(tag).__name__}
            )
        
        # Check tag is not empty
        if not tag.strip():
            return ValidationResult(
                False,
                f"Tag {i+1} cannot be empty",
                {"tag_index": i}
            )
        
        # Check tag length
        if len(tag) > 50:
            return ValidationResult(
                False,
                f"Tag {i+1} too long (max 50 characters, got {len(tag)})",
                {"tag_index": i, "tag_length": len(tag), "tag": tag}
            )
        
        # Check tag contains only alphanumeric, hyphens, spaces, and underscores
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', tag):
            return ValidationResult(
                False,
                f"Tag {i+1} contains invalid characters (only letters, numbers, spaces, hyphens, underscores allowed): '{tag}'",
                {"tag_index": i, "tag": tag}
            )
    
    return ValidationResult(True)


def validate_draft_url(url: str) -> ValidationResult:
    """
    Validate Medium draft URL format.
    
    Checks:
    - URL is not empty if provided
    - URL is valid format
    - URL is a Medium domain (medium.com or <publication>.medium.com)
    - URL path matches draft or story pattern
    
    Valid patterns:
    - https://medium.com/p/<id>/edit
    - https://medium.com/p/<id>
    - https://medium.com/@<user>/<slug>-<id>
    - https://<publication>.medium.com/<slug>-<id>
    - https://medium.com/new-story
    
    Args:
        url: Draft URL to validate (can be empty)
        
    Returns:
        ValidationResult with is_valid and error_message
    """
    # Empty URL is valid (optional field)
    if not url or not url.strip():
        return ValidationResult(True)
    
    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        return ValidationResult(
            False,
            f"Invalid URL format: {str(e)}",
            {"url": url, "error": str(e)}
        )
    
    # Check scheme is https
    if parsed.scheme != 'https':
        return ValidationResult(
            False,
            f"URL must use HTTPS protocol, got: {parsed.scheme}",
            {"url": url, "scheme": parsed.scheme}
        )
    
    # Check domain is Medium (medium.com, www.medium.com, or <publication>.medium.com)
    netloc = parsed.netloc
    is_medium_domain = (
        netloc == 'medium.com'
        or netloc == 'www.medium.com'
        or (netloc.endswith('.medium.com') and len(netloc) > len('.medium.com'))
    )
    
    if not is_medium_domain:
        return ValidationResult(
            False,
            f"URL must be a Medium domain (medium.com or <publication>.medium.com), got: {netloc}",
            {"url": url, "domain": netloc}
        )
    
    # Check path is not empty
    if not parsed.path or parsed.path == '/':
        return ValidationResult(
            False,
            "URL must include a story path",
            {"url": url}
        )
    
    # For publication subdomains (e.g., https://towardsdatascience.medium.com/<slug>-<id>)
    is_publication_subdomain = (
        netloc.endswith('.medium.com')
        and netloc not in ('medium.com', 'www.medium.com')
    )
    
    if is_publication_subdomain:
        # Publication subdomain paths: /<slug>-<id> (at least one word char)
        if re.match(r'^/[\w][\w\-]*$', parsed.path):
            return ValidationResult(True)
        return ValidationResult(
            False,
            "Publication URL path must match /<slug>-<id> format",
            {"url": url, "path": parsed.path}
        )
    
    # Check path matches valid patterns for medium.com / www.medium.com
    valid_patterns = [
        r'^/@[\w\-]+/[\w\-]+$',       # /@username/story-slug
        r'^/p/[\w\-]+/edit$',          # /p/story-id/edit
        r'^/p/[\w\-]+$',              # /p/story-id
        r'^/new-story$',              # /new-story
    ]
    
    path_valid = any(re.match(pattern, parsed.path) for pattern in valid_patterns)
    
    if not path_valid:
        return ValidationResult(
            False,
            "URL does not match Medium story format "
            "(expected: /@user/slug, /p/<id>, /p/<id>/edit, or /new-story)",
            {"url": url, "path": parsed.path}
        )
    
    return ValidationResult(True)


def list_placeholders(blocks: List) -> List[str]:
    """
    Scan ContentBlocks for table and image placeholders.
    
    Returns a list of placeholder descriptions for user notification
    after typing is complete.
    
    Args:
        blocks: List of ContentBlock objects to scan
        
    Returns:
        List of placeholder description strings
    """
    placeholders: List[str] = []
    for block in blocks:
        if block.type == "table_placeholder":
            placeholders.append(f"[table: {block.content}]")
        elif block.type == "image_placeholder":
            alt_text = block.metadata.get("alt_text", block.content)
            placeholders.append(f"[image: {alt_text}]")
    return placeholders


def validate_and_truncate_tags(tags: List[str]) -> Tuple[List[str], List[str]]:
    """
    Validate and truncate article tags.
    
    Enforces max 5 tags (uses first 5 if more provided) and validates
    each tag contains only alphanumeric characters, hyphens, and spaces.
    
    Args:
        tags: List of tag strings
        
    Returns:
        Tuple of (valid_tags, errors) where valid_tags are accepted tags
        and errors are descriptive error messages for rejected tags
    """
    if not isinstance(tags, list):
        return [], [f"Tags must be a list, got {type(tags).__name__}"]
    
    # Truncate to first 5 tags
    truncated = tags[:5]
    
    valid_tags: List[str] = []
    errors: List[str] = []
    
    tag_pattern = re.compile(r'^[a-zA-Z0-9\s\-]+$')
    
    for i, tag in enumerate(truncated):
        if not isinstance(tag, str):
            errors.append(f"Tag {i+1} must be a string, got {type(tag).__name__}")
            continue
        
        if not tag.strip():
            errors.append(f"Tag {i+1} cannot be empty")
            continue
        
        if not tag_pattern.match(tag):
            errors.append(
                f"Tag {i+1} contains invalid characters "
                f"(only letters, numbers, spaces, hyphens allowed): '{tag}'"
            )
            continue
        
        valid_tags.append(tag)
    
    return valid_tags, errors


def validate_version_filename(filename: str) -> Optional[Tuple[int, str]]:
    """Validate a version filename matches the pattern ``v{N}-{article-name}.md``.

    The filename (not a full path) must satisfy:
    - Starts with ``v`` followed by a positive integer *N* (no leading zeros).
    - A single hyphen separates the version prefix from the article name.
    - The article name is non-empty **kebab-case**: one or more segments of
      lowercase ASCII letters or digits, separated by single hyphens.  No
      leading, trailing, or consecutive hyphens are allowed.
    - Ends with ``.md``.

    Args:
        filename: The bare filename to validate (e.g. ``v2-my-article.md``).

    Returns:
        A ``(version_number, article_name)`` tuple when valid, or ``None``
        when the filename does not match the expected pattern.

    Examples:
        >>> validate_version_filename("v1-hello-world.md")
        (1, 'hello-world')
        >>> validate_version_filename("v3-chatbots-to-coworkers.md")
        (3, 'chatbots-to-coworkers')
        >>> validate_version_filename("not-a-version.md") is None
        True
    """
    if not isinstance(filename, str):
        return None

    # Pattern breakdown:
    #   v          — literal 'v'
    #   ([1-9]\d*) — positive integer without leading zeros (group 1)
    #   -          — separator between version and article name
    #   (          — start article-name capture (group 2)
    #     [a-z0-9]+          — first segment (lowercase alphanum)
    #     (?:-[a-z0-9]+)*    — optional additional hyphen-separated segments
    #   )          — end article-name capture
    #   \.md$      — literal .md extension at end
    pattern = re.compile(r'^v([1-9]\d*)-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$')
    match = pattern.match(filename)
    if not match:
        return None

    version_number = int(match.group(1))
    article_name = match.group(2)
    return (version_number, article_name)


def validate_change_instructions(instructions: str) -> ValidationResult:
    """
    Validate change instructions for version updates.
    
    Checks:
    - Instructions are not empty
    - Instructions length is reasonable (< 10KB)
    - Instructions contain at least one action keyword
    
    Args:
        instructions: Change instructions text
        
    Returns:
        ValidationResult with is_valid and error_message
    """
    # Check if instructions are empty
    if not instructions or not instructions.strip():
        return ValidationResult(
            False,
            "Change instructions cannot be empty"
        )
    
    # Check instructions length
    max_length = 10 * 1024  # 10KB
    if len(instructions.encode('utf-8')) > max_length:
        return ValidationResult(
            False,
            f"Instructions too long (max {max_length // 1024}KB)",
            {"size": len(instructions.encode('utf-8'))}
        )
    
    # Check for at least one action keyword
    action_keywords = [
        'replace', 'update', 'change', 'modify',
        'add', 'insert', 'append',
        'delete', 'remove',
        'section', 'paragraph', 'content'
    ]
    
    instructions_lower = instructions.lower()
    has_action = any(keyword in instructions_lower for keyword in action_keywords)
    
    if not has_action:
        return ValidationResult(
            False,
            "Instructions must describe what to change (use words like: replace, add, delete, update)",
            {"keywords": action_keywords}
        )
    
    return ValidationResult(True)


def validate_oauth_timeout(timeout_seconds: int) -> ValidationResult:
    """
    Validate OAuth timeout value.
    
    Checks:
    - Timeout is a positive integer
    - Timeout is within reasonable range (30-600 seconds)
    
    Args:
        timeout_seconds: Timeout value in seconds
        
    Returns:
        ValidationResult with is_valid and error_message
    """
    # Check if timeout is an integer
    if not isinstance(timeout_seconds, int):
        return ValidationResult(
            False,
            f"Timeout must be an integer, got {type(timeout_seconds).__name__}",
            {"type": type(timeout_seconds).__name__}
        )
    
    # Check if timeout is positive
    if timeout_seconds <= 0:
        return ValidationResult(
            False,
            f"Timeout must be positive, got {timeout_seconds}",
            {"timeout": timeout_seconds}
        )
    
    # Check if timeout is within reasonable range
    min_timeout = 30   # 30 seconds minimum
    max_timeout = 600  # 10 minutes maximum
    
    if timeout_seconds < min_timeout:
        return ValidationResult(
            False,
            f"Timeout too short (minimum {min_timeout} seconds, got {timeout_seconds})",
            {"timeout": timeout_seconds, "min": min_timeout}
        )
    
    if timeout_seconds > max_timeout:
        return ValidationResult(
            False,
            f"Timeout too long (maximum {max_timeout} seconds, got {timeout_seconds})",
            {"timeout": timeout_seconds, "max": max_timeout}
        )
    
    return ValidationResult(True)


def validate_version_number(version: str) -> ValidationResult:
    """
    Validate version number format.
    
    Checks:
    - Version matches pattern: v1, v2, v3, etc.
    - Version number is reasonable (1-99)
    
    Args:
        version: Version string (e.g., "v1", "v2")
        
    Returns:
        ValidationResult with is_valid and error_message
    """
    # Check if version is empty
    if not version or not version.strip():
        return ValidationResult(
            False,
            "Version cannot be empty"
        )
    
    # Check version format
    match = re.match(r'^v(\d+)$', version.lower())
    if not match:
        return ValidationResult(
            False,
            f"Version must be in format 'v1', 'v2', etc., got: '{version}'",
            {"version": version}
        )
    
    # Check version number is reasonable
    version_num = int(match.group(1))
    if version_num < 1 or version_num > 99:
        return ValidationResult(
            False,
            f"Version number must be between 1 and 99, got: {version_num}",
            {"version": version, "number": version_num}
        )
    
    return ValidationResult(True)


# Convenience functions that raise exceptions instead of returning ValidationResult


def validate_file_path_or_raise(file_path: str) -> None:
    """
    Validate file path and raise FileError if invalid.
    
    Args:
        file_path: Path to validate
        
    Raises:
        FileError: If validation fails
    """
    result = validate_file_path(file_path)
    if not result:
        raise FileError(result.error_message, result.details)


def validate_markdown_content_or_raise(content: str) -> None:
    """
    Validate markdown content and raise ContentError if invalid.
    
    Args:
        content: Content to validate
        
    Raises:
        ContentError: If validation fails
    """
    result = validate_markdown_content(content)
    if not result:
        raise ContentError(result.error_message, result.details)


def validate_frontmatter_or_raise(frontmatter: dict) -> None:
    """
    Validate frontmatter and raise ContentError if invalid.
    
    Args:
        frontmatter: Frontmatter to validate
        
    Raises:
        ContentError: If validation fails
    """
    result = validate_frontmatter(frontmatter)
    if not result:
        raise ContentError(result.error_message, result.details)


def validate_tags_or_raise(tags: List[str]) -> None:
    """
    Validate tags and raise ContentError if invalid.
    
    Args:
        tags: Tags to validate
        
    Raises:
        ContentError: If validation fails
    """
    result = validate_tags(tags)
    if not result:
        raise ContentError(result.error_message, result.details)


def validate_draft_url_or_raise(url: str) -> None:
    """
    Validate draft URL and raise ContentError if invalid.
    
    Args:
        url: URL to validate
        
    Raises:
        ContentError: If validation fails
    """
    result = validate_draft_url(url)
    if not result:
        raise ContentError(result.error_message, result.details)


def validate_change_instructions_or_raise(instructions: str) -> None:
    """
    Validate change instructions and raise ContentError if invalid.
    
    Args:
        instructions: Instructions to validate
        
    Raises:
        ContentError: If validation fails
    """
    result = validate_change_instructions(instructions)
    if not result:
        raise ContentError(result.error_message, result.details)

"""
Tests for input validation utilities.
"""

import pytest
from pathlib import Path
from medium_publisher.utils.validators import (
    ValidationResult,
    validate_file_path,
    validate_markdown_content,
    validate_frontmatter,
    validate_tags,
    validate_draft_url,
    validate_change_instructions,
    validate_oauth_timeout,
    validate_version_number,
    validate_version_filename,
    validate_file_path_or_raise,
    validate_markdown_content_or_raise,
    validate_frontmatter_or_raise,
    validate_tags_or_raise,
    validate_draft_url_or_raise,
    validate_change_instructions_or_raise,
)
from medium_publisher.utils.exceptions import FileError, ContentError


class TestValidationResult:
    """Test ValidationResult class."""
    
    def test_valid_result(self):
        """Test valid result."""
        result = ValidationResult(True)
        assert result.is_valid
        assert result.error_message == ""
        assert result.details == {}
        assert bool(result) is True
        assert str(result) == "Validation passed"
    
    def test_invalid_result(self):
        """Test invalid result."""
        result = ValidationResult(False, "Error message")
        assert not result.is_valid
        assert result.error_message == "Error message"
        assert bool(result) is False
        assert str(result) == "Error message"
    
    def test_result_with_details(self):
        """Test result with details."""
        result = ValidationResult(False, "Error", {"key": "value"})
        assert result.details == {"key": "value"}


class TestValidateFilePath:
    """Test file path validation."""
    
    def test_empty_path(self):
        """Test empty path."""
        result = validate_file_path("")
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_whitespace_path(self):
        """Test whitespace-only path."""
        result = validate_file_path("   ")
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_nonexistent_file(self):
        """Test nonexistent file."""
        result = validate_file_path("nonexistent.md")
        assert not result
        assert "not found" in result.error_message.lower()
    
    def test_directory_path(self, tmp_path):
        """Test directory path."""
        result = validate_file_path(str(tmp_path))
        assert not result
        assert "not a file" in result.error_message.lower()
    
    def test_wrong_extension(self, tmp_path):
        """Test wrong file extension."""
        file = tmp_path / "test.txt"
        file.write_text("content")
        result = validate_file_path(str(file))
        assert not result
        assert ".md extension" in result.error_message
    
    def test_empty_file(self, tmp_path):
        """Test empty file."""
        file = tmp_path / "test.md"
        file.touch()
        result = validate_file_path(str(file))
        assert not result
        assert "empty" in result.error_message.lower()
    
    def test_valid_file(self, tmp_path):
        """Test valid markdown file."""
        file = tmp_path / "test.md"
        file.write_text("# Test Article\n\nContent here.")
        result = validate_file_path(str(file))
        assert result
        assert result.is_valid
    
    def test_case_insensitive_extension(self, tmp_path):
        """Test case-insensitive extension matching."""
        file = tmp_path / "test.MD"
        file.write_text("content")
        result = validate_file_path(str(file))
        assert result


class TestValidateMarkdownContent:
    """Test markdown content validation."""
    
    def test_empty_content(self):
        """Test empty content."""
        result = validate_markdown_content("")
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_whitespace_content(self):
        """Test whitespace-only content."""
        result = validate_markdown_content("   \n\n   ")
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_content_too_large(self):
        """Test content exceeding size limit."""
        large_content = "x" * (500 * 1024 + 1)  # 500KB + 1 byte
        result = validate_markdown_content(large_content)
        assert not result
        assert "too large" in result.error_message.lower()
    
    def test_content_with_null_bytes(self):
        """Test content with null bytes."""
        result = validate_markdown_content("content\x00here")
        assert not result
        assert "null bytes" in result.error_message.lower()
    
    def test_valid_content(self):
        """Test valid markdown content."""
        content = "# Title\n\nParagraph with **bold** and *italic*."
        result = validate_markdown_content(content)
        assert result


class TestValidateFrontmatter:
    """Test frontmatter validation."""
    
    def test_not_dict(self):
        """Test non-dictionary frontmatter."""
        result = validate_frontmatter("not a dict")
        assert not result
        assert "must be a dictionary" in result.error_message
    
    def test_missing_title(self):
        """Test missing title field."""
        result = validate_frontmatter({})
        assert not result
        assert "title" in result.error_message.lower()
    
    def test_empty_title(self):
        """Test empty title."""
        result = validate_frontmatter({"title": ""})
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_whitespace_title(self):
        """Test whitespace-only title."""
        result = validate_frontmatter({"title": "   "})
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_title_too_long(self):
        """Test title exceeding length limit."""
        result = validate_frontmatter({"title": "x" * 201})
        assert not result
        assert "too long" in result.error_message.lower()
        assert "200" in result.error_message
    
    def test_subtitle_too_long(self):
        """Test subtitle exceeding length limit."""
        result = validate_frontmatter({
            "title": "Valid Title",
            "subtitle": "x" * 301
        })
        assert not result
        assert "subtitle" in result.error_message.lower()
        assert "too long" in result.error_message.lower()
    
    def test_invalid_tags(self):
        """Test invalid tags."""
        result = validate_frontmatter({
            "title": "Valid Title",
            "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]  # Too many
        })
        assert not result
        assert "5 tags" in result.error_message.lower()
    
    def test_valid_frontmatter(self):
        """Test valid frontmatter."""
        result = validate_frontmatter({
            "title": "My Article",
            "subtitle": "A great article",
            "tags": ["python", "programming"]
        })
        assert result
    
    def test_valid_frontmatter_no_tags(self):
        """Test valid frontmatter without tags."""
        result = validate_frontmatter({"title": "My Article"})
        assert result
    
    def test_valid_frontmatter_empty_tags(self):
        """Test valid frontmatter with empty tags list."""
        result = validate_frontmatter({"title": "My Article", "tags": []})
        assert result


class TestValidateTags:
    """Test tag validation."""
    
    def test_not_list(self):
        """Test non-list tags."""
        result = validate_tags("not a list")
        assert not result
        assert "must be a list" in result.error_message
    
    def test_too_many_tags(self):
        """Test more than 5 tags."""
        result = validate_tags(["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"])
        assert not result
        assert "5 tags" in result.error_message.lower()
    
    def test_non_string_tag(self):
        """Test non-string tag."""
        result = validate_tags(["tag1", 123])
        assert not result
        assert "must be a string" in result.error_message
    
    def test_empty_tag(self):
        """Test empty tag."""
        result = validate_tags(["tag1", ""])
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_whitespace_tag(self):
        """Test whitespace-only tag."""
        result = validate_tags(["tag1", "   "])
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_tag_too_long(self):
        """Test tag exceeding length limit."""
        result = validate_tags(["x" * 51])
        assert not result
        assert "too long" in result.error_message.lower()
        assert "50" in result.error_message
    
    def test_tag_invalid_characters(self):
        """Test tag with invalid characters."""
        result = validate_tags(["tag@invalid"])
        assert not result
        assert "invalid characters" in result.error_message.lower()
    
    def test_valid_tags(self):
        """Test valid tags."""
        result = validate_tags(["python", "programming", "web-dev"])
        assert result
    
    def test_tags_with_spaces(self):
        """Test tags with spaces."""
        result = validate_tags(["machine learning", "data science"])
        assert result
    
    def test_tags_with_underscores(self):
        """Test tags with underscores."""
        result = validate_tags(["web_development", "python_3"])
        assert result
    
    def test_tags_with_numbers(self):
        """Test tags with numbers."""
        result = validate_tags(["python3", "web2.0"])
        assert not result  # Dot is not allowed
    
    def test_empty_list(self):
        """Test empty tag list."""
        result = validate_tags([])
        assert result


class TestValidateDraftUrl:
    """Test draft URL validation."""
    
    def test_empty_url(self):
        """Test empty URL (valid - optional field)."""
        result = validate_draft_url("")
        assert result
    
    def test_whitespace_url(self):
        """Test whitespace-only URL (valid - optional field)."""
        result = validate_draft_url("   ")
        assert result
    
    def test_invalid_url_format(self):
        """Test invalid URL format."""
        result = validate_draft_url("not a url")
        assert not result
        # URL parser treats "not a url" as a path with empty scheme
        assert "https" in result.error_message.lower() or "protocol" in result.error_message.lower()
    
    def test_non_https_url(self):
        """Test non-HTTPS URL."""
        result = validate_draft_url("http://medium.com/@user/story")
        assert not result
        assert "https" in result.error_message.lower()
    
    def test_non_medium_domain(self):
        """Test non-Medium domain."""
        result = validate_draft_url("https://example.com/@user/story")
        assert not result
        assert "medium" in result.error_message.lower()
    
    def test_empty_path(self):
        """Test URL with empty path."""
        result = validate_draft_url("https://medium.com")
        assert not result
        assert "path" in result.error_message.lower()
    
    def test_root_path(self):
        """Test URL with root path only."""
        result = validate_draft_url("https://medium.com/")
        assert not result
        assert "path" in result.error_message.lower()
    
    def test_invalid_path_pattern(self):
        """Test URL with invalid path pattern."""
        result = validate_draft_url("https://medium.com/invalid/path/here")
        assert not result
        assert "format" in result.error_message.lower()
    
    def test_valid_username_story_url(self):
        """Test valid @username/story URL."""
        result = validate_draft_url("https://medium.com/@johndoe/my-article-123")
        assert result
    
    def test_valid_p_story_url(self):
        """Test valid /p/story-id URL."""
        result = validate_draft_url("https://medium.com/p/abc123def")
        assert result
    
    def test_valid_new_story_url(self):
        """Test valid /new-story URL."""
        result = validate_draft_url("https://medium.com/new-story")
        assert result
    
    def test_www_subdomain(self):
        """Test www.medium.com domain."""
        result = validate_draft_url("https://www.medium.com/@user/story")
        assert result


class TestValidateChangeInstructions:
    """Test change instructions validation."""
    
    def test_empty_instructions(self):
        """Test empty instructions."""
        result = validate_change_instructions("")
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_whitespace_instructions(self):
        """Test whitespace-only instructions."""
        result = validate_change_instructions("   \n\n   ")
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_instructions_too_long(self):
        """Test instructions exceeding size limit."""
        large_instructions = "x" * (10 * 1024 + 1)  # 10KB + 1 byte
        result = validate_change_instructions(large_instructions)
        assert not result
        assert "too long" in result.error_message.lower()
    
    def test_no_action_keywords(self):
        """Test instructions without action keywords."""
        result = validate_change_instructions("This is just some text")
        assert not result
        assert "describe what to change" in result.error_message.lower()
    
    def test_valid_replace_instruction(self):
        """Test valid replace instruction."""
        result = validate_change_instructions("Replace the introduction section with new content")
        assert result
    
    def test_valid_add_instruction(self):
        """Test valid add instruction."""
        result = validate_change_instructions("Add a new section about testing")
        assert result
    
    def test_valid_delete_instruction(self):
        """Test valid delete instruction."""
        result = validate_change_instructions("Delete the old examples section")
        assert result
    
    def test_valid_update_instruction(self):
        """Test valid update instruction."""
        result = validate_change_instructions("Update the conclusion paragraph")
        assert result
    
    def test_case_insensitive_keywords(self):
        """Test case-insensitive keyword matching."""
        result = validate_change_instructions("REPLACE the section")
        assert result


class TestValidateOAuthTimeout:
    """Test OAuth timeout validation."""
    
    def test_non_integer_timeout(self):
        """Test non-integer timeout."""
        result = validate_oauth_timeout("300")
        assert not result
        assert "must be an integer" in result.error_message
    
    def test_negative_timeout(self):
        """Test negative timeout."""
        result = validate_oauth_timeout(-10)
        assert not result
        assert "must be positive" in result.error_message
    
    def test_zero_timeout(self):
        """Test zero timeout."""
        result = validate_oauth_timeout(0)
        assert not result
        assert "must be positive" in result.error_message
    
    def test_timeout_too_short(self):
        """Test timeout below minimum."""
        result = validate_oauth_timeout(20)
        assert not result
        assert "too short" in result.error_message.lower()
        assert "30" in result.error_message
    
    def test_timeout_too_long(self):
        """Test timeout above maximum."""
        result = validate_oauth_timeout(700)
        assert not result
        assert "too long" in result.error_message.lower()
        assert "600" in result.error_message
    
    def test_valid_timeout_minimum(self):
        """Test valid timeout at minimum."""
        result = validate_oauth_timeout(30)
        assert result
    
    def test_valid_timeout_maximum(self):
        """Test valid timeout at maximum."""
        result = validate_oauth_timeout(600)
        assert result
    
    def test_valid_timeout_middle(self):
        """Test valid timeout in middle range."""
        result = validate_oauth_timeout(300)
        assert result


class TestValidateVersionNumber:
    """Test version number validation."""
    
    def test_empty_version(self):
        """Test empty version."""
        result = validate_version_number("")
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_whitespace_version(self):
        """Test whitespace-only version."""
        result = validate_version_number("   ")
        assert not result
        assert "cannot be empty" in result.error_message
    
    def test_invalid_format(self):
        """Test invalid version format."""
        result = validate_version_number("version1")
        assert not result
        assert "format" in result.error_message.lower()
    
    def test_no_number(self):
        """Test version without number."""
        result = validate_version_number("v")
        assert not result
        assert "format" in result.error_message.lower()
    
    def test_version_zero(self):
        """Test version 0."""
        result = validate_version_number("v0")
        assert not result
        assert "between 1 and 99" in result.error_message
    
    def test_version_too_high(self):
        """Test version above 99."""
        result = validate_version_number("v100")
        assert not result
        assert "between 1 and 99" in result.error_message
    
    def test_valid_version_v1(self):
        """Test valid version v1."""
        result = validate_version_number("v1")
        assert result
    
    def test_valid_version_v99(self):
        """Test valid version v99."""
        result = validate_version_number("v99")
        assert result
    
    def test_valid_version_uppercase(self):
        """Test valid version with uppercase V."""
        result = validate_version_number("V5")
        assert result
    
    def test_valid_version_mixed_case(self):
        """Test valid version with mixed case."""
        result = validate_version_number("V10")
        assert result


class TestValidateOrRaiseFunctions:
    """Test convenience functions that raise exceptions."""
    
    def test_validate_file_path_or_raise_valid(self, tmp_path):
        """Test validate_file_path_or_raise with valid file."""
        file = tmp_path / "test.md"
        file.write_text("content")
        # Should not raise
        validate_file_path_or_raise(str(file))
    
    def test_validate_file_path_or_raise_invalid(self):
        """Test validate_file_path_or_raise with invalid file."""
        with pytest.raises(FileError) as exc_info:
            validate_file_path_or_raise("nonexistent.md")
        assert "not found" in str(exc_info.value).lower()
    
    def test_validate_markdown_content_or_raise_valid(self):
        """Test validate_markdown_content_or_raise with valid content."""
        # Should not raise
        validate_markdown_content_or_raise("# Title\n\nContent")
    
    def test_validate_markdown_content_or_raise_invalid(self):
        """Test validate_markdown_content_or_raise with invalid content."""
        with pytest.raises(ContentError) as exc_info:
            validate_markdown_content_or_raise("")
        assert "cannot be empty" in str(exc_info.value)
    
    def test_validate_frontmatter_or_raise_valid(self):
        """Test validate_frontmatter_or_raise with valid frontmatter."""
        # Should not raise
        validate_frontmatter_or_raise({"title": "My Article"})
    
    def test_validate_frontmatter_or_raise_invalid(self):
        """Test validate_frontmatter_or_raise with invalid frontmatter."""
        with pytest.raises(ContentError) as exc_info:
            validate_frontmatter_or_raise({})
        assert "title" in str(exc_info.value).lower()
    
    def test_validate_tags_or_raise_valid(self):
        """Test validate_tags_or_raise with valid tags."""
        # Should not raise
        validate_tags_or_raise(["python", "programming"])
    
    def test_validate_tags_or_raise_invalid(self):
        """Test validate_tags_or_raise with invalid tags."""
        with pytest.raises(ContentError) as exc_info:
            validate_tags_or_raise(["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"])
        assert "5 tags" in str(exc_info.value).lower()
    
    def test_validate_draft_url_or_raise_valid(self):
        """Test validate_draft_url_or_raise with valid URL."""
        # Should not raise
        validate_draft_url_or_raise("https://medium.com/@user/story")
    
    def test_validate_draft_url_or_raise_invalid(self):
        """Test validate_draft_url_or_raise with invalid URL."""
        with pytest.raises(ContentError) as exc_info:
            validate_draft_url_or_raise("https://example.com/story")
        # Should fail on non-Medium domain
        assert "medium" in str(exc_info.value).lower()
    
    def test_validate_change_instructions_or_raise_valid(self):
        """Test validate_change_instructions_or_raise with valid instructions."""
        # Should not raise
        validate_change_instructions_or_raise("Replace the section")
    
    def test_validate_change_instructions_or_raise_invalid(self):
        """Test validate_change_instructions_or_raise with invalid instructions."""
        with pytest.raises(ContentError) as exc_info:
            validate_change_instructions_or_raise("")
        assert "cannot be empty" in str(exc_info.value)


class TestValidateVersionFilename:
    """Tests for validate_version_filename utility.

    Validates: Requirements 1.2, 1.3
    """

    # --- Valid filenames ---

    def test_valid_simple(self):
        result = validate_version_filename("v1-hello-world.md")
        assert result == (1, "hello-world")

    def test_valid_single_segment(self):
        result = validate_version_filename("v2-article.md")
        assert result == (2, "article")

    def test_valid_multi_segment(self):
        result = validate_version_filename("v3-chatbots-to-coworkers.md")
        assert result == (3, "chatbots-to-coworkers")

    def test_valid_double_digit_version(self):
        result = validate_version_filename("v10-my-article.md")
        assert result == (10, "my-article")

    def test_valid_single_char_name(self):
        result = validate_version_filename("v1-a.md")
        assert result == (1, "a")

    def test_valid_digits_in_name(self):
        result = validate_version_filename("v1-article2.md")
        assert result == (1, "article2")

    def test_valid_mixed_segments(self):
        result = validate_version_filename("v4-a1-b2-c3.md")
        assert result == (4, "a1-b2-c3")

    # --- Invalid filenames ---

    def test_invalid_no_v_prefix(self):
        assert validate_version_filename("1-hello.md") is None

    def test_invalid_uppercase_v(self):
        assert validate_version_filename("V1-hello.md") is None

    def test_invalid_version_zero(self):
        assert validate_version_filename("v0-hello.md") is None

    def test_invalid_leading_zero(self):
        assert validate_version_filename("v01-hello.md") is None

    def test_invalid_no_article_name(self):
        assert validate_version_filename("v1.md") is None

    def test_invalid_trailing_hyphen(self):
        assert validate_version_filename("v1-.md") is None

    def test_invalid_consecutive_hyphens(self):
        assert validate_version_filename("v1-hello--world.md") is None

    def test_invalid_uppercase_name(self):
        assert validate_version_filename("v1-Hello.md") is None

    def test_invalid_space_in_name(self):
        assert validate_version_filename("v1-hello world.md") is None

    def test_invalid_wrong_extension(self):
        assert validate_version_filename("v1-hello.txt") is None

    def test_invalid_no_extension(self):
        assert validate_version_filename("v1-hello") is None

    def test_invalid_empty_string(self):
        assert validate_version_filename("") is None

    def test_invalid_non_string(self):
        assert validate_version_filename(123) is None

    def test_invalid_underscore_in_name(self):
        assert validate_version_filename("v1-hello_world.md") is None

    def test_invalid_special_chars(self):
        assert validate_version_filename("v1-hello@world.md") is None

"""
Tests for ArticleParser.
"""

import pytest
from pathlib import Path
import tempfile
import os

from medium_publisher.core.article_parser import ArticleParser
from medium_publisher.core.models import Article
from medium_publisher.utils.exceptions import FileError, ContentError


class TestArticleParser:
    """Test suite for ArticleParser class."""
    
    @pytest.fixture
    def parser(self):
        """Create ArticleParser instance."""
        return ArticleParser()
    
    @pytest.fixture
    def valid_markdown(self):
        """Valid markdown content with frontmatter."""
        return """---
title: Test Article
subtitle: A test subtitle
tags:
  - python
  - testing
keywords:
  - pytest
  - automation
status: draft
---

# Introduction

This is a test article with some content.

## Section 1

More content here.
"""
    
    @pytest.fixture
    def temp_markdown_file(self, valid_markdown):
        """Create temporary markdown file."""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(valid_markdown)
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    
    # Test parse_file() method
    
    def test_parse_file_success(self, parser, temp_markdown_file):
        """Test successful file parsing."""
        article = parser.parse_file(temp_markdown_file)
        
        assert isinstance(article, Article)
        assert article.title == "Test Article"
        assert article.subtitle == "A test subtitle"
        assert article.tags == ["python", "testing"]
        assert article.keywords == ["pytest", "automation"]
        assert article.status == "draft"
        assert "Introduction" in article.content
        assert article.file_path == str(Path(temp_markdown_file).absolute())
    
    def test_parse_file_nonexistent(self, parser):
        """Test parsing nonexistent file raises FileError."""
        with pytest.raises(FileError, match="File not found"):
            parser.parse_file("nonexistent.md")
    
    def test_parse_file_not_a_file(self, parser):
        """Test parsing directory raises FileError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileError, match="not a file"):
                parser.parse_file(tmpdir)
    
    def test_parse_file_wrong_extension(self, parser):
        """Test parsing non-markdown file raises FileError."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            with pytest.raises(FileError, match="Invalid file extension"):
                parser.parse_file(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_parse_file_read_error(self, parser, temp_markdown_file):
        """Test file read error handling."""
        # Make file unreadable (Unix-like systems)
        if os.name != 'nt':  # Skip on Windows
            os.chmod(temp_markdown_file, 0o000)
            try:
                with pytest.raises(FileError, match="Failed to read file"):
                    parser.parse_file(temp_markdown_file)
            finally:
                os.chmod(temp_markdown_file, 0o644)
    
    def test_parse_file_malformed_frontmatter(self, parser):
        """Test parsing file with malformed frontmatter."""
        content = """---
title: Test
invalid yaml: [unclosed
---

Content here.
"""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            with pytest.raises(ContentError, match="Invalid YAML"):
                parser.parse_file(temp_path)
        finally:
            os.unlink(temp_path)

    
    def test_parse_file_missing_required_field(self, parser):
        """Test parsing file with missing required field."""
        content = """---
subtitle: No title
---

Content here.
"""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            with pytest.raises(ContentError, match="validation failed"):
                parser.parse_file(temp_path)
        finally:
            os.unlink(temp_path)
    
    # Test extract_frontmatter() method
    
    def test_extract_frontmatter_success(self, parser, valid_markdown):
        """Test successful frontmatter extraction."""
        frontmatter = parser.extract_frontmatter(valid_markdown)
        
        assert isinstance(frontmatter, dict)
        assert frontmatter['title'] == "Test Article"
        assert frontmatter['subtitle'] == "A test subtitle"
        assert frontmatter['tags'] == ["python", "testing"]
        assert frontmatter['status'] == "draft"
    
    def test_extract_frontmatter_missing_delimiter(self, parser):
        """Test extraction fails without opening delimiter."""
        content = "title: Test\n---\n\nContent"
        
        with pytest.raises(ContentError, match="Missing frontmatter"):
            parser.extract_frontmatter(content)
    
    def test_extract_frontmatter_no_closing_delimiter(self, parser):
        """Test extraction fails without closing delimiter."""
        content = "---\ntitle: Test\n\nContent"
        
        with pytest.raises(ContentError, match="Malformed frontmatter"):
            parser.extract_frontmatter(content)
    
    def test_extract_frontmatter_invalid_yaml(self, parser):
        """Test extraction fails with invalid YAML."""
        content = "---\ntitle: Test\ninvalid: [unclosed\n---\n\nContent"
        
        with pytest.raises(ContentError, match="Invalid YAML"):
            parser.extract_frontmatter(content)
    
    def test_extract_frontmatter_not_dict(self, parser):
        """Test extraction fails if YAML is not a dictionary."""
        content = "---\n- item1\n- item2\n---\n\nContent"
        
        with pytest.raises(ContentError, match="must be a YAML dictionary"):
            parser.extract_frontmatter(content)
    
    def test_extract_frontmatter_empty(self, parser):
        """Test extraction with empty frontmatter."""
        content = "---\n\n---\n\nContent"
        
        frontmatter = parser.extract_frontmatter(content)
        assert frontmatter == {}

    
    # Test extract_body() method
    
    def test_extract_body_success(self, parser, valid_markdown):
        """Test successful body extraction."""
        body = parser.extract_body(valid_markdown)
        
        assert isinstance(body, str)
        assert "# Introduction" in body
        assert "## Section 1" in body
        assert "---" not in body  # Frontmatter removed
        assert "title:" not in body
    
    def test_extract_body_malformed_frontmatter(self, parser):
        """Test body extraction fails with malformed frontmatter."""
        content = "---\ntitle: Test\n\nContent"  # No closing delimiter
        
        with pytest.raises(ContentError, match="malformed frontmatter"):
            parser.extract_body(content)
    
    def test_extract_body_empty(self, parser):
        """Test body extraction fails with empty body."""
        content = "---\ntitle: Test\n---\n\n   \n"  # Only whitespace
        
        with pytest.raises(ContentError, match="body is empty"):
            parser.extract_body(content)
    
    def test_extract_body_strips_whitespace(self, parser):
        """Test body extraction strips leading/trailing whitespace."""
        content = "---\ntitle: Test\n---\n\n\n  Content here  \n\n\n"
        
        body = parser.extract_body(content)
        assert body == "Content here"
    
    # Test validate_article() method
    
    def test_validate_article_success(self, parser):
        """Test successful article validation."""
        article = Article(
            title="Test Article",
            content="Some content",
            status="draft"
        )
        
        assert parser.validate_article(article) is True
    
    def test_validate_article_missing_title(self, parser):
        """Test validation fails with missing title."""
        article = Article(
            title="",
            content="Some content"
        )
        
        with pytest.raises(ValueError, match="missing required fields"):
            parser.validate_article(article)
    
    def test_validate_article_missing_content(self, parser):
        """Test validation fails with missing content."""
        article = Article(
            title="Test",
            content=""
        )
        
        with pytest.raises(ValueError, match="missing required fields"):
            parser.validate_article(article)
    
    def test_validate_article_invalid_status(self, parser):
        """Test validation fails with invalid status."""
        article = Article(
            title="Test",
            content="Content",
            status="invalid"
        )
        
        with pytest.raises(ValueError, match="Invalid status"):
            parser.validate_article(article)
    
    def test_validate_article_too_many_tags(self, parser):
        """Test validation fails with too many tags."""
        article = Article(
            title="Test",
            content="Content",
            tags=["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]
        )
        
        with pytest.raises(ValueError, match="Too many tags"):
            parser.validate_article(article)

    
    # Integration tests
    
    def test_parse_file_with_minimal_frontmatter(self, parser):
        """Test parsing file with minimal frontmatter."""
        content = """---
title: Minimal Article
---

Just some content.
"""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            article = parser.parse_file(temp_path)
            assert article.title == "Minimal Article"
            assert article.subtitle == ""
            assert article.tags == []
            assert article.status == "draft"  # Default
            assert "Just some content" in article.content
        finally:
            os.unlink(temp_path)
    
    def test_parse_file_with_all_fields(self, parser):
        """Test parsing file with all possible fields."""
        content = """---
title: Complete Article
subtitle: With all fields
tags:
  - tag1
  - tag2
  - tag3
keywords:
  - keyword1
  - keyword2
status: public
---

# Main Content

This article has everything.

## Section

More details here.
"""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            article = parser.parse_file(temp_path)
            assert article.title == "Complete Article"
            assert article.subtitle == "With all fields"
            assert len(article.tags) == 3
            assert len(article.keywords) == 2
            assert article.status == "public"
            assert "Main Content" in article.content
            assert "Section" in article.content
        finally:
            os.unlink(temp_path)
    
    def test_parse_file_unicode_content(self, parser):
        """Test parsing file with unicode characters."""
        content = """---
title: Unicode Test 你好
subtitle: Émojis 🎉
tags:
  - python
---

Content with unicode: café, naïve, 日本語
"""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            article = parser.parse_file(temp_path)
            assert "你好" in article.title
            assert "🎉" in article.subtitle
            assert "café" in article.content
            assert "日本語" in article.content
        finally:
            os.unlink(temp_path)

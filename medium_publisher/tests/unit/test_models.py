"""
Unit tests for data models.
"""

import pytest
from medium_publisher.core.models import Article, ContentBlock, Format


class TestFormat:
    """Tests for Format dataclass."""
    
    def test_format_creation(self):
        """Test creating a Format object."""
        fmt = Format(type="bold", start=0, end=5)
        assert fmt.type == "bold"
        assert fmt.start == 0
        assert fmt.end == 5
        assert fmt.url == ""
    
    def test_format_with_url(self):
        """Test creating a Format with URL."""
        fmt = Format(type="link", start=0, end=5, url="https://example.com")
        assert fmt.type == "link"
        assert fmt.url == "https://example.com"
    
    def test_format_validation_valid_types(self):
        """Test validation accepts valid format types."""
        valid_types = ["bold", "italic", "code", "link"]
        for fmt_type in valid_types:
            fmt = Format(type=fmt_type, start=0, end=5, url="https://example.com")
            assert fmt.validate() is True
    
    def test_format_validation_invalid_type(self):
        """Test validation rejects invalid format type."""
        fmt = Format(type="invalid", start=0, end=5)
        with pytest.raises(ValueError, match="Invalid format type"):
            fmt.validate()
    
    def test_format_validation_negative_start(self):
        """Test validation rejects negative start index."""
        fmt = Format(type="bold", start=-1, end=5)
        with pytest.raises(ValueError, match="start index must be >= 0"):
            fmt.validate()
    
    def test_format_validation_end_before_start(self):
        """Test validation rejects end <= start."""
        fmt = Format(type="bold", start=5, end=5)
        with pytest.raises(ValueError, match="end index .* must be > start index"):
            fmt.validate()
    
    def test_format_validation_link_requires_url(self):
        """Test validation requires URL for link type."""
        fmt = Format(type="link", start=0, end=5, url="")
        with pytest.raises(ValueError, match="requires a URL"):
            fmt.validate()


class TestContentBlock:
    """Tests for ContentBlock dataclass."""
    
    def test_content_block_creation(self):
        """Test creating a ContentBlock object."""
        block = ContentBlock(type="paragraph", content="Test content")
        assert block.type == "paragraph"
        assert block.content == "Test content"
        assert block.formatting == []
        assert block.level == 0
        assert block.metadata == {}
    
    def test_content_block_with_formatting(self):
        """Test ContentBlock with formatting."""
        fmt = Format(type="bold", start=0, end=4)
        block = ContentBlock(
            type="paragraph",
            content="Test content",
            formatting=[fmt]
        )
        assert len(block.formatting) == 1
        assert block.formatting[0].type == "bold"
    
    def test_content_block_header_with_level(self):
        """Test header ContentBlock with level."""
        block = ContentBlock(type="header", content="Header", level=2)
        assert block.type == "header"
        assert block.level == 2
    
    def test_content_block_with_metadata(self):
        """Test ContentBlock with metadata."""
        block = ContentBlock(
            type="image_placeholder",
            content="TODO: Insert image",
            metadata={"alt_text": "Example image"}
        )
        assert block.metadata["alt_text"] == "Example image"
    
    def test_content_block_validation_valid_types(self):
        """Test validation accepts valid block types."""
        valid_types = [
            "paragraph", "header", "code",
            "list", "table_placeholder", "image_placeholder"
        ]
        for block_type in valid_types:
            block = ContentBlock(type=block_type, content="Test")
            if block_type == "header":
                block.level = 2
            if block_type == "image_placeholder":
                block.metadata = {"alt_text": "Test"}
            assert block.validate() is True
    
    def test_content_block_validation_invalid_type(self):
        """Test validation rejects invalid block type."""
        block = ContentBlock(type="invalid", content="Test")
        with pytest.raises(ValueError, match="Invalid block type"):
            block.validate()
    
    def test_content_block_validation_empty_content(self):
        """Test validation rejects empty content."""
        block = ContentBlock(type="paragraph", content="")
        with pytest.raises(ValueError, match="content cannot be empty"):
            block.validate()

    def test_content_block_validation_invalid_header_level(self):
        """Test validation rejects invalid header level."""
        block = ContentBlock(type="header", content="Header", level=1)
        with pytest.raises(ValueError, match="Header level must be 2, 3, or 4"):
            block.validate()
    
    def test_content_block_validation_format_out_of_bounds(self):
        """Test validation rejects format exceeding content length."""
        fmt = Format(type="bold", start=0, end=100)
        block = ContentBlock(
            type="paragraph",
            content="Short",
            formatting=[fmt]
        )
        with pytest.raises(ValueError, match="exceeds content length"):
            block.validate()
    
    def test_content_block_validation_image_requires_alt_text(self):
        """Test validation requires alt_text for image placeholder."""
        block = ContentBlock(
            type="image_placeholder",
            content="TODO: Insert image"
        )
        with pytest.raises(ValueError, match="requires 'alt_text'"):
            block.validate()


class TestArticle:
    """Tests for Article dataclass."""
    
    def test_article_creation(self):
        """Test creating an Article object."""
        article = Article(title="Test Article")
        assert article.title == "Test Article"
        assert article.subtitle == ""
        assert article.content == ""
        assert article.tags == []
        assert article.keywords == []
        assert article.status == "draft"
        assert article.file_path == ""
    
    def test_article_with_all_fields(self):
        """Test Article with all fields populated."""
        article = Article(
            title="Test Article",
            subtitle="A subtitle",
            content="Article content",
            tags=["python", "testing"],
            keywords=["test", "article"],
            status="public",
            file_path="article.md"
        )
        assert article.title == "Test Article"
        assert article.subtitle == "A subtitle"
        assert article.content == "Article content"
        assert len(article.tags) == 2
        assert len(article.keywords) == 2
        assert article.status == "public"
        assert article.file_path == "article.md"
    
    def test_article_validation_valid(self):
        """Test validation accepts valid article."""
        article = Article(
            title="Test Article",
            content="Content",
            tags=["python", "testing"],
            status="draft",
            file_path="article.md"
        )
        assert article.validate() is True
    
    def test_article_validation_empty_title(self):
        """Test validation rejects empty title."""
        article = Article(title="")
        with pytest.raises(ValueError, match="title cannot be empty"):
            article.validate()
    
    def test_article_validation_whitespace_title(self):
        """Test validation rejects whitespace-only title."""
        article = Article(title="   ")
        with pytest.raises(ValueError, match="title cannot be empty"):
            article.validate()
    
    def test_article_validation_title_too_long(self):
        """Test validation rejects title over 200 characters."""
        article = Article(title="x" * 201)
        with pytest.raises(ValueError, match="title too long"):
            article.validate()
    
    def test_article_validation_invalid_status(self):
        """Test validation rejects invalid status."""
        article = Article(title="Test", status="invalid")
        with pytest.raises(ValueError, match="Invalid status"):
            article.validate()
    
    def test_article_validation_too_many_tags(self):
        """Test validation rejects more than 5 tags."""
        article = Article(
            title="Test",
            tags=["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]
        )
        with pytest.raises(ValueError, match="Too many tags"):
            article.validate()
    
    def test_article_validation_invalid_tag_format(self):
        """Test validation rejects tags with invalid characters."""
        article = Article(title="Test", tags=["valid-tag", "invalid@tag"])
        with pytest.raises(ValueError, match="Invalid tag"):
            article.validate()
    
    def test_article_validation_valid_tag_formats(self):
        """Test validation accepts valid tag formats."""
        article = Article(
            title="Test",
            tags=["python", "web-development", "API Testing"]
        )
        assert article.validate() is True
    
    def test_article_validation_invalid_file_extension(self):
        """Test validation rejects non-markdown file extension."""
        article = Article(title="Test", file_path="article.txt")
        with pytest.raises(ValueError, match="Invalid file extension"):
            article.validate()
    
    def test_article_validation_valid_file_extension(self):
        """Test validation accepts markdown file extension."""
        article = Article(title="Test", file_path="article.md")
        assert article.validate() is True
    
    def test_article_has_required_fields_true(self):
        """Test has_required_fields returns True when fields present."""
        article = Article(title="Test", content="Content")
        assert article.has_required_fields() is True
    
    def test_article_has_required_fields_false_no_title(self):
        """Test has_required_fields returns False without title."""
        article = Article(title="", content="Content")
        assert article.has_required_fields() is False
    
    def test_article_has_required_fields_false_no_content(self):
        """Test has_required_fields returns False without content."""
        article = Article(title="Test", content="")
        assert article.has_required_fields() is False

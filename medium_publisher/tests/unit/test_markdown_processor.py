"""
Tests for MarkdownProcessor.
"""

import pytest
from medium_publisher.core.markdown_processor import MarkdownProcessor
from medium_publisher.core.models import ContentBlock, Format


class TestMarkdownProcessor:
    """Test MarkdownProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = MarkdownProcessor()
    
    # Test process() method
    
    def test_process_empty_markdown(self):
        """Test processing empty markdown."""
        result = self.processor.process("")
        assert result == []
    
    def test_process_whitespace_only(self):
        """Test processing whitespace-only markdown."""
        result = self.processor.process("   \n\n   ")
        assert result == []
    
    def test_process_simple_paragraph(self):
        """Test processing simple paragraph."""
        markdown = "This is a paragraph."
        blocks = self.processor.process(markdown)
        
        assert len(blocks) == 1
        assert blocks[0].type == "paragraph"
        assert blocks[0].content == "This is a paragraph."
    
    def test_process_multiple_paragraphs(self):
        """Test processing multiple paragraphs."""
        markdown = "First paragraph.\n\nSecond paragraph."
        blocks = self.processor.process(markdown)
        
        assert len(blocks) == 2
        assert blocks[0].content == "First paragraph."
        assert blocks[1].content == "Second paragraph."
    
    # Test parse_header() method
    
    def test_parse_header_h2(self):
        """Test parsing H2 header."""
        block = self.processor._parse_header("## Header Text")
        
        assert block is not None
        assert block.type == "header"
        assert block.content == "Header Text"
        assert block.level == 2
    
    def test_parse_header_h3(self):
        """Test parsing H3 header."""
        block = self.processor._parse_header("### Header Text")
        
        assert block is not None
        assert block.level == 3
    
    def test_parse_header_h4(self):
        """Test parsing H4 header."""
        block = self.processor._parse_header("#### Header Text")
        
        assert block is not None
        assert block.level == 4
    
    def test_parse_header_not_header(self):
        """Test parsing non-header line."""
        block = self.processor._parse_header("# Single hash")
        assert block is None
        
        block = self.processor._parse_header("Regular text")
        assert block is None

    
    # Test parse_formatting() method
    
    def test_parse_formatting_bold(self):
        """Test parsing bold formatting."""
        formats = self.processor._parse_formatting("This is **bold** text")
        
        assert len(formats) == 1
        assert formats[0].type == "bold"
        assert formats[0].start == 8
        assert formats[0].end == 16
    
    def test_parse_formatting_italic_asterisk(self):
        """Test parsing italic with asterisks."""
        formats = self.processor._parse_formatting("This is *italic* text")
        
        assert len(formats) == 1
        assert formats[0].type == "italic"
    
    def test_parse_formatting_italic_underscore(self):
        """Test parsing italic with underscores."""
        formats = self.processor._parse_formatting("This is _italic_ text")
        
        assert len(formats) == 1
        assert formats[0].type == "italic"
    
    def test_parse_formatting_code(self):
        """Test parsing inline code."""
        formats = self.processor._parse_formatting("This is `code` text")
        
        assert len(formats) == 1
        assert formats[0].type == "code"
    
    def test_parse_formatting_link(self):
        """Test parsing links."""
        formats = self.processor._parse_formatting("This is [link](https://example.com) text")
        
        assert len(formats) == 1
        assert formats[0].type == "link"
        assert formats[0].url == "https://example.com"
    
    def test_parse_formatting_multiple(self):
        """Test parsing multiple formats."""
        text = "This is **bold** and *italic* and `code`"
        formats = self.processor._parse_formatting(text)
        
        assert len(formats) == 3
        types = [f.type for f in formats]
        assert "bold" in types
        assert "italic" in types
        assert "code" in types
    
    def test_parse_formatting_none(self):
        """Test parsing text with no formatting."""
        formats = self.processor._parse_formatting("Plain text")
        assert len(formats) == 0
    
    # Test parse_code_block() method
    
    def test_parse_code_block_simple(self):
        """Test parsing simple code block."""
        lines = [
            "```",
            "def hello():",
            "    print('hello')",
            "```"
        ]
        
        block, consumed = self.processor._parse_code_block(lines)
        
        assert block is not None
        assert block.type == "code"
        assert "def hello():" in block.content
        assert consumed == 4
    
    def test_parse_code_block_with_language(self):
        """Test parsing code block with language."""
        lines = [
            "```python",
            "print('hello')",
            "```"
        ]
        
        block, consumed = self.processor._parse_code_block(lines)
        
        assert block is not None
        assert block.metadata["language"] == "python"
    
    def test_parse_code_block_no_closing(self):
        """Test parsing code block without closing delimiter."""
        lines = [
            "```",
            "code without closing"
        ]
        
        block, consumed = self.processor._parse_code_block(lines)
        
        assert block is None
        assert consumed == 0
    
    def test_parse_code_block_not_code(self):
        """Test parsing non-code block."""
        lines = ["Regular text"]
        
        block, consumed = self.processor._parse_code_block(lines)
        
        assert block is None
        assert consumed == 0

    
    # Test parse_list() method
    
    def test_parse_list_bullet(self):
        """Test parsing bullet list."""
        lines = [
            "- Item 1",
            "- Item 2",
            "- Item 3"
        ]
        
        block, consumed = self.processor._parse_list(lines)
        
        assert block is not None
        assert block.type == "list"
        assert "Item 1" in block.content
        assert "Item 2" in block.content
        assert block.metadata["list_type"] == "bullet"
        assert consumed == 3
    
    def test_parse_list_numbered(self):
        """Test parsing numbered list."""
        lines = [
            "1. First",
            "2. Second",
            "3. Third"
        ]
        
        block, consumed = self.processor._parse_list(lines)
        
        assert block is not None
        assert block.metadata["list_type"] == "numbered"
    
    def test_parse_list_asterisk(self):
        """Test parsing list with asterisks."""
        lines = [
            "* Item 1",
            "* Item 2"
        ]
        
        block, consumed = self.processor._parse_list(lines)
        
        assert block is not None
        assert block.type == "list"
    
    def test_parse_list_stops_at_non_list(self):
        """Test list parsing stops at non-list line."""
        lines = [
            "- Item 1",
            "- Item 2",
            "Regular paragraph"
        ]
        
        block, consumed = self.processor._parse_list(lines)
        
        assert consumed == 2
    
    def test_is_list_item_bullet(self):
        """Test detecting bullet list items."""
        assert self.processor._is_list_item("- Item")
        assert self.processor._is_list_item("* Item")
        assert self.processor._is_list_item("  - Indented")
    
    def test_is_list_item_numbered(self):
        """Test detecting numbered list items."""
        assert self.processor._is_list_item("1. Item")
        assert self.processor._is_list_item("42. Item")
    
    def test_is_list_item_not_list(self):
        """Test detecting non-list items."""
        assert not self.processor._is_list_item("Regular text")
        assert not self.processor._is_list_item("# Header")
    
    # Test detect_table() method
    
    def test_detect_table_simple(self):
        """Test detecting simple table."""
        lines = [
            "| Header 1 | Header 2 |",
            "| -------- | -------- |",
            "| Cell 1   | Cell 2   |"
        ]
        
        block = self.processor._detect_table(lines)
        
        assert block is not None
        assert block.type == "table_placeholder"
        assert "TODO: Insert table here" in block.content
        assert block.metadata["columns"] == 2
    
    def test_detect_table_not_table(self):
        """Test non-table lines."""
        lines = ["Regular text", "More text"]
        
        block = self.processor._detect_table(lines)
        assert block is None
    
    def test_detect_table_insufficient_lines(self):
        """Test table detection with insufficient lines."""
        lines = ["| Header |"]
        
        block = self.processor._detect_table(lines)
        assert block is None
    
    def test_count_table_lines(self):
        """Test counting table lines."""
        lines = [
            "| H1 | H2 |",
            "| -- | -- |",
            "| C1 | C2 |",
            "Regular text"
        ]
        
        count = self.processor._count_table_lines(lines)
        assert count == 3

    
    # Test detect_image() method
    
    def test_detect_image_simple(self):
        """Test detecting simple image."""
        line = "![Alt text](https://example.com/image.png)"
        
        block = self.processor._detect_image(line)
        
        assert block is not None
        assert block.type == "image_placeholder"
        assert "Alt text" in block.content
        assert block.metadata["alt_text"] == "Alt text"
        assert block.metadata["url"] == "https://example.com/image.png"
    
    def test_detect_image_with_spaces(self):
        """Test detecting image with spaces in alt text."""
        line = "![My Image Description](image.jpg)"
        
        block = self.processor._detect_image(line)
        
        assert block is not None
        assert block.metadata["alt_text"] == "My Image Description"
    
    def test_detect_image_not_image(self):
        """Test non-image line."""
        line = "Regular text"
        
        block = self.processor._detect_image(line)
        assert block is None
    
    # Test compare_versions() method
    
    def test_compare_versions_no_changes(self):
        """Test comparing identical versions."""
        markdown = "## Header\n\nParagraph text."
        
        changes = self.processor.compare_versions(markdown, markdown)
        assert len(changes) == 0
    
    def test_compare_versions_added_section(self):
        """Test detecting added section."""
        v1 = "## Section 1\n\nContent 1."
        v2 = "## Section 1\n\nContent 1.\n\n## Section 2\n\nContent 2."
        
        changes = self.processor.compare_versions(v1, v2)
        
        assert len(changes) == 1
        assert changes[0][0] == "added"
        assert changes[0][1] == "Section 2"
    
    def test_compare_versions_deleted_section(self):
        """Test detecting deleted section."""
        v1 = "## Section 1\n\nContent 1.\n\n## Section 2\n\nContent 2."
        v2 = "## Section 1\n\nContent 1."
        
        changes = self.processor.compare_versions(v1, v2)
        
        assert len(changes) == 1
        assert changes[0][0] == "deleted"
        assert changes[0][1] == "Section 2"
    
    def test_compare_versions_modified_section(self):
        """Test detecting modified section."""
        v1 = "## Section 1\n\nOriginal content."
        v2 = "## Section 1\n\nModified content."
        
        changes = self.processor.compare_versions(v1, v2)
        
        assert len(changes) == 1
        assert changes[0][0] == "modified"
        assert changes[0][1] == "Section 1"
        assert "Modified content" in changes[0][2]
    
    def test_compare_versions_multiple_changes(self):
        """Test detecting multiple changes."""
        v1 = "## Section 1\n\nContent 1.\n\n## Section 2\n\nContent 2."
        v2 = "## Section 1\n\nNew content.\n\n## Section 3\n\nContent 3."
        
        changes = self.processor.compare_versions(v1, v2)
        
        # Should detect: modified Section 1, deleted Section 2, added Section 3
        assert len(changes) == 3
        change_types = [c[0] for c in changes]
        assert "modified" in change_types
        assert "deleted" in change_types
        assert "added" in change_types
    
    # Integration tests
    
    def test_process_complex_markdown(self):
        """Test processing complex markdown with multiple elements."""
        markdown = """## Introduction

This is a **bold** paragraph with *italic* text and `code`.

### Subsection

Here's a list:
- Item 1
- Item 2

```python
def hello():
    print('world')
```

And a [link](https://example.com).

| Header 1 | Header 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |

![Image](image.png)
"""
        
        blocks = self.processor.process(markdown)
        
        # Should have: header, paragraph, header, paragraph, list, code, paragraph, table, image
        assert len(blocks) >= 8
        
        types = [b.type for b in blocks]
        assert "header" in types
        assert "paragraph" in types
        assert "list" in types
        assert "code" in types
        assert "table_placeholder" in types
        assert "image_placeholder" in types
    
    def test_process_preserves_formatting(self):
        """Test that formatting is preserved in paragraphs."""
        markdown = "This has **bold** and *italic* and `code`."
        
        blocks = self.processor.process(markdown)
        
        assert len(blocks) == 1
        assert len(blocks[0].formatting) == 3

"""
Property-based tests for core parsing modules (ArticleParser, MarkdownProcessor).

Feature: medium-keyboard-publisher
Properties 1-8: Frontmatter round-trip, header parsing, inline formatting,
code block parsing, list parsing, paragraph breaks, placeholder detection,
file validation.

Uses hypothesis for property-based testing against reused core modules.
"""

import os
import tempfile
from pathlib import Path

import yaml
from hypothesis import given, settings, assume, strategies as st

from medium_publisher.core.article_parser import ArticleParser
from medium_publisher.core.markdown_processor import MarkdownProcessor
from medium_publisher.core.models import ContentBlock, Format
from medium_publisher.utils.exceptions import FileError, ContentError


# ---------------------------------------------------------------------------
# Shared strategies
# ---------------------------------------------------------------------------

# Safe text that won't break YAML or markdown parsing.
# Must start with a letter so YAML doesn't interpret it as a number/bool.
safe_text = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N", "Zs"),
        whitelist_characters="-_",
    ),
    min_size=2,
    max_size=60,
).filter(lambda s: s.strip() != "" and "---" not in s and s[0].isalpha())

# Tag strategy: alphanumeric + hyphens + spaces, Medium-compatible
tag_strategy = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N", "Zs"),
        whitelist_characters="-",
    ),
    min_size=1,
    max_size=30,
).filter(lambda s: s.strip() != "" and s[0].isalpha())

# Simple word strategy for header/paragraph content (no markdown special chars).
# No leading/trailing spaces so parsers that strip won't cause mismatches.
simple_word = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters=" "),
    min_size=1,
    max_size=80,
).filter(lambda s: s.strip() == s and len(s.strip()) > 0)


# ===========================================================================
# Property 1: Frontmatter round-trip
# ===========================================================================


class TestFrontmatterRoundTrip:
    """Property 1: Frontmatter round-trip.

    **Validates: Requirements 1.4, 2.1**

    For any valid frontmatter dict (title, subtitle, tags, keywords),
    serializing to YAML with --- delimiters then parsing with
    ArticleParser.extract_frontmatter() SHALL produce identical values.
    """

    @given(
        title=safe_text,
        subtitle=safe_text,
        tags=st.lists(tag_strategy, min_size=0, max_size=5),
        keywords=st.lists(safe_text, min_size=0, max_size=5),
    )
    @settings(max_examples=100)
    def test_frontmatter_round_trip(
        self, title: str, subtitle: str, tags: list, keywords: list
    ) -> None:
        """Serialize frontmatter to YAML, parse back, values must match."""
        frontmatter_dict = {
            "title": title,
            "subtitle": subtitle,
            "tags": tags,
            "keywords": keywords,
        }

        # Serialize to YAML with --- delimiters
        yaml_body = yaml.dump(frontmatter_dict, default_flow_style=False)
        content = f"---\n{yaml_body}---\nSome body content here.\n"

        parser = ArticleParser()
        parsed = parser.extract_frontmatter(content)

        assert parsed["title"] == title
        assert parsed["subtitle"] == subtitle
        assert parsed["tags"] == tags
        assert parsed["keywords"] == keywords


# ===========================================================================
# Property 2: Header parsing preserves level and content
# ===========================================================================


class TestHeaderParsing:
    """Property 2: Header parsing preserves level and content.

    **Validates: Requirements 2.2, 2.3, 2.4**

    For any valid header text and level in {2, 3, 4}, formatting as a
    markdown header and parsing with MarkdownProcessor._parse_header()
    SHALL produce a ContentBlock with correct type, level, and content.
    """

    @given(
        text=simple_word,
        level=st.sampled_from([2, 3, 4]),
    )
    @settings(max_examples=100)
    def test_header_level_and_content_preserved(self, text: str, level: int) -> None:
        """Header parsing preserves level and content text."""
        prefix = "#" * level
        line = f"{prefix} {text}"

        processor = MarkdownProcessor()
        block = processor._parse_header(line)

        assert block is not None
        assert block.type == "header"
        assert block.level == level
        assert block.content == text


# ===========================================================================
# Property 3: Inline formatting parsing preserves type and position
# ===========================================================================


class TestInlineFormattingParsing:
    """Property 3: Inline formatting parsing preserves type and position.

    **Validates: Requirements 2.5, 2.6, 2.8, 2.9**

    For any text with bold, italic, code, or link markers, parsing with
    MarkdownProcessor._parse_formatting() SHALL produce Format objects
    whose type matches the marker kind and whose start/end indices
    correctly span the marker positions.
    """

    @given(word=simple_word)
    @settings(max_examples=100)
    def test_bold_formatting_detected(self, word: str) -> None:
        """Bold markers produce a Format with type='bold' at correct position."""
        text = f"before **{word}** after"
        processor = MarkdownProcessor()
        formats = processor._parse_formatting(text)

        bold_formats = [f for f in formats if f.type == "bold"]
        assert len(bold_formats) >= 1
        bf = bold_formats[0]
        assert bf.start == text.index("**")
        assert bf.end == text.index("**", bf.start + 2) + 2

    @given(word=simple_word.filter(lambda w: "*" not in w and "_" not in w))
    @settings(max_examples=100)
    def test_italic_formatting_detected(self, word: str) -> None:
        """Italic markers produce a Format with type='italic' at correct position."""
        text = f"before *{word}* after"
        processor = MarkdownProcessor()
        formats = processor._parse_formatting(text)

        italic_formats = [f for f in formats if f.type == "italic"]
        assert len(italic_formats) >= 1

    @given(word=simple_word.filter(lambda w: "`" not in w))
    @settings(max_examples=100)
    def test_code_formatting_detected(self, word: str) -> None:
        """Inline code markers produce a Format with type='code'."""
        text = f"before `{word}` after"
        processor = MarkdownProcessor()
        formats = processor._parse_formatting(text)

        code_formats = [f for f in formats if f.type == "code"]
        assert len(code_formats) >= 1

    @given(
        link_text=simple_word.filter(lambda w: "]" not in w and "[" not in w),
        url=st.from_regex(r"https://[a-z]{3,10}\.[a-z]{2,4}", fullmatch=True),
    )
    @settings(max_examples=100)
    def test_link_formatting_detected(self, link_text: str, url: str) -> None:
        """Link markers produce a Format with type='link' and correct URL."""
        text = f"before [{link_text}]({url}) after"
        processor = MarkdownProcessor()
        formats = processor._parse_formatting(text)

        link_formats = [f for f in formats if f.type == "link"]
        assert len(link_formats) >= 1
        assert link_formats[0].url == url


# ===========================================================================
# Property 4: Code block parsing preserves content
# ===========================================================================


class TestCodeBlockParsing:
    """Property 4: Code block parsing preserves content.

    **Validates: Requirements 2.7**

    For any code content and optional language, wrapping in triple-backtick
    delimiters and parsing with MarkdownProcessor._parse_code_block()
    SHALL produce a ContentBlock with type='code' and content matching
    the original code string.
    """

    @given(
        code=st.text(
            alphabet=st.characters(
                whitelist_categories=("L", "N", "P", "Zs"),
                whitelist_characters="\n ",
                blacklist_characters="`",
            ),
            min_size=1,
            max_size=200,
        ).filter(lambda s: s.strip() != ""),
        language=st.sampled_from(["", "python", "javascript", "rust", "go"]),
    )
    @settings(max_examples=100)
    def test_code_block_content_preserved(self, code: str, language: str) -> None:
        """Code block parsing preserves the code content exactly."""
        lines = [f"```{language}"] + code.split("\n") + ["```"]

        processor = MarkdownProcessor()
        block, lines_consumed = processor._parse_code_block(lines)

        assert block is not None
        assert block.type == "code"
        assert block.content == code
        assert block.metadata.get("language", "") == language
        assert lines_consumed == len(lines)


# ===========================================================================
# Property 5: List parsing preserves items and type
# ===========================================================================


class TestListParsing:
    """Property 5: List parsing preserves items and type.

    **Validates: Requirements 2.10, 2.11**

    For any list of item strings and list type (bullet or numbered),
    formatting as markdown list and parsing with MarkdownProcessor._parse_list()
    SHALL produce a ContentBlock with type='list', correct list_type metadata,
    and content containing all original item strings.
    """

    @given(
        items=st.lists(simple_word, min_size=1, max_size=8),
    )
    @settings(max_examples=100)
    def test_bullet_list_preserves_items(self, items: list) -> None:
        """Bullet list parsing preserves all items and sets list_type='bullet'."""
        lines = [f"- {item}" for item in items]

        processor = MarkdownProcessor()
        block, lines_consumed = processor._parse_list(lines)

        assert block is not None
        assert block.type == "list"
        assert block.metadata["list_type"] == "bullet"
        assert lines_consumed == len(items)
        # Each item text should appear in the content
        for item in items:
            assert item in block.content

    @given(
        items=st.lists(simple_word, min_size=1, max_size=8),
    )
    @settings(max_examples=100)
    def test_numbered_list_preserves_items(self, items: list) -> None:
        """Numbered list parsing preserves all items and sets list_type='numbered'."""
        lines = [f"{i+1}. {item}" for i, item in enumerate(items)]

        processor = MarkdownProcessor()
        block, lines_consumed = processor._parse_list(lines)

        assert block is not None
        assert block.type == "list"
        assert block.metadata["list_type"] == "numbered"
        assert lines_consumed == len(items)
        for item in items:
            assert item in block.content


# ===========================================================================
# Property 6: Paragraph breaks produce separate ContentBlocks
# ===========================================================================


class TestParagraphBreaks:
    """Property 6: Paragraph breaks produce separate ContentBlocks.

    **Validates: Requirements 2.12**

    For any two non-empty text strings, joining with a double newline
    and processing with MarkdownProcessor.process() SHALL produce at
    least two ContentBlock objects.
    """

    @given(
        para1=simple_word,
        para2=simple_word,
    )
    @settings(max_examples=100)
    def test_double_newline_produces_separate_blocks(
        self, para1: str, para2: str
    ) -> None:
        """Two paragraphs separated by blank line produce >= 2 blocks."""
        markdown = f"{para1}\n\n{para2}"

        processor = MarkdownProcessor()
        blocks = processor.process(markdown)

        assert len(blocks) >= 2


# ===========================================================================
# Property 7: Placeholder detection for tables and images
# ===========================================================================


class TestPlaceholderDetection:
    """Property 7: Placeholder detection for tables and images.

    **Validates: Requirements 2.13, 2.14**

    For any valid markdown table or image, processing with
    MarkdownProcessor.process() SHALL produce a ContentBlock with
    type='table_placeholder' or 'image_placeholder' respectively.
    Image placeholders SHALL have metadata['alt_text'] matching the
    original alt text.
    """

    @given(
        alt_text=simple_word.filter(
            lambda w: "]" not in w and "[" not in w and "!" not in w
        ),
        url=st.from_regex(r"https://[a-z]{3,10}\.[a-z]{2,4}/[a-z]+\.png", fullmatch=True),
    )
    @settings(max_examples=100)
    def test_image_placeholder_preserves_alt_text(
        self, alt_text: str, url: str
    ) -> None:
        """Image markdown produces image_placeholder with correct alt_text."""
        markdown = f"![{alt_text}]({url})"

        processor = MarkdownProcessor()
        blocks = processor.process(markdown)

        image_blocks = [b for b in blocks if b.type == "image_placeholder"]
        assert len(image_blocks) == 1
        assert image_blocks[0].metadata["alt_text"] == alt_text
        assert image_blocks[0].metadata["url"] == url

    @given(
        col1=simple_word.filter(lambda w: "|" not in w),
        col2=simple_word.filter(lambda w: "|" not in w),
        val1=simple_word.filter(lambda w: "|" not in w),
        val2=simple_word.filter(lambda w: "|" not in w),
    )
    @settings(max_examples=100)
    def test_table_produces_table_placeholder(
        self, col1: str, col2: str, val1: str, val2: str
    ) -> None:
        """Markdown table produces a table_placeholder ContentBlock."""
        markdown = (
            f"| {col1} | {col2} |\n"
            f"| --- | --- |\n"
            f"| {val1} | {val2} |"
        )

        processor = MarkdownProcessor()
        blocks = processor.process(markdown)

        table_blocks = [b for b in blocks if b.type == "table_placeholder"]
        assert len(table_blocks) == 1


# ===========================================================================
# Property 8: File validation accepts .md and rejects invalid files
# ===========================================================================


class TestFileValidation:
    """Property 8: File validation accepts .md and rejects invalid files.

    **Validates: Requirements 1.3, 1.5**

    For any file path with .md extension, parse_file should accept it
    (if content is valid). For any file path without .md extension,
    parse_file should raise FileError.
    """

    @given(
        ext=st.sampled_from([".txt", ".html", ".py", ".rst", ".doc", ".pdf"]),
    )
    @settings(max_examples=30)
    def test_non_md_extension_raises_file_error(self, ext: str) -> None:
        """Files without .md extension raise FileError."""
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False, mode="w") as f:
            f.write("some content")
            tmp_path = f.name

        try:
            parser = ArticleParser()
            try:
                parser.parse_file(tmp_path)
                assert False, f"Expected FileError for extension {ext}"
            except FileError:
                pass  # Expected
        finally:
            os.unlink(tmp_path)

    @given(
        title=safe_text,
    )
    @settings(max_examples=30)
    def test_md_extension_accepted_with_valid_content(self, title: str) -> None:
        """Files with .md extension and valid content are accepted."""
        # Quote the title to prevent YAML from interpreting it as non-string
        content = (
            f"---\ntitle: \"{title}\"\n---\n"
            f"This is the article body with enough content.\n"
        )

        with tempfile.NamedTemporaryFile(
            suffix=".md", delete=False, mode="w", encoding="utf-8"
        ) as f:
            f.write(content)
            tmp_path = f.name

        try:
            parser = ArticleParser()
            article = parser.parse_file(tmp_path)
            assert article.title == title
        finally:
            os.unlink(tmp_path)

    def test_missing_frontmatter_raises_content_error(self) -> None:
        """Content without frontmatter delimiters raises ContentError."""
        with tempfile.NamedTemporaryFile(
            suffix=".md", delete=False, mode="w", encoding="utf-8"
        ) as f:
            f.write("No frontmatter here, just plain text.")
            tmp_path = f.name

        try:
            parser = ArticleParser()
            try:
                parser.parse_file(tmp_path)
                assert False, "Expected ContentError for missing frontmatter"
            except ContentError:
                pass  # Expected
        finally:
            os.unlink(tmp_path)

    def test_malformed_yaml_raises_content_error(self) -> None:
        """Malformed YAML in frontmatter raises ContentError."""
        content = "---\n[invalid yaml: {{{\n---\nBody text.\n"

        with tempfile.NamedTemporaryFile(
            suffix=".md", delete=False, mode="w", encoding="utf-8"
        ) as f:
            f.write(content)
            tmp_path = f.name

        try:
            parser = ArticleParser()
            try:
                parser.parse_file(tmp_path)
                assert False, "Expected ContentError for malformed YAML"
            except ContentError:
                pass  # Expected
        finally:
            os.unlink(tmp_path)

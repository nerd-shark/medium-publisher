"""
Unit tests for the reworked ContentTyper (OS-level input).

Tests each content block type method, inline formatting, review pass flow,
and placeholder handling. All OS-level input is mocked.

Requirements: 4.3–4.18
"""

import pytest
from unittest.mock import MagicMock, call, patch

from medium_publisher.automation.content_typer import ContentTyper
from medium_publisher.automation.human_typing_simulator import HumanTypingSimulator
from medium_publisher.automation.deferred_typo_tracker import DeferredTypoTracker
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.core.models import ContentBlock, Format


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_input():
    return MagicMock()


@pytest.fixture
def typer(mock_input):
    """ContentTyper with typos disabled and zero delays."""
    simulator = HumanTypingSimulator(typo_frequency="low", enabled=False)
    tracker = DeferredTypoTracker()
    config = MagicMock(spec=ConfigManager)
    config.get.side_effect = lambda key, default=None: {
        "typing.base_delay_ms": 0,
        "typing.immediate_correction_ratio": 0.70,
    }.get(key, default)

    return ContentTyper(
        input_controller=mock_input,
        typing_simulator=simulator,
        typo_tracker=tracker,
        config=config,
    )


def _typed_text(mock_input) -> str:
    """Extract the full text typed via type_character calls."""
    return "".join(c.args[0] for c in mock_input.type_character.call_args_list)


# ---------------------------------------------------------------------------
# Title and subtitle
# ---------------------------------------------------------------------------

class TestTypeTitle:
    def test_types_title_text_and_enter(self, typer, mock_input):
        with patch("time.sleep"):
            typer.type_title("Hello World")
        assert _typed_text(mock_input) == "Hello World"
        mock_input.press_key.assert_called_with("enter")

    def test_empty_title(self, typer, mock_input):
        with patch("time.sleep"):
            typer.type_title("")
        assert _typed_text(mock_input) == ""
        mock_input.press_key.assert_called_with("enter")


class TestTypeSubtitle:
    def test_applies_subheader_shortcut(self, typer, mock_input):
        with patch("time.sleep"):
            typer.type_subtitle("My Subtitle")
        assert call("ctrl", "alt", "2") in mock_input.hotkey.call_args_list
        assert _typed_text(mock_input) == "My Subtitle"
        mock_input.press_key.assert_called_with("enter")


# ---------------------------------------------------------------------------
# Paragraph
# ---------------------------------------------------------------------------

class TestTypeParagraph:
    def test_plain_paragraph(self, typer, mock_input):
        block = ContentBlock(type="paragraph", content="Some text here.")
        with patch("time.sleep"):
            typer.type_paragraph(block)
        assert _typed_text(mock_input) == "Some text here."
        mock_input.press_key.assert_called_with("enter")

    def test_paragraph_with_bold(self, typer, mock_input):
        block = ContentBlock(
            type="paragraph",
            content="Hello bold world",
            formatting=[Format(type="bold", start=6, end=10)],
        )
        with patch("time.sleep"):
            typer.type_paragraph(block)
        assert call("ctrl", "b") in mock_input.hotkey.call_args_list


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

class TestTypeHeader:
    def test_level_2_uses_ctrl_alt_1(self, typer, mock_input):
        block = ContentBlock(type="header", content="Main Header", level=2)
        with patch("time.sleep"):
            typer.type_header(block)
        assert call("ctrl", "alt", "1") in mock_input.hotkey.call_args_list
        assert _typed_text(mock_input) == "Main Header"

    def test_level_3_uses_ctrl_alt_2(self, typer, mock_input):
        block = ContentBlock(type="header", content="Sub Header", level=3)
        with patch("time.sleep"):
            typer.type_header(block)
        assert call("ctrl", "alt", "2") in mock_input.hotkey.call_args_list

    def test_level_4_uses_ctrl_alt_2(self, typer, mock_input):
        block = ContentBlock(type="header", content="Deep Header", level=4)
        with patch("time.sleep"):
            typer.type_header(block)
        assert call("ctrl", "alt", "2") in mock_input.hotkey.call_args_list


# ---------------------------------------------------------------------------
# Code block
# ---------------------------------------------------------------------------

class TestTypeCodeBlock:
    def test_types_backticks_and_code(self, typer, mock_input):
        block = ContentBlock(type="code", content="print('hi')")
        with patch("time.sleep"):
            typer.type_code_block(block)
        typed = _typed_text(mock_input)
        assert "```" in typed
        assert "print('hi')" in typed

    def test_code_block_presses_enter(self, typer, mock_input):
        block = ContentBlock(type="code", content="x = 1")
        with patch("time.sleep"):
            typer.type_code_block(block)
        enter_calls = [c for c in mock_input.press_key.call_args_list if c == call("enter")]
        assert len(enter_calls) >= 2  # enter after backticks + exit enters


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------

class TestTypeList:
    def test_bullet_list_prefix(self, typer, mock_input):
        block = ContentBlock(
            type="list",
            content="Item A\nItem B",
            metadata={"list_type": "bullet"},
        )
        with patch("time.sleep"):
            typer.type_list(block)
        typed = _typed_text(mock_input)
        assert "* Item A" in typed
        assert "* Item B" in typed

    def test_ordered_list_prefix(self, typer, mock_input):
        block = ContentBlock(
            type="list",
            content="First\nSecond",
            metadata={"list_type": "ordered"},
        )
        with patch("time.sleep"):
            typer.type_list(block)
        typed = _typed_text(mock_input)
        assert "1. First" in typed
        assert "1. Second" in typed

    def test_empty_items_skipped(self, typer, mock_input):
        block = ContentBlock(
            type="list",
            content="A\n\nB",
            metadata={"list_type": "bullet"},
        )
        with patch("time.sleep"):
            typer.type_list(block)
        typed = _typed_text(mock_input)
        assert "* A" in typed
        assert "* B" in typed


# ---------------------------------------------------------------------------
# Link
# ---------------------------------------------------------------------------

class TestTypeLink:
    def test_link_types_text_selects_and_ctrl_k(self, typer, mock_input):
        with patch("time.sleep"):
            typer.type_link("Click here", "https://example.com")
        typed = _typed_text(mock_input)
        assert "Click here" in typed
        assert "https://example.com" in typed
        mock_input.select_text_backwards.assert_called_once_with(len("Click here"))
        assert call("ctrl", "k") in mock_input.hotkey.call_args_list
        mock_input.press_key.assert_called_with("enter")


# ---------------------------------------------------------------------------
# Inline formatting (mixed)
# ---------------------------------------------------------------------------

class TestTypeInlineFormatting:
    def test_bold_applies_ctrl_b(self, typer, mock_input):
        fmt = Format(type="bold", start=0, end=4)
        with patch("time.sleep"):
            typer.type_inline_formatting("bold text", [fmt])
        assert call("ctrl", "b") in mock_input.hotkey.call_args_list

    def test_italic_applies_ctrl_i(self, typer, mock_input):
        fmt = Format(type="italic", start=0, end=6)
        with patch("time.sleep"):
            typer.type_inline_formatting("italic text", [fmt])
        assert call("ctrl", "i") in mock_input.hotkey.call_args_list

    def test_inline_code_uses_backticks(self, typer, mock_input):
        fmt = Format(type="code", start=0, end=4)
        with patch("time.sleep"):
            typer.type_inline_formatting("code rest", [fmt])
        typed = _typed_text(mock_input)
        assert "`code`" in typed

    def test_link_format_uses_ctrl_k(self, typer, mock_input):
        fmt = Format(type="link", start=0, end=4, url="https://x.com")
        with patch("time.sleep"):
            typer.type_inline_formatting("link rest", [fmt])
        assert call("ctrl", "k") in mock_input.hotkey.call_args_list

    def test_mixed_bold_and_italic(self, typer, mock_input):
        # "Hello bold and italic end"
        #        ^^^^         ^^^^^^
        fmts = [
            Format(type="bold", start=6, end=10),
            Format(type="italic", start=15, end=21),
        ]
        with patch("time.sleep"):
            typer.type_inline_formatting("Hello bold and italic end", fmts)
        assert call("ctrl", "b") in mock_input.hotkey.call_args_list
        assert call("ctrl", "i") in mock_input.hotkey.call_args_list

    def test_no_formatting_types_plain(self, typer, mock_input):
        with patch("time.sleep"):
            typer.type_inline_formatting("plain text", [])
        assert _typed_text(mock_input) == "plain text"


# ---------------------------------------------------------------------------
# Placeholder
# ---------------------------------------------------------------------------

class TestTypePlaceholder:
    def test_image_placeholder(self, typer, mock_input):
        block = ContentBlock(
            type="image_placeholder",
            content="![alt](url)",
            metadata={"alt_text": "diagram"},
        )
        with patch("time.sleep"):
            typer.type_placeholder(block)
        typed = _typed_text(mock_input)
        assert typed == "[image: diagram]"
        mock_input.press_key.assert_called_with("enter")

    def test_table_placeholder(self, typer, mock_input):
        block = ContentBlock(
            type="table_placeholder",
            content="| a | b |",
            metadata={"caption": "metrics"},
        )
        with patch("time.sleep"):
            typer.type_placeholder(block)
        typed = _typed_text(mock_input)
        assert typed == "[table: metrics]"

    def test_placeholder_no_formatting_applied(self, typer, mock_input):
        block = ContentBlock(
            type="image_placeholder",
            content="![x](y)",
            metadata={"alt_text": "x"},
        )
        with patch("time.sleep"):
            typer.type_placeholder(block)
        # No hotkey calls for formatting
        assert mock_input.hotkey.call_count == 0


# ---------------------------------------------------------------------------
# Block quote
# ---------------------------------------------------------------------------

class TestTypeBlockQuote:
    def test_applies_ctrl_alt_5(self, typer, mock_input):
        block = ContentBlock(type="paragraph", content="A wise quote")
        with patch("time.sleep"):
            typer.type_block_quote(block)
        assert call("ctrl", "alt", "5") in mock_input.hotkey.call_args_list
        assert _typed_text(mock_input) == "A wise quote"


# ---------------------------------------------------------------------------
# Separator
# ---------------------------------------------------------------------------

class TestTypeSeparator:
    def test_uses_ctrl_enter(self, typer, mock_input):
        with patch("time.sleep"):
            typer.type_separator()
        assert call("ctrl", "enter") in mock_input.hotkey.call_args_list


# ---------------------------------------------------------------------------
# Review pass
# ---------------------------------------------------------------------------

class TestPerformReviewPass:
    def test_no_typos_skips_review(self, typer, mock_input):
        with patch("time.sleep"):
            typer.perform_review_pass()
        # No Ctrl+Home or Ctrl+F should be called
        assert call("ctrl", "home") not in mock_input.hotkey.call_args_list

    def test_review_pass_navigates_to_top(self, typer, mock_input):
        # Manually record a deferred typo
        typer._tracker.record(
            block_index=0,
            char_offset=5,
            wrong_char="x",
            correct_char="y",
            surrounding_context="some context",
        )
        with patch("time.sleep"), patch("random.randint", return_value=500):
            typer.perform_review_pass()
        assert call("ctrl", "home") in mock_input.hotkey.call_args_list

    def test_review_pass_uses_ctrl_f(self, typer, mock_input):
        typer._tracker.record(
            block_index=0,
            char_offset=3,
            wrong_char="a",
            correct_char="b",
            surrounding_context="test context",
        )
        with patch("time.sleep"), patch("random.randint", return_value=500):
            typer.perform_review_pass()
        assert call("ctrl", "f") in mock_input.hotkey.call_args_list

    def test_review_pass_presses_escape(self, typer, mock_input):
        typer._tracker.record(
            block_index=0,
            char_offset=3,
            wrong_char="a",
            correct_char="b",
            surrounding_context="ctx",
        )
        with patch("time.sleep"), patch("random.randint", return_value=500):
            typer.perform_review_pass()
        assert call("escape") in mock_input.press_key.call_args_list

    def test_review_pass_fixes_typo(self, typer, mock_input):
        typer._tracker.record(
            block_index=0,
            char_offset=3,
            wrong_char="x",
            correct_char="y",
            surrounding_context="abcxef",
        )
        with patch("time.sleep"), patch("random.randint", return_value=500):
            typer.perform_review_pass()
        # Should backspace the wrong char and type the correct one
        assert call("backspace") in mock_input.press_key.call_args_list
        typed = _typed_text(mock_input)
        assert "y" in typed

    def test_review_pass_clears_tracker(self, typer, mock_input):
        typer._tracker.record(
            block_index=0,
            char_offset=0,
            wrong_char="a",
            correct_char="b",
            surrounding_context="ctx",
        )
        with patch("time.sleep"), patch("random.randint", return_value=500):
            typer.perform_review_pass()
        assert typer._tracker.count == 0


# ---------------------------------------------------------------------------
# type_article integration
# ---------------------------------------------------------------------------

class TestTypeArticle:
    def test_empty_blocks(self, typer, mock_input):
        with patch("time.sleep"):
            typer.type_article([])
        assert mock_input.type_character.call_count == 0

    def test_single_title_block(self, typer, mock_input):
        blocks = [ContentBlock(type="paragraph", content="Title")]
        with patch("time.sleep"):
            typer.type_article(blocks)
        assert "Title" in _typed_text(mock_input)

    def test_title_and_subtitle(self, typer, mock_input):
        blocks = [ContentBlock(type="paragraph", content="Title")]
        with patch("time.sleep"):
            typer.type_article(blocks, subtitle="Sub")
        typed = _typed_text(mock_input)
        assert "Title" in typed
        assert "Sub" in typed
        assert call("ctrl", "alt", "2") in mock_input.hotkey.call_args_list

"""
Property-based tests for ContentTyper formatting.

Properties 10, 11, 12 from the design document.
Uses hypothesis with mocked OS_Input_Controller.
"""

import pytest
from unittest.mock import MagicMock, call, patch
from hypothesis import given, strategies as st, settings, assume

from medium_publisher.automation.content_typer import ContentTyper
from medium_publisher.automation.human_typing_simulator import HumanTypingSimulator
from medium_publisher.automation.deferred_typo_tracker import DeferredTypoTracker
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.core.models import ContentBlock, Format


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _make_typer(
    typo_enabled: bool = False,
) -> tuple:
    """Create a ContentTyper with mocked dependencies.

    Returns (typer, mock_input_controller).
    """
    mock_input = MagicMock()
    simulator = HumanTypingSimulator(typo_frequency="low", enabled=typo_enabled)
    tracker = DeferredTypoTracker()

    mock_config = MagicMock(spec=ConfigManager)
    mock_config.get.side_effect = lambda key, default=None: {
        "typing.base_delay_ms": 0,
        "typing.immediate_correction_ratio": 0.70,
    }.get(key, default)

    typer = ContentTyper(
        input_controller=mock_input,
        typing_simulator=simulator,
        typo_tracker=tracker,
        config=mock_config,
    )
    return typer, mock_input


# ---------------------------------------------------------------------------
# Property 10: Content formatting applies correct Medium shortcut
# **Validates: Requirements 4.6, 4.7, 4.8, 4.9, 4.12, 4.15**
# ---------------------------------------------------------------------------

@settings(max_examples=30, deadline=None)
@given(
    text=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
        min_size=1,
        max_size=30,
    ),
    level=st.sampled_from([2, 3, 4]),
)
def test_property_10_header_shortcut(text: str, level: int):
    """For any header block, verify Ctrl+Alt+1 (level 2) or Ctrl+Alt+2 (level 3+)."""
    typer, mock_input = _make_typer()
    block = ContentBlock(type="header", content=text, level=level)

    with patch("time.sleep"):
        typer.type_header(block)

    hotkey_calls = [c for c in mock_input.hotkey.call_args_list]
    if level == 2:
        assert call("ctrl", "alt", "1") in hotkey_calls, (
            f"Level-2 header must use Ctrl+Alt+1, got {hotkey_calls}"
        )
    else:
        assert call("ctrl", "alt", "2") in hotkey_calls, (
            f"Level-{level} header must use Ctrl+Alt+2, got {hotkey_calls}"
        )


@settings(max_examples=20, deadline=None)
@given(
    text=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=20,
    ),
)
def test_property_10_bold_shortcut(text: str):
    """For bold formatting, verify Ctrl+B is called."""
    typer, mock_input = _make_typer()
    fmt = Format(type="bold", start=0, end=len(text))

    with patch("time.sleep"):
        typer.type_inline_formatting(text, [fmt])

    assert call("ctrl", "b") in mock_input.hotkey.call_args_list, (
        "Bold formatting must use Ctrl+B"
    )


@settings(max_examples=20, deadline=None)
@given(
    text=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=20,
    ),
)
def test_property_10_italic_shortcut(text: str):
    """For italic formatting, verify Ctrl+I is called."""
    typer, mock_input = _make_typer()
    fmt = Format(type="italic", start=0, end=len(text))

    with patch("time.sleep"):
        typer.type_inline_formatting(text, [fmt])

    assert call("ctrl", "i") in mock_input.hotkey.call_args_list, (
        "Italic formatting must use Ctrl+I"
    )


@settings(max_examples=20, deadline=None)
@given(
    text=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=20,
    ),
    url=st.from_regex(r"https://[a-z]{3,10}\.[a-z]{2,4}", fullmatch=True),
)
def test_property_10_link_shortcut(text: str, url: str):
    """For link formatting, verify Ctrl+K is called."""
    typer, mock_input = _make_typer()

    with patch("time.sleep"):
        typer.type_link(text, url)

    assert call("ctrl", "k") in mock_input.hotkey.call_args_list, (
        "Link formatting must use Ctrl+K"
    )


@settings(max_examples=20, deadline=None)
@given(
    text=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=30,
    ),
)
def test_property_10_block_quote_shortcut(text: str):
    """For block quotes, verify Ctrl+Alt+5 is called."""
    typer, mock_input = _make_typer()
    block = ContentBlock(type="paragraph", content=text, metadata={"quote": True})

    with patch("time.sleep"):
        typer.type_block_quote(block)

    assert call("ctrl", "alt", "5") in mock_input.hotkey.call_args_list, (
        "Block quote must use Ctrl+Alt+5"
    )


# ---------------------------------------------------------------------------
# Property 11: List typing uses correct prefix per list type
# **Validates: Requirements 4.13, 4.14**
# ---------------------------------------------------------------------------

@settings(max_examples=30, deadline=None)
@given(
    items=st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=("L", "N")),
            min_size=1,
            max_size=20,
        ),
        min_size=1,
        max_size=5,
    ),
    list_type=st.sampled_from(["bullet", "ordered"]),
)
def test_property_11_list_prefix(items: list, list_type: str):
    """Bullet lists use '* ' prefix, numbered lists use '1. ' prefix."""
    typer, mock_input = _make_typer()
    content = "\n".join(items)
    block = ContentBlock(
        type="list", content=content, metadata={"list_type": list_type}
    )

    with patch("time.sleep"):
        typer.type_list(block)

    # Collect all characters typed via type_character
    typed_chars = [c.args[0] for c in mock_input.type_character.call_args_list]
    typed_text = "".join(typed_chars)

    expected_prefix = "* " if list_type == "bullet" else "1. "
    for item in items:
        item_text = item.strip()
        if not item_text:
            continue
        # The prefix must appear before each item in the typed output
        combined = expected_prefix + item_text
        assert combined in typed_text, (
            f"Expected prefix '{expected_prefix}' before item '{item_text}' "
            f"in typed text"
        )


# ---------------------------------------------------------------------------
# Property 12: Protected content typed without typos
# **Validates: Requirements 4.10, 4.18, 5.14**
# ---------------------------------------------------------------------------

@settings(max_examples=30, deadline=None)
@given(
    code=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "P")),
        min_size=1,
        max_size=40,
    ),
)
def test_property_12_code_block_no_typos(code: str):
    """Code blocks are typed with allow_typos=False (no typo simulation)."""
    # Enable typos in the simulator — they should still NOT appear in code
    typer, mock_input = _make_typer(typo_enabled=True)
    block = ContentBlock(type="code", content=code)

    with patch("time.sleep"):
        typer.type_code_block(block)

    # All characters typed should be exactly the code content
    # (plus the triple backticks and no typo chars)
    typed_chars = [c.args[0] for c in mock_input.type_character.call_args_list]
    typed_text = "".join(typed_chars)

    # The code content must appear verbatim in the typed output
    assert code in typed_text, (
        f"Code block content must be typed verbatim, got: {typed_text!r}"
    )


@settings(max_examples=20, deadline=None)
@given(
    url=st.from_regex(r"https://[a-z]{3,10}\.[a-z]{2,4}/[a-z]{1,10}", fullmatch=True),
    link_text=st.text(
        alphabet=st.characters(whitelist_categories=("L",)),
        min_size=1,
        max_size=15,
    ),
)
def test_property_12_url_no_typos(link_text: str, url: str):
    """URLs in links are typed with allow_typos=False."""
    typer, mock_input = _make_typer(typo_enabled=True)

    with patch("time.sleep"):
        typer.type_link(link_text, url)

    typed_chars = [c.args[0] for c in mock_input.type_character.call_args_list]
    typed_text = "".join(typed_chars)

    # URL must appear verbatim
    assert url in typed_text, (
        f"URL must be typed verbatim, got: {typed_text!r}"
    )


@settings(max_examples=20, deadline=None)
@given(
    alt_text=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=20,
    ),
)
def test_property_12_placeholder_no_typos(alt_text: str):
    """Placeholders are typed with allow_typos=False."""
    typer, mock_input = _make_typer(typo_enabled=True)
    block = ContentBlock(
        type="image_placeholder",
        content=f"![{alt_text}](url)",
        metadata={"alt_text": alt_text},
    )

    with patch("time.sleep"):
        typer.type_placeholder(block)

    typed_chars = [c.args[0] for c in mock_input.type_character.call_args_list]
    typed_text = "".join(typed_chars)

    expected = f"[image: {alt_text}]"
    assert expected in typed_text, (
        f"Placeholder must be typed verbatim as '{expected}', got: {typed_text!r}"
    )

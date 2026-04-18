"""
Content Typer Module (OS-level input)

Types article content into the focused window using OS-level keyboard events
via OS_Input_Controller. Handles formatting, typo simulation with immediate
and deferred correction, and a review pass for deferred typos.
"""

import random
import time
from typing import List, Optional

from medium_publisher.automation.os_input_controller import OS_Input_Controller
from medium_publisher.automation.human_typing_simulator import HumanTypingSimulator
from medium_publisher.automation.deferred_typo_tracker import DeferredTypoTracker
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.core.models import ContentBlock, Format
from medium_publisher.utils.logger import get_logger

logger = get_logger("automation.content_typer")


class ContentTyper:
    """Types article content into the focused window using OS-level input.

    Dependencies are injected: OS_Input_Controller for keyboard events,
    HumanTypingSimulator for typo generation and timing, DeferredTypoTracker
    for recording typos fixed in the review pass, and ConfigManager for
    typing configuration.
    """

    def __init__(
        self,
        input_controller: OS_Input_Controller,
        typing_simulator: HumanTypingSimulator,
        typo_tracker: DeferredTypoTracker,
        config: ConfigManager,
    ) -> None:
        self._input = input_controller
        self._simulator = typing_simulator
        self._tracker = typo_tracker
        self._config = config

        self._base_delay_ms: int = config.get("typing.base_delay_ms", 200)
        self._immediate_ratio: float = config.get(
            "typing.immediate_correction_ratio", 0.70
        )
        self._current_block_index: int = 0

        logger.info(
            "ContentTyper initialized: base_delay=%dms, immediate_ratio=%.0f%%",
            self._base_delay_ms,
            self._immediate_ratio * 100,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def type_article(
        self, blocks: List[ContentBlock], subtitle: str = ""
    ) -> None:
        """Type a complete article: title block, optional subtitle, then content blocks.

        The first block is assumed to be the title. After typing all blocks
        a review pass corrects any deferred typos.

        Args:
            blocks: Ordered list of ContentBlocks (first is title).
            subtitle: Optional subtitle text.
        """
        if not blocks:
            logger.warning("type_article called with empty block list")
            return

        # First block is the title
        self.type_title(blocks[0].content)
        self._current_block_index = 0

        if subtitle:
            self.type_subtitle(subtitle)

        # Remaining blocks
        for idx, block in enumerate(blocks[1:], start=1):
            self._current_block_index = idx
            self._type_block(block)

        # Review pass for deferred typos
        self.perform_review_pass()
        logger.info("Article typing complete (%d blocks)", len(blocks))

    def type_title(self, title: str) -> None:
        """Type the article title and press Enter."""
        logger.info("Typing title: %s", title[:40])
        self._type_with_typos(title)
        self._input.press_key("enter")

    def type_subtitle(self, subtitle: str) -> None:
        """Type subtitle, apply Subheader format (Ctrl+Alt+2), press Enter."""
        logger.info("Typing subtitle")
        self._input.hotkey("ctrl", "alt", "2")
        self._delay()
        self._type_with_typos(subtitle)
        self._input.press_key("enter")

    def type_paragraph(self, block: ContentBlock) -> None:
        """Type paragraph text with inline formatting, then Enter."""
        if block.formatting:
            self.type_inline_formatting(block.content, block.formatting)
        else:
            self._type_with_typos(block.content)
        self._input.press_key("enter")

    def type_header(self, block: ContentBlock) -> None:
        """Type header with correct Medium shortcut.

        Level 2 → Ctrl+Alt+1 (Header)
        Level 3+ → Ctrl+Alt+2 (Subheader)

        After typing the header text and pressing Enter, reset to normal
        paragraph formatting so the next block isn't styled as a header.
        """
        if block.level == 2:
            self._input.hotkey("ctrl", "alt", "1")
        else:
            self._input.hotkey("ctrl", "alt", "2")
        self._delay()
        self._type_with_typos(block.content)
        self._input.press_key("enter")
        # Reset to normal paragraph formatting (Ctrl+Alt+5 in Medium)
        self._input.hotkey("ctrl", "alt", "5")
        self._delay()

    def type_code_block(self, block: ContentBlock) -> None:
        """Type triple backticks, code content (no typos), then exit code block."""
        # Enter code block mode
        self._type_with_typos("```", allow_typos=False)
        self._input.press_key("enter")
        self._delay()

        # Type code without typos
        self._type_with_typos(block.content, allow_typos=False)

        # Exit code block
        self._input.press_key("enter")
        self._input.press_key("enter")

    def type_list(self, block: ContentBlock) -> None:
        """Type list items with '* ' or '1. ' prefix per item."""
        list_type = block.metadata.get("list_type", "bullet")
        items = block.content.split("\n")

        for item in items:
            item_text = item.strip()
            if not item_text:
                continue
            if list_type == "ordered":
                self._type_with_typos("1. ", allow_typos=False)
            else:
                self._type_with_typos("* ", allow_typos=False)
            self._type_with_typos(item_text)
            self._input.press_key("enter")

    def type_link(self, text: str, url: str) -> None:
        """Type link text, select it, Ctrl+K, type URL, Enter."""
        self._type_with_typos(text)
        self._input.select_text_backwards(len(text))
        self._delay()
        self._input.hotkey("ctrl", "k")
        self._delay()
        self._type_with_typos(url, allow_typos=False)
        self._input.press_key("enter")

    def type_inline_formatting(
        self, text: str, formatting: List[Format]
    ) -> None:
        """Type text and apply bold/italic/code/link formatting to marked ranges.

        Formatting is applied by sorting ranges, typing segments between them
        normally, and applying the appropriate shortcut for each formatted range.
        """
        if not formatting:
            self._type_with_typos(text)
            return

        # Sort formatting by start position
        sorted_fmt = sorted(formatting, key=lambda f: f.start)
        pos = 0

        for fmt in sorted_fmt:
            # Type text before this format range
            if fmt.start > pos:
                self._type_with_typos(text[pos : fmt.start])

            segment = text[fmt.start : fmt.end]

            if fmt.type == "code":
                # Inline code: backtick, text, backtick
                self._type_with_typos("`", allow_typos=False)
                self._type_with_typos(segment, allow_typos=False)
                self._type_with_typos("`", allow_typos=False)
            elif fmt.type == "link":
                self.type_link(segment, fmt.url)
            elif fmt.type == "bold":
                self._type_with_typos(segment)
                self._input.select_text_backwards(len(segment))
                self._delay()
                self._input.hotkey("ctrl", "b")
                self._delay()
                self._input.press_key("right")
            elif fmt.type == "italic":
                self._type_with_typos(segment)
                self._input.select_text_backwards(len(segment))
                self._delay()
                self._input.hotkey("ctrl", "i")
                self._delay()
                self._input.press_key("right")

            pos = fmt.end

        # Type remaining text after last format
        if pos < len(text):
            self._type_with_typos(text[pos:])

    def type_placeholder(self, block: ContentBlock) -> None:
        """Type placeholder text without formatting or typos."""
        if block.type == "image_placeholder":
            alt = block.metadata.get("alt_text", "")
            placeholder = f"[image: {alt}]" if alt else "[image]"
        elif block.type == "table_placeholder":
            caption = block.metadata.get("caption", "")
            placeholder = f"[table: {caption}]" if caption else "[table]"
        else:
            placeholder = f"[{block.type}]"

        self._type_with_typos(placeholder, allow_typos=False)
        self._input.press_key("enter")

    def type_block_quote(self, block: ContentBlock) -> None:
        """Apply Ctrl+Alt+5 then type quote text."""
        self._input.hotkey("ctrl", "alt", "5")
        self._delay()
        self._type_with_typos(block.content)
        self._input.press_key("enter")

    def type_separator(self) -> None:
        """Insert separator via Ctrl+Enter."""
        self._input.hotkey("ctrl", "enter")
        self._delay()

    # ------------------------------------------------------------------
    # Review pass
    # ------------------------------------------------------------------

    def perform_review_pass(self) -> None:
        """Navigate to top and fix each deferred typo using Ctrl+F.

        For each deferred typo:
        1. Ctrl+F to open find dialog
        2. Type surrounding_context to locate the typo
        3. Close find dialog (Escape)
        4. Navigate to the typo position and fix it
        """
        typos = self._tracker.get_all()
        if not typos:
            logger.info("No deferred typos to fix")
            return

        logger.info("Starting review pass: %d deferred typos", len(typos))

        # Go to top of document
        self._input.hotkey("ctrl", "home")
        self._delay()

        for typo in typos:
            # Open find dialog
            self._input.hotkey("ctrl", "f")
            self._delay()

            # Type surrounding context to locate the typo
            self._type_with_typos(typo.surrounding_context, allow_typos=False)
            self._delay()

            # Close find dialog
            self._input.press_key("escape")
            self._delay()

            # Simulate reading pause
            pause_ms = random.randint(500, 2000)
            time.sleep(pause_ms / 1000.0)

            # Select the wrong character and replace with correct one
            self._input.press_key("backspace")
            self._type_with_typos(typo.correct_char, allow_typos=False)

        self._tracker.clear()
        logger.info("Review pass complete")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _type_block(self, block: ContentBlock) -> None:
        """Dispatch a ContentBlock to the appropriate typing method."""
        dispatch = {
            "paragraph": self.type_paragraph,
            "header": self.type_header,
            "code": self.type_code_block,
            "list": self.type_list,
            "table_placeholder": self.type_placeholder,
            "image_placeholder": self.type_placeholder,
        }

        # Check for block quote via metadata
        if block.metadata.get("quote"):
            self.type_block_quote(block)
            return

        handler = dispatch.get(block.type)
        if handler:
            handler(block)
        else:
            logger.warning("Unknown block type '%s', typing as paragraph", block.type)
            self.type_paragraph(block)

    def _type_with_typos(
        self, text: str, allow_typos: bool = True
    ) -> None:
        """Type text with human-like typos.

        When allow_typos is True and the simulator decides to make a typo:
        - 70% (configurable) are corrected immediately: type wrong char,
          continue 1-3 chars, backspace to delete, retype correctly.
        - 30% are deferred: record in tracker for the review pass.

        Args:
            text: Text to type.
            allow_typos: False for code, URLs, placeholders.
        """
        if not text:
            return

        i = 0
        while i < len(text):
            char = text[i]

            # Typing delay with variation
            delay_ms = self._simulator.get_typing_delay(self._base_delay_ms)
            time.sleep(delay_ms / 1000.0)

            # Thinking pause
            pause = self._simulator.get_thinking_pause()
            if pause > 0:
                time.sleep(pause / 1000.0)

            if allow_typos and self._simulator.should_make_typo():
                typo_char = self._simulator.generate_typo(char)

                if random.random() < self._immediate_ratio:
                    # Immediate correction: type typo, continue 1-3 chars, backspace, retype
                    self._input.type_character(typo_char)
                    correction_delay = self._simulator.get_correction_delay()

                    # Type a few more correct chars before noticing
                    extra_typed = 0
                    for j in range(correction_delay):
                        next_idx = i + 1 + j
                        if next_idx < len(text):
                            time.sleep(delay_ms / 1000.0)
                            self._input.type_character(text[next_idx])
                            extra_typed += 1

                    # Backspace to delete typo + extra chars
                    for _ in range(1 + extra_typed):
                        self._input.press_key("backspace")
                        time.sleep(delay_ms / 2000.0)

                    # Retype correct characters
                    self._input.type_character(char)
                    for j in range(extra_typed):
                        next_idx = i + 1 + j
                        if next_idx < len(text):
                            time.sleep(delay_ms / 1000.0)
                            self._input.type_character(text[next_idx])

                    # Advance past the extra chars we already retyped
                    i += 1 + extra_typed
                else:
                    # Deferred correction: type wrong char, record for review pass
                    self._input.type_character(typo_char)

                    # Build surrounding context (~20 chars)
                    ctx_start = max(0, i - 10)
                    ctx_end = min(len(text), i + 10)
                    context = text[ctx_start:ctx_end]

                    self._tracker.record(
                        block_index=self._current_block_index,
                        char_offset=i,
                        wrong_char=typo_char,
                        correct_char=char,
                        surrounding_context=context,
                    )
                    i += 1
            else:
                self._input.type_character(char)
                i += 1

    def _delay(self, ms: Optional[int] = None) -> None:
        """Sleep for a short formatting delay.

        Args:
            ms: Milliseconds to sleep. Defaults to 50.
        """
        time.sleep((ms or 50) / 1000.0)

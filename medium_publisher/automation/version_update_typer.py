"""
Version Update Typer — applies change instructions to a Medium draft.

Orchestrates the find → select → delete → type cycle for each
ChangeInstruction using OS-level keyboard automation.  All keyboard
actions flow through OS_Input_Controller (which checks EmergencyStop
and FocusWindowDetector before every action).  Content typing is
delegated to ContentTyper for human-like behavior and formatting.
"""

import time
from typing import Callable, List, Optional

from medium_publisher.automation.os_input_controller import OS_Input_Controller
from medium_publisher.automation.content_typer import ContentTyper
from medium_publisher.core.change_parser import (
    ChangeAction,
    ChangeInstruction,
    ChangeParser,
)
from medium_publisher.core.config_manager import ConfigManager
from medium_publisher.core.models import ContentBlock, Format, UpdateResult
from medium_publisher.utils.exceptions import (
    EmergencyStopError,
    FocusLostError,
    InputControlError,
)
from medium_publisher.utils.logger import get_logger

logger = get_logger("automation.version_update_typer")


class VersionUpdateTyper:
    """Applies change instructions to a Medium draft via OS-level keyboard automation.

    For each ChangeInstruction the workflow is:
    1. Open Ctrl+F and type the search marker to locate the section.
    2. Close the find dialog and position the cursor.
    3. Select old content using Shift+Arrow keys.
    4. Delete the selected content.
    5. Type replacement content via ContentTyper (with formatting / typos).

    All keyboard actions go through OS_Input_Controller which checks
    EmergencyStop and FocusWindowDetector before every action.
    """

    def __init__(
        self,
        input_controller: OS_Input_Controller,
        content_typer: ContentTyper,
        change_parser: ChangeParser,
        config: ConfigManager,
    ) -> None:
        """Initialise with injected dependencies.

        Args:
            input_controller: OS-level keyboard/mouse controller.
            content_typer: Types content with human-like behaviour.
            change_parser: Extracts search markers from instructions.
            config: Application configuration.
        """
        self._input = input_controller
        self._typer = content_typer
        self._parser = change_parser
        self._config = config

        # Configurable delays (milliseconds)
        self._find_delay_ms: int = config.get("version_update.find_delay_ms", 300)
        self._action_delay_ms: int = config.get("version_update.action_delay_ms", 150)

        logger.info(
            "VersionUpdateTyper initialized: find_delay=%dms, action_delay=%dms",
            self._find_delay_ms,
            self._action_delay_ms,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def apply_changes(
        self,
        instructions: List[ChangeInstruction],
        article_content: str,
        status_cb: Optional[Callable[[str], None]] = None,
    ) -> UpdateResult:
        """Apply all change instructions to the currently focused Medium editor.

        Instructions are sorted into document order (top → bottom) before
        processing.  Instructions whose search marker cannot be found are
        skipped with a logged warning.

        Args:
            instructions: Change instructions to apply.
            article_content: Full article markdown (used for search-marker
                extraction and document-order sorting).
            status_cb: Optional callback for status messages.

        Returns:
            UpdateResult with counts of applied, skipped, and failed
            instructions.
        """
        total = len(instructions)
        logger.info("apply_changes: processing %d instructions", total)

        result = UpdateResult(
            success=False,
            total_instructions=total,
        )

        if not instructions:
            logger.warning("apply_changes called with empty instruction list")
            return result

        # Sort instructions by document position (top → bottom)
        sorted_instructions = self._sort_by_document_order(instructions, article_content)

        for idx, instruction in enumerate(sorted_instructions):
            section_name = instruction.section or instruction.raw_instruction[:40]
            if status_cb:
                status_cb(f"Applying {idx + 1}/{total}: {section_name}")

            try:
                applied = self._apply_single_change(instruction, article_content)
                if applied:
                    result.applied_count += 1
                    result.applied_sections.append(section_name)
                    logger.info("Instruction %d/%d applied: %s", idx + 1, total, section_name)
                else:
                    result.skipped_count += 1
                    result.skipped_sections.append((section_name, "section not found"))
                    logger.warning("Instruction %d/%d skipped: %s", idx + 1, total, section_name)

            except EmergencyStopError:
                logger.warning("Emergency stop during instruction %d/%d", idx + 1, total)
                self._input.release_all_keys()
                result.failed_count += 1
                result.failed_sections.append((section_name, "emergency stop"))
                raise  # Propagate so the workflow layer can save progress

            except FocusLostError:
                logger.warning("Focus lost during instruction %d/%d", idx + 1, total)
                result.failed_count += 1
                result.failed_sections.append((section_name, "focus lost"))
                raise  # Propagate so the workflow layer can pause

            except (InputControlError, Exception) as exc:
                logger.error(
                    "Instruction %d/%d failed (%s): %s",
                    idx + 1, total, section_name, exc,
                )
                result.failed_count += 1
                result.failed_sections.append((section_name, str(exc)))
                # Continue with remaining instructions

        result.success = result.applied_count > 0
        logger.info(
            "apply_changes complete: applied=%d, skipped=%d, failed=%d",
            result.applied_count, result.skipped_count, result.failed_count,
        )
        return result

    # ------------------------------------------------------------------
    # Single-instruction dispatch
    # ------------------------------------------------------------------

    def _apply_single_change(
        self,
        instruction: ChangeInstruction,
        article_content: str,
    ) -> bool:
        """Apply a single change instruction.

        Dispatches to the appropriate handler based on the instruction's
        action type.

        Args:
            instruction: The change instruction to apply.
            article_content: Full article markdown for marker extraction.

        Returns:
            True if the instruction was applied successfully, False if
            the target section was not found and the instruction was skipped.
        """
        action = instruction.action

        if action in (ChangeAction.ADD, ChangeAction.INSERT_AFTER, ChangeAction.INSERT_BEFORE):
            return self._handle_add(instruction, article_content)
        elif action in (ChangeAction.REPLACE, ChangeAction.UPDATE):
            return self._handle_replace(instruction, article_content)
        elif action == ChangeAction.DELETE:
            return self._handle_delete(instruction, article_content)
        else:
            logger.warning("Unknown action '%s', skipping instruction", action)
            return False

    # ------------------------------------------------------------------
    # Action handlers
    # ------------------------------------------------------------------

    def _handle_add(
        self, instruction: ChangeInstruction, article_content: str
    ) -> bool:
        """Handle ADD / INSERT_AFTER / INSERT_BEFORE instructions.

        Navigates to the referenced position section, then types the new
        content after (or before) it.

        Returns:
            True on success, False if the reference section was not found.
        """
        markers = self._parser.extract_search_markers(instruction, article_content)

        # For ADD with no position reference, append at end of document
        if not markers["section_found"] and instruction.action == ChangeAction.ADD:
            logger.info("ADD with no anchor — moving to end of document")
            self._input.hotkey("ctrl", "end")
            self._delay(self._action_delay_ms)
            self._input.press_key("enter")
            self._delay(self._action_delay_ms)
            if instruction.new_content:
                self._type_replacement(instruction.new_content, [])
            return True

        if not markers["section_found"]:
            logger.warning(
                "Reference section not found for %s: %s",
                instruction.action.value, instruction.section,
            )
            return False

        # Navigate to the reference section
        if not self._find_section(markers["start_marker"]):
            return False

        if instruction.action == ChangeAction.INSERT_BEFORE:
            # Move to start of the found line, then insert above
            self._input.press_key("home")
            self._delay(self._action_delay_ms)
            self._input.press_key("enter")
            self._input.press_key("up")
            self._delay(self._action_delay_ms)
        else:
            # INSERT_AFTER / ADD: move to end of section
            if markers.get("end_marker"):
                # Navigate to end marker to find section boundary
                if not self._find_section(markers["end_marker"]):
                    # Fallback: just go to end of current line
                    self._input.press_key("end")
            else:
                self._input.press_key("end")
            self._delay(self._action_delay_ms)
            self._input.press_key("enter")
            self._delay(self._action_delay_ms)

        if instruction.new_content:
            self._type_replacement(instruction.new_content, [])

        return True

    def _handle_replace(
        self, instruction: ChangeInstruction, article_content: str
    ) -> bool:
        """Handle REPLACE / UPDATE instructions.

        Finds the section, selects old content, deletes it, then types
        the replacement content.

        Returns:
            True on success, False if the section was not found.
        """
        markers = self._parser.extract_search_markers(instruction, article_content)

        if not markers["section_found"]:
            logger.warning(
                "Section not found for %s: %s",
                instruction.action.value, instruction.section,
            )
            return False

        if not self._find_section(markers["start_marker"]):
            return False

        # Calculate character count of old section for selection
        old_content = self._extract_section_content(
            article_content, markers["start_marker"], markers.get("end_marker")
        )
        if old_content:
            self._select_and_delete(len(old_content))
        else:
            logger.warning("Could not determine old content length for '%s'", instruction.section)

        # Type replacement content
        if instruction.new_content:
            self._type_replacement(instruction.new_content, [])

        return True

    def _handle_delete(
        self, instruction: ChangeInstruction, article_content: str
    ) -> bool:
        """Handle DELETE instructions.

        Finds the section, selects content including header, and deletes
        it without typing replacement content.

        Returns:
            True on success, False if the section was not found.
        """
        markers = self._parser.extract_search_markers(instruction, article_content)

        if not markers["section_found"]:
            logger.warning(
                "Section not found for DELETE: %s", instruction.section,
            )
            return False

        if not self._find_section(markers["start_marker"]):
            return False

        # Select and delete the entire section (header + body)
        old_content = self._extract_section_content(
            article_content, markers["start_marker"], markers.get("end_marker")
        )
        if old_content:
            self._select_and_delete(len(old_content))
        else:
            logger.warning("Could not determine section length for DELETE '%s'", instruction.section)

        return True

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _find_section(self, search_marker: str) -> bool:
        """Open Ctrl+F, type the search marker, close the dialog.

        Args:
            search_marker: Text to type into the browser find dialog.

        Returns:
            True if the find operation completed (we assume the browser
            highlights the match).  False if the marker is empty.
        """
        if not search_marker:
            logger.warning("_find_section called with empty search marker")
            return False

        logger.debug("_find_section: searching for '%s'", search_marker[:50])

        # Open find dialog
        self._input.hotkey("ctrl", "f")
        self._delay(self._find_delay_ms)

        # Type the search marker (no typos — this is a literal search)
        self._input.type_text(search_marker, delay_ms=20)
        self._delay(self._find_delay_ms)

        # Close find dialog — cursor should now be at the found text
        self._input.press_key("escape")
        self._delay(self._action_delay_ms)

        return True

    def _select_and_delete(self, char_count: int) -> None:
        """Select *char_count* characters forward using Shift+Right, then delete.

        Args:
            char_count: Number of characters to select and delete.
        """
        if char_count <= 0:
            return

        logger.debug("_select_and_delete: selecting %d characters", char_count)

        # Select characters using Shift+Right arrow
        for _ in range(char_count):
            self._input.hotkey("shift", "right")

        self._delay(self._action_delay_ms)

        # Delete the selection
        self._input.press_key("backspace")
        self._delay(self._action_delay_ms)

    def _type_replacement(
        self,
        new_content: str,
        formatting: List[Format],
    ) -> None:
        """Type replacement content via ContentTyper with formatting.

        Builds a ContentBlock and delegates to the appropriate ContentTyper
        method based on content characteristics.

        Args:
            new_content: The replacement text to type.
            formatting: List of Format objects for inline formatting.
        """
        if not new_content:
            return

        logger.debug("_type_replacement: typing %d chars", len(new_content))

        # Build a ContentBlock for ContentTyper dispatch
        block = self._content_to_block(new_content, formatting)

        dispatch = {
            "paragraph": self._typer.type_paragraph,
            "header": self._typer.type_header,
            "code": self._typer.type_code_block,
            "list": self._typer.type_list,
            "table_placeholder": self._typer.type_placeholder,
            "image_placeholder": self._typer.type_placeholder,
        }

        handler = dispatch.get(block.type)
        if handler:
            handler(block)
        else:
            # Fallback: type as paragraph
            self._typer.type_paragraph(block)

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------

    def _sort_by_document_order(
        self,
        instructions: List[ChangeInstruction],
        article_content: str,
    ) -> List[ChangeInstruction]:
        """Sort instructions by their section's position in the document.

        Instructions whose section is not found are placed at the end.

        Args:
            instructions: Unsorted change instructions.
            article_content: Full article markdown.

        Returns:
            Instructions sorted by ascending document position.
        """
        def _position_key(instr: ChangeInstruction) -> int:
            markers = self._parser.extract_search_markers(instr, article_content)
            if markers["section_found"] and markers.get("line_number") is not None:
                return markers["line_number"]
            # Unknown position → sort to end
            return 999_999

        return sorted(instructions, key=_position_key)

    def _extract_section_content(
        self,
        article_content: str,
        start_marker: str,
        end_marker: Optional[str],
    ) -> Optional[str]:
        """Extract the text between *start_marker* and *end_marker*.

        Args:
            article_content: Full article markdown.
            start_marker: Text marking the start of the section.
            end_marker: Text marking the end (next section header), or
                None to take everything until the end of the document.

        Returns:
            The section text, or None if the start marker is not found.
        """
        if not start_marker:
            return None

        start_idx = article_content.find(start_marker)
        if start_idx == -1:
            return None

        if end_marker:
            end_idx = article_content.find(end_marker, start_idx + len(start_marker))
            if end_idx == -1:
                # End marker not found — take to end of document
                return article_content[start_idx:]
            return article_content[start_idx:end_idx]

        return article_content[start_idx:]

    @staticmethod
    def _content_to_block(
        content: str, formatting: List[Format]
    ) -> ContentBlock:
        """Infer a ContentBlock type from raw content text.

        Simple heuristic:
        - Lines starting with ``#`` → header (level derived from ``#`` count)
        - Lines starting with triple backticks → code
        - Lines starting with ``* `` or ``1. `` → list
        - Everything else → paragraph

        Args:
            content: Raw text content.
            formatting: Inline formatting to attach.

        Returns:
            A ContentBlock with inferred type.
        """
        stripped = content.strip()

        if stripped.startswith("```"):
            # Strip the backtick fences for the code block content
            lines = stripped.split("\n")
            code_lines = lines[1:-1] if len(lines) > 2 else lines[1:]
            return ContentBlock(
                type="code",
                content="\n".join(code_lines),
                formatting=formatting,
            )

        if stripped.startswith("#"):
            # Count heading level
            level = 0
            for ch in stripped:
                if ch == "#":
                    level += 1
                else:
                    break
            level = max(2, min(level, 4))  # Clamp to 2–4
            header_text = stripped.lstrip("#").strip()
            return ContentBlock(
                type="header",
                content=header_text,
                formatting=formatting,
                level=level,
            )

        if stripped.startswith("* ") or stripped.startswith("- ") or stripped.startswith("1. "):
            return ContentBlock(
                type="list",
                content=content,
                formatting=formatting,
            )

        return ContentBlock(
            type="paragraph",
            content=content,
            formatting=formatting,
        )

    def _delay(self, ms: int) -> None:
        """Sleep for *ms* milliseconds."""
        time.sleep(ms / 1000.0)

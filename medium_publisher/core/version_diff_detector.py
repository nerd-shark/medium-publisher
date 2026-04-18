"""
Version Diff Detector for comparing article versions.

Wraps MarkdownProcessor.compare_versions() and converts raw diff tuples
into ChangeInstruction objects compatible with VersionUpdateTyper.
"""

from typing import List

from .markdown_processor import MarkdownProcessor
from .change_parser import ChangeInstruction, ChangeAction
from medium_publisher.utils.logger import get_logger
from medium_publisher.utils.exceptions import FileError


logger = get_logger("VersionDiffDetector")

# Mapping from compare_versions() change_type strings to ChangeAction enum
_CHANGE_TYPE_MAP = {
    "added": ChangeAction.ADD,
    "modified": ChangeAction.REPLACE,
    "deleted": ChangeAction.DELETE,
}


class VersionDiffDetector:
    """Detects changes between two article versions and produces ChangeInstructions.

    Wraps MarkdownProcessor.compare_versions() to convert diff results
    into the same ChangeInstruction format used by ChangeParser, enabling
    a unified processing pipeline in VersionUpdateTyper.
    """

    def __init__(self, markdown_processor: MarkdownProcessor):
        """
        Args:
            markdown_processor: Injected MarkdownProcessor for diff comparison.
        """
        self._processor = markdown_processor
        self.logger = logger

    def detect_changes(
        self, old_file: str, new_file: str
    ) -> List[ChangeInstruction]:
        """Compare two version files and return structured change instructions.

        Reads both files, calls compare_versions(), and maps each diff tuple
        to a ChangeInstruction.

        Args:
            old_file: Path to the previous version markdown file.
            new_file: Path to the current version markdown file.

        Returns:
            List of ChangeInstruction objects sorted by document order.

        Raises:
            FileError: If either file cannot be read.
        """
        self.logger.info(
            "Detecting changes between versions",
            extra={"context": f"old={old_file}, new={new_file}"},
        )

        old_content = self._read_file(old_file)
        new_content = self._read_file(new_file)

        diffs = self._processor.compare_versions(old_content, new_content)
        self.logger.info(
            "Diff comparison complete",
            extra={"context": f"{len(diffs)} differences found"},
        )

        instructions = [
            self._diff_to_instruction(change_type, section_id, content)
            for change_type, section_id, content in diffs
        ]

        sorted_instructions = self._sort_by_document_order(
            instructions, new_content
        )
        return sorted_instructions

    def _diff_to_instruction(
        self, change_type: str, section_id: str, new_content: str
    ) -> ChangeInstruction:
        """Convert a single diff tuple to a ChangeInstruction.

        Args:
            change_type: One of 'added', 'modified', 'deleted'.
            section_id: Header text identifying the section.
            new_content: New content for the section (empty for deletes).

        Returns:
            A ChangeInstruction with the appropriate ChangeAction.
        """
        action = _CHANGE_TYPE_MAP.get(change_type)
        if action is None:
            self.logger.warning(
                "Unknown change type, defaulting to REPLACE",
                extra={"context": f"change_type={change_type}"},
            )
            action = ChangeAction.REPLACE

        return ChangeInstruction(
            action=action,
            section=section_id,
            new_content=new_content if new_content else None,
            raw_instruction=f"{change_type}: {section_id}",
        )

    def _sort_by_document_order(
        self,
        instructions: List[ChangeInstruction],
        article_content: str,
    ) -> List[ChangeInstruction]:
        """Sort instructions by their section's position in the document.

        Sections that appear earlier in the document are processed first.
        Sections not found in the document are placed at the end.

        Args:
            instructions: Unsorted list of ChangeInstructions.
            article_content: Full markdown content of the new version.

        Returns:
            Instructions sorted by ascending document position.
        """
        content_lower = article_content.lower()

        def _position_key(instruction: ChangeInstruction) -> int:
            if not instruction.section:
                return len(article_content)
            idx = content_lower.find(instruction.section.lower())
            return idx if idx >= 0 else len(article_content)

        return sorted(instructions, key=_position_key)

    @staticmethod
    def _read_file(file_path: str) -> str:
        """Read a markdown file and return its content.

        Args:
            file_path: Path to the file.

        Returns:
            File content as a string.

        Raises:
            FileError: If the file cannot be read.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileError(
                f"Version file not found: {file_path}",
                details={"path": file_path},
            )
        except OSError as e:
            raise FileError(
                f"Cannot read version file: {file_path}",
                details={"path": file_path, "error": str(e)},
            )

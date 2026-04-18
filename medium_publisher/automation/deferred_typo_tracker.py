"""
Deferred typo tracker for the review pass.

Records typos intentionally left uncorrected during typing,
to be fixed in a review pass at the end of the document.
"""

from typing import List

from medium_publisher.core.models import DeferredTypo
from medium_publisher.utils.logger import get_logger

logger = get_logger("automation.deferred_typo_tracker")


class DeferredTypoTracker:
    """Records and retrieves deferred typos for the review pass.

    Typos are stored in insertion order and returned sorted by
    document position (block_index, then char_offset) so the
    review pass can process them top-to-bottom.
    """

    def __init__(self) -> None:
        self._typos: List[DeferredTypo] = []

    def record(
        self,
        block_index: int,
        char_offset: int,
        wrong_char: str,
        correct_char: str,
        surrounding_context: str,
    ) -> None:
        """Record a deferred typo for later correction.

        Args:
            block_index: Index of the ContentBlock containing the typo.
            char_offset: Character offset within the block's typed text.
            wrong_char: The incorrect character that was typed.
            correct_char: The character that should have been typed.
            surrounding_context: ~20 chars of surrounding text for Ctrl+F search.
        """
        typo = DeferredTypo(
            block_index=block_index,
            char_offset=char_offset,
            wrong_char=wrong_char,
            correct_char=correct_char,
            surrounding_context=surrounding_context,
        )
        self._typos.append(typo)
        logger.debug(
            "Recorded deferred typo: block=%d offset=%d '%s'->'%s'",
            block_index,
            char_offset,
            wrong_char,
            correct_char,
        )

    def get_all(self) -> List[DeferredTypo]:
        """Return all deferred typos sorted in document order.

        Sorted by (block_index, char_offset) so the review pass
        can process corrections from top to bottom.
        """
        return sorted(
            self._typos,
            key=lambda t: (t.block_index, t.char_offset),
        )

    def clear(self) -> None:
        """Clear all recorded typos (after review pass completes)."""
        count = len(self._typos)
        self._typos.clear()
        logger.info("Cleared %d deferred typos", count)

    @property
    def count(self) -> int:
        """Number of deferred typos pending correction."""
        return len(self._typos)

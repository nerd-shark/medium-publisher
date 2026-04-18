"""
Property-based tests for DeferredTypoTracker.

Feature: medium-keyboard-publisher
Property 17: Deferred typo recording preserves all fields

**Validates: Requirements 5.7**
"""

from hypothesis import given, settings, strategies as st

from medium_publisher.automation.deferred_typo_tracker import DeferredTypoTracker


# --- Strategies ---

single_char = st.text(
    min_size=1,
    max_size=1,
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "S")),
)

context_text = st.text(
    min_size=1,
    max_size=50,
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "S", "Z")),
)

typo_record = st.fixed_dictionaries(
    {
        "block_index": st.integers(min_value=0, max_value=10000),
        "char_offset": st.integers(min_value=0, max_value=100000),
        "wrong_char": single_char,
        "correct_char": single_char,
        "surrounding_context": context_text,
    }
)


class TestDeferredTypoTrackerProperty17:
    """Property 17: Deferred typo recording preserves all fields.

    **Validates: Requirements 5.7**

    For any block index, character offset, wrong character, correct character,
    and surrounding context string, recording via DeferredTypoTracker.record()
    and retrieving via get_all() SHALL return a DeferredTypo with identical fields.
    """

    @given(
        block_index=st.integers(min_value=0, max_value=10000),
        char_offset=st.integers(min_value=0, max_value=100000),
        wrong_char=single_char,
        correct_char=single_char,
        surrounding_context=context_text,
    )
    @settings(max_examples=100)
    def test_record_and_retrieve_preserves_fields(
        self,
        block_index: int,
        char_offset: int,
        wrong_char: str,
        correct_char: str,
        surrounding_context: str,
    ) -> None:
        """Recording a typo and retrieving it preserves every field."""
        tracker = DeferredTypoTracker()
        tracker.record(block_index, char_offset, wrong_char, correct_char, surrounding_context)

        typos = tracker.get_all()
        assert len(typos) == 1

        typo = typos[0]
        assert typo.block_index == block_index
        assert typo.char_offset == char_offset
        assert typo.wrong_char == wrong_char
        assert typo.correct_char == correct_char
        assert typo.surrounding_context == surrounding_context

    @given(records=st.lists(typo_record, min_size=2, max_size=20))
    @settings(max_examples=50)
    def test_get_all_returns_document_order(self, records: list) -> None:
        """Typos returned by get_all() are sorted by (block_index, char_offset)."""
        tracker = DeferredTypoTracker()
        for rec in records:
            tracker.record(**rec)

        typos = tracker.get_all()
        assert len(typos) == len(records)

        for i in range(len(typos) - 1):
            current = (typos[i].block_index, typos[i].char_offset)
            nxt = (typos[i + 1].block_index, typos[i + 1].char_offset)
            assert current <= nxt, (
                f"Typos not in document order: {current} > {nxt}"
            )

    @given(records=st.lists(typo_record, min_size=1, max_size=10))
    @settings(max_examples=50)
    def test_count_matches_recorded(self, records: list) -> None:
        """count property equals the number of recorded typos."""
        tracker = DeferredTypoTracker()
        for rec in records:
            tracker.record(**rec)
        assert tracker.count == len(records)

    @given(records=st.lists(typo_record, min_size=1, max_size=10))
    @settings(max_examples=50)
    def test_clear_removes_all(self, records: list) -> None:
        """clear() removes all recorded typos."""
        tracker = DeferredTypoTracker()
        for rec in records:
            tracker.record(**rec)
        assert tracker.count > 0

        tracker.clear()
        assert tracker.count == 0
        assert tracker.get_all() == []

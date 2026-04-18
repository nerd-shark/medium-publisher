"""
Property-based tests for data models.

Feature: medium-keyboard-publisher
Property 17: Deferred typo recording preserves all fields

Validates: Requirements 5.7
"""

from hypothesis import given, settings, strategies as st

from medium_publisher.core.models import DeferredTypo


# Strategy for generating printable single characters (non-empty)
single_char = st.text(min_size=1, max_size=1, alphabet=st.characters(
    whitelist_categories=("L", "N", "P", "S"),
))

# Strategy for generating surrounding context strings (~1-50 chars)
context_text = st.text(min_size=1, max_size=50, alphabet=st.characters(
    whitelist_categories=("L", "N", "P", "S", "Z"),
))


class TestDeferredTypoRoundTrip:
    """Property 17: Deferred typo recording preserves all fields.

    **Validates: Requirements 5.7**

    For any block index, character offset, wrong character, correct character,
    and surrounding context string, creating a DeferredTypo and accessing its
    fields SHALL return values identical to the originals.
    """

    @given(
        block_index=st.integers(min_value=0, max_value=10000),
        char_offset=st.integers(min_value=0, max_value=100000),
        wrong_char=single_char,
        correct_char=single_char,
        surrounding_context=context_text,
    )
    @settings(max_examples=100)
    def test_all_fields_preserved(
        self,
        block_index: int,
        char_offset: int,
        wrong_char: str,
        correct_char: str,
        surrounding_context: str,
    ) -> None:
        """Creating a DeferredTypo preserves every field exactly."""
        typo = DeferredTypo(
            block_index=block_index,
            char_offset=char_offset,
            wrong_char=wrong_char,
            correct_char=correct_char,
            surrounding_context=surrounding_context,
        )

        assert typo.block_index == block_index
        assert typo.char_offset == char_offset
        assert typo.wrong_char == wrong_char
        assert typo.correct_char == correct_char
        assert typo.surrounding_context == surrounding_context

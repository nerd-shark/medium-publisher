"""
Property-based tests for validation functions.

Tests Properties 21, 22, and 23 from the design document:
- Property 21: Draft URL validation
- Property 22: Placeholder listing includes all placeholders
- Property 23: Tag validation enforces max 5 and valid characters
"""

import re
from typing import List

import pytest
from hypothesis import given, strategies as st, settings, assume

from medium_publisher.utils.validators import (
    validate_draft_url,
    validate_and_truncate_tags,
    list_placeholders,
)
from medium_publisher.core.models import ContentBlock


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Strategy for valid Medium hex-style IDs (alphanumeric)
medium_id_st = st.from_regex(r"[a-z0-9]{8,12}", fullmatch=True)

# Strategy for valid URL slugs
slug_st = st.from_regex(r"[a-z][a-z0-9\-]{2,30}", fullmatch=True)

# Strategy for valid Medium usernames (alphanumeric + underscores)
username_st = st.from_regex(r"[a-zA-Z][a-zA-Z0-9_]{1,20}", fullmatch=True)

# Strategy for publication subdomains
publication_st = st.from_regex(r"[a-z][a-z0-9]{2,15}", fullmatch=True)

# Strategy for valid tag strings (alphanumeric + hyphens + spaces)
valid_tag_st = st.from_regex(r"[a-zA-Z][a-zA-Z0-9 \-]{0,30}", fullmatch=True)

# Strategy for tags with invalid characters
invalid_tag_st = st.from_regex(r"[a-zA-Z]+[!@#$%^&*()+=]+", fullmatch=True)


class TestProperty21DraftUrlValidation:
    """Property 21: Draft URL validation.

    Valid Medium URLs accepted, non-Medium URLs rejected.

    **Validates: Requirements 7.2**
    """

    @given(story_id=medium_id_st)
    @settings(max_examples=50)
    def test_p_id_edit_urls_accepted(self, story_id: str) -> None:
        """https://medium.com/p/<id>/edit is accepted."""
        url = f"https://medium.com/p/{story_id}/edit"
        result = validate_draft_url(url)
        assert result.is_valid, f"Expected valid for {url}: {result.error_message}"

    @given(story_id=medium_id_st)
    @settings(max_examples=50)
    def test_p_id_urls_accepted(self, story_id: str) -> None:
        """https://medium.com/p/<id> is accepted."""
        url = f"https://medium.com/p/{story_id}"
        result = validate_draft_url(url)
        assert result.is_valid, f"Expected valid for {url}: {result.error_message}"

    @given(user=username_st, slug=slug_st)
    @settings(max_examples=50)
    def test_username_story_urls_accepted(self, user: str, slug: str) -> None:
        """https://medium.com/@<user>/<slug>-<id> is accepted."""
        url = f"https://medium.com/@{user}/{slug}"
        result = validate_draft_url(url)
        assert result.is_valid, f"Expected valid for {url}: {result.error_message}"

    @given(pub=publication_st, slug=slug_st)
    @settings(max_examples=50)
    def test_publication_subdomain_urls_accepted(self, pub: str, slug: str) -> None:
        """https://<publication>.medium.com/<slug>-<id> is accepted."""
        url = f"https://{pub}.medium.com/{slug}"
        result = validate_draft_url(url)
        assert result.is_valid, f"Expected valid for {url}: {result.error_message}"

    @given(domain=st.from_regex(r"[a-z]{3,10}\.(com|org|net)", fullmatch=True))
    @settings(max_examples=50)
    def test_non_medium_domains_rejected(self, domain: str) -> None:
        """Non-Medium domains are rejected."""
        assume(not domain.endswith("medium.com"))
        url = f"https://{domain}/@user/story-slug"
        result = validate_draft_url(url)
        assert not result.is_valid, f"Expected invalid for {url}"

    def test_new_story_url_accepted(self) -> None:
        """https://medium.com/new-story is accepted."""
        result = validate_draft_url("https://medium.com/new-story")
        assert result.is_valid

    def test_empty_url_accepted(self) -> None:
        """Empty URL is accepted (optional field)."""
        result = validate_draft_url("")
        assert result.is_valid

    def test_http_rejected(self) -> None:
        """HTTP (non-HTTPS) URLs are rejected."""
        result = validate_draft_url("http://medium.com/p/abc123/edit")
        assert not result.is_valid


class TestProperty22PlaceholderListing:
    """Property 22: Placeholder listing includes all placeholders.

    For any list of ContentBlocks with placeholders,
    list_placeholders returns all of them.

    **Validates: Requirements 8.2**
    """

    @given(
        n_table=st.integers(min_value=0, max_value=5),
        n_image=st.integers(min_value=0, max_value=5),
        n_paragraph=st.integers(min_value=0, max_value=5),
    )
    @settings(max_examples=100)
    def test_placeholder_count_matches(
        self, n_table: int, n_image: int, n_paragraph: int
    ) -> None:
        """list_placeholders returns exactly N entries for N placeholders."""
        blocks: List[ContentBlock] = []

        for i in range(n_table):
            blocks.append(ContentBlock(
                type="table_placeholder",
                content=f"table {i}",
            ))

        for i in range(n_image):
            blocks.append(ContentBlock(
                type="image_placeholder",
                content=f"image {i}",
                metadata={"alt_text": f"alt {i}"},
            ))

        for i in range(n_paragraph):
            blocks.append(ContentBlock(
                type="paragraph",
                content=f"paragraph {i}",
            ))

        result = list_placeholders(blocks)
        assert len(result) == n_table + n_image

    @given(
        table_captions=st.lists(
            st.text(min_size=1, max_size=30).filter(lambda s: s.strip()),
            min_size=0, max_size=5,
        ),
        image_alts=st.lists(
            st.text(min_size=1, max_size=30).filter(lambda s: s.strip()),
            min_size=0, max_size=5,
        ),
    )
    @settings(max_examples=100)
    def test_placeholder_descriptions_preserved(
        self, table_captions: List[str], image_alts: List[str]
    ) -> None:
        """Each placeholder description appears in the output."""
        blocks: List[ContentBlock] = []

        for caption in table_captions:
            blocks.append(ContentBlock(
                type="table_placeholder",
                content=caption,
            ))

        for alt in image_alts:
            blocks.append(ContentBlock(
                type="image_placeholder",
                content=alt,
                metadata={"alt_text": alt},
            ))

        result = list_placeholders(blocks)

        for caption in table_captions:
            assert f"[table: {caption}]" in result

        for alt in image_alts:
            assert f"[image: {alt}]" in result

    def test_empty_blocks_returns_empty(self) -> None:
        """Empty block list returns empty placeholder list."""
        assert list_placeholders([]) == []

    def test_no_placeholders_returns_empty(self) -> None:
        """Blocks with no placeholders return empty list."""
        blocks = [
            ContentBlock(type="paragraph", content="Hello world"),
            ContentBlock(type="header", content="Title", level=2),
        ]
        assert list_placeholders(blocks) == []


class TestProperty23TagValidation:
    """Property 23: Tag validation enforces max 5 and valid characters.

    Tags with invalid chars rejected, max 5 enforced.

    **Validates: Requirements 9.1, 9.3, 9.4, 9.5**
    """

    @given(tags=st.lists(valid_tag_st, min_size=0, max_size=10))
    @settings(max_examples=100)
    def test_max_5_tags_enforced(self, tags: List[str]) -> None:
        """validate_and_truncate_tags never returns more than 5 valid tags."""
        valid_tags, errors = validate_and_truncate_tags(tags)
        assert len(valid_tags) <= 5

    @given(tags=st.lists(valid_tag_st, min_size=6, max_size=10))
    @settings(max_examples=50)
    def test_first_5_tags_used_when_over_limit(self, tags: List[str]) -> None:
        """When more than 5 tags provided, first 5 are used."""
        valid_tags, errors = validate_and_truncate_tags(tags)
        # All first 5 should be valid (they match valid_tag_st)
        assert len(valid_tags) == 5
        assert valid_tags == tags[:5]

    @given(tags=st.lists(valid_tag_st, min_size=1, max_size=5))
    @settings(max_examples=100)
    def test_valid_tags_all_accepted(self, tags: List[str]) -> None:
        """Tags with only alphanumeric, hyphens, spaces are accepted."""
        valid_tags, errors = validate_and_truncate_tags(tags)
        assert len(errors) == 0
        assert valid_tags == tags

    @given(tags=st.lists(invalid_tag_st, min_size=1, max_size=5))
    @settings(max_examples=50)
    def test_invalid_character_tags_rejected(self, tags: List[str]) -> None:
        """Tags with special characters are rejected."""
        valid_tags, errors = validate_and_truncate_tags(tags)
        assert len(errors) == len(tags)
        assert len(valid_tags) == 0

    @given(
        valid=st.lists(valid_tag_st, min_size=1, max_size=2),
        invalid=st.lists(invalid_tag_st, min_size=1, max_size=2),
    )
    @settings(max_examples=50)
    def test_mixed_tags_partial_acceptance(
        self, valid: List[str], invalid: List[str]
    ) -> None:
        """Mixed valid/invalid tags: valid accepted, invalid rejected."""
        mixed = valid + invalid
        # Truncate to 5 to match function behavior
        mixed = mixed[:5]
        valid_tags, errors = validate_and_truncate_tags(mixed)
        # At least the valid ones in the first 5 should be accepted
        expected_valid_count = len([t for t in mixed if re.match(r'^[a-zA-Z0-9\s\-]+$', t)])
        assert len(valid_tags) == expected_valid_count

    def test_non_list_returns_error(self) -> None:
        """Non-list input returns empty valid list and error."""
        valid_tags, errors = validate_and_truncate_tags("not a list")
        assert valid_tags == []
        assert len(errors) == 1

    def test_empty_list_returns_empty(self) -> None:
        """Empty list returns empty valid list and no errors."""
        valid_tags, errors = validate_and_truncate_tags([])
        assert valid_tags == []
        assert errors == []

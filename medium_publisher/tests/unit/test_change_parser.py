"""
Tests for ChangeParser.
"""

import pytest
from medium_publisher.core.change_parser import (
    ChangeParser,
    ChangeInstruction,
    ChangeAction
)


@pytest.fixture
def parser():
    """Create a ChangeParser instance."""
    return ChangeParser()


@pytest.fixture
def sample_article():
    """Sample article content for testing."""
    return """# Article Title

## Introduction

This is the introduction section.

## Design Principles

These are the design principles.

## Implementation

This is the implementation section.

## Conclusion

This is the conclusion.
"""


class TestChangeParserInit:
    """Tests for ChangeParser initialization."""
    
    def test_init(self, parser):
        """Test parser initialization."""
        assert parser is not None
        assert parser.logger is not None
        assert parser._patterns is not None
        assert len(parser._patterns) == 6  # 6 action types


class TestParseSingleInstruction:
    """Tests for parsing single instructions."""
    
    def test_parse_replace_instruction(self, parser):
        """Test parsing replace instruction."""
        instruction = parser._parse_single_instruction(
            "Replace the introduction section with new content"
        )
        
        assert instruction is not None
        assert instruction.action == ChangeAction.REPLACE
        assert instruction.section == "introduction"  # Captures just "introduction"
    
    def test_parse_replace_with_quotes(self, parser):
        """Test parsing replace instruction with quotes."""
        instruction = parser._parse_single_instruction(
            "Replace 'Design Principles' with updated content"
        )
        
        assert instruction is not None
        assert instruction.action == ChangeAction.REPLACE
        assert instruction.section == "design principles"  # Lowercase for case-insensitive matching
    
    def test_parse_add_instruction(self, parser):
        """Test parsing add instruction."""
        instruction = parser._parse_single_instruction(
            "Add a new section called 'Testing Strategy'"
        )
        
        assert instruction is not None
        assert instruction.action == ChangeAction.ADD
        assert "testing strategy" in instruction.section.lower()  # Case-insensitive check
    
    def test_parse_update_instruction(self, parser):
        """Test parsing update instruction."""
        instruction = parser._parse_single_instruction(
            "Update the conclusion section"
        )
        
        assert instruction is not None
        assert instruction.action == ChangeAction.UPDATE
        assert instruction.section == "conclusion"  # Captures just "conclusion"
    
    def test_parse_delete_instruction(self, parser):
        """Test parsing delete instruction."""
        instruction = parser._parse_single_instruction(
            "Delete the 'Old Approach' section"
        )
        
        assert instruction is not None
        assert instruction.action == ChangeAction.DELETE
        assert instruction.section == "old approach"  # Lowercase for case-insensitive matching
    
    def test_parse_insert_after_instruction(self, parser):
        """Test parsing insert after instruction."""
        instruction = parser._parse_single_instruction(
            "Add a new section after 'Design Principles'"
        )
        
        assert instruction is not None
        assert instruction.action == ChangeAction.INSERT_AFTER
        assert instruction.section == "design principles"  # Lowercase for case-insensitive matching
    
    def test_parse_insert_before_instruction(self, parser):
        """Test parsing insert before instruction."""
        instruction = parser._parse_single_instruction(
            "Insert a section before 'Conclusion'"
        )
        
        assert instruction is not None
        assert instruction.action == ChangeAction.INSERT_BEFORE
        assert instruction.section == "conclusion"  # Lowercase for case-insensitive matching
    
    def test_parse_unparseable_instruction(self, parser):
        """Test parsing unparseable instruction."""
        instruction = parser._parse_single_instruction(
            "This is not a valid instruction"
        )
        
        assert instruction is None



class TestParseInstructions:
    """Tests for parsing multiple instructions."""
    
    def test_parse_empty_instructions(self, parser):
        """Test parsing empty instructions."""
        changes = parser.parse_instructions("")
        assert changes == []
    
    def test_parse_single_instruction(self, parser):
        """Test parsing single instruction."""
        instructions = "Replace the introduction with new content"
        changes = parser.parse_instructions(instructions)
        
        assert len(changes) == 1
        assert changes[0].action == ChangeAction.REPLACE
        assert changes[0].section == "introduction"
    
    def test_parse_multiple_instructions(self, parser):
        """Test parsing multiple instructions."""
        instructions = """
        Replace the introduction section with new content
        Add a new section after 'Design Principles'
        Delete the 'Old Approach' section
        Update the conclusion
        """
        changes = parser.parse_instructions(instructions)
        
        assert len(changes) == 4
        assert changes[0].action == ChangeAction.REPLACE
        assert changes[1].action == ChangeAction.INSERT_AFTER
        assert changes[2].action == ChangeAction.DELETE
        assert changes[3].action == ChangeAction.UPDATE
    
    def test_parse_instructions_with_blank_lines(self, parser):
        """Test parsing instructions with blank lines."""
        instructions = """
        Replace the introduction section with new content
        
        Add a new section called 'Testing'
        
        Delete the 'old content' section
        """
        changes = parser.parse_instructions(instructions)
        
        assert len(changes) == 3
    
    def test_parse_instructions_preserves_raw(self, parser):
        """Test that raw instruction is preserved."""
        instructions = "Replace 'Introduction' with new content"
        changes = parser.parse_instructions(instructions)
        
        assert len(changes) == 1
        assert changes[0].raw_instruction == instructions


class TestIdentifySections:
    """Tests for identifying sections."""
    
    def test_identify_sections_empty(self, parser):
        """Test identifying sections from empty list."""
        sections = parser.identify_sections([])
        assert sections == []
    
    def test_identify_sections_single(self, parser):
        """Test identifying single section."""
        instructions = [
            ChangeInstruction(
                action=ChangeAction.REPLACE,
                section="introduction"  # Lowercase
            )
        ]
        sections = parser.identify_sections(instructions)
        
        assert len(sections) == 1
        assert "introduction" in sections
    
    def test_identify_sections_multiple(self, parser):
        """Test identifying multiple sections."""
        instructions = [
            ChangeInstruction(action=ChangeAction.REPLACE, section="introduction"),
            ChangeInstruction(action=ChangeAction.UPDATE, section="conclusion"),
            ChangeInstruction(action=ChangeAction.DELETE, section="old section"),
        ]
        sections = parser.identify_sections(instructions)
        
        assert len(sections) == 3
        assert "introduction" in sections
        assert "conclusion" in sections
        assert "old section" in sections
    
    def test_identify_sections_duplicates(self, parser):
        """Test that duplicate sections are removed."""
        instructions = [
            ChangeInstruction(action=ChangeAction.REPLACE, section="introduction"),
            ChangeInstruction(action=ChangeAction.UPDATE, section="introduction"),
        ]
        sections = parser.identify_sections(instructions)
        
        assert len(sections) == 1
        assert "introduction" in sections
    
    def test_identify_sections_with_position(self, parser):
        """Test identifying sections including position markers."""
        instructions = [
            ChangeInstruction(
                action=ChangeAction.INSERT_AFTER,
                section="new section",
                position="design principles"
            )
        ]
        sections = parser.identify_sections(instructions)
        
        assert len(sections) == 2
        assert "new section" in sections
        assert "design principles" in sections
    
    def test_identify_sections_sorted(self, parser):
        """Test that sections are returned sorted."""
        instructions = [
            ChangeInstruction(action=ChangeAction.REPLACE, section="zebra"),
            ChangeInstruction(action=ChangeAction.UPDATE, section="apple"),
            ChangeInstruction(action=ChangeAction.DELETE, section="mango"),
        ]
        sections = parser.identify_sections(instructions)
        
        assert sections == ["apple", "mango", "zebra"]



class TestExtractSearchMarkers:
    """Tests for extracting search markers."""
    
    def test_extract_markers_no_section(self, parser, sample_article):
        """Test extracting markers with no section."""
        instruction = ChangeInstruction(action=ChangeAction.ADD)
        markers = parser.extract_search_markers(instruction, sample_article)
        
        assert markers["start_marker"] is None
        assert markers["end_marker"] is None
        assert markers["section_found"] is False
        assert markers["line_number"] is None
    
    def test_extract_markers_section_found(self, parser, sample_article):
        """Test extracting markers when section is found."""
        instruction = ChangeInstruction(
            action=ChangeAction.REPLACE,
            section="introduction"  # Lowercase
        )
        markers = parser.extract_search_markers(instruction, sample_article)
        
        assert markers["section_found"] is True
        assert markers["start_marker"] is not None
        assert "Introduction" in markers["start_marker"]  # Actual header has capital
        assert markers["line_number"] is not None
        assert markers["line_number"] > 0
    
    def test_extract_markers_section_not_found(self, parser, sample_article):
        """Test extracting markers when section is not found."""
        instruction = ChangeInstruction(
            action=ChangeAction.REPLACE,
            section="nonexistent section"  # Lowercase
        )
        markers = parser.extract_search_markers(instruction, sample_article)
        
        assert markers["section_found"] is False
        assert markers["start_marker"] is None
    
    def test_extract_markers_with_end_marker(self, parser, sample_article):
        """Test extracting markers with end marker."""
        instruction = ChangeInstruction(
            action=ChangeAction.REPLACE,
            section="design principles"  # Lowercase
        )
        markers = parser.extract_search_markers(instruction, sample_article)
        
        assert markers["section_found"] is True
        assert markers["start_marker"] is not None
        assert markers["end_marker"] is not None
    
    def test_extract_markers_last_section(self, parser, sample_article):
        """Test extracting markers for last section (no end marker)."""
        instruction = ChangeInstruction(
            action=ChangeAction.REPLACE,
            section="conclusion"  # Lowercase
        )
        markers = parser.extract_search_markers(instruction, sample_article)
        
        assert markers["section_found"] is True
        assert markers["start_marker"] is not None
        # Last section may not have end marker
    
    def test_extract_markers_case_insensitive(self, parser, sample_article):
        """Test that section search is case insensitive."""
        instruction = ChangeInstruction(
            action=ChangeAction.REPLACE,
            section="introduction"  # lowercase
        )
        markers = parser.extract_search_markers(instruction, sample_article)
        
        assert markers["section_found"] is True
        assert markers["start_marker"] is not None
    
    def test_extract_markers_line_number_accuracy(self, parser, sample_article):
        """Test that line numbers are accurate."""
        instruction = ChangeInstruction(
            action=ChangeAction.REPLACE,
            section="introduction"  # Lowercase
        )
        markers = parser.extract_search_markers(instruction, sample_article)
        
        # Introduction should be around line 3
        assert markers["line_number"] is not None
        assert 2 <= markers["line_number"] <= 4


class TestCreateSectionPattern:
    """Tests for creating section patterns."""
    
    def test_create_pattern_simple(self, parser):
        """Test creating pattern for simple section name."""
        pattern = parser._create_section_pattern("Introduction")
        assert pattern is not None
        assert "Introduction" in pattern
    
    def test_create_pattern_with_spaces(self, parser):
        """Test creating pattern for section with spaces."""
        pattern = parser._create_section_pattern("Design Principles")
        assert pattern is not None
        assert "Design" in pattern
        assert "Principles" in pattern
    
    def test_create_pattern_escapes_special_chars(self, parser):
        """Test that special regex characters are escaped."""
        pattern = parser._create_section_pattern("Section (Part 1)")
        assert pattern is not None
        # Should not raise regex error when used
        import re
        re.compile(pattern)  # Should not raise


class TestIntegration:
    """Integration tests for ChangeParser."""
    
    def test_full_workflow(self, parser, sample_article):
        """Test complete workflow from instructions to markers."""
        instructions = """
        Replace the introduction section with new content
        Add a new section after 'Design Principles'
        Update the conclusion
        """
        
        # Parse instructions
        changes = parser.parse_instructions(instructions)
        assert len(changes) == 3
        
        # Identify sections
        sections = parser.identify_sections(changes)
        assert len(sections) >= 3
        
        # Extract markers for first change
        markers = parser.extract_search_markers(changes[0], sample_article)
        assert markers["section_found"] is True
    
    def test_complex_instructions(self, parser):
        """Test parsing complex real-world instructions."""
        instructions = """
        Replace 'Getting Started' with updated installation steps
        Add a new 'Troubleshooting' section after 'Configuration'
        Update 'API Reference' to include new endpoints
        Delete the deprecated 'Legacy API' section
        Insert a 'Migration Guide' before 'Conclusion'
        """
        
        changes = parser.parse_instructions(instructions)
        assert len(changes) == 5
        
        # Verify action types
        actions = [c.action for c in changes]
        assert ChangeAction.REPLACE in actions
        assert ChangeAction.INSERT_AFTER in actions
        assert ChangeAction.UPDATE in actions
        assert ChangeAction.DELETE in actions
        assert ChangeAction.INSERT_BEFORE in actions

"""
Change Parser for parsing user change instructions.

This module provides functionality to parse natural language instructions
for updating article versions, identifying sections to modify, and extracting
search markers for content replacement.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
import re

from medium_publisher.utils.logger import get_logger


class ChangeAction(Enum):
    """Types of change actions."""
    REPLACE = "replace"
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    INSERT_AFTER = "insert_after"
    INSERT_BEFORE = "insert_before"


@dataclass
class ChangeInstruction:
    """Represents a parsed change instruction."""
    action: ChangeAction
    section: Optional[str] = None
    search_text: Optional[str] = None
    new_content: Optional[str] = None
    position: Optional[str] = None  # For insert_after/insert_before
    raw_instruction: str = ""


class ChangeParser:
    """
    Parser for user change instructions.
    
    Parses natural language instructions like:
    - "Replace the introduction section with new content"
    - "Add a new section after 'Design Principles'"
    - "Update the conclusion"
    - "Delete the 'Old Approach' section"
    """
    
    def __init__(self):
        """Initialize the change parser."""
        self.logger = get_logger("ChangeParser")
        
        # Patterns for different instruction types (order matters - check specific patterns first)
        self._patterns = {
            ChangeAction.INSERT_AFTER: [
                r"(?:add|insert)\s+.*?\s+after\s+['\"]([^'\"]+)['\"]",
            ],
            ChangeAction.INSERT_BEFORE: [
                r"(?:add|insert)\s+.*?\s+before\s+['\"]([^'\"]+)['\"]",
            ],
            ChangeAction.REPLACE: [
                r"replace\s+['\"]([^'\"]+)['\"]",
                r"replace\s+(?:the\s+)?(.+?)\s+(?:section\s+)?with",
            ],
            ChangeAction.DELETE: [
                r"delete\s+(?:the\s+)?['\"]([^'\"]+)['\"]",
                r"remove\s+(?:the\s+)?['\"]([^'\"]+)['\"]",
                r"delete\s+(?:the\s+)?(?:deprecated\s+)?(.+?)(?:\s+section)?(?:\s*$)",
                r"remove\s+(?:the\s+)?(.+?)(?:\s+section)?(?:\s*$)",
            ],
            ChangeAction.UPDATE: [
                r"update\s+(?:the\s+)?['\"]([^'\"]+)['\"]",
                r"modify\s+(?:the\s+)?['\"]([^'\"]+)['\"]",
                r"change\s+(?:the\s+)?['\"]([^'\"]+)['\"]",
                r"update\s+(?:the\s+)?(.+?)(?:\s+to\s+include|\s+section|\s*$)",
                r"modify\s+(?:the\s+)?(.+?)(?:\s+section|\s*$)",
                r"change\s+(?:the\s+)?(.+?)(?:\s+section|\s*$)",
            ],
            ChangeAction.ADD: [
                r"add\s+(?:a\s+)?(?:new\s+)?(?:section\s+)?(?:called\s+)?['\"]([^'\"]+)['\"]",
                r"create\s+(?:a\s+)?(?:new\s+)?(?:section\s+)?['\"]([^'\"]+)['\"]",
                r"add\s+(?:a\s+)?(?:new\s+)?(.+?)(?:\s+section)?(?:\s*$)",
            ],
        }

    
    def parse_instructions(self, instructions: str) -> List[ChangeInstruction]:
        """
        Parse user change instructions into structured change objects.
        
        Args:
            instructions: Natural language change instructions (multi-line)
            
        Returns:
            List of ChangeInstruction objects
            
        Example:
            >>> parser = ChangeParser()
            >>> instructions = '''
            ... Replace the introduction section with new content
            ... Add a new section after 'Design Principles'
            ... Delete the 'Old Approach' section
            ... '''
            >>> changes = parser.parse_instructions(instructions)
        """
        self.logger.info("Parsing change instructions", extra={"context": f"{len(instructions)} chars"})
        
        changes = []
        lines = [line.strip() for line in instructions.split('\n') if line.strip()]
        
        for line in lines:
            instruction = self._parse_single_instruction(line)
            if instruction:
                changes.append(instruction)
                self.logger.debug(
                    "Parsed instruction",
                    extra={"context": f"action={instruction.action.value}, section={instruction.section}"}
                )
        
        self.logger.info("Parsed instructions", extra={"context": f"{len(changes)} changes identified"})
        return changes
    
    def _parse_single_instruction(self, instruction: str) -> Optional[ChangeInstruction]:
        """
        Parse a single instruction line.
        
        Args:
            instruction: Single line instruction
            
        Returns:
            ChangeInstruction or None if not parseable
        """
        instruction_lower = instruction.lower()
        
        # Try each action pattern
        for action, patterns in self._patterns.items():
            for pattern in patterns:
                match = re.search(pattern, instruction_lower, re.IGNORECASE)
                if match:
                    section = match.group(1).strip() if match.groups() else None
                    
                    return ChangeInstruction(
                        action=action,
                        section=section,
                        raw_instruction=instruction
                    )
        
        self.logger.warning("Could not parse instruction", extra={"context": instruction})
        return None
    
    def identify_sections(self, instructions: List[ChangeInstruction]) -> List[str]:
        """
        Identify all section names mentioned in instructions.
        
        Args:
            instructions: List of parsed change instructions
            
        Returns:
            List of unique section names
        """
        sections = set()
        
        for instruction in instructions:
            if instruction.section:
                sections.add(instruction.section)
            if instruction.position:
                sections.add(instruction.position)
        
        section_list = sorted(list(sections))
        self.logger.info("Identified sections", extra={"context": f"{len(section_list)} sections"})
        
        return section_list

    
    def extract_search_markers(
        self,
        instruction: ChangeInstruction,
        article_content: str
    ) -> Dict[str, Any]:
        """
        Extract search markers for finding content in the editor.
        
        Args:
            instruction: Change instruction to process
            article_content: Full article content to search
            
        Returns:
            Dictionary with search markers:
            - start_marker: Text to search for section start
            - end_marker: Text to search for section end (optional)
            - section_found: Whether section was found in content
            - line_number: Approximate line number (optional)
        """
        self.logger.info(
            "Extracting search markers",
            extra={"context": f"action={instruction.action.value}, section={instruction.section}"}
        )
        
        markers = {
            "start_marker": None,
            "end_marker": None,
            "section_found": False,
            "line_number": None
        }
        
        if not instruction.section:
            return markers
        
        # Search for section header in content
        section_pattern = self._create_section_pattern(instruction.section)
        match = re.search(section_pattern, article_content, re.IGNORECASE | re.MULTILINE)
        
        if match:
            markers["section_found"] = True
            markers["start_marker"] = match.group(0)
            
            # Calculate line number
            lines_before = article_content[:match.start()].count('\n')
            markers["line_number"] = lines_before + 1
            
            # Find end marker (next header or end of content)
            end_match = re.search(
                r'\n#{2,4}\s+',
                article_content[match.end():],
                re.MULTILINE
            )
            
            if end_match:
                end_pos = match.end() + end_match.start()
                # Get a few words before the next header as end marker
                end_context = article_content[max(0, end_pos - 50):end_pos].strip()
                markers["end_marker"] = end_context.split('\n')[-1] if end_context else None
            
            self.logger.info(
                "Found section",
                extra={"context": f"line={markers['line_number']}, start={markers['start_marker'][:30]}"}
            )
        else:
            self.logger.warning(
                "Section not found",
                extra={"context": f"section={instruction.section}"}
            )
        
        return markers
    
    def _create_section_pattern(self, section_name: str) -> str:
        """
        Create regex pattern for finding section header.

        Args:
            section_name: Name of section to find

        Returns:
            Regex pattern string
        """
        # Split into words and escape each word separately
        words = section_name.split()
        escaped_words = [re.escape(word) for word in words]

        # Join with flexible whitespace pattern
        pattern_text = r'\s+'.join(escaped_words)

        # Match markdown headers (##, ###, ####) with the section name
        # Use (?i) inline flag for case-insensitive matching
        # Build pattern without f-string to avoid brace escaping issues
        pattern = r'(?i)^#{2,4}\s+' + pattern_text + r'\s*$'

        return pattern

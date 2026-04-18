"""
Markdown processor for Medium Article Publisher.

This module converts markdown content to Medium-compatible content blocks
with proper formatting and placeholders for unsupported elements.
"""

import re
from typing import List, Optional, Tuple
from dataclasses import dataclass

from .models import ContentBlock, Format
from medium_publisher.utils.logger import get_logger


logger = get_logger("MarkdownProcessor")


class MarkdownProcessor:
    """
    Processes markdown content and converts it to ContentBlock objects.
    
    Handles headers, formatting (bold, italic, code), code blocks, lists,
    links, and creates placeholders for tables and images.
    """
    
    def __init__(self):
        """Initialize the markdown processor."""
        self.logger = logger
        
    def process(self, markdown: str) -> List[ContentBlock]:
        """
        Convert markdown to list of content blocks.
        
        Args:
            markdown: Raw markdown content
            
        Returns:
            List of ContentBlock objects
        """
        self.logger.info("Processing markdown content")
        
        if not markdown or not markdown.strip():
            self.logger.warning("Empty markdown content")
            return []
        
        blocks = []
        lines = markdown.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip empty lines
            if not line.strip():
                i += 1
                continue
            
            # Check for code block
            if line.strip().startswith('```'):
                code_block, lines_consumed = self._parse_code_block(lines[i:])
                if code_block:
                    blocks.append(code_block)
                    i += lines_consumed
                    continue
            
            # Check for table
            table_block = self._detect_table(lines[i:])
            if table_block:
                blocks.append(table_block)
                # Skip table lines (header + separator + rows)
                i += self._count_table_lines(lines[i:])
                continue
            
            # Check for image
            image_block = self._detect_image(line)
            if image_block:
                blocks.append(image_block)
                i += 1
                continue
            
            # Check for header
            header_block = self._parse_header(line)
            if header_block:
                blocks.append(header_block)
                i += 1
                continue
            
            # Check for list
            if self._is_list_item(line):
                list_block, lines_consumed = self._parse_list(lines[i:])
                if list_block:
                    blocks.append(list_block)
                    i += lines_consumed
                    continue
            
            # Regular paragraph
            paragraph_block = self._parse_paragraph(line)
            blocks.append(paragraph_block)
            i += 1
        
        self.logger.info(f"Processed {len(blocks)} content blocks")
        return blocks

    
    def _parse_header(self, line: str) -> Optional[ContentBlock]:
        """
        Parse markdown headers (##, ###, ####).
        
        Args:
            line: Line to parse
            
        Returns:
            HeaderBlock or None if not a header
        """
        match = re.match(r'^(#{2,4})\s+(.+)$', line)
        if not match:
            return None
        
        hashes, text = match.groups()
        level = len(hashes)
        
        # Parse inline formatting
        formatting = self._parse_formatting(text)
        
        return ContentBlock(
            type="header",
            content=text,
            formatting=formatting,
            level=level
        )
    
    def _parse_formatting(self, text: str) -> List[Format]:
        """
        Parse inline formatting (bold, italic, code, links).
        
        Args:
            text: Text to parse
            
        Returns:
            List of Format objects
        """
        formats = []
        
        # Parse bold (**text**)
        for match in re.finditer(r'\*\*(.+?)\*\*', text):
            formats.append(Format(
                type="bold",
                start=match.start(),
                end=match.end(),
                url=""
            ))
        
        # Parse italic (*text* or _text_)
        for match in re.finditer(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', text):
            formats.append(Format(
                type="italic",
                start=match.start(),
                end=match.end(),
                url=""
            ))
        
        for match in re.finditer(r'_(.+?)_', text):
            formats.append(Format(
                type="italic",
                start=match.start(),
                end=match.end(),
                url=""
            ))
        
        # Parse inline code (`code`)
        for match in re.finditer(r'`(.+?)`', text):
            formats.append(Format(
                type="code",
                start=match.start(),
                end=match.end(),
                url=""
            ))
        
        # Parse links ([text](url))
        for match in re.finditer(r'\[(.+?)\]\((.+?)\)', text):
            formats.append(Format(
                type="link",
                start=match.start(),
                end=match.end(),
                url=match.group(2)
            ))
        
        return formats

    
    def _parse_code_block(self, lines: List[str]) -> Tuple[Optional[ContentBlock], int]:
        """
        Parse code blocks (```language...```).
        
        Args:
            lines: Lines starting with code block
            
        Returns:
            Tuple of (CodeBlock or None, lines consumed)
        """
        if not lines[0].strip().startswith('```'):
            return None, 0
        
        # Extract language (optional)
        first_line = lines[0].strip()
        language = first_line[3:].strip() if len(first_line) > 3 else ""
        
        # Find closing ```
        code_lines = []
        i = 1
        while i < len(lines):
            if lines[i].strip() == '```':
                # Found closing delimiter
                code_content = '\n'.join(code_lines)
                return ContentBlock(
                    type="code",
                    content=code_content,
                    formatting=[],
                    metadata={"language": language}
                ), i + 1
            code_lines.append(lines[i])
            i += 1
        
        # No closing delimiter found - treat as regular paragraph
        return None, 0
    
    def _is_list_item(self, line: str) -> bool:
        """
        Check if line is a list item.
        
        Args:
            line: Line to check
            
        Returns:
            True if list item
        """
        # Bullet list: - item or * item
        if re.match(r'^\s*[-*]\s+.+', line):
            return True
        
        # Numbered list: 1. item
        if re.match(r'^\s*\d+\.\s+.+', line):
            return True
        
        return False
    
    def _parse_list(self, lines: List[str]) -> Tuple[Optional[ContentBlock], int]:
        """
        Parse bullet or numbered lists.
        
        Args:
            lines: Lines starting with list
            
        Returns:
            Tuple of (ListBlock or None, lines consumed)
        """
        if not self._is_list_item(lines[0]):
            return None, 0
        
        list_items = []
        i = 0
        
        while i < len(lines) and self._is_list_item(lines[i]):
            # Extract list item text
            match = re.match(r'^\s*(?:[-*]|\d+\.)\s+(.+)', lines[i])
            if match:
                list_items.append(match.group(1))
            i += 1
        
        # Combine list items
        content = '\n'.join(list_items)
        
        # Determine list type
        is_numbered = re.match(r'^\s*\d+\.', lines[0])
        list_type = "numbered" if is_numbered else "bullet"
        
        return ContentBlock(
            type="list",
            content=content,
            formatting=[],
            metadata={"list_type": list_type}
        ), i

    
    def _parse_paragraph(self, line: str) -> ContentBlock:
        """
        Parse regular paragraph with inline formatting.
        
        Args:
            line: Line to parse
            
        Returns:
            ContentBlock for paragraph
        """
        formatting = self._parse_formatting(line)
        
        return ContentBlock(
            type="paragraph",
            content=line,
            formatting=formatting
        )
    
    def _detect_table(self, lines: List[str]) -> Optional[ContentBlock]:
        """
        Detect markdown tables and return placeholder.
        
        Args:
            lines: Lines to check
            
        Returns:
            Table placeholder block or None
        """
        if len(lines) < 2:
            return None
        
        # Check for table separator (| --- | --- |)
        if not re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[1]):
            return None
        
        # Check for header row (| Header | Header |)
        if not re.match(r'^\s*\|.+\|\s*$', lines[0]):
            return None
        
        # Extract column count from header
        columns = len([c for c in lines[0].split('|') if c.strip()])
        
        return ContentBlock(
            type="table_placeholder",
            content="TODO: Insert table here",
            formatting=[],
            metadata={"columns": columns}
        )
    
    def _count_table_lines(self, lines: List[str]) -> int:
        """
        Count how many lines belong to a table.
        
        Args:
            lines: Lines starting with table
            
        Returns:
            Number of table lines
        """
        count = 0
        for line in lines:
            if re.match(r'^\s*\|.+\|\s*$', line):
                count += 1
            else:
                break
        return count
    
    def _detect_image(self, line: str) -> Optional[ContentBlock]:
        """
        Detect markdown images and return placeholder with alt text.
        
        Args:
            line: Line to check
            
        Returns:
            Image placeholder block or None
        """
        match = re.match(r'!\[(.+?)\]\((.+?)\)', line.strip())
        if not match:
            return None
        
        alt_text = match.group(1)
        image_url = match.group(2)
        
        return ContentBlock(
            type="image_placeholder",
            content=f"TODO: Insert image here - {alt_text}",
            formatting=[],
            metadata={"alt_text": alt_text, "url": image_url}
        )

    
    def compare_versions(self, version1: str, version2: str) -> List[Tuple[str, str, str]]:
        """
        Compare two markdown versions and identify changed sections.
        
        Args:
            version1: First version markdown content
            version2: Second version markdown content
            
        Returns:
            List of tuples (change_type, section_identifier, new_content)
            change_type: 'added', 'modified', 'deleted'
            section_identifier: Header text or line number
            new_content: New content for the section
        """
        self.logger.info("Comparing markdown versions")
        
        # Process both versions
        blocks1 = self.process(version1)
        blocks2 = self.process(version2)
        
        changes = []
        
        # Create section maps (header -> content)
        sections1 = self._create_section_map(blocks1)
        sections2 = self._create_section_map(blocks2)
        
        # Find added sections
        for section_id in sections2:
            if section_id not in sections1:
                changes.append((
                    'added',
                    section_id,
                    sections2[section_id]
                ))
        
        # Find deleted sections
        for section_id in sections1:
            if section_id not in sections2:
                changes.append((
                    'deleted',
                    section_id,
                    ''
                ))
        
        # Find modified sections
        for section_id in sections1:
            if section_id in sections2:
                if sections1[section_id] != sections2[section_id]:
                    changes.append((
                        'modified',
                        section_id,
                        sections2[section_id]
                    ))
        
        self.logger.info(f"Found {len(changes)} changes between versions")
        return changes
    
    def _create_section_map(self, blocks: List[ContentBlock]) -> dict:
        """
        Create a map of sections from content blocks.
        
        Args:
            blocks: List of content blocks
            
        Returns:
            Dictionary mapping section identifiers to content
        """
        sections = {}
        current_section = "introduction"
        current_content = []
        
        for block in blocks:
            if block.type == "header":
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = block.content.strip()
                current_content = []
            else:
                current_content.append(block.content)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections

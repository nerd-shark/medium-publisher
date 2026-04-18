"""
Article parser for Medium Article Publisher.

This module provides functionality to parse markdown files with YAML frontmatter
and extract article metadata and content.
"""

from pathlib import Path
from typing import Dict, Any
import yaml
import re

from .models import Article
from medium_publisher.utils.exceptions import FileError, ContentError
from medium_publisher.utils.logger import get_logger


logger = get_logger(__name__)


class ArticleParser:
    """
    Parser for markdown articles with YAML frontmatter.
    
    Parses markdown files containing YAML frontmatter metadata and markdown
    content body. Validates the structure and extracts data into Article objects.
    """
    
    def __init__(self):
        """Initialize the ArticleParser."""
        self.logger = get_logger(self.__class__.__name__)
    
    def parse_file(self, file_path: str) -> Article:
        """
        Parse a markdown file and return an Article object.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Article object with parsed data
            
        Raises:
            FileError: If file doesn't exist or can't be read
            ContentError: If file content is malformed
        """
        self.logger.info(f"Parsing article file: {file_path}")
        
        # Validate file path
        path = Path(file_path)
        if not path.exists():
            raise FileError(f"File not found: {file_path}")
        
        if not path.is_file():
            raise FileError(f"Path is not a file: {file_path}")
        
        if path.suffix != ".md":
            raise FileError(
                f"Invalid file extension '{path.suffix}'. Must be .md"
            )
        
        # Read file content
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise FileError(f"Failed to read file {file_path}: {e}")

        
        # Extract frontmatter and body
        try:
            frontmatter = self.extract_frontmatter(content)
            body = self.extract_body(content)
        except Exception as e:
            raise ContentError(f"Failed to parse file content: {e}")
        
        # Create Article object
        raw_tags = frontmatter.get('tags', [])
        raw_keywords = frontmatter.get('keywords', [])

        # Normalize tags/keywords: split comma-separated strings into lists
        if isinstance(raw_tags, str):
            raw_tags = [t.strip() for t in raw_tags.split(',') if t.strip()]
        if isinstance(raw_keywords, str):
            raw_keywords = [k.strip() for k in raw_keywords.split(',') if k.strip()]

        article = Article(
            title=frontmatter.get('title', ''),
            subtitle=frontmatter.get('subtitle', ''),
            content=body,
            tags=raw_tags,
            keywords=raw_keywords,
            status=frontmatter.get('status', 'draft'),
            file_path=str(path.absolute())
        )
        
        # Validate article
        try:
            self.validate_article(article)
        except ValueError as e:
            raise ContentError(f"Article validation failed: {e}")
        
        self.logger.info(
            f"Successfully parsed article: {article.title} "
            f"({len(body)} chars, {len(article.tags)} tags)"
        )
        
        return article
    
    def extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Extract YAML frontmatter from markdown content.
        
        Frontmatter must be at the beginning of the file, enclosed in '---'
        delimiters.
        
        Args:
            content: Raw markdown content
            
        Returns:
            Dictionary of frontmatter metadata
            
        Raises:
            ContentError: If frontmatter is malformed or missing
        """
        self.logger.debug("Extracting frontmatter")
        
        # Check for frontmatter delimiters
        if not content.startswith('---'):
            raise ContentError(
                "Missing frontmatter. File must start with '---'"
            )
        
        # Find the closing delimiter
        # Pattern: --- at start, content, --- (with optional whitespace)
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            raise ContentError(
                "Malformed frontmatter. Must be enclosed in '---' delimiters"
            )
        
        frontmatter_text = match.group(1)
        
        # Parse YAML
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            raise ContentError(f"Invalid YAML in frontmatter: {e}")
        
        # Handle empty frontmatter (returns None)
        if frontmatter is None:
            frontmatter = {}
        
        if not isinstance(frontmatter, dict):
            raise ContentError(
                "Frontmatter must be a YAML dictionary"
            )
        
        self.logger.debug(f"Extracted frontmatter with {len(frontmatter)} fields")
        
        return frontmatter

    
    def extract_body(self, content: str) -> str:
        """
        Extract article body (remove frontmatter).
        
        Args:
            content: Raw markdown content with frontmatter
            
        Returns:
            Article body without frontmatter
            
        Raises:
            ContentError: If body extraction fails
        """
        self.logger.debug("Extracting article body")
        
        # Find the end of frontmatter
        pattern = r'^---\s*\n.*?\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            raise ContentError(
                "Cannot extract body: malformed frontmatter"
            )
        
        # Get content after frontmatter
        body = content[match.end():]
        
        # Strip leading/trailing whitespace
        body = body.strip()
        
        if not body:
            raise ContentError("Article body is empty")
        
        self.logger.debug(f"Extracted body: {len(body)} characters")
        
        return body
    
    def validate_article(self, article: Article) -> bool:
        """
        Validate article has required fields and valid data.
        
        Args:
            article: Article object to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        self.logger.debug(f"Validating article: {article.title}")
        
        # Check required fields
        if not article.has_required_fields():
            raise ValueError(
                "Article missing required fields (title and content)"
            )
        
        # Run Article's built-in validation
        article.validate()
        
        self.logger.debug("Article validation passed")
        
        return True

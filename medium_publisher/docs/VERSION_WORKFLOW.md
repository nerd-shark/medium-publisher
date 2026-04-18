# Version Update Workflow

## Overview

The version update workflow allows iterative refinement of articles through multiple versions (v1, v2, v3, etc.) without retyping the entire article. Users provide natural language instructions describing changes, and the system applies them to the Medium draft.

## Workflow Phases

### Phase 1: Initial Publication (v1)

```
1. User selects markdown file
2. User selects version "v1"
3. System parses v1 content
4. System types complete article
5. Article published as draft
6. System waits for next action
```

### Phase 2: Version Update (v2, v3, etc.)

```
1. User selects next version (v2)
2. User enters change instructions
3. System parses instructions
4. System identifies sections to modify
5. System applies changes:
   a. Find section in editor
   b. Select content to replace
   c. Delete selected content
   d. Type new content
6. System waits for next action
7. Repeat for v3, v4, etc.
```

### Phase 3: Final Publication

```
1. User reviews all changes
2. User manually inserts tables/images
3. User publishes article (draft or public)
```

## Change Instruction Format

### Supported Instructions

#### 1. Replace Section

**Format**: "Replace [section name] with [new content]"

**Examples**:
- "Replace the introduction with new content"
- "Replace section 'Design Principles' with updated text"
- "Replace the conclusion"

**Behavior**:
- Finds section by name/heading
- Selects entire section
- Deletes old content
- Types new content from v2 markdown

#### 2. Update Section

**Format**: "Update [section name]"

**Examples**:
- "Update the methodology section"
- "Update 'Implementation Details'"

**Behavior**:
- Similar to replace
- Implies modifications rather than complete rewrite
- Finds and replaces section content

#### 3. Add Section

**Format**: "Add [new section] after [existing section]"

**Examples**:
- "Add new section 'Performance Metrics' after 'Implementation'"
- "Add conclusion after results"

**Behavior**:
- Finds insertion point
- Positions cursor after existing section
- Types new section content

#### 4. Delete Section

**Format**: "Delete [section name]"

**Examples**:
- "Delete the 'Future Work' section"
- "Remove the appendix"

**Behavior**:
- Finds section by name
- Selects entire section
- Deletes content

#### 5. Multiple Changes

**Format**: Multiple instructions separated by newlines or semicolons

**Example**:
```
Replace the introduction with new content
Update the methodology section
Add new section 'Results' after methodology
Delete the old conclusion
```

**Behavior**:
- Processes instructions sequentially
- Maintains context between changes
- Applies all changes in order

## Section Identification

### By Heading

```markdown
## Introduction
Content here...

## Methodology
Content here...
```

**Instruction**: "Replace the introduction"
**Match**: Finds "## Introduction" heading

### By Exact Text

**Instruction**: "Replace section starting with 'In this article'"
**Match**: Searches for exact text "In this article"

### By Markers

**Instruction**: "Replace content between 'START' and 'END'"
**Match**: Finds text between markers

## Implementation Details

### ChangeParser Class

```python
class ChangeParser:
    """Parse version update instructions."""
    
    def parse_instructions(self, instructions: str) -> List[ChangeInstruction]:
        """Parse natural language instructions.
        
        Args:
            instructions: User's change instructions
        
        Returns:
            List of parsed change instructions
        """
        # Split into individual instructions
        lines = instructions.strip().split('\n')
        
        changes = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Parse instruction type
            if 'replace' in line.lower():
                change = self._parse_replace(line)
            elif 'update' in line.lower():
                change = self._parse_update(line)
            elif 'add' in line.lower():
                change = self._parse_add(line)
            elif 'delete' in line.lower() or 'remove' in line.lower():
                change = self._parse_delete(line)
            else:
                # Unknown instruction, skip
                continue
            
            if change:
                changes.append(change)
        
        return changes
    
    def _parse_replace(self, instruction: str) -> ChangeInstruction:
        """Parse replace instruction."""
        # Extract section name
        # "Replace the introduction" → section="introduction"
        # "Replace section 'Design'" → section="Design"
        
        patterns = [
            r"replace\s+(?:the\s+)?['\"]?([^'\"]+)['\"]?",
            r"replace\s+section\s+['\"]([^'\"]+)['\"]",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, instruction, re.IGNORECASE)
            if match:
                section = match.group(1).strip()
                return ChangeInstruction(
                    action="replace",
                    section=section,
                    search_start=f"## {section}",  # Assume markdown heading
                    search_end=None  # Until next heading
                )
        
        return None
```

### MediumEditor Integration

```python
class MediumEditor:
    async def apply_version_changes(self, changes: List[ChangeInstruction], 
                                    new_content: dict):
        """Apply version changes to draft.
        
        Args:
            changes: List of change instructions
            new_content: New content blocks by section
        """
        for change in changes:
            if change.action == "replace":
                await self.replace_section(
                    change.section,
                    new_content[change.section]
                )
            elif change.action == "add":
                await self.add_section(
                    change.section,
                    change.after_section,
                    new_content[change.section]
                )
            elif change.action == "delete":
                await self.delete_section(change.section)
    
    async def replace_section(self, section_name: str, 
                             new_blocks: List[ContentBlock]):
        """Replace a section with new content.
        
        Args:
            section_name: Name of section to replace
            new_blocks: New content blocks
        """
        # Find section heading
        found = await self.find_section(f"## {section_name}")
        if not found:
            raise ContentError(f"Section '{section_name}' not found")
        
        # Select section content (until next heading)
        await self.select_section(
            start_text=f"## {section_name}",
            end_text="##"  # Next heading
        )
        
        # Delete selected content
        await self.delete_selected_content()
        
        # Type new content
        await self.typer.type_content(new_blocks)
```

### Section Selection Algorithm

```python
async def select_section(self, start_text: str, end_text: str):
    """Select content between start and end markers.
    
    Args:
        start_text: Start marker (e.g., "## Introduction")
        end_text: End marker (e.g., "##" for next heading)
    """
    # Use browser's find functionality
    await self.page.keyboard.press("Control+F")
    await self.page.keyboard.type(start_text)
    await self.page.keyboard.press("Enter")
    await self.page.keyboard.press("Escape")
    
    # Move to end of start marker
    await self.page.keyboard.press("End")
    
    # Start selection
    await self.page.keyboard.down("Shift")
    
    # Find end marker
    await self.page.keyboard.press("Control+F")
    await self.page.keyboard.type(end_text)
    await self.page.keyboard.press("Enter")
    await self.page.keyboard.press("Escape")
    
    # End selection
    await self.page.keyboard.up("Shift")
```

## Version Comparison

### MarkdownProcessor.compare_versions()

```python
def compare_versions(self, v1_markdown: str, v2_markdown: str) -> List[Change]:
    """Identify changed sections between versions.
    
    Args:
        v1_markdown: Version 1 markdown content
        v2_markdown: Version 2 markdown content
    
    Returns:
        List of changes with section names and new content
    """
    # Parse both versions into sections
    v1_sections = self._parse_sections(v1_markdown)
    v2_sections = self._parse_sections(v2_markdown)
    
    changes = []
    
    # Find modified sections
    for section_name, v2_content in v2_sections.items():
        if section_name not in v1_sections:
            # New section
            changes.append(Change(
                action="add",
                section=section_name,
                content=v2_content
            ))
        elif v1_sections[section_name] != v2_content:
            # Modified section
            changes.append(Change(
                action="replace",
                section=section_name,
                content=v2_content
            ))
    
    # Find deleted sections
    for section_name in v1_sections:
        if section_name not in v2_sections:
            changes.append(Change(
                action="delete",
                section=section_name
            ))
    
    return changes

def _parse_sections(self, markdown: str) -> dict:
    """Parse markdown into sections by heading.
    
    Args:
        markdown: Markdown content
    
    Returns:
        Dict mapping section names to content
    """
    sections = {}
    current_section = None
    current_content = []
    
    for line in markdown.split('\n'):
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections
```

## User Interface

### Version Selector

```python
class MainWindow(QMainWindow):
    def setup_version_ui(self):
        """Set up version selection UI."""
        # Version selector dropdown
        self.version_selector = QComboBox()
        self.version_selector.addItems(['v1', 'v2', 'v3', 'v4', 'v5'])
        self.version_selector.currentTextChanged.connect(self.on_version_changed)
        
        # Current version display
        self.current_version_label = QLabel("Current: v1")
        
        # Change instructions input
        self.change_instructions = QTextEdit()
        self.change_instructions.setPlaceholderText(
            "Enter change instructions:\n"
            "- Replace the introduction\n"
            "- Update methodology section\n"
            "- Add new section after results"
        )
        
        # Apply changes button
        self.apply_changes_btn = QPushButton("Apply Changes")
        self.apply_changes_btn.clicked.connect(self.apply_changes)
        self.apply_changes_btn.setEnabled(False)
    
    def on_version_changed(self, version: str):
        """Handle version selection change."""
        self.current_version_label.setText(f"Current: {version}")
        
        # Enable change instructions for v2+
        if version != 'v1':
            self.change_instructions.setEnabled(True)
            self.apply_changes_btn.setEnabled(True)
        else:
            self.change_instructions.setEnabled(False)
            self.apply_changes_btn.setEnabled(False)
```

### Progress Feedback

```python
async def apply_changes(self):
    """Apply version changes."""
    version = self.version_selector.currentText()
    instructions = self.change_instructions.toPlainText()
    
    # Parse instructions
    self.update_status(f"Parsing change instructions for {version}...")
    parser = ChangeParser()
    changes = parser.parse_instructions(instructions)
    
    # Load new version content
    self.update_status(f"Loading {version} content...")
    article = self.article_parser.parse_file(self.file_path, version)
    
    # Apply each change
    for i, change in enumerate(changes):
        self.update_status(
            f"Applying change {i+1}/{len(changes)}: {change.action} {change.section}"
        )
        self.update_progress(i, len(changes))
        
        await self.medium_editor.apply_change(change, article)
    
    self.update_status(f"{version} changes applied successfully")
    self.update_progress(len(changes), len(changes))
```

## Example Workflow

### Article Evolution: v1 → v2 → v3

**v1 (Initial Draft)**:
```markdown
## Introduction
This article explores AI agents.

## What Are AI Agents?
AI agents are autonomous systems.

## Conclusion
AI agents are the future.
```

**v2 (Expanded)**:
```markdown
## Introduction
This comprehensive article explores the fascinating world of AI agents.

## What Are AI Agents?
AI agents are autonomous systems that can perceive, reason, and act.

## Types of AI Agents
There are several types: reactive, deliberative, and hybrid.

## Conclusion
AI agents represent a significant advancement in artificial intelligence.
```

**Change Instructions for v2**:
```
Replace the introduction
Update the "What Are AI Agents?" section
Add new section "Types of AI Agents" after "What Are AI Agents?"
Replace the conclusion
```

**v3 (Refined)**:
```markdown
## Introduction
This comprehensive article explores the fascinating world of AI agents.

## What Are AI Agents?
AI agents are autonomous systems that can perceive, reason, and act.

## Types of AI Agents
There are several types: reactive, deliberative, and hybrid agents.

## Real-World Applications
AI agents are used in robotics, gaming, and automation.

## Conclusion
AI agents represent a significant advancement in artificial intelligence.
```

**Change Instructions for v3**:
```
Update the "Types of AI Agents" section
Add new section "Real-World Applications" after "Types of AI Agents"
```

## Error Handling

### Section Not Found

```python
try:
    await medium_editor.replace_section("Introduction", new_content)
except ContentError as e:
    logger.error(f"Section not found: {e}")
    # Prompt user to verify section name
    # Or try fuzzy matching
```

### Ambiguous Instructions

```python
def validate_instructions(self, instructions: str) -> List[str]:
    """Validate change instructions.
    
    Returns:
        List of warnings/errors
    """
    warnings = []
    
    # Check for ambiguous section names
    if "section" in instructions.lower() and "'" not in instructions:
        warnings.append("Section name not quoted - may be ambiguous")
    
    # Check for conflicting instructions
    if "replace" in instructions and "update" in instructions:
        warnings.append("Both 'replace' and 'update' used - clarify intent")
    
    return warnings
```

### Selection Failures

```python
async def replace_section(self, section_name: str, new_blocks: List[ContentBlock]):
    """Replace section with retry logic."""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            await self._replace_section_impl(section_name, new_blocks)
            return
        except BrowserError as e:
            if attempt == max_retries - 1:
                raise
            
            logger.warning(f"Selection failed, retrying ({attempt+1}/{max_retries})")
            await asyncio.sleep(2)
```

## Best Practices

1. **Clear Instructions**: Use specific section names
2. **One Change Per Line**: Separate instructions clearly
3. **Test Incrementally**: Apply v2, verify, then v3
4. **Backup Versions**: Keep all markdown versions
5. **Review Before Publishing**: Check all changes in browser

## Limitations

1. **Section Detection**: Relies on markdown headings (##)
2. **Complex Changes**: May require manual intervention
3. **Formatting Preservation**: Some formatting may be lost
4. **Table/Image Handling**: Still requires manual insertion
5. **Browser State**: Requires stable browser connection

## Future Enhancements

1. **Smart Diff**: Automatic change detection
2. **Fuzzy Matching**: Better section identification
3. **Undo/Redo**: Revert changes if needed
4. **Change Preview**: Show changes before applying
5. **Batch Operations**: Apply multiple versions at once

---

**Document Version**: 1.0
**Last Updated**: 2025-03-01
**Maintained By**: Development Team

# Version Update Workflow

## Overview

The version update workflow allows iterative refinement of articles through multiple versions (v1, v2, v3, etc.) without retyping the entire article. Users provide change instructions, and the `VersionUpdateTyper` applies them to the Medium draft using OS-level keyboard automation (Ctrl+F to find sections, Shift+Arrow to select, Backspace to delete, then type replacement content).

## Workflow Phases

### Phase 1: Initial Publication (v1)

```
1. User selects markdown file (v1)
2. System parses content into blocks
3. ContentTyper types complete article via OS-level input
4. Article appears as draft in Medium
5. System waits for next action
```

### Phase 2: Version Update (v2, v3, etc.)

```
1. User selects next version file (v2)
2. User enters change instructions (or auto-detected from diff)
3. ChangeParser extracts search markers and actions
4. VersionUpdateTyper applies changes:
   a. Ctrl+F → type search marker to locate section
   b. Escape to close find dialog
   c. Shift+Right to select old content
   d. Backspace to delete
   e. ContentTyper types new content with formatting
5. Repeat for each instruction
6. System waits for next action
```

### Phase 3: Final Publication

```
1. User reviews all changes in browser
2. User manually inserts tables/images at placeholders
3. User publishes article (draft or public)
```

## Change Instruction Format

### Supported Actions

#### 1. Replace Section

**Format**: "Replace [section name] with [new content]"

**Behavior**:
- Opens Ctrl+F, types section heading to locate it
- Closes find dialog
- Selects section content (Shift+Right for character count)
- Deletes selection (Backspace)
- Types new content via ContentTyper

#### 2. Add Section

**Format**: "Add [new section] after [existing section]"

**Behavior**:
- Finds the reference section via Ctrl+F
- Navigates to end of that section
- Presses Enter to create new line
- Types new section content

#### 3. Delete Section

**Format**: "Delete [section name]"

**Behavior**:
- Finds section via Ctrl+F
- Selects entire section (header + body)
- Deletes selection

#### 4. Multiple Changes

Instructions are processed sequentially, sorted by document position (top → bottom):

```
Replace the introduction
Update the methodology section
Add new section 'Results' after methodology
Delete the old conclusion
```

## VersionUpdateTyper Implementation

### Architecture

```python
class VersionUpdateTyper:
    """Applies change instructions via OS-level keyboard automation.
    
    Dependencies (injected):
        input_controller: OS_Input_Controller (pyautogui wrapper)
        content_typer: ContentTyper (types with formatting/typos)
        change_parser: ChangeParser (extracts search markers)
        config: ConfigManager (delays, timeouts)
    """
    
    def __init__(self, input_controller, content_typer, change_parser, config):
        self._input = input_controller
        self._typer = content_typer
        self._parser = change_parser
        self._config = config
        self._find_delay_ms = config.get("version_update.find_delay_ms", 300)
        self._action_delay_ms = config.get("version_update.action_delay_ms", 150)
```

### Core Method: apply_changes()

```python
def apply_changes(self, instructions, article_content, status_cb=None):
    """Apply all change instructions to the focused Medium editor.
    
    Args:
        instructions: List of ChangeInstruction objects
        article_content: Full article markdown (for marker extraction)
        status_cb: Optional callback for status messages
    
    Returns:
        UpdateResult with applied/skipped/failed counts
    """
    # Sort instructions by document position (top → bottom)
    sorted_instructions = self._sort_by_document_order(instructions, article_content)
    
    for idx, instruction in enumerate(sorted_instructions):
        status_cb(f"Applying {idx + 1}/{total}: {instruction.section}")
        
        if instruction.action in (REPLACE, UPDATE):
            self._handle_replace(instruction, article_content)
        elif instruction.action in (ADD, INSERT_AFTER):
            self._handle_add(instruction, article_content)
        elif instruction.action == DELETE:
            self._handle_delete(instruction, article_content)
```

### Find Section (Ctrl+F)

```python
def _find_section(self, search_marker: str) -> bool:
    """Open Ctrl+F, type search text, close dialog.
    
    Uses OS-level keyboard input — no browser API.
    """
    # Open find dialog
    self._input.hotkey("ctrl", "f")
    time.sleep(self._find_delay_ms / 1000.0)
    
    # Type search marker (no typos — literal search)
    self._input.type_text(search_marker, delay_ms=20)
    time.sleep(self._find_delay_ms / 1000.0)
    
    # Close find dialog — cursor at found text
    self._input.press_key("escape")
    time.sleep(self._action_delay_ms / 1000.0)
    
    return True
```

### Select and Delete

```python
def _select_and_delete(self, char_count: int):
    """Select characters forward using Shift+Right, then delete."""
    for _ in range(char_count):
        self._input.hotkey("shift", "right")
    
    time.sleep(self._action_delay_ms / 1000.0)
    self._input.press_key("backspace")
    time.sleep(self._action_delay_ms / 1000.0)
```

### Type Replacement Content

```python
def _type_replacement(self, new_content: str, formatting: list):
    """Type replacement content via ContentTyper.
    
    Infers block type (paragraph, header, code, list) from content
    and delegates to the appropriate ContentTyper method.
    """
    block = self._content_to_block(new_content, formatting)
    
    dispatch = {
        "paragraph": self._typer.type_paragraph,
        "header": self._typer.type_header,
        "code": self._typer.type_code_block,
        "list": self._typer.type_list,
    }
    
    handler = dispatch.get(block.type, self._typer.type_paragraph)
    handler(block)
```

## Section Identification

### By Heading

The ChangeParser extracts search markers from instructions:

```markdown
## Introduction
Content here...

## Methodology
Content here...
```

**Instruction**: "Replace the introduction"
**Search marker**: "## Introduction" (typed into Ctrl+F)

### Document Order Sorting

Instructions are sorted by their section's position in the markdown source to avoid cursor position conflicts when applying multiple changes.

## User Interface

### Version Selector

```python
# Version selector dropdown (v1-v5)
self.version_selector = QComboBox()
self.version_selector.addItems(['v1', 'v2', 'v3', 'v4', 'v5'])

# Change instructions input (enabled for v2+)
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
```

### Progress Feedback

The UI shows progress as each instruction is applied:
- "Applying 1/3: Introduction"
- "Applying 2/3: Methodology"
- "Applying 3/3: Conclusion"

## Example Workflow

### Article Evolution: v1 → v2 → v3

**v1 (Initial Draft)** — typed in full by ContentTyper:
```markdown
## Introduction
This article explores AI agents.

## What Are AI Agents?
AI agents are autonomous systems.

## Conclusion
AI agents are the future.
```

**v2 Change Instructions**:
```
Replace the introduction
Update the "What Are AI Agents?" section
Add new section "Types of AI Agents" after "What Are AI Agents?"
Replace the conclusion
```

**What VersionUpdateTyper does for each instruction**:
1. Ctrl+F → "## Introduction" → Escape → Select old content → Backspace → Type new intro
2. Ctrl+F → "## What Are AI Agents?" → Escape → Select → Backspace → Type updated content
3. Ctrl+F → "## What Are AI Agents?" → navigate to end → Enter → Type new section
4. Ctrl+F → "## Conclusion" → Escape → Select → Backspace → Type new conclusion

## Error Handling

### Section Not Found

If Ctrl+F doesn't find the search marker, the instruction is skipped with a warning:

```python
if not self._find_section(markers["start_marker"]):
    result.skipped_count += 1
    result.skipped_sections.append((section_name, "section not found"))
    return False
```

### Emergency Stop During Update

If emergency stop triggers mid-update, all modifier keys are released and the error propagates:

```python
except EmergencyStopError:
    self._input.release_all_keys()
    raise  # Workflow layer saves progress
```

### Focus Lost

If the browser loses focus during an update, typing pauses:

```python
except FocusLostError:
    result.failed_count += 1
    raise  # Workflow layer can pause and wait for focus
```

## Safety

All keyboard actions in VersionUpdateTyper go through `OS_Input_Controller`, which checks:
1. **Emergency stop**: Before every keystroke
2. **Focus detection**: Before every keystroke

This means the version update can be stopped instantly at any point, and won't type into the wrong window.

## Limitations

1. **Section Detection**: Relies on exact text match via Ctrl+F
2. **Character Count**: Selection accuracy depends on knowing exact old content length
3. **Complex Changes**: Heavily restructured articles may need manual intervention
4. **Table/Image Handling**: Still requires manual insertion at placeholders
5. **Find Dialog Timing**: Needs sufficient delay for browser find to respond

## Best Practices

1. **Clear Instructions**: Use exact section heading names
2. **One Change Per Line**: Separate instructions clearly
3. **Test Incrementally**: Apply v2, verify, then v3
4. **Keep Versions**: Maintain all markdown version files
5. **Review Before Publishing**: Always check changes in browser before publishing

---

**Last Updated**: 2025-03-01

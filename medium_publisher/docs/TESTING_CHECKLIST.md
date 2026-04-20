# Testing Checklist for Medium Keyboard Publisher

This checklist validates all features of the Medium Keyboard Publisher application.

## Pre-Testing Setup

### Test Environment

- [ ] Windows 10 or Windows 11
- [ ] Python 3.11+ installed
- [ ] Virtual environment activated (`venv\Scripts\activate` from workspace root)
- [ ] All dependencies installed (`pip install -r medium_publisher/requirements.txt`)
- [ ] Internet connection available
- [ ] Browser (Chrome or Edge) installed
- [ ] Display scaling noted (100%, 125%, 150%)
- [ ] Medium account available for testing

### Test Files

- [ ] Sample markdown files prepared (with frontmatter)
- [ ] Test Medium account credentials
- [ ] Google account for OAuth testing (if applicable)

## Application Launch

### First Launch

- [ ] Run `python -m medium_publisher.main` from workspace root
- [ ] Main window displays correctly
- [ ] All UI elements visible
- [ ] Status bar shows "Ready"
- [ ] Window stays on top (if "Always on top" is checked)
- [ ] No import errors in console

### Configuration

- [ ] Default configuration loads
- [ ] Settings dialog opens
- [ ] All settings display correctly
- [ ] Settings can be modified and saved
- [ ] Settings persist after restart

## Screen Recognition

### Reference Image Detection

- [ ] Reference images exist in `medium_publisher/assets/medium/`
- [ ] Images match current display scaling
- [ ] `pyautogui.locateOnScreen()` finds test image on screen
- [ ] Confidence threshold (default 0.8) works for your display
- [ ] Lower confidence (0.6-0.7) finds elements that default misses
- [ ] Higher confidence (0.9) avoids false matches

### Multi-Monitor

- [ ] App works with browser on primary monitor
- [ ] App works with browser on secondary monitor (if applicable)
- [ ] No coordinate offset issues between monitors

### Display Scaling

- [ ] Works at 100% scaling
- [ ] Works at 150% scaling (or recaptured images match)
- [ ] No misclicks due to DPI mismatch

## OS-Level Typing

### Basic Typing

- [ ] Characters appear in focused text field
- [ ] Typing speed matches configured `base_delay_ms`
- [ ] Speed variation is noticeable (not perfectly uniform)
- [ ] Special characters type correctly (punctuation, symbols)
- [ ] Newlines (Enter key) work

### Keyboard Shortcuts

- [ ] Ctrl+B applies bold in Medium editor
- [ ] Ctrl+I applies italic in Medium editor
- [ ] Ctrl+Alt+1 applies Header format
- [ ] Ctrl+Alt+2 applies Subheader format
- [ ] Ctrl+K opens link dialog
- [ ] Ctrl+Enter inserts separator

### Text Selection

- [ ] Shift+Left selects text backwards (for formatting)
- [ ] Selected text receives formatting correctly
- [ ] Selection count matches text length

## Emergency Stop

### Hotkey Stop

- [ ] Press Ctrl+Shift+Escape during typing
- [ ] Typing stops immediately (within 100ms)
- [ ] Status shows "EMERGENCY STOP"
- [ ] All held modifier keys released

### Mouse Corner Stop

- [ ] Move mouse to screen corner during typing
- [ ] Typing stops immediately

### UI Button Stop

- [ ] Click red "Emergency Stop" button
- [ ] Typing stops, status updates

### Key Release on Stop

- [ ] After emergency stop, no keys remain stuck
- [ ] Can type normally in other applications after stop
- [ ] Ctrl, Shift, Alt all released properly

## Focus Detection

### Focus Lost

- [ ] Start typing, then click a different window
- [ ] Typing pauses automatically
- [ ] Status shows focus lost notification

### Focus Restored

- [ ] Click back on the browser window
- [ ] Typing resumes (or prompts to resume)

### Focus During Formatting

- [ ] Focus check happens before every keystroke
- [ ] No partial formatting applied when focus lost mid-operation

## Human Typing Simulation

### Typo Generation

- [ ] Set typo frequency to "medium" (5%)
- [ ] Typos appear during typing (wrong adjacent keys)
- [ ] Immediate corrections: wrong char → 1-3 more chars → backspace → correct
- [ ] Deferred corrections: wrong char stays, fixed in review pass

### Review Pass

- [ ] After all content typed, app goes to top (Ctrl+Home)
- [ ] Uses Ctrl+F to find each deferred typo
- [ ] Fixes each typo by selecting and retyping

### Protected Content

- [ ] No typos in code blocks
- [ ] No typos in URLs
- [ ] No typos in placeholder text
- [ ] No typos in formatting markers (backticks, etc.)

### Thinking Pauses

- [ ] Brief pauses occur occasionally during typing
- [ ] Pauses feel natural (100-500ms range)

## Content Formatting

### Headers

- [ ] `##` headers get Ctrl+Alt+1 (Medium Header)
- [ ] `###` headers get Ctrl+Alt+2 (Medium Subheader)

### Inline Formatting

- [ ] Bold text: typed, selected backwards, Ctrl+B applied
- [ ] Italic text: typed, selected backwards, Ctrl+I applied
- [ ] Inline code: wrapped in backtick characters
- [ ] Links: text typed, selected, Ctrl+K, URL typed, Enter

### Block Elements

- [ ] Code blocks: triple backticks, content (no typos), exit
- [ ] Bullet lists: `* ` prefix triggers Medium list
- [ ] Numbered lists: `1. ` prefix triggers Medium list
- [ ] Block quotes: Ctrl+Alt+5 applied
- [ ] Separators: Ctrl+Enter pressed

### Placeholders

- [ ] Images: `[image: alt text]` typed as plain text
- [ ] Tables: `[table: ...]` typed as plain text
- [ ] No formatting or typos in placeholders

## Batch Publishing

### Sequential Processing

- [ ] Select multiple files via "Select Batch"
- [ ] Articles typed one after another
- [ ] Progress shows "Article 1 of 3", etc.

### Error Handling

- [ ] Invalid file in batch is skipped
- [ ] Next article continues normally
- [ ] Completion summary shows success/failure counts

## Version Updates

### Find and Replace

- [ ] Ctrl+F opens browser find dialog
- [ ] Search text typed correctly (no typos)
- [ ] Section located in editor
- [ ] Old content selected and deleted
- [ ] New content typed with formatting

### Change Instructions

- [ ] Replace instructions work
- [ ] Add instructions work
- [ ] Delete instructions work
- [ ] Multiple instructions processed sequentially

## Progress Display

- [ ] Progress bar advances per block
- [ ] Block counter shows "Block: N / Total"
- [ ] Elapsed time counter runs
- [ ] Remaining time estimate updates

## Logging

- [ ] Log file created at `~/.medium_publisher/logs/`
- [ ] State transitions logged
- [ ] Errors logged with context
- [ ] Emergency stops logged

## Error Handling

### Crash Recovery

- [ ] Force-kill app during typing (Task Manager)
- [ ] No modifier keys remain stuck (atexit hook)
- [ ] App restarts cleanly

### Content Errors

- [ ] Malformed markdown shows error message
- [ ] Missing frontmatter shows error message
- [ ] Empty file handled gracefully

## Edge Cases

- [ ] Very long article (10,000+ words) — no issues
- [ ] Article with emoji and unicode — typed correctly
- [ ] Mixed formatting in one paragraph — applied correctly
- [ ] Article with only code blocks — no typos introduced
- [ ] Rapid emergency stop during formatting shortcut — keys released

## Final Verification

- [ ] No crashes during full test session
- [ ] No data loss or corruption
- [ ] Performance acceptable at configured speed
- [ ] All critical features work end-to-end

---

**Tester Name**: _______________
**Test Date**: _______________
**Application Version**: _______________
**Windows Version**: _______________
**Display Scaling**: _______________

**Notes**:

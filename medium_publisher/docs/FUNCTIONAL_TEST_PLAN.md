# Medium Keyboard Publisher — Functional Test Plan

## Purpose

Manual functional test plan for validating all features of the Medium Keyboard Publisher before release. Each test case includes steps, expected results, and pass/fail tracking.

## Test Environment

- Windows 10/11
- Python 3.11+
- Browser: Chrome or Edge
- Medium account with Google OAuth
- Display: consistent scaling (100% or 150%)
- Launch: `python -m medium_publisher.main` from workspace root
- Venv: `venv\Scripts\activate` from workspace root
- Test article files prepared (see Appendix A)

## Status Tracking

| Symbol | Meaning |
|---|---|
| ⬜ | Not tested |
| ✅ | Pass |
| ❌ | Fail |
| ⏭️ | Skipped |

---

## FT-1: Application Launch and UI

### FT-1.1: Application starts successfully ⬜
1. Run `python -m medium_publisher.main`
2. **Expected**: Window appears with title "Medium Keyboard Publisher"
3. **Expected**: Status bar shows "Ready"
4. **Expected**: Window stays on top of other windows

### FT-1.2: Initial button states ⬜
1. Launch the application (no file selected)
2. **Expected**: "Start Typing" button is disabled
3. **Expected**: "Pause" button is disabled
4. **Expected**: "Emergency Stop" button is enabled
5. **Expected**: "Settings" button is enabled
6. **Expected**: "Select File" and "Select Batch" buttons are enabled

### FT-1.3: Always-on-top toggle ⬜
1. Uncheck "Always on top" checkbox
2. Click on another window
3. **Expected**: Publisher window goes behind the other window
4. Check "Always on top" again
5. **Expected**: Publisher window returns to front

---

## FT-2: File Selection

### FT-2.1: Single file selection ⬜
1. Click "Select File"
2. **Expected**: File dialog opens filtered to `.md` files
3. Select a valid markdown file with frontmatter
4. **Expected**: File path appears in the text field
5. **Expected**: Article info panel shows title, character count, block count, estimated time, tags
6. **Expected**: "Start Typing" button becomes enabled

### FT-2.2: Invalid file rejection ⬜
1. Click "Select File"
2. Change filter to "All Files" and select a `.txt` file
3. **Expected**: Error message about invalid file extension

### FT-2.3: Batch file selection ⬜
1. Click "Select Batch"
2. Select 3 markdown files
3. **Expected**: Label shows "3 files selected"
4. **Expected**: Article info shows batch summary with file names
5. **Expected**: "Start Typing" button becomes enabled

### FT-2.4: Last directory remembered ⬜
1. Select a file from a specific directory
2. Close and reopen the application
3. Click "Select File"
4. **Expected**: File dialog opens in the same directory as last time

---

## FT-3: Draft URL Validation

### FT-3.1: Valid Medium URL accepted ⬜
1. Paste `https://medium.com/p/abc123def/edit` in the draft URL field
2. **Expected**: Status label shows "Valid Medium URL" in green

### FT-3.2: Invalid URL rejected ⬜
1. Paste `https://example.com/article` in the draft URL field
2. **Expected**: Status label shows "Invalid URL" in red

### FT-3.3: Empty URL accepted ⬜
1. Leave the draft URL field empty
2. **Expected**: Status label shows "Leave empty to create a new story" in gray

### FT-3.4: Publication subdomain URL accepted ⬜
1. Paste `https://towardsdatascience.medium.com/my-article-abc123`
2. **Expected**: Status label shows "Valid Medium URL" in green

---

## FT-4: Navigation and Login

### FT-4.1: Opens Medium in browser ⬜
1. Select a markdown file
2. Click "Start Typing"
3. **Expected**: After countdown, Medium.com opens in default browser
4. **Expected**: Status shows navigation progress

### FT-4.2: Detects logged-out state ⬜
1. Ensure you're logged out of Medium
2. Start typing
3. **Expected**: App detects logged-out homepage via screen recognition and clicks "Sign in"

### FT-4.3: Navigates Google OAuth ⬜
1. Start from logged-out state
2. **Expected**: App clicks "Sign in with Google" (locates button via reference image)
3. **Expected**: App selects the configured Google account
4. **Expected**: If 2FA required, status shows "Complete 2FA in the browser"

### FT-4.4: Detects already logged-in state ⬜
1. Log into Medium manually first
2. Start typing
3. **Expected**: App detects logged-in state and navigates directly to editor

### FT-4.5: Draft URL navigation ⬜
1. Create a draft on Medium, copy its URL
2. Paste the URL in the draft URL field
3. Start typing
4. **Expected**: App navigates to the draft instead of creating a new story

### FT-4.6: Navigation timeout ⬜
1. Start typing with browser minimized or on wrong page
2. Wait 30 seconds
3. **Expected**: Error message about page load timeout with retry option

### FT-4.7: Alt Google sign-in screen ⬜
1. If Google shows the alternate account chooser layout
2. **Expected**: App still detects and clicks the correct account (uses google-sign-in-alt.png fallback)

---

## FT-5: Typing — Content Formatting

### FT-5.1: Title and subtitle ⬜
1. Use an article with title and subtitle in frontmatter
2. Start typing
3. **Expected**: Title is typed first, followed by Enter
4. **Expected**: Subtitle is typed with Subheader formatting (Ctrl+Alt+2)

### FT-5.2: Headers ⬜
1. Use an article with `##` and `###` headers
2. **Expected**: `##` headers get Ctrl+Alt+1 (Medium Header)
3. **Expected**: `###` headers get Ctrl+Alt+2 (Medium Subheader)

### FT-5.3: Bold and italic ⬜
1. Use an article with `**bold**` and `*italic*` text
2. **Expected**: Bold text is typed, selected backwards, then Ctrl+B applied
3. **Expected**: Italic text is typed, selected backwards, then Ctrl+I applied

### FT-5.4: Inline code ⬜
1. Use an article with `` `inline code` ``
2. **Expected**: Text is wrapped in backtick characters

### FT-5.5: Links ⬜
1. Use an article with `[link text](https://example.com)`
2. **Expected**: Link text typed, selected, Ctrl+K pressed, URL typed, Enter pressed

### FT-5.6: Code blocks ⬜
1. Use an article with a fenced code block
2. **Expected**: Triple backticks typed, Enter, code content typed WITHOUT typos, exit code block

### FT-5.7: Bullet lists ⬜
1. Use an article with `* item` or `- item` lists
2. **Expected**: Each item prefixed with `* ` to trigger Medium's bullet list

### FT-5.8: Numbered lists ⬜
1. Use an article with `1. item` lists
2. **Expected**: Each item prefixed with `1. ` to trigger Medium's numbered list

### FT-5.9: Block quotes ⬜
1. Use an article with `> quote text`
2. **Expected**: Ctrl+Alt+5 applied, then quote text typed

### FT-5.10: Separators ⬜
1. Use an article with `---` horizontal rule
2. **Expected**: Ctrl+Enter pressed to insert Medium separator

### FT-5.11: Image placeholders ⬜
1. Use an article with `![alt text](url)`
2. **Expected**: `[image: alt text]` typed as plain text (no formatting, no typos)

### FT-5.12: Table placeholders ⬜
1. Use an article with a markdown table
2. **Expected**: `[table: ...]` typed as plain text

---

## FT-6: Human-Like Typing Behavior

### FT-6.1: Variable typing speed ⬜
1. Watch the typing speed during a paragraph
2. **Expected**: Speed varies — not perfectly uniform, some characters faster, some slower

### FT-6.2: Thinking pauses ⬜
1. Watch typing between sentences and paragraphs
2. **Expected**: Brief pauses between sentences (100-500ms) and longer pauses between paragraphs

### FT-6.3: Immediate typo correction ⬜
1. Set typo frequency to "medium" (5%) in Settings
2. Watch typing
3. **Expected**: Occasional wrong characters typed, then 1–3 more characters, then backspace to fix

### FT-6.4: Deferred typo correction (review pass) ⬜
1. Set typo frequency to "medium" or "high"
2. Watch the full typing flow
3. **Expected**: After all content is typed, the app goes to top (Ctrl+Home), uses Ctrl+F to find and fix remaining typos

### FT-6.5: No typos in protected content ⬜
1. Use an article with code blocks, URLs, and placeholders
2. **Expected**: These are typed perfectly — no typos introduced

---

## FT-7: Safety Controls

### FT-7.1: Emergency stop via hotkey ⬜
1. Start typing an article
2. Press Ctrl+Shift+Escape during typing
3. **Expected**: Typing stops immediately (within 100ms)
4. **Expected**: All held modifier keys released
5. **Expected**: Status shows "EMERGENCY STOP"

### FT-7.2: Emergency stop via mouse corner ⬜
1. Start typing an article
2. Move mouse to any screen corner
3. **Expected**: Typing stops immediately

### FT-7.3: Emergency stop via UI button ⬜
1. Start typing an article
2. Click the red "Emergency Stop" button
3. **Expected**: Typing stops, status shows "EMERGENCY STOP"

### FT-7.4: Pause and resume ⬜
1. Start typing an article
2. Click "Pause"
3. **Expected**: Typing stops after current character, button changes to "Resume"
4. Click "Resume"
5. **Expected**: Typing continues from where it paused

### FT-7.5: Focus window detection ⬜
1. Start typing an article
2. Click on a different window (not the browser)
3. **Expected**: Typing pauses automatically
4. **Expected**: Notification about lost focus
5. Click back on the browser
6. **Expected**: Typing resumes (or prompts to resume)

### FT-7.6: Countdown before typing ⬜
1. Click "Start Typing"
2. **Expected**: Large countdown display shows 3, 2, 1, Go!
3. **Expected**: Typing begins only after countdown reaches 0

### FT-7.7: Button states during typing ⬜
1. Start typing
2. **Expected**: "Start Typing" disabled, "Pause" enabled
3. **Expected**: "Select File", "Select Batch", "Settings" disabled
4. **Expected**: "Emergency Stop" always enabled

---

## FT-8: Batch Publishing

### FT-8.1: Sequential article processing ⬜
1. Select 3 markdown files via "Select Batch"
2. Start typing
3. **Expected**: Articles typed one after another
4. **Expected**: Progress shows "Article 1 of 3", "Article 2 of 3", etc.

### FT-8.2: Pause between articles ⬜
1. Run a batch of 2+ articles
2. **Expected**: Brief pause between articles before the next one starts

### FT-8.3: Skip on failure ⬜
1. Include one invalid file in a batch (e.g., missing frontmatter)
2. **Expected**: Invalid file is skipped with error logged
3. **Expected**: Next article continues normally

### FT-8.4: Completion summary ⬜
1. Complete a batch run
2. **Expected**: Summary shows how many succeeded and failed

---

## FT-9: Completion and Placeholders

### FT-9.1: Completion notification ⬜
1. Let an article finish typing completely
2. **Expected**: Completion dialog appears

### FT-9.2: Placeholder listing ⬜
1. Use an article with images and tables
2. Let typing complete
3. **Expected**: Completion notification lists all placeholders (e.g., "[image: diagram]", "[table: metrics]")
4. **Expected**: User can manually insert actual images/tables at those locations

---

## FT-10: Settings

### FT-10.1: Settings dialog opens ⬜
1. Click "Settings"
2. **Expected**: Settings dialog appears with all sections (Typing, Safety, Navigation, Paths, UI)

### FT-10.2: Typing speed change ⬜
1. Change base delay to 80ms (faster)
2. Save and start typing
3. **Expected**: Typing is noticeably faster

### FT-10.3: Typo frequency change ⬜
1. Change typo frequency from "low" to "high"
2. Save and start typing
3. **Expected**: More typos appear during typing

### FT-10.4: Emergency stop hotkey change ⬜
1. Change hotkey to "ctrl+shift+q"
2. Save, start typing, press Ctrl+Shift+Q
3. **Expected**: Emergency stop triggers with new hotkey

### FT-10.5: Settings persistence ⬜
1. Change several settings and save
2. Close and reopen the application
3. Open Settings
4. **Expected**: All changed values are preserved

### FT-10.6: Screen confidence adjustment ⬜
1. Lower screen confidence to 0.6
2. Start typing
3. **Expected**: Screen recognition is more lenient (may match slightly different UI)

---

## FT-11: Progress Display

### FT-11.1: Block progress bar ⬜
1. Start typing a multi-block article
2. **Expected**: Progress bar advances as each block is typed
3. **Expected**: Block counter shows "Block: N / Total"

### FT-11.2: Estimated time remaining ⬜
1. Start typing
2. **Expected**: Elapsed time counter runs
3. **Expected**: Remaining time estimate updates as progress advances

### FT-11.3: Batch progress label ⬜
1. Run a batch of 3 articles
2. **Expected**: Label shows "Article 1 of 3", updates for each article

---

## FT-12: Error Handling

### FT-12.1: Crash recovery — keys released ⬜
1. Force-kill the application during typing (Task Manager)
2. **Expected**: No modifier keys remain stuck (atexit hook releases them)
3. If keys feel stuck, press and release Ctrl, Shift, Alt manually

### FT-12.2: Error during typing ⬜
1. Simulate an error (e.g., close the browser mid-typing)
2. **Expected**: Emergency stop triggers automatically (focus lost)
3. **Expected**: Error message displayed
4. **Expected**: All modifier keys released

### FT-12.3: Log file written ⬜
1. Run the application and perform some actions
2. Check `~/.medium_publisher/logs/medium_publisher.log`
3. **Expected**: Log file exists with timestamped entries
4. **Expected**: State transitions, errors, and key operations logged

---

## FT-13: Edge Cases

### FT-13.1: Empty article ⬜
1. Select a markdown file with frontmatter but no body content
2. **Expected**: Appropriate error or warning displayed

### FT-13.2: Very long article ⬜
1. Select a markdown file with 10,000+ words
2. **Expected**: Typing proceeds without issues
3. **Expected**: Estimated time is reasonable

### FT-13.3: Special characters and unicode ⬜
1. Use an article with emoji, accented characters, symbols
2. **Expected**: Characters typed correctly

### FT-13.4: Mixed formatting in one paragraph ⬜
1. Use a paragraph with bold, italic, code, and links mixed together
2. **Expected**: Each formatting range applied correctly without corrupting adjacent text

### FT-13.5: Nested lists ⬜
1. Use an article with nested bullet/numbered lists
2. **Expected**: Items typed with correct prefixes (Medium may not support deep nesting — verify behavior)

---

## Appendix A: Test Article Files

Create these files for testing:

### test-basic.md
Basic article with title, subtitle, 2 paragraphs, 1 header.

### test-formatting.md
Article with all formatting types: bold, italic, code, links, headers, lists, block quotes, separators.

### test-code.md
Article with multiple code blocks in different languages.

### test-placeholders.md
Article with images (`![alt](url)`) and markdown tables.

### test-long.md
Article with 5000+ words for performance testing.

### test-unicode.md
Article with emoji, accented characters (é, ñ, ü), and symbols (→, ©, ™).

### test-batch-1.md, test-batch-2.md, test-batch-3.md
Three short articles for batch testing.

### test-invalid.md
File with missing or malformed frontmatter for error testing.

---

## Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Tester | | | |
| Developer | | | |

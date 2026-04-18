# Medium Keyboard Publisher - Requirements

## Introduction

This specification defines the requirements for a desktop application that publishes markdown articles to Medium using OS-level keyboard and mouse control (pyautogui, pynput). Unlike browser automation approaches (Playwright), this application types content through the operating system's input layer, producing real keyboard and mouse events indistinguishable from human input. The application opens Medium in the user's default browser, uses screen image recognition to detect login state and navigate the UI, and handles parsing, typing, formatting, and human-like behavior simulation.

## Glossary

- **Markdown_File**: Source article file in markdown format with YAML frontmatter containing title, subtitle, tags, and keywords
- **Medium_Editor**: Medium's web-based rich text editor where articles are composed, managed by the user in their own browser
- **Keyboard_Publisher**: The desktop application that types content into the focused window using OS-level input events
- **OS_Input_Controller**: Component using pyautogui and pynput to generate real keyboard and mouse events at the operating system level
- **Frontmatter**: YAML metadata block at the beginning of markdown files enclosed by `---` delimiters
- **Content_Block**: A parsed unit of article content (paragraph, header, code block, list, link, placeholder) ready for typing
- **Human_Typing_Simulator**: Component that introduces realistic typing patterns including variable speed (~60 WPM base), typos, immediate corrections, and deferred corrections via review pass
- **Emergency_Stop**: Safety mechanism that immediately halts all keyboard and mouse automation when triggered
- **Focus_Window**: The currently active window receiving keyboard input from the operating system
- **Screen_Recognition**: Component using pyautogui's `locateOnScreen()` to find UI elements by matching reference screenshot images
- **Reference_Image**: A pre-captured screenshot of a specific UI element (button, icon, text) used for Screen_Recognition matching
- **Login_Detector**: Component that uses Screen_Recognition to determine if the user is logged into Medium or needs to authenticate
- **Draft_Mode**: Publishing state where the article is saved as a draft for review
- **Public_Mode**: Publishing state where the article is immediately visible to readers
- **Publishing_Session**: A single execution of the application to type one or more articles into Medium
- **Version_Cycle**: The iterative process of updating an article through v1, v2, v3, etc. by modifying specific sections

## Requirements

### Requirement 1: Select Markdown File for Publishing

**User Story:** As a content creator, I want to select a markdown file from my filesystem, so that I can publish it to Medium.

#### Acceptance Criteria

1. WHEN the user launches the application, THE Keyboard_Publisher SHALL display a native desktop window with a file selection button
2. WHEN the user clicks the file selection button, THE Keyboard_Publisher SHALL open a file selection dialog filtered to .md files
3. WHEN the user selects a file, THE Keyboard_Publisher SHALL validate the file has a .md extension
4. WHEN the user selects a valid markdown file, THE Keyboard_Publisher SHALL parse the Frontmatter and display article metadata (title, subtitle, tags, character count, estimated typing time)
5. IF the selected file is not a valid Markdown_File, THEN THE Keyboard_Publisher SHALL display a descriptive error message and allow reselection
6. THE Keyboard_Publisher SHALL remember the last selected directory across sessions
7. THE Keyboard_Publisher SHALL allow selection of multiple Markdown_Files for batch publishing

### Requirement 2: Parse Markdown Content

**User Story:** As a content creator, I want my markdown content parsed correctly, so that formatting is preserved when typed into Medium.

#### Acceptance Criteria

1. THE Keyboard_Publisher SHALL parse YAML Frontmatter to extract metadata (title, subtitle, tags, keywords)
2. THE Keyboard_Publisher SHALL parse markdown headers (##) and convert them to Content_Blocks with Medium Header level (Ctrl+Alt+1)
3. THE Keyboard_Publisher SHALL parse markdown subheaders (###) and convert them to Content_Blocks with Medium Subheader level (Ctrl+Alt+2)
4. THE Keyboard_Publisher SHALL treat any deeper heading levels (####, #####) as Subheader since Medium only supports two heading levels
3. THE Keyboard_Publisher SHALL parse bold text (\*\*text\*\*) and convert to Content_Blocks with bold formatting markers
4. THE Keyboard_Publisher SHALL parse italic text (\*text\*) and convert to Content_Blocks with italic formatting markers
5. THE Keyboard_Publisher SHALL parse code blocks (\`\`\`language\`\`\`) and convert to Content_Blocks with code block type
6. THE Keyboard_Publisher SHALL parse inline code (\`code\`) and convert to Content_Blocks with inline code formatting markers
7. THE Keyboard_Publisher SHALL parse links (\[text\](url)) and convert to Content_Blocks with link metadata
8. THE Keyboard_Publisher SHALL parse bullet lists and convert to Content_Blocks with list type
9. THE Keyboard_Publisher SHALL parse numbered lists and convert to Content_Blocks with ordered list type
10. THE Keyboard_Publisher SHALL preserve paragraph breaks (double newlines) as separate Content_Blocks
11. WHEN markdown tables are detected, THE Keyboard_Publisher SHALL insert a placeholder Content_Block with the format `[table: <caption or context>]` (e.g., `[table: performance comparison]`)
12. WHEN markdown images are detected, THE Keyboard_Publisher SHALL insert a placeholder Content_Block with the format `[image: <alt text>]` (e.g., `[image: featured image]`, `[image: architecture diagram]`)

### Requirement 3: Browser Navigation and Login Detection

**User Story:** As a content creator, I want the application to open Medium, detect if I'm logged in, and help me log in if needed, so that I don't have to manually set up the browser before typing.

#### Reference Images

The application ships with pre-captured Reference_Images in `assets/medium/` representing each page state in the navigation flow:

| Reference Image | Page State | Key Indicators |
|---|---|---|
| `home-page-logged-out.png` | Medium homepage (logged out) | "Sign in" button, "Get started" button visible |
| `sign-in-screen.png` | Medium sign-in page | Authentication options including Google OAuth |
| `google-sign-in.png` | Google OAuth account chooser | "Choose an account" page with user's Google accounts listed |
| `medium-logged-in.png` | Medium homepage (logged in) | Profile avatar, "Write" button visible |
| `medium-drafts-page.png` | Medium drafts list | List of user's draft articles |
| `medium-new-story-page.png` | Medium new story editor | Empty editor with title field ready for input |

#### Navigation State Machine

```
START → Open Medium.com
  ↓
[Screen Recognition: Which page?]
  ├── Matches home-page-logged-out.png → Click "Sign in" → sign-in-screen
  ├── Matches sign-in-screen.png → Click "Sign in with Google" → google-sign-in
  ├── Matches google-sign-in.png → Click configured Google account (default: diverdan326@gmail.com) → Wait for 2FA if needed → poll for logged-in state
  ├── Matches medium-logged-in.png → Click "Write" or navigate to new story / draft URL
  ├── Matches medium-drafts-page.png → Click target draft or navigate to new story
  └── Matches medium-new-story-page.png → Ready to type (DONE)
```

#### Acceptance Criteria

1. THE Keyboard_Publisher SHALL open Medium.com in the user's default browser using `webbrowser.open()`
2. THE Keyboard_Publisher SHALL wait for the browser to load and then use Screen_Recognition to detect the current page state
3. THE Login_Detector SHALL use pyautogui `locateOnScreen()` with Reference_Images to identify which page state the browser is currently showing
4. THE Login_Detector SHALL check against all 6 Reference_Images to determine the current state: logged-out homepage, sign-in screen, Google OAuth screen, logged-in homepage, drafts page, or new story editor
5. WHERE the screen matches `home-page-logged-out.png`, THE Keyboard_Publisher SHALL locate and click the "Sign in" button to navigate to the sign-in screen
6. WHERE the screen matches `sign-in-screen.png`, THE Keyboard_Publisher SHALL locate and click the "Sign in with Google" button
7. WHERE the screen matches `google-sign-in.png`, THE Keyboard_Publisher SHALL use Screen_Recognition to locate and click the configured Google account (default: diverdan326@gmail.com) on the "Choose an account" page
8. WHERE the user has Google 2FA enabled, THE Keyboard_Publisher SHALL display a status message: "Complete 2FA in the browser" and wait for the user to complete authentication manually (up to 5 minutes timeout)
9. THE Login_Detector SHALL poll for page state changes every 2 seconds during the login flow
10. WHERE the screen matches `medium-logged-in.png`, THE Keyboard_Publisher SHALL locate and click the "Write" button or navigate to the new story page
11. WHERE a draft URL is provided, THE Keyboard_Publisher SHALL navigate to the draft URL instead of the new story page
12. WHERE the screen matches `medium-drafts-page.png`, THE Keyboard_Publisher SHALL navigate to the new story page or the specified draft URL
13. WHERE the screen matches `medium-new-story-page.png`, THE Keyboard_Publisher SHALL report "Ready to type" and enable the Start Typing button
14. IF no Reference_Image matches the current screen within 30 seconds, THEN THE Keyboard_Publisher SHALL display an error with a screenshot of the current state and allow retry
15. IF login is not detected within the timeout period (5 minutes), THEN THE Keyboard_Publisher SHALL display an error and allow retry
16. THE Keyboard_Publisher SHALL ship with the default Reference_Images in `assets/medium/` for the 6 page states listed above
17. THE Keyboard_Publisher SHALL allow users to recapture Reference_Images via a settings interface for when Medium updates its UI
18. THE Keyboard_Publisher SHALL support configurable confidence threshold for Screen_Recognition matching (default: 0.8)
19. THE Keyboard_Publisher SHALL log each state transition in the navigation flow for debugging

### Requirement 4: Type Content Using OS-Level Keyboard Control

**User Story:** As a content creator, I want the application to type my article into Medium's editor using real keyboard events, so that Medium cannot detect automation.

#### Acceptance Criteria

1. THE OS_Input_Controller SHALL generate real operating system keyboard events using pyautogui and pynput
2. THE OS_Input_Controller SHALL type content into whatever window currently has focus (the Focus_Window)
3. WHEN typing the article title, THE OS_Input_Controller SHALL type the title text followed by Enter to move to the next line
4. WHEN the Frontmatter contains a subtitle, THE OS_Input_Controller SHALL type the subtitle text on the line immediately after the title and apply Medium's Subheader format (Ctrl+Alt+2), then press Enter to move to the content area
5. WHEN typing a paragraph, THE OS_Input_Controller SHALL type the paragraph text followed by Enter to create a new line
5. WHEN typing a header (## in markdown), THE OS_Input_Controller SHALL type the header text and apply Medium's Header format using Ctrl+Alt+1
6. WHEN typing a subheader (### in markdown), THE OS_Input_Controller SHALL type the subheader text and apply Medium's Subheader format using Ctrl+Alt+2
7. WHEN typing bold text, THE OS_Input_Controller SHALL select the text and apply bold formatting using Ctrl+B
8. WHEN typing italic text, THE OS_Input_Controller SHALL select the text and apply italic formatting using Ctrl+I
9. WHEN typing a code block, THE OS_Input_Controller SHALL type three backticks (```) to enter code block mode, then type the code without typo simulation
10. WHEN typing inline code, THE OS_Input_Controller SHALL wrap the text with backtick characters (`)
11. WHEN typing a link, THE OS_Input_Controller SHALL type the link text, select it, press Ctrl+K, and type the URL followed by Enter
12. WHEN typing a bullet list item, THE OS_Input_Controller SHALL type `* ` (asterisk + space) at the beginning of the line to trigger Medium's bullet list, then type the item text
13. WHEN typing a numbered list item, THE OS_Input_Controller SHALL type `1. ` (number + dot + space) at the beginning of the line to trigger Medium's numbered list, then type the item text
14. WHEN typing a block quote, THE OS_Input_Controller SHALL apply Medium's quote format using Ctrl+Alt+5
15. WHEN typing a separator/horizontal rule, THE OS_Input_Controller SHALL insert a separator using Ctrl+Enter
16. THE OS_Input_Controller SHALL handle special characters and unicode correctly
17. THE OS_Input_Controller SHALL type placeholder lines for tables and images (e.g., `[image: featured image]`, `[table: metrics]`) without formatting

### Requirement 5: Simulate Human-Like Typing Behavior

**User Story:** As a content creator, I want the typing to appear human-like, so that Medium's bot detection does not flag my account.

#### Acceptance Criteria

1. THE Human_Typing_Simulator SHALL vary typing speed randomly within ±30% of the configured base delay per keystroke (default: 200ms, representing ~60 WPM)
2. THE Human_Typing_Simulator SHALL add occasional thinking pauses of 500ms-2s between sentences and 1-3s between paragraphs
3. WHERE human-like typing is enabled, THE Human_Typing_Simulator SHALL introduce realistic typos at a configurable frequency (low: 2%, medium: 5%, high: 8%)
4. WHERE a typo is introduced, THE Human_Typing_Simulator SHALL type an adjacent key on the QWERTY keyboard layout
5. THE Human_Typing_Simulator SHALL classify each typo into one of two correction patterns: immediate correction (default 70%) or deferred correction (default 30%)
6. WHERE a typo is classified as immediate correction, THE Human_Typing_Simulator SHALL continue typing 1-3 additional characters, then use backspace to delete the typo and extra characters, and retype correctly
7. WHERE a typo is classified as deferred correction, THE Human_Typing_Simulator SHALL NOT correct the typo during typing and SHALL record its location (paragraph index, character offset, wrong character, correct character)
8. WHEN all content has been typed, THE Human_Typing_Simulator SHALL perform a review pass to correct all deferred typos
9. DURING the review pass, THE OS_Input_Controller SHALL navigate to the top of the document using Ctrl+Home
10. DURING the review pass, THE OS_Input_Controller SHALL use Ctrl+F to find each deferred typo by searching for the surrounding text context
11. DURING the review pass, THE OS_Input_Controller SHALL pause briefly (500-2000ms) at each typo location to simulate reading/noticing the error
12. DURING the review pass, THE OS_Input_Controller SHALL select the incorrect character(s), delete them, and type the correct character(s)
13. DURING the review pass, THE OS_Input_Controller SHALL close the find dialog (Escape) after each correction and proceed to the next deferred typo
14. THE Human_Typing_Simulator SHALL NOT introduce typos in code blocks, URLs, or placeholder lines (e.g., `[image: ...]`, `[table: ...]`)
15. THE Keyboard_Publisher SHALL calculate and display estimated typing time before publishing, accounting for both immediate and deferred typo overhead
18. THE Keyboard_Publisher SHALL allow configuration of the immediate vs deferred typo ratio in settings (default: 70/30)

### Requirement 6: Safety Controls for OS-Level Input

**User Story:** As a content creator, I want safety controls to stop automation immediately, so that I can regain control of my keyboard and mouse at any time.

#### Acceptance Criteria

1. THE Keyboard_Publisher SHALL provide an Emergency_Stop mechanism that immediately halts all keyboard and mouse automation
2. WHEN the user moves the mouse to any screen corner, THE Keyboard_Publisher SHALL trigger the Emergency_Stop (pyautogui failsafe)
3. WHEN the user presses a configurable hotkey (default: Ctrl+Shift+Escape), THE Keyboard_Publisher SHALL trigger the Emergency_Stop
4. WHEN the Emergency_Stop is triggered, THE OS_Input_Controller SHALL release all held keys and stop all pending input events within 100ms
5. THE Keyboard_Publisher SHALL provide a pause/resume toggle button in the application window
6. WHEN the user clicks pause, THE OS_Input_Controller SHALL stop typing after completing the current word
7. WHEN the user clicks resume, THE OS_Input_Controller SHALL continue typing from where it paused
8. THE Keyboard_Publisher SHALL display a visible countdown (3, 2, 1) before starting to type, giving the user time to focus the correct window
9. IF the Focus_Window changes during typing, THEN THE Keyboard_Publisher SHALL pause typing and notify the user to refocus the Medium_Editor

### Requirement 7: Draft URL and Navigation Support

**User Story:** As a content creator, I want to provide a Medium draft URL, so that the application types into an existing draft instead of requiring a new story.

#### Acceptance Criteria

1. THE Keyboard_Publisher SHALL provide an optional input field for a Medium draft URL
2. WHERE a draft URL is provided, THE Keyboard_Publisher SHALL validate the URL matches Medium's draft or story URL format
3. IF the draft URL is invalid, THEN THE Keyboard_Publisher SHALL display an error message describing the expected format
4. THE Keyboard_Publisher SHALL display instructions for the user to navigate to the draft URL or new story page in their browser before typing begins
5. WHERE no draft URL is provided, THE Keyboard_Publisher SHALL instruct the user to navigate to Medium's new story page manually

### Requirement 8: Preview Before Publishing

**User Story:** As a content creator, I want to review the typed article before publishing, so that I can verify formatting and manually insert tables and images.

#### Acceptance Criteria

1. WHEN content typing is complete, THE Keyboard_Publisher SHALL pause and display a completion notification
2. WHERE placeholders exist in the typed content (e.g., `[image: ...]`, `[table: ...]`), THE Keyboard_Publisher SHALL list all placeholders and notify the user to manually insert the actual images and tables before publishing
3. THE Keyboard_Publisher SHALL provide options to: mark as complete, or cancel the session
4. WHEN the user marks as complete, THE Keyboard_Publisher SHALL log the session as successful and proceed to the next article (if batch publishing)

### Requirement 9: Article Metadata Entry

**User Story:** As a content creator, I want article tags and subtitle typed automatically, so that my articles are properly categorized.

#### Acceptance Criteria

1. THE Keyboard_Publisher SHALL provide an option to type tags from Frontmatter into Medium's tag input field using keyboard control
2. THE Keyboard_Publisher SHALL provide an option to type the subtitle from Frontmatter into Medium's subtitle field using keyboard control
3. THE Keyboard_Publisher SHALL support up to 5 tags (Medium's limit)
4. IF more than 5 tags are provided in Frontmatter, THEN THE Keyboard_Publisher SHALL use the first 5 tags
5. THE Keyboard_Publisher SHALL validate tags contain only alphanumeric characters, hyphens, and spaces
6. THE Keyboard_Publisher SHALL display instructions for the user to focus the appropriate field before typing metadata

### Requirement 10: Batch Publishing

**User Story:** As a content creator, I want to publish multiple articles in one session, so that I can efficiently publish a series of articles.

#### Acceptance Criteria

1. THE Keyboard_Publisher SHALL allow selection of multiple Markdown_Files for sequential publishing
2. WHEN multiple files are selected, THE Keyboard_Publisher SHALL process them sequentially, pausing between each for user confirmation
3. THE Keyboard_Publisher SHALL display progress for each article (e.g., "Article 1 of 3")
4. IF one article fails or is cancelled, THEN THE Keyboard_Publisher SHALL allow the user to skip to the next article
5. WHEN all articles are processed, THE Keyboard_Publisher SHALL display a summary report of successful and failed publications

### Requirement 11: Iterative Version Updates

**User Story:** As a content creator, I want to update an article through multiple versions incrementally, so that I can refine content without retyping the entire article.

#### Acceptance Criteria

1. WHEN publishing version 1, THE Keyboard_Publisher SHALL type the complete article content
2. WHEN version 1 is complete, THE Keyboard_Publisher SHALL pause and wait for user instructions
3. THE Keyboard_Publisher SHALL provide an interface for the user to describe changes for the next version
4. WHEN the user provides change instructions, THE Keyboard_Publisher SHALL parse the instructions to identify sections to modify
5. THE Keyboard_Publisher SHALL use keyboard shortcuts (Ctrl+F) to navigate to specified sections in the Medium_Editor
6. THE Keyboard_Publisher SHALL select old content using Shift+arrow keys and delete it
7. THE Keyboard_Publisher SHALL type new content with human-like behavior at the deletion point
8. THE Keyboard_Publisher SHALL preserve unchanged sections
9. THE Keyboard_Publisher SHALL support multiple iteration cycles (v1 → v2 → v3 → etc.)
10. THE Keyboard_Publisher SHALL maintain context of the current version number across the session

### Requirement 12: Application Settings

**User Story:** As a content creator, I want to configure application settings, so that I can customize typing behavior and safety controls.

#### Acceptance Criteria

1. THE Keyboard_Publisher SHALL provide a settings dialog for configuration
2. THE Keyboard_Publisher SHALL allow configuration of base typing speed (delay between keystrokes, default 200ms / ~60 WPM)
3. THE Keyboard_Publisher SHALL allow configuration of typing speed variation range (default: ±30%)
4. THE Keyboard_Publisher SHALL allow configuration of human-like typing simulation (enabled/disabled)
5. THE Keyboard_Publisher SHALL allow configuration of typo frequency (low/medium/high)
6. THE Keyboard_Publisher SHALL allow configuration of the immediate vs deferred typo correction ratio (default: 70% immediate, 30% deferred)
6. THE Keyboard_Publisher SHALL allow configuration of default publish mode (draft vs public)
7. THE Keyboard_Publisher SHALL allow configuration of the Emergency_Stop hotkey
8. THE Keyboard_Publisher SHALL allow configuration of the pre-typing countdown duration
9. THE Keyboard_Publisher SHALL allow configuration of the default article directory
10. THE Keyboard_Publisher SHALL allow configuration of the Google account email to select on the OAuth account chooser (default: diverdan326@gmail.com)
11. THE Keyboard_Publisher SHALL save settings to a persistent configuration file (YAML format)
12. THE Keyboard_Publisher SHALL load saved settings on application startup

### Requirement 13: Error Handling and Logging

**User Story:** As a content creator, I want errors handled gracefully with detailed logging, so that I can diagnose and recover from issues.

#### Acceptance Criteria

1. IF an unexpected error occurs during typing, THEN THE Keyboard_Publisher SHALL trigger the Emergency_Stop, log the error, and display an error message
2. IF the Markdown_File contains unsupported syntax, THEN THE Keyboard_Publisher SHALL log a warning and skip the unsupported element
3. THE Keyboard_Publisher SHALL provide a scrollable log display in the application window showing operation history
4. THE Keyboard_Publisher SHALL write logs to a rotating log file (rotate at 10MB)
5. THE Keyboard_Publisher SHALL log at configurable levels (DEBUG, INFO, WARNING, ERROR)
6. THE Keyboard_Publisher SHALL save typing progress (last typed Content_Block index) to allow manual recovery after errors
7. IF the application crashes, THEN THE Keyboard_Publisher SHALL log the crash details and release all held keys before exiting

### Requirement 14: Desktop User Interface

**User Story:** As a content creator, I want a user-friendly native desktop interface, so that I can easily control the typing automation.

#### Acceptance Criteria

1. THE Keyboard_Publisher SHALL provide a native desktop window using PyQt6
2. THE Keyboard_Publisher SHALL display application status (idle, countdown, typing, paused, complete, error)
3. THE Keyboard_Publisher SHALL display a real-time log of operations
4. THE Keyboard_Publisher SHALL provide buttons for: Select File, Start Typing, Pause/Resume, Emergency Stop, Settings
5. THE Keyboard_Publisher SHALL disable buttons when their actions are not available (e.g., disable Start when no file is selected)
6. THE Keyboard_Publisher SHALL provide keyboard shortcuts for common actions
7. THE Keyboard_Publisher SHALL remember window size and position across sessions
8. THE Keyboard_Publisher SHALL display the current article's character count and estimated typing time (accounting for typo overhead)
9. THE Keyboard_Publisher SHALL display a progress bar showing typing progress within the current article
10. THE Keyboard_Publisher SHALL always remain on top of other windows (configurable) so the user can see status while Medium is focused

## Non-Functional Requirements

### NFR-1: Performance

1. THE Keyboard_Publisher SHALL type content at a configurable base speed (default 200ms per keystroke, ~60 WPM)
2. THE Keyboard_Publisher SHALL vary typing speed randomly (±30%) to simulate human typing
3. THE Keyboard_Publisher SHALL type common words/patterns faster and uncommon words slower within the variation range
4. THE Keyboard_Publisher SHALL calculate and display estimated typing time before publishing, accounting for typos, corrections, and review pass
5. THE Keyboard_Publisher SHALL handle articles up to 50,000 words

### NFR-2: Reliability

1. THE Keyboard_Publisher SHALL release all held keys when the application exits (normal or abnormal)
2. THE Keyboard_Publisher SHALL save typing progress periodically to enable manual recovery
3. THE Keyboard_Publisher SHALL retry failed keyboard operations up to 3 times before reporting an error

### NFR-3: Usability

1. THE Keyboard_Publisher SHALL provide clear error messages with actionable guidance
2. THE Keyboard_Publisher SHALL provide progress indicators for long-running typing operations
3. THE Keyboard_Publisher SHALL follow Windows platform UI conventions
4. THE Keyboard_Publisher SHALL display clear instructions for manual steps (focusing browser, navigating to draft URL)

### NFR-4: Security

1. THE Keyboard_Publisher SHALL NOT store any Medium or Google credentials (user authenticates directly with Google in the browser)
2. THE Keyboard_Publisher SHALL NOT log sensitive content from articles
3. THE Keyboard_Publisher SHALL store configuration files with appropriate file permissions
4. THE Keyboard_Publisher SHALL store Reference_Images locally and not transmit them over the network

### NFR-5: Maintainability

1. THE Keyboard_Publisher SHALL use modular architecture separating UI, parsing, typing, and safety concerns
2. THE Keyboard_Publisher SHALL separate OS input control logic from content processing logic
3. THE Keyboard_Publisher SHALL provide comprehensive logging for debugging

## Constraints

- Must run on Windows 10/11
- Requires Python 3.11+
- Requires pyautogui and pynput for OS-level input control
- Requires PyQt6 for desktop UI
- Requires Pillow/OpenCV for screen image recognition
- User must have a browser installed (app opens Medium automatically)
- Screen recognition accuracy depends on display resolution and scaling settings
- Limited by Medium's rate limits and terms of service
- No browser automation libraries (Playwright, Selenium) are used

## Assumptions

- User has a valid Medium account (Google-linked or email/password)
- User's markdown files follow consistent Frontmatter format (title, subtitle, tags)
- Medium's keyboard shortcuts for formatting (Ctrl+B, Ctrl+I, Ctrl+Alt+2, etc.) remain stable
- Medium's visual UI elements (buttons, icons) remain recognizable by Reference_Images
- The application runs on the same machine where the browser is open
- User has permission to use automation tools on their own account
- Display scaling is consistent (reference images captured at the same DPI/scaling as runtime)

## Dependencies

- pyautogui (OS-level keyboard and mouse control, screen image recognition via `locateOnScreen()`)
- pynput (keyboard event monitoring for hotkeys and emergency stop)
- PyQt6 (native desktop UI)
- Pillow (image processing for screen recognition)
- python-frontmatter or PyYAML (frontmatter parsing)
- markdown2 or mistune (markdown parsing)
- PyYAML (configuration management)

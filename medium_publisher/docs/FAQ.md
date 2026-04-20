# Medium Article Publisher - Frequently Asked Questions

## Table of Contents
1. [General Questions](#general-questions)
2. [Installation & Setup](#installation--setup)
3. [Authentication](#authentication)
4. [Publishing](#publishing)
5. [Typing Speed](#typing-speed)
6. [Human Typing](#human-typing)
7. [Screen Recognition](#screen-recognition)
8. [Version Management](#version-management)
9. [Safety Features](#safety-features)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)

## General Questions

### What is the Medium Article Publisher?

A desktop application that types your markdown articles into Medium's editor using OS-level keyboard input (pyautogui) with realistic human-like behavior. It recognizes screen states via reference images rather than browser automation.

### Why use this instead of copy-paste?

- Automated formatting (headers, bold, italic, code blocks) via keyboard shortcuts
- Version management for incremental updates
- Human-like typing patterns
- Batch publishing multiple articles
- Consistent, repeatable workflow

### How does it work technically?

The app uses:
- **pyautogui** to send keystrokes at the OS level (same as physically typing)
- **pynput** to monitor keyboard for emergency stop
- **Screen recognition** (reference PNG images) to detect navigation states
- **No browser automation** — your regular browser is used as-is

### What platforms are supported?

Currently Windows 10/11 only. Linux and macOS support may be added in the future.

## Installation & Setup

### What are the system requirements?

- Windows 10/11 (64-bit)
- Python 3.11+
- 4 GB RAM
- Internet connection
- A browser where you're logged into Medium (or can log in)

### How long does installation take?

Approximately 3-5 minutes:
- Python dependencies: 2-3 minutes
- Configuration review: 1-2 minutes

No browser download required — the app uses your existing browser.

### Do I need to install a special browser?

No. The application sends keystrokes to whatever window has focus. You use your own browser (Chrome, Firefox, Edge, etc.) and navigate to Medium yourself or let the app guide you via screen recognition.

### Where are files stored?

- **Application**: Installation directory
- **Configuration**: `config/default_config.yaml`
- **Reference images**: `assets/medium/`
- **Articles**: Wherever you keep your markdown files

### How do I launch the application?

```cmd
python -m medium_publisher.main
```

Run from the workspace root directory.

## Authentication

### How does login work?

The application does NOT log you in automatically. Instead:

1. The app detects whether you're logged in by checking the screen (reference images)
2. If not logged in, it navigates to Medium's sign-in page
3. **You complete the OAuth flow manually** in your browser
4. The app detects when login succeeds (screen recognition)
5. Publishing proceeds

### Why doesn't the app handle login automatically?

Because there's no browser automation (no Playwright/Selenium). The app only sends keystrokes and reads the screen. OAuth flows require clicking specific UI elements that change frequently — manual login is more reliable and secure.

### How long do I have to log in?

Default: 300 seconds (5 minutes), configurable via `navigation.login_timeout_seconds`.

### What if I'm already logged in?

The app detects this via screen recognition and skips the login wait entirely.

### Does the app store my credentials?

No. The app never sees or stores your password. You authenticate directly in your browser.

### Can I use Google 2FA / security keys?

Yes — since you complete login manually in your browser, any authentication method Google supports will work.

## Publishing

### What markdown features are supported?

**Supported** (typed with keyboard shortcuts):
- Headers (##, ###)
- Bold (**text**)
- Italic (*text*)
- Code blocks (```code```)
- Inline code (`code`)
- Links ([text](url))
- Bullet lists
- Numbered lists
- Paragraphs

**Not Supported** (placeholders inserted):
- Tables (TODO placeholder)
- Images (TODO placeholder)

### Why aren't tables and images supported?

These require mouse interaction with Medium's UI (drag-and-drop, file pickers). Since the app uses keyboard input only, it inserts TODO placeholders for you to handle manually.

### What happens if publishing fails mid-article?

- Emergency stop triggered: typing halts immediately
- Focus lost: typing pauses, raises `FocusLostError`
- Progress is tracked by SessionManager for potential resume
- Logs contain detailed error information

## Typing Speed

### How fast does it type?

Speed is controlled by `typing.base_delay_ms` in config (default: 150ms per keystroke). With default settings:
- ~400 characters per minute (without pauses/typos)
- Actual speed varies with thinking pauses, paragraph pauses, and typo corrections

### Can I make it faster?

Yes. Lower `base_delay_ms`:
- 50ms: ~1200 chars/min theoretical
- 100ms: ~600 chars/min theoretical
- 150ms (default): ~400 chars/min theoretical
- 250ms: ~240 chars/min theoretical

There is no hard rate limit enforced by the app. Speed is entirely controlled by your config.

### Is there a rate limit?

No. Unlike browser automation tools that enforce artificial rate limits, this app types at whatever speed you configure. However, typing too fast may:
- Look less human-like
- Potentially trigger Medium's anti-automation detection (unconfirmed)

**Recommendation**: Keep `base_delay_ms` at 100+ for safety.

### How long does it take to publish an article?

Depends on your `base_delay_ms` setting and content length. With defaults (150ms, human typing enabled):
- 500 chars: ~2-3 minutes
- 2000 chars: ~8-12 minutes
- 5000 chars: ~20-30 minutes

Thinking pauses and paragraph pauses add ~20-40% overhead.

## Human Typing

### What is human typing simulation?

Realistic typing behavior including:
- Speed variations (±30% per keystroke by default)
- Thinking pauses between sentences
- Paragraph pauses between blocks
- Optional typos with corrections

### How do typos work?

When `typo_frequency` is not "none":
1. App decides to make a typo (based on configured frequency)
2. Types an adjacent key (QWERTY layout)
3. Either corrects immediately (backspace + retype) or defers correction
4. `immediate_correction_ratio` controls the split (default 70% immediate)

### Are typos made in code blocks?

No. Typos are disabled for code blocks, URLs, and special formatting sequences.

### Can I disable typos entirely?

Yes. Set `typing.typo_frequency: "none"` in config (this is the default).

## Screen Recognition

### How does screen recognition work?

The app takes screenshots and compares them against reference PNG images stored in `assets/medium/`. When a reference image matches the screen above the confidence threshold, the app knows what state it's in.

### What if screen recognition fails?

Common causes and fixes:
- **Display scaling mismatch**: Reference images were captured at a different DPI. Recapture at your resolution.
- **Theme change**: Medium updated their UI. Update reference images.
- **Low confidence**: Lower `navigation.screen_confidence` (e.g., 0.7)
- **Multiple monitors**: Ensure the browser is on the primary monitor

### Can I update reference images?

Yes. Take new screenshots of the relevant UI elements and save them as PNG files in `assets/medium/`. Match the existing naming convention.

### What states does the app recognize?

- `LOGGED_OUT_HOME` — Medium homepage, not logged in
- `SIGN_IN_SCREEN` — Medium sign-in page
- `GOOGLE_SIGN_IN` — Google OAuth page
- `LOGGED_IN_HOME` — Medium homepage, logged in
- `DRAFTS_PAGE` — User's drafts list
- `NEW_STORY_EDITOR` — Medium's story editor (ready for typing)

## Version Management

### What is the version workflow?

Update articles incrementally (v1 → v2 → v3) without retyping the entire article. Only changed sections are retyped.

### How do I use versions?

1. Publish `article-v1.md` (full article typed)
2. Create `article-v2.md` with changes
3. Write change instructions (what to replace/add/delete)
4. App finds sections and applies changes (only modified content is retyped)

### What change actions are supported?

- **Replace**: Find section by header, delete, type new content
- **Delete**: Remove section
- **Add**: Append new section
- **Insert After/Before**: Insert content relative to existing section

## Safety Features

### What is the emergency stop?

Press `Ctrl+Shift+Escape` (configurable) at any time to immediately halt all typing. This is monitored by pynput in a background thread and works regardless of which window has focus.

### What is focus checking?

When `safety.focus_check_enabled` is true, the app verifies the target window has focus before each keystroke batch. If focus is lost (you clicked another window), typing pauses and raises `FocusLostError` to prevent keystrokes going to the wrong application.

### What is the countdown?

Before typing begins, a countdown (default 3 seconds) gives you time to position your cursor or cancel. Configurable via `safety.countdown_seconds`.

## Configuration

### Where is configuration stored?

`config/default_config.yaml` in the project directory.

### How do I change settings?

Edit `config/default_config.yaml` directly, or use the Settings UI in the application.

### What are the main config sections?

- `typing`: Speed, variation, human typing, typos
- `publishing`: Default mode, max tags
- `safety`: Emergency stop, countdown, focus check
- `navigation`: Screen confidence, timeouts, email
- `ui`: Window behavior
- `assets`: Reference images directory

### How do I reset to defaults?

```cmd
git checkout -- config\default_config.yaml
```

## Troubleshooting

### Application won't start

1. Verify Python: `python --version` (need 3.11+)
2. Install dependencies: `pip install -r requirements.txt`
3. Run from workspace root: `python -m medium_publisher.main`

### Keystrokes going to wrong window

1. Enable `safety.focus_check_enabled: true`
2. Ensure the browser window is focused before typing starts
3. Don't click other windows during typing
4. Use emergency stop (`Ctrl+Shift+Escape`) if needed

### Screen recognition not detecting states

1. Check `assets/medium/` has reference images
2. Lower `navigation.screen_confidence` (try 0.7)
3. Verify display scaling matches reference images
4. Ensure browser is on primary monitor
5. Recapture reference images if Medium's UI changed

### Login detection timing out

1. Increase `navigation.login_timeout_seconds`
2. Complete login faster in your browser
3. Verify the logged-in reference image matches your screen

### Typing seems stuck

1. Check if focus was lost (look for FocusLostError in logs)
2. Check if emergency stop was accidentally triggered
3. Verify the editor is ready (cursor blinking in Medium's editor)
4. Check logs for NavigationError or InputControlError

### Where are logs?

Check the application's log output. Log level can be adjusted in the logger configuration.

---

**Still Have Questions?** See the [User Guide](USER_GUIDE_KEYBOARD_PUBLISHER.md) for detailed walkthroughs or [CONFIGURATION.md](CONFIGURATION.md) for all settings.

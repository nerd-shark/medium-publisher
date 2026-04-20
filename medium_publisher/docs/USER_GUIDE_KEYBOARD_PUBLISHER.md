# Medium Keyboard Publisher — User Guide

## What It Does

Medium Keyboard Publisher types your markdown articles into Medium's editor using real OS-level keyboard and mouse events. It opens Medium in your default browser, navigates through login using screen recognition, and types your content character-by-character with human-like timing, typos, and corrections — making the input indistinguishable from manual typing.

## Prerequisites

- Windows 10/11
- Python 3.11+
- A web browser installed (Chrome, Edge, Firefox — whichever is your default)
- A Medium account linked to Google
- Display scaling consistent with reference images (typically 100% or 150%)

No Playwright. No Chromium installation. No browser automation libraries. The app uses your existing browser and controls it through OS-level input.

## Installation

Run these commands from the **workspace root** (the folder that *contains* `medium_publisher/`):

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r medium_publisher\requirements.txt
```

Dependencies installed: PyQt6, pyautogui, pynput, Pillow, pywin32, pycryptodome, markdown2, PyYAML, python-dotenv, keyring.

## Launching

You must launch from the **workspace root** so Python can find the `medium_publisher` package:

```cmd
venv\Scripts\activate
python -m medium_publisher.main
```

If you get `ModuleNotFoundError: No module named 'medium_publisher'`, you're probably running from inside the `medium_publisher/` directory. Move up one level (`cd ..`) and try again.

The application window appears and stays on top of other windows by default.

## Preparing Your Article

Your markdown file needs YAML frontmatter:

```markdown
---
title: My Article Title
subtitle: An optional subtitle
tags:
  - python
  - automation
keywords:
  - medium publishing
---

## Introduction

Your article content here with **bold**, *italic*, `inline code`, and [links](https://example.com).

### Code Example

```python
print("hello world")
```

* Bullet item one
* Bullet item two

1. Numbered item one
2. Numbered item two

> A block quote

---

## Conclusion

Final thoughts.
```

### Supported Formatting

| Markdown | What Happens in Medium |
|---|---|
| `## Header` | Ctrl+Alt+1 (Medium Header) |
| `### Subheader` | Ctrl+Alt+2 (Medium Subheader) |
| `**bold**` | Text typed, selected, Ctrl+B |
| `*italic*` | Text typed, selected, Ctrl+I |
| `` `code` `` | Wrapped in backticks |
| `[text](url)` | Text typed, selected, Ctrl+K, URL typed |
| `* item` | `* ` prefix triggers Medium bullet list |
| `1. item` | `1. ` prefix triggers Medium numbered list |
| `> quote` | Ctrl+Alt+5 |
| `---` | Ctrl+Enter (separator) |
| ` ``` ` code block | Triple backticks, code typed without typos |
| `![alt](url)` | Placeholder: `[image: alt]` |
| Tables | Placeholder: `[table: caption]` |

Images and tables are typed as placeholder text. You insert the actual content manually after typing completes.

## Publishing Workflow

### Single Article

1. Click "Select File" and pick your `.md` file
2. Review the article info panel (title, character count, estimated time, tags)
3. Optionally paste a Medium draft URL (to type into an existing draft)
4. Click "Start Typing"
5. A countdown (3, 2, 1) gives you time to position yourself
6. The app opens Medium.com in your default browser via `webbrowser.open()`
7. Screen recognition detects the page state and navigates through login
8. Once in the editor, content is typed character-by-character using pyautogui
9. After typing completes, a review pass fixes any deferred typos
10. A completion notification lists any placeholders you need to fill manually

### Batch Publishing

1. Click "Select Batch" and pick multiple `.md` files
2. Click "Start Typing"
3. Articles are typed sequentially with a pause between each
4. Progress shows "Article N of M"
5. If one article fails, it's skipped and the next one starts

### Draft URL

If you already have a Medium draft open, paste its URL in the draft URL field. Supported formats:
- `https://medium.com/p/<id>/edit`
- `https://medium.com/@<user>/<slug>`
- `https://<publication>.medium.com/<slug>`

Leave empty to create a new story.

## How Navigation Works

The app doesn't use any browser automation API. Instead, it:

1. Opens a URL in your default browser using Python's `webbrowser` module
2. Waits a moment for the page to load
3. Takes a screenshot and searches for reference PNG images using `pyautogui.locateOnScreen()`
4. Based on which reference image matches, determines the current page state
5. Clicks the appropriate button (at the coordinates where the image was found)
6. Repeats until the editor is reached

This is a finite state machine with states like: `MEDIUM_HOME → SIGN_IN_PAGE → GOOGLE_OAUTH → ACCOUNT_SELECTOR → EDITOR_READY`.

## Login Flow

1. Opens Medium.com in your default browser
2. Detects the current page state by matching reference screenshots
3. Clicks through: Sign In → Sign in with Google → Select account
4. If 2FA is required, displays "Complete 2FA in the browser" and waits (up to 5 minutes)
5. Navigates to the new story editor (or your draft URL)

If the screen doesn't match any reference image within 30 seconds, an error is shown with a retry option.

### Recapturing Reference Images

If Medium or Google updates their UI and screen recognition stops working:

1. Navigate to the page manually in your browser
2. Use the Settings dialog to recapture reference images
3. Images are stored in `medium_publisher/assets/medium/`
4. Make sure your display scaling matches when you recapture

## Safety Controls

### Emergency Stop (most important)

Three ways to halt all automation immediately:

1. **Hotkey**: Press `Ctrl+Shift+Escape` (configurable in Settings)
2. **Mouse corner**: Move your mouse to any screen corner
3. **UI button**: Click the red "Emergency Stop" button

All held modifier keys are released instantly. Typing progress is saved.

### Pause / Resume

- Click "Pause" to stop typing after the current word
- Click "Resume" to continue from where it paused
- Pause does NOT release keys or lose progress

### Focus Detection

If you switch away from the browser window during typing, the app automatically pauses and notifies you. Refocus the browser to continue. This prevents typing into the wrong application.

### Countdown

A 3-second countdown (configurable) runs before typing starts, giving you time to ensure the Medium editor has focus.

## Settings

Open Settings from the main window. All settings are saved to `~/.medium_publisher/config.yaml` and override the defaults in `medium_publisher/config/default_config.yaml`.

### Typing

| Setting | Default | Description |
|---|---|---|
| Base delay | 200 ms | Time between keystrokes (~60 WPM) |
| Speed variation | ±30% | Random variation around base delay |
| Typo frequency | Low (2%) | How often typos are introduced |
| Immediate/deferred ratio | 70/30 | 70% of typos fixed inline, 30% fixed in review pass |

### Safety

| Setting | Default | Description |
|---|---|---|
| Emergency stop hotkey | Ctrl+Shift+Escape | Key combo to halt everything |
| Mouse corner failsafe | Enabled | Move mouse to corner to stop |
| Countdown duration | 3 seconds | Pre-typing countdown |

### Navigation

| Setting | Default | Description |
|---|---|---|
| Google account email | (your email) | Account to select on Google OAuth screen |
| Screen confidence | 0.8 | Image matching threshold (0.0–1.0) |
| Navigation timeout | 30 seconds | Max wait for page state detection |

### UI

| Setting | Default | Description |
|---|---|---|
| Always on top | Yes | Keep app window above other windows |
| Remember window position | Yes | Restore window position on restart |

## Troubleshooting

### Typing goes to the wrong window
The app types into whatever window has focus. Make sure the Medium editor is focused before the countdown finishes. The focus detector should pause if focus is lost, but verify it's enabled in Settings.

### Screen recognition fails
- Check your display scaling matches when the reference images were captured
- Lower the screen confidence threshold in Settings (try 0.7)
- Recapture reference images at your current resolution/scaling
- Ensure your browser isn't in dark mode if references were captured in light mode
- Check that the browser window isn't partially off-screen

### Emergency stop doesn't work
- The mouse-to-corner failsafe always works (move mouse to any screen corner)
- If the hotkey doesn't trigger, check if another app is capturing that key combo
- You can always kill the Python process from Task Manager as a last resort

### Stuck modifier keys
If Ctrl/Shift/Alt feel stuck after a crash, the app releases all keys on exit. If it didn't clean up properly, press and release each modifier key manually, or tap Ctrl, Shift, and Alt once each.

### ModuleNotFoundError on launch
You're running from the wrong directory. Launch from the workspace root:
```cmd
cd C:\path\to\workspace-root
venv\Scripts\activate
python -m medium_publisher.main
```

### Login flow gets stuck
- The navigation state machine has a 30-second timeout per state
- If it can't detect the next state, it shows an error with retry option
- Try recapturing reference images if the UI has changed
- Ensure your browser is maximized (reference images assume a specific layout)

### Logs
Logs are written to `~/.medium_publisher/logs/medium_publisher.log` (rotates at 10MB). Check here for detailed error information including which reference images were searched for and whether they matched.

## Technical Notes

- All typing happens through `pyautogui.press()` and `pyautogui.typewrite()` — OS-level events
- Screen recognition uses `pyautogui.locateOnScreen()` with Pillow for image matching
- The browser is opened via `webbrowser.open()` — no browser automation library is involved
- The app has no access to the DOM, cookies, or network requests — it only sees pixels on screen
- Typing runs in a QThread so the PyQt6 UI stays responsive throughout
- The human typing simulator uses a Gaussian distribution for delays and a keyboard-adjacency model for typos

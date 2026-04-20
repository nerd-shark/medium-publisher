# Quick Start Guide

## TL;DR — Get Publishing in 3 Minutes

### 1. Install (from workspace root — the folder containing `medium_publisher/`)

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r medium_publisher\requirements.txt
```

### 2. Launch

```cmd
venv\Scripts\activate
python -m medium_publisher.main
```

### 3. Publish

1. Select your markdown file (needs YAML frontmatter with `title`)
2. Click "Start Typing"
3. The app opens Medium in your default browser
4. Screen recognition navigates through login (complete Google OAuth manually if prompted)
5. Content is typed character-by-character into the editor
6. Done — review your draft in Medium

## What Works

✅ OS-level typing via pyautogui (real keystrokes)
✅ Screen recognition for navigation (reference PNG images)
✅ Human-like typing (variable speed, optional typos, thinking pauses)
✅ Formatting (headers, bold, italic, code, links, lists, quotes)
✅ Emergency stop (Ctrl+Shift+Escape, mouse corner, UI button)
✅ Focus detection (pauses if browser loses focus)
✅ Batch publishing (multiple articles sequentially)
✅ Version updates (modify existing drafts incrementally)

## Common Issues

**ModuleNotFoundError**: You're in the wrong directory. Run from the workspace root, not inside `medium_publisher/`.

**Screen recognition fails**: Lower confidence threshold in Settings (try 0.7). Check display scaling matches reference images.

**Typing goes to wrong window**: Enable focus detection in Settings. Don't click other windows during typing.

## File Locations

- **Logs**: `%USERPROFILE%\.medium_publisher\logs\`
- **Config**: `medium_publisher\config\default_config.yaml`
- **Reference images**: `medium_publisher\assets\medium\`

## Documentation

- [User Guide](docs/USER_GUIDE_KEYBOARD_PUBLISHER.md) — Full usage instructions
- [Setup](docs/SETUP.md) — Detailed installation
- [Architecture](docs/ARCHITECTURE.md) — How it works
- [Configuration](docs/CONFIGURATION.md) — All settings
- [Troubleshooting](docs/TROUBLESHOOTING.md) — Common problems
- [FAQ](docs/FAQ.md) — Frequently asked questions

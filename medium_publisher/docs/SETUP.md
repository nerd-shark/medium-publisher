# Medium Article Publisher - Setup Instructions

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [First-Time Setup](#first-time-setup)
4. [Verification](#verification)
5. [Troubleshooting Installation](#troubleshooting-installation)

## System Requirements

### Operating System
- Windows 10 (64-bit) or later
- Windows 11 (64-bit)

### Software Requirements
- **Python**: 3.11 or higher
- **Internet Connection**: Required for Medium access
- **A web browser**: Chrome, Edge, or Firefox (your default browser is used)
- **Disk Space**: ~200 MB (Python packages only — no bundled browser)
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Display**: Consistent scaling (100% or 150%) for screen recognition

### Medium Account
- Active Medium account
- Google account linked to Medium (Google OAuth is the supported login flow)

## Installation

All commands run from the **workspace root** — the folder that *contains* `medium_publisher/`.

### Step 1: Install Python

1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```
   Should output: `Python 3.11.x` or higher

### Step 2: Download Application

1. Download or clone the application source code
2. Extract to a directory (e.g., `C:\projects\medium-workspace\`)
3. Open Command Prompt in that directory (the workspace root)

### Step 3: Create Virtual Environment

```cmd
REM Create virtual environment (from workspace root)
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Verify activation (prompt should show (venv))
```

### Step 4: Install Dependencies

**Important**: The requirements file is inside the `medium_publisher/` subdirectory.

**Option A: Standard Installation (Public PyPI)**

```cmd
pip install -r medium_publisher\requirements.txt --index-url https://pypi.org/simple/
```

**Option B: Corporate Environment with CodeArtifact**

```cmd
pip install -r medium_publisher\requirements.txt --index-url https://pypi.org/simple/ --extra-index-url https://your-codeartifact-url/simple/
```

**Option C: Default pip Configuration**

```cmd
pip install -r medium_publisher\requirements.txt
```

**Packages Installed**:
- PyQt6 — Desktop UI framework
- pyautogui — OS-level mouse/keyboard control
- pynput — Keyboard/mouse event listening (hotkeys, focus detection)
- Pillow — Image processing for screen recognition
- pywin32 — Windows API access (window management)
- pycryptodome — Encryption utilities
- markdown2 — Markdown parsing
- PyYAML — Configuration files
- python-dotenv — Environment variable loading
- keyring — Secure credential storage

**That's it.** No browser installation step. The app uses your existing default browser via the `webbrowser` module.

### Step 5: Verify Installation

```cmd
REM Launch the application (from workspace root)
python -m medium_publisher.main
```

The PyQt6 application window should appear. If it does, you're good to go.

## First-Time Setup

### Step 1: Configure Settings

1. Launch the application: `python -m medium_publisher.main`
2. Click the **Settings** button (⚙️ icon)
3. Configure your preferences:

**Typing Settings**:
- Base Delay: 200ms (default, ~60 WPM)
- Speed Variation: ±30%
- Typo Frequency: Low (2%)
- Immediate/Deferred Ratio: 70/30

**Safety Settings**:
- Emergency Stop Hotkey: Ctrl+Shift+Escape
- Mouse Corner Failsafe: Enabled
- Countdown Duration: 3 seconds

**Navigation Settings**:
- Google Account Email: Your Google email for OAuth
- Screen Confidence Threshold: 0.8

**UI Settings**:
- Always on Top: Yes
- Remember Window Position: Yes

4. Click **Save**

### Step 2: Verify Display Scaling

Screen recognition relies on reference PNG images matching what's on screen. If your display scaling doesn't match the reference images:

1. Check your Windows display scaling (Settings → Display → Scale)
2. The reference images were captured at a specific scaling (typically 100% or 150%)
3. If recognition fails, you can recapture reference images from Settings

### Step 3: Prepare Test Article

Create a test markdown file (`test-article.md`):

```markdown
---
title: "Test Article"
subtitle: "Testing the Medium Publisher"
tags:
  - test
  - automation
---

# Introduction

This is a test article to verify the Medium Article Publisher is working correctly.

## Section 1

Some test content here with **bold** and *italic* text.

## Conclusion

If you can see this article in Medium, the publisher is working!
```

### Step 4: Test the Full Flow

1. Click **"Select File"** and pick your test markdown
2. Review the article info (title, character count, estimated time)
3. Click **"Start Typing"**
4. The app opens Medium.com in your default browser
5. Screen recognition detects the page state and navigates through login
6. Once in the editor, content is typed character-by-character
7. After completion, review the article in Medium

## Verification

### Verify All Dependencies

```cmd
venv\Scripts\activate
python -c "import PyQt6; import pyautogui; import pynput; import PIL; import markdown2; import yaml; import keyring; print('All dependencies installed successfully!')"
```

Expected output: `All dependencies installed successfully!`

### Verify Configuration

Check configuration files exist:

```cmd
dir medium_publisher\config\

REM Should show:
REM - default_config.yaml
```

### Verify Reference Images

```cmd
dir medium_publisher\assets\medium\

REM Should show PNG files used for screen recognition
```

### Verify Logs

After first run, check logs directory:

```cmd
dir %USERPROFILE%\.medium_publisher\logs\

REM Should show log files
```

## Troubleshooting Installation

### Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH:
   - Open System Properties → Environment Variables
   - Add Python installation directory to PATH
   - Restart Command Prompt

### ModuleNotFoundError: No module named 'medium_publisher'

**Error**: Running `python -m medium_publisher.main` gives ModuleNotFoundError

**Solution**: You're running from the wrong directory. You must be in the workspace root (the folder that *contains* `medium_publisher/`), not inside it.

```cmd
REM Wrong — inside the package
cd medium_publisher
python -m medium_publisher.main  ← FAILS

REM Correct — at workspace root
cd ..
python -m medium_publisher.main  ← WORKS
```

### Pip Install Fails

**Error**: `pip install` fails with permission error

**Solution**:
```cmd
pip install --user -r medium_publisher\requirements.txt --index-url https://pypi.org/simple/
```

**Error**: `401 Error` or `Could not find a version that satisfies the requirement`

**Solution**: Your pip is configured to use a custom index that doesn't have all packages.
```cmd
pip install -r medium_publisher\requirements.txt --index-url https://pypi.org/simple/
```

### PyQt6 Import Error

**Error**: `ImportError: DLL load failed while importing QtCore`

**Solution**:
```cmd
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6
```

### pyautogui Fails to Import

**Error**: `ImportError: No module named 'pyautogui'` or Pillow-related errors

**Solution**:
```cmd
pip uninstall pyautogui Pillow
pip install Pillow pyautogui
```

### Screen Recognition Not Working

**Symptoms**: App can't detect Medium's login page or editor state

**Solutions**:
1. Check display scaling matches reference images
2. Lower confidence threshold in Settings (try 0.7)
3. Recapture reference images at your current resolution/scaling
4. Ensure your browser isn't in dark mode if references were captured in light mode

### Keyring Access Error

**Error**: `keyring.errors.NoKeyringError`

**Solution**:
- Windows Credential Manager should work automatically
- If not, credentials will be prompted each time
- This doesn't prevent the app from working

### Virtual Environment Issues

**Error**: Cannot activate virtual environment

**Solution**:
```cmd
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r medium_publisher\requirements.txt
```

### Permission Denied Errors

**Error**: `PermissionError: [WinError 5] Access is denied`

**Solution**:
1. Run Command Prompt as Administrator
2. Or install to user directory:
   ```cmd
   pip install --user -r medium_publisher\requirements.txt
   ```

## Post-Installation

### Create Desktop Shortcut (Optional)

Create a batch file `launch_medium_publisher.bat`:
```cmd
@echo off
cd /d C:\path\to\workspace-root
call venv\Scripts\activate
python -m medium_publisher.main
```

Create a shortcut to this batch file on your desktop.

### Update Application

```cmd
venv\Scripts\activate
git pull
pip install -r medium_publisher\requirements.txt --upgrade --index-url https://pypi.org/simple/
```

### Uninstall

```cmd
rmdir /s /q C:\path\to\workspace-root\venv
rmdir /s /q %USERPROFILE%\.medium_publisher
```

## Next Steps

1. Read the [User Guide](USER_GUIDE_KEYBOARD_PUBLISHER.md) for detailed usage instructions
2. Review the [Architecture](ARCHITECTURE.md) for technical details

---

**Installation Complete!** You're ready to start publishing articles to Medium.

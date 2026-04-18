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
- **Internet Connection**: Required for Medium access and browser automation
- **Disk Space**: ~500 MB (includes Python packages and Chromium browser)
- **RAM**: Minimum 4 GB (8 GB recommended)

### Medium Account
- Active Medium account
- Google account (if using Google OAuth)
- Email/password credentials (if using traditional login)

## Installation

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

1. Download the application source code
2. Extract to a directory (e.g., `C:\medium_publisher\`)
3. Open Command Prompt in that directory

### Step 3: Create Virtual Environment

```cmd
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Verify activation (prompt should show (venv))
```

### Step 4: Install Dependencies

**Important**: If you're in a corporate environment with AWS CodeArtifact or custom pip index, you may need to use the public PyPI index.

**Option A: Standard Installation (Public PyPI)**

```cmd
REM Install from public PyPI (recommended)
pip install -r requirements.txt --index-url https://pypi.org/simple/
```

**Option B: Corporate Environment with CodeArtifact**

If you need both CodeArtifact and public PyPI:

```cmd
REM Use public PyPI as primary, CodeArtifact as fallback
pip install -r requirements.txt --index-url https://pypi.org/simple/ --extra-index-url https://your-codeartifact-url/simple/
```

**Option C: Default pip Configuration**

If your pip is already configured correctly:

```cmd
REM Install with default configuration
pip install -r requirements.txt
```

**Packages Installed**:
- PyQt6 (desktop UI)
- playwright (browser automation)
- PyYAML (configuration)
- keyring (credential storage)
- pytest (testing framework)
- And other dependencies

### Step 5: Install Playwright Browsers

```cmd
REM Install Chromium browser for automation
playwright install chromium

REM This downloads ~150 MB
```

### Step 6: Verify Installation

```cmd
REM Run application
python main.py

REM Application window should appear
```

## First-Time Setup

### Step 1: Configure Settings

1. Launch the application: `python main.py`
2. Click the **Settings** button (⚙️ icon)
3. Configure your preferences:

**Typing Settings**:
- Typing Speed: 30ms (default, adjust if needed)
- Human-like Typing: Enabled (recommended)
- Typo Frequency: Low or Medium

**Publishing Settings**:
- Default Mode: Draft (recommended for first use)

**Browser Settings**:
- Browser Visibility: Visible (recommended for first use)

**Paths Settings**:
- Default Article Directory: Select your articles folder

**Credentials Settings**:
- Remember Login: Enabled (for convenience)

4. Click **Save**

### Step 2: Prepare Test Article

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

Some test content here.

## Conclusion

If you can see this article in Medium, the publisher is working!
```

### Step 3: Authenticate with Medium

**Option A: Google OAuth (Recommended)**

1. Click **"Login"** button
2. Select **"Google OAuth"** from dropdown
3. Browser window opens to Medium login page
4. Click **"Sign in with Google"** in the browser
5. Complete Google authentication
6. Application detects successful login
7. Status shows: "Logged in successfully"

**Option B: Email/Password**

1. Click **"Login"** button
2. Select **"Email/Password"** from dropdown
3. Enter your Medium email and password
4. Click **"Login"**
5. If 2FA is enabled, complete it in the browser
6. Status shows: "Logged in successfully"

### Step 4: Publish Test Article

1. Click **"Select File"** button
2. Navigate to `test-article.md`
3. Select the file
4. Review the estimated time (should be ~5-10 minutes for short article)
5. Click **"Publish Version"** button
6. Confirm the operation
7. Watch the progress bar
8. When complete, review the article in Medium
9. Verify content is correct
10. Publish or delete the test article in Medium

## Verification

### Verify Installation

Run the verification script:

```cmd
REM Activate virtual environment
venv\Scripts\activate

REM Run verification
python -c "import PyQt6; import playwright; import yaml; import keyring; print('All dependencies installed successfully!')"
```

Expected output: `All dependencies installed successfully!`

### Verify Browser

```cmd
REM Check Playwright browsers
playwright --version

REM Should show version number
```

### Verify Configuration

Check configuration files exist:

```cmd
dir medium_publisher\config\

REM Should show:
REM - default_config.yaml
REM - selectors.yaml
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

### Pip Install Fails

**Error**: `pip install` fails with permission error

**Solution**:
```cmd
REM Run as administrator or use --user flag
pip install --user -r requirements.txt --index-url https://pypi.org/simple/
```

**Error**: `401 Error, Credentials not correct` or `Could not find a version that satisfies the requirement`

**Solution**: Your pip is configured to use AWS CodeArtifact or a custom index that doesn't have all packages.

```cmd
REM Use public PyPI index
pip install -r requirements.txt --index-url https://pypi.org/simple/
```

**Error**: `WARNING: Retrying` or connection timeout

**Solution**: Network or firewall issue
```cmd
REM Use corporate proxy if required
set HTTP_PROXY=http://proxy:port
set HTTPS_PROXY=http://proxy:port
pip install -r requirements.txt --index-url https://pypi.org/simple/
```

### Playwright Install Fails

**Error**: `playwright install` fails

**Solution**:
```cmd
REM Try with specific browser
playwright install chromium --force

REM Or install system dependencies
playwright install-deps chromium
```

### Virtual Environment Issues

**Error**: Cannot activate virtual environment

**Solution**:
```cmd
REM Delete and recreate
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### PyQt6 Import Error

**Error**: `ImportError: DLL load failed while importing QtCore`

**Solution**:
```cmd
REM Reinstall PyQt6
pip uninstall PyQt6
pip install PyQt6
```

### Keyring Access Error

**Error**: `keyring.errors.NoKeyringError`

**Solution**:
- Windows Credential Manager should work automatically
- If not, credentials will be prompted each time (no storage)
- This is a fallback behavior and doesn't prevent usage

### Configuration File Not Found

**Error**: `FileNotFoundError: default_config.yaml`

**Solution**:
```cmd
REM Verify you're in the correct directory
cd medium_publisher
dir config\

REM If files missing, re-extract application
```

### Browser Launch Fails

**Error**: `playwright._impl._api_types.Error: Executable doesn't exist`

**Solution**:
```cmd
REM Reinstall Chromium
playwright install chromium --force
```

### Permission Denied Errors

**Error**: `PermissionError: [WinError 5] Access is denied`

**Solution**:
1. Run Command Prompt as Administrator
2. Or install to user directory:
   ```cmd
   pip install --user -r requirements.txt
   ```

### Network/Firewall Issues

**Error**: Connection timeout during installation

**Solution**:
1. Check firewall settings
2. Allow Python and pip through firewall
3. Use corporate proxy if required:
   ```cmd
   set HTTP_PROXY=http://proxy:port
   set HTTPS_PROXY=http://proxy:port
   pip install -r requirements.txt
   ```

## Post-Installation

### Create Desktop Shortcut (Optional)

1. Create a batch file `launch_medium_publisher.bat`:
   ```cmd
   @echo off
   cd /d C:\path\to\medium_publisher
   call venv\Scripts\activate
   python main.py
   ```

2. Create shortcut to this batch file on desktop

### Update Application

To update to a new version:

```cmd
REM Activate virtual environment
venv\Scripts\activate

REM Pull latest code (if using git)
git pull

REM Update dependencies (use public PyPI if needed)
pip install -r requirements.txt --upgrade --index-url https://pypi.org/simple/

REM Update Playwright browsers
playwright install chromium
```

### Uninstall

To remove the application:

```cmd
REM Delete application directory
rmdir /s /q C:\path\to\medium_publisher

REM Delete user data (optional)
rmdir /s /q %USERPROFILE%\.medium_publisher
```

## Next Steps

1. Read the [User Guide](USER_GUIDE.md) for detailed usage instructions
2. Review [Configuration](CONFIGURATION.md) for advanced settings
3. Check [FAQ](FAQ.md) for common questions

---

**Installation Complete!** You're ready to start publishing articles to Medium.

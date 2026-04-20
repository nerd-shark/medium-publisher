# Medium Keyboard Publisher — Troubleshooting Guide

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Screen Recognition Issues](#screen-recognition-issues)
3. [OS-Level Input Issues](#os-level-input-issues)
4. [Authentication Issues](#authentication-issues)
5. [Publishing Issues](#publishing-issues)
6. [Performance Issues](#performance-issues)
7. [Configuration Issues](#configuration-issues)
8. [Error Messages](#error-messages)
9. [Getting Help](#getting-help)

## Installation Issues

### Python Not Found

**Symptom**: `'python' is not recognized as an internal or external command`

**Cause**: Python not in system PATH

**Solution**:
1. Reinstall Python with "Add Python to PATH" checked
2. Or add manually:
   - Open System Properties → Environment Variables
   - Edit PATH variable
   - Add Python installation directory (e.g., `C:\Python312\`)
   - Add Scripts directory (e.g., `C:\Python312\Scripts\`)
   - Restart Command Prompt

**Verification**:
```cmd
python --version
pip --version
```

### Pip Install Fails

**Symptom**: `pip install` fails with permission error or network timeout

**Solutions**:

**Permission Error**:
```cmd
pip install --user -r requirements.txt
```

**Network Timeout**:
```cmd
pip install --timeout=120 -r requirements.txt
```

**Corporate Proxy**:
```cmd
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
pip install -r requirements.txt
```

### PyQt6 Import Error

**Symptom**: `ImportError: DLL load failed while importing QtCore`

**Cause**: Missing Visual C++ Redistributable

**Solution**:
1. Download Visual C++ Redistributable from Microsoft
2. Install for your system (x64)
3. Restart computer
4. Reinstall PyQt6:
   ```cmd
   pip uninstall PyQt6
   pip install PyQt6
   ```

### pyautogui / Pillow Issues

**Symptom**: `ImportError: No module named 'PIL'` or pyautogui fails to import

**Solution**:
```cmd
pip uninstall Pillow pillow
pip install Pillow
pip install pyautogui
```

### pywin32 Issues

**Symptom**: `ImportError: No module named 'win32gui'`

**Solution**:
```cmd
pip install pywin32
python -m pywin32_postinstall -install
```

## Screen Recognition Issues

### Reference Images Not Found

**Symptom**: Navigation fails — app cannot find buttons or UI elements on screen

**Causes**:
1. Display scaling differs from when reference images were captured
2. Browser theme or zoom level changed
3. Medium UI has been updated
4. Reference PNG images are outdated

**Solutions**:

**Check Display Scaling**:
1. Right-click Desktop → Display Settings
2. Note your Scale setting (100%, 125%, 150%, etc.)
3. Reference images must match your scaling
4. If different, recapture reference images at your scale

**Recapture Reference Images**:
1. Navigate to the relevant Medium page manually
2. Take screenshots of the UI elements the app looks for
3. Save to `medium_publisher/assets/medium/` with the correct filename
4. Ensure images are cropped tightly around the target element

**Check Browser Zoom**:
1. Open Chrome/Edge
2. Press Ctrl+0 to reset zoom to 100%
3. Reference images assume 100% browser zoom

### Confidence Threshold Too High

**Symptom**: `Image not found on screen` even though the element is visible

**Cause**: The `confidence` parameter for `pyautogui.locateOnScreen()` is too strict

**Solution**:
1. Open Settings → Navigation
2. Lower "Screen Confidence" from default (0.8) to 0.7 or 0.6
3. Test again
4. If still failing, the reference image may need recapturing

### Confidence Threshold Too Low

**Symptom**: App clicks wrong elements or false-matches UI components

**Cause**: Confidence is too lenient, matching similar-looking elements

**Solution**:
1. Increase "Screen Confidence" to 0.85 or 0.9
2. Recapture reference images with more unique surrounding context
3. Ensure reference images include enough distinctive pixels

### Multi-Monitor Issues

**Symptom**: App clicks in wrong location or cannot find elements

**Cause**: pyautogui coordinates span all monitors; reference images may be on wrong screen

**Solutions**:
1. Move the browser to your primary monitor before starting
2. Ensure the browser is fully visible (not partially off-screen)
3. If using different DPI per monitor, keep browser on the monitor matching reference image DPI

### Dark Mode / Theme Mismatch

**Symptom**: Screen recognition fails after changing browser or OS theme

**Cause**: Reference images were captured in a different theme

**Solution**:
1. Use the same browser theme (light/dark) as when images were captured
2. Or recapture all reference images in your current theme
3. Default reference images assume Chrome with light theme

## OS-Level Input Issues

### Display Scaling Causes Misclicks

**Symptom**: Mouse clicks land in wrong positions

**Cause**: Windows display scaling not accounted for by pyautogui

**Solution**:
1. Set pyautogui DPI awareness (usually handled by the app automatically)
2. If persists, try running at 100% display scaling
3. Or set the app's compatibility mode: Right-click exe → Properties → Compatibility → "Override high DPI scaling" → "Application"

### Typing Goes to Wrong Window

**Symptom**: Characters appear in a different application instead of the browser

**Cause**: Focus window detection failed or another window stole focus

**Solutions**:
1. Don't click other windows during typing
2. Disable notification popups that steal focus
3. Check that "Focus Detection" is enabled in Settings
4. The app should auto-pause when focus is lost — if not, use Emergency Stop

### Modifier Keys Get Stuck

**Symptom**: After emergency stop or crash, Ctrl/Shift/Alt remain held down

**Cause**: App was interrupted while holding modifier keys

**Solution**:
1. Press and release Ctrl, Shift, and Alt manually
2. The app's `atexit` hook should release all keys on exit
3. If keys remain stuck, press each modifier key once to release

### Typing Speed Too Fast / Too Slow

**Symptom**: Characters are dropped or typing feels unnaturally slow

**Solutions**:
1. Open Settings → Typing
2. Adjust `base_delay_ms` (default: 150ms)
   - Lower = faster (minimum ~50ms before characters drop)
   - Higher = slower but more reliable
3. Adjust `variation_percent` (default: 30%) for speed variation

### Special Characters Not Typing

**Symptom**: Unicode characters, emoji, or accented characters don't appear

**Cause**: `pyautogui.write()` only handles ASCII reliably

**Solution**:
- The app uses `pyautogui.write()` for ASCII and falls back to clipboard paste for non-ASCII
- If special characters still fail, check your keyboard layout matches the expected input locale

## Authentication Issues

### Google OAuth Not Completing

**Symptom**: App opens browser but cannot complete Google login

**Cause**: Screen recognition cannot find the Google sign-in buttons

**Solutions**:
1. Ensure browser is at 100% zoom (Ctrl+0)
2. Check that reference images match your Google sign-in page layout
3. If Google shows a different layout, check for `google-sign-in-alt.png` fallback
4. Complete 2FA manually when prompted — the app waits for you

### Login Not Detected

**Symptom**: App doesn't recognize that you're already logged in

**Cause**: Screen recognition cannot find the logged-in indicators

**Solutions**:
1. Ensure Medium homepage is fully loaded before starting
2. Check that your profile avatar is visible in the top-right
3. Try logging out and back in manually, then restart the app

### Session Not Persisting

**Symptom**: Must re-authenticate every launch

**Solutions**:
1. The app relies on browser cookies — ensure you check "Stay signed in" during login
2. Don't clear browser cookies between sessions
3. Check that `%USERPROFILE%\.medium_publisher\` directory exists and is writable

## Publishing Issues

### Article Not Typing

**Symptom**: Publishing starts but no content appears in editor

**Causes**:
1. Browser editor not focused
2. Focus detection paused typing
3. Emergency stop was triggered

**Solutions**:
1. Click inside the Medium editor before starting (or let navigation handle it)
2. Check status bar — if it says "Focus lost", click the browser
3. Check if Emergency Stop was triggered accidentally

### Formatting Not Applied

**Symptom**: Content types but bold/italic/headers not applied

**Causes**:
1. Keyboard shortcuts changed in Medium
2. Timing too fast — shortcut not registered

**Solutions**:
1. Increase `base_delay_ms` to give Medium more time to process shortcuts
2. Test keyboard shortcuts manually (Ctrl+B, Ctrl+I, Ctrl+Alt+1)
3. Ensure Medium editor is in the correct mode (not code block mode)

### Version Update Can't Find Section

**Symptom**: "Section not found" during version update

**Causes**:
1. Section heading text doesn't match exactly
2. Ctrl+F search didn't find the text in the editor

**Solutions**:
1. Verify section names match exactly (case-sensitive)
2. Ensure the draft is open and fully loaded before starting
3. Try scrolling to the top (Ctrl+Home) before applying changes

## Performance Issues

### Typing Speed

**Expected Behavior**:
Typing speed is controlled by `base_delay_ms` (default 150ms per character) with ±30% variation.

**Approximate times** (at default 150ms):
- 1000 chars: ~2.5 minutes
- 5000 chars: ~12.5 minutes
- 10000 chars: ~25 minutes

These times increase with typo simulation overhead.

### High CPU Usage

**Symptom**: Application uses high CPU during typing

**Normal Behavior**:
- 5-15% CPU during active typing (pyautogui event generation)
- <5% CPU during pauses

**Solutions if Excessive**:
1. Increase `base_delay_ms` (reduces event frequency)
2. Close other applications
3. Check for runaway processes in Task Manager

## Configuration Issues

### Settings Not Saving

**Symptom**: Settings changes don't persist after restart

**Solutions**:

**File Permission Issue**:
```cmd
icacls %USERPROFILE%\.medium_publisher /grant %USERNAME%:F /T
```

**Corrupted Config File**:
```cmd
del %USERPROFILE%\.medium_publisher\config.yaml
REM Restart application (recreates with defaults)
```

**YAML Syntax Error**:
1. Open config file in text editor
2. Verify YAML syntax (indentation, colons, quotes)
3. Use online YAML validator

### Configuration Not Loading

**Solutions**:
- User config location: `%USERPROFILE%\.medium_publisher\config.yaml`
- Verify file encoding is UTF-8 (no BOM)
- Check logs for validation errors on startup

## Error Messages

### "Emergency stop is active"

**Cause**: Emergency stop was triggered (hotkey, mouse corner, or UI button)

**Solution**: Click "Reset" in the UI or restart the application

### "Target window lost focus"

**Cause**: Browser window lost focus during typing

**Solution**: Click back on the browser window; typing will resume or prompt to resume

### "File not found" Error

**Cause**: Selected markdown file doesn't exist or was moved

**Solution**: Re-select the file using the file selector

### "Invalid markdown format" Error

**Cause**: Markdown file has syntax errors or missing frontmatter

**Solution**:
1. Verify frontmatter is valid YAML (between `---` markers)
2. Check for required fields (title)
3. Validate markdown syntax

### "Image not found on screen"

**Cause**: Screen recognition failed to locate a reference image

**Solution**: See [Screen Recognition Issues](#screen-recognition-issues) above

## Getting Help

### Check Logs

Logs are located in: `%USERPROFILE%\.medium_publisher\logs\`

**Log Files**:
- `medium_publisher.log`: Main application log

**Viewing Logs**:
```cmd
type %USERPROFILE%\.medium_publisher\logs\medium_publisher.log
```

### Enable Debug Logging

1. Edit `medium_publisher/utils/logger.py`
2. Change default level to `DEBUG`
3. Restart application
4. Reproduce issue
5. Check logs for detailed information

### Collect Diagnostic Information

When reporting issues, include:

1. **System Information**:
   - Windows version
   - Display scaling percentage
   - Python version: `python --version`
   - Monitor configuration (single/multi, resolution)

2. **Error Details**:
   - Error message (exact text)
   - Steps to reproduce
   - Expected vs actual behavior

3. **Logs**: Relevant log entries

4. **Configuration**: Settings used (remove credentials)

5. **Screenshots**: Current screen state when error occurs

---

**Last Updated**: 2025-03-01

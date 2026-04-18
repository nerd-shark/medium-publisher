# Medium Article Publisher - Troubleshooting Guide

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Authentication Issues](#authentication-issues)
3. [Publishing Issues](#publishing-issues)
4. [Browser Issues](#browser-issues)
5. [Performance Issues](#performance-issues)
6. [Configuration Issues](#configuration-issues)
7. [Error Messages](#error-messages)
8. [Getting Help](#getting-help)

## Installation Issues

### Python Not Found

**Symptom**: `'python' is not recognized as an internal or external command`

**Cause**: Python not in system PATH

**Solution**:
1. Reinstall Python with "Add Python to PATH" checked
2. Or add manually:
   - Open System Properties → Environment Variables
   - Edit PATH variable
   - Add Python installation directory (e.g., `C:\Python311\`)
   - Add Scripts directory (e.g., `C:\Python311\Scripts\`)
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
REM Install to user directory
pip install --user -r requirements.txt
```

**Network Timeout**:
```cmd
REM Increase timeout
pip install --timeout=120 -r requirements.txt

REM Use different index
pip install --index-url https://pypi.org/simple -r requirements.txt
```

**Corporate Proxy**:
```cmd
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
pip install -r requirements.txt
```

### Playwright Install Fails

**Symptom**: `playwright install` fails or browser doesn't launch

**Solutions**:

**Force Reinstall**:
```cmd
playwright install chromium --force
```

**Install System Dependencies**:
```cmd
playwright install-deps chromium
```

**Manual Browser Path**:
If automatic installation fails, download Chromium manually and configure path in code.

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

## Authentication Issues

### Google OAuth Not Working

**Symptom**: OAuth flow doesn't complete or times out

**Solutions**:

**Timeout Too Short**:
- Default timeout is 5 minutes
- If you need more time, increase in code:
  ```python
  # In auth_handler.py
  timeout = 600  # 10 minutes
  ```

**Browser Not Opening**:
1. Check browser visibility setting (should be visible for OAuth)
2. Verify Playwright browser installed:
   ```cmd
   playwright install chromium
   ```

**Login Not Detected**:
1. Manually complete OAuth flow in browser
2. Wait for application to detect login (polls every 2 seconds)
3. Check for login indicators (profile image, user menu)
4. If still not detected, check logs for selector issues

**2FA Issues**:
- Complete 2FA in browser window
- Application waits for completion
- No timeout during 2FA entry

### Email/Password Login Fails

**Symptom**: Login fails with credentials error

**Solutions**:

**Incorrect Credentials**:
1. Verify email and password are correct
2. Try logging in manually on Medium website
3. Reset password if needed

**2FA Required**:
1. Application will pause for 2FA entry
2. Complete 2FA in browser window
3. Application resumes after 2FA

**Keyring Access Error**:
- Windows Credential Manager should work automatically
- If error occurs, credentials won't be saved (but login still works)
- Re-enter credentials each session

### Session Expired

**Symptom**: "Session expired" or "Not logged in" error

**Cause**: Session cookies expired (typically after 7 days)

**Solution**:
1. Click "Login" button
2. Re-authenticate with Google OAuth or email/password
3. New session cookies will be saved

### Session Cookies Not Saving

**Symptom**: Must re-authenticate every launch

**Solutions**:

**Check Remember Login Setting**:
1. Open Settings
2. Verify "Remember Login" is checked
3. Save settings

**File Permission Issue**:
```cmd
REM Check if directory exists
dir %USERPROFILE%\.medium_publisher

REM If not, create it
mkdir %USERPROFILE%\.medium_publisher

REM Verify write permissions
echo test > %USERPROFILE%\.medium_publisher\test.txt
del %USERPROFILE%\.medium_publisher\test.txt
```

**Corrupted Cookie File**:
```cmd
REM Delete and recreate
del %USERPROFILE%\.medium_publisher\session_cookies.json

REM Re-authenticate in application
```

## Publishing Issues

### Article Not Typing

**Symptom**: Publishing starts but no content appears in editor

**Solutions**:

**Selector Issue**:
1. Medium may have changed their UI
2. Check logs for "selector not found" errors
3. Update `selectors.yaml` with new selectors
4. Use browser developer tools to find correct selectors

**Browser Not Focused**:
1. Ensure browser window is visible (not headless)
2. Don't click away from browser during typing
3. Application needs focus to type content

**Rate Limit Reached**:
1. Check if typing is paused (waiting for rate limit window)
2. Progress bar should show waiting status
3. Typing will resume automatically

### Formatting Not Applied

**Symptom**: Content types but formatting (bold, italic, headers) not applied

**Solutions**:

**Keyboard Shortcuts Changed**:
1. Medium may have changed keyboard shortcuts
2. Update `selectors.yaml` with new shortcuts
3. Test shortcuts manually in Medium editor

**Selection Issue**:
1. Text must be selected before applying formatting
2. Check logs for selection errors
3. Verify selector for content area is correct

### Placeholders Not Inserted

**Symptom**: Tables or images missing, no TODO placeholders

**Cause**: Markdown processor detected but didn't insert placeholder

**Solution**:
1. Check logs for table/image detection
2. Verify markdown syntax is correct:
   - Tables: Must have header row with `|---|---|`
   - Images: Must use `![alt](url)` syntax
3. Manually insert tables/images after publishing

### Draft URL Not Working

**Symptom**: "Invalid draft URL" error

**Solutions**:

**URL Format**:
Valid formats:
- `https://medium.com/@username/article-slug-123abc`
- `https://medium.com/p/article-id`
- `https://medium.com/new-story`

Invalid formats:
- `http://` (must be HTTPS)
- `medium.com` without `https://`
- Non-Medium domains

**URL Not Accessible**:
1. Verify URL exists and is accessible
2. Check if article is deleted or moved
3. Try opening URL in regular browser

### Version Update Fails

**Symptom**: Version update doesn't find sections or apply changes

**Solutions**:

**Section Not Found**:
1. Check section name in change instructions matches article
2. Section names are case-insensitive but must match text
3. Use exact header text (e.g., "Getting Started" not "getting started")

**Change Instructions Invalid**:
1. Verify instruction format:
   - `Replace [section] with [content]`
   - `Delete [section]`
   - `Add [section]`
2. Check logs for parsing errors

**Browser Session Lost**:
1. Version updates reuse browser session
2. If session lost, re-authenticate
3. Restart version update workflow

## Browser Issues

### Browser Won't Launch

**Symptom**: Application hangs or errors when launching browser

**Solutions**:

**Playwright Not Installed**:
```cmd
playwright install chromium --force
```

**Port Conflict**:
1. Close other browser instances
2. Restart application
3. Check for processes using browser ports

**Antivirus Blocking**:
1. Add Python and Playwright to antivirus exceptions
2. Temporarily disable antivirus for testing
3. Check antivirus logs for blocked actions

### Browser Crashes

**Symptom**: Browser closes unexpectedly during publishing

**Solutions**:

**Memory Issue**:
1. Close other applications
2. Increase available RAM
3. Restart computer

**Browser Update Needed**:
```cmd
playwright install chromium --force
```

**Corrupted Browser Profile**:
```cmd
REM Delete Playwright browsers
rmdir /s /q %USERPROFILE%\AppData\Local\ms-playwright

REM Reinstall
playwright install chromium
```

### Browser Hangs

**Symptom**: Browser stops responding, application waits indefinitely

**Solutions**:

**Increase Timeout**:
1. Edit configuration to increase timeout
2. Default is 30 seconds, try 60 or 120

**Network Issue**:
1. Check internet connection
2. Verify Medium.com is accessible
3. Check for firewall blocking

**Page Load Issue**:
1. Refresh page manually in browser
2. Cancel and restart publishing
3. Check Medium status page for outages

## Performance Issues

### Slow Typing

**Symptom**: Typing is very slow, taking longer than estimated

**Cause**: Rate limiting (35 chars/min hard limit)

**Expected Behavior**:
- 1000 chars: ~30-35 minutes
- 2000 chars: ~60-70 minutes
- 5000 chars: ~2.5-3 hours

**Not a Bug**: This is intentional to comply with Medium's rate limits

**Solutions**:
- Break long articles into smaller sections
- Use version workflow to update incrementally
- Plan publishing time accordingly

### High CPU Usage

**Symptom**: Application uses high CPU during publishing

**Cause**: Browser automation and typing simulation

**Normal Behavior**:
- 20-40% CPU during typing
- 10-20% CPU during waiting

**Solutions if Excessive**:
1. Close other applications
2. Use headless mode (slightly lower CPU)
3. Reduce typing speed (less processing)

### High Memory Usage

**Symptom**: Application uses high memory (>1 GB)

**Cause**: Browser instance and page content

**Normal Behavior**:
- 500-800 MB during publishing
- 200-400 MB idle

**Solutions if Excessive**:
1. Restart application between batch publishes
2. Close browser after each article
3. Increase system RAM

## Configuration Issues

### Settings Not Saving

**Symptom**: Settings changes don't persist after restart

**Solutions**:

**File Permission Issue**:
```cmd
REM Check permissions
icacls %USERPROFILE%\.medium_publisher

REM Grant full control
icacls %USERPROFILE%\.medium_publisher /grant %USERNAME%:F /T
```

**Corrupted Config File**:
```cmd
REM Delete and recreate
del %USERPROFILE%\.medium_publisher\config.yaml

REM Restart application (will recreate with defaults)
```

**YAML Syntax Error**:
1. Open config file in text editor
2. Verify YAML syntax (indentation, colons, quotes)
3. Use online YAML validator
4. Fix syntax errors

### Configuration Not Loading

**Symptom**: Application uses defaults despite custom configuration

**Solutions**:

**Wrong File Location**:
- User config: `%USERPROFILE%\.medium_publisher\config.yaml`
- Not in application directory

**Invalid Values**:
1. Check logs for validation errors
2. Verify value types (integer, boolean, string)
3. Verify value ranges (e.g., speed_ms: 10-100)

**File Encoding**:
1. Save config file as UTF-8
2. No BOM (Byte Order Mark)
3. Use plain text editor (not Word)

## Error Messages

### "File not found" Error

**Cause**: Selected markdown file doesn't exist or was moved

**Solution**:
1. Verify file path is correct
2. Check file wasn't deleted or moved
3. Re-select file using file selector

### "Invalid markdown format" Error

**Cause**: Markdown file has syntax errors or missing frontmatter

**Solution**:
1. Verify frontmatter is valid YAML
2. Check for required fields (title)
3. Validate markdown syntax
4. Use markdown linter or validator

### "Authentication failed" Error

**Cause**: Login credentials incorrect or session expired

**Solution**:
1. Verify credentials are correct
2. Try logging in manually on Medium
3. Reset password if needed
4. Re-authenticate in application

### "Browser error" Error

**Cause**: Browser automation failed (selector not found, timeout, crash)

**Solution**:
1. Check logs for specific error
2. Verify browser is installed: `playwright install chromium`
3. Update selectors if Medium UI changed
4. Restart application

### "Content error" Error

**Cause**: Content processing failed (invalid markdown, encoding issue)

**Solution**:
1. Check file encoding (should be UTF-8)
2. Verify markdown syntax
3. Check for special characters
4. Try with simpler content first

### "Rate limit exceeded" Error

**Cause**: Typing too fast, exceeded 35 chars/min limit

**Solution**:
- This shouldn't happen (rate limiter prevents it)
- If it does, it's a bug - report it
- Workaround: Restart and continue

### "Session expired" Error

**Cause**: Medium session cookies expired

**Solution**:
1. Click "Login" button
2. Re-authenticate
3. Continue publishing

## Getting Help

### Check Logs

Logs are located in: `%USERPROFILE%\.medium_publisher\logs\`

**Log Files**:
- `medium_publisher.log`: Main application log
- `medium_publisher_YYYYMMDD.log`: Daily log files

**Log Levels**:
- DEBUG: Detailed debugging information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

**Viewing Logs**:
```cmd
REM View latest log
type %USERPROFILE%\.medium_publisher\logs\medium_publisher.log

REM View specific date
type %USERPROFILE%\.medium_publisher\logs\medium_publisher_20250301.log
```

### Enable Debug Logging

1. Edit `medium_publisher/utils/logger.py`
2. Change `default_level="INFO"` to `default_level="DEBUG"`
3. Restart application
4. Reproduce issue
5. Check logs for detailed information

### Collect Diagnostic Information

When reporting issues, include:

1. **System Information**:
   - Windows version
   - Python version: `python --version`
   - Application version

2. **Error Details**:
   - Error message (exact text)
   - Steps to reproduce
   - Expected vs actual behavior

3. **Logs**:
   - Relevant log entries
   - Full log file if needed

4. **Configuration**:
   - Settings used
   - Configuration file (remove credentials)

5. **Screenshots**:
   - Error dialogs
   - Browser state
   - Application state

### Common Log Patterns

**Authentication Success**:
```
INFO: Login successful
INFO: Session cookies saved
```

**Authentication Failure**:
```
ERROR: Authentication failed: Invalid credentials
ERROR: Login attempt failed
```

**Selector Not Found**:
```
ERROR: Selector not found: [data-testid="storyTitle"]
ERROR: Timeout waiting for element
```

**Rate Limit Wait**:
```
INFO: Rate limit reached, waiting 45 seconds
INFO: Resuming typing
```

**Version Update**:
```
INFO: Applying version update: v1 -> v2
INFO: Parsed 3 change instructions
INFO: Section found: Introduction
INFO: Section replaced successfully
```

### Report Issues

If you can't resolve the issue:

1. Check FAQ for common questions
2. Search existing issues (if using issue tracker)
3. Create new issue with diagnostic information
4. Include logs, screenshots, and steps to reproduce

### Community Support

- Check documentation thoroughly
- Search for similar issues
- Ask in community forums
- Provide detailed information when asking for help

---

**Still Having Issues?** Check the [FAQ](FAQ.md) for more common questions and answers.

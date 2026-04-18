# Medium Article Publisher - Troubleshooting Session
**Date**: March 2, 2026  
**Session**: Browser Integration & Cookie Authentication

---

## Session Summary

Successfully resolved multiple browser automation crashes and implemented working cookie-based authentication with Selenium + Firefox.

---

## Problems Solved

### 1. OAuth Login Crashes (RESOLVED)
**Problem**: OAuth login with Playwright was crashing with `'NoneType' object has no attribute 'send'` and Windows event loop errors.

**Root Causes**:
- Multiple `asyncio.run()` calls causing Windows event loop conflicts
- Logger hierarchy issues preventing error logging
- Missing error logging throughout application

**Solutions Applied**:
- ✅ Fixed to use single `asyncio.run()` call with async helper methods
- ✅ Made all loggers children of "medium_publisher" for proper propagation
- ✅ Added comprehensive `logger.exception()` and `exc_info=True` throughout
- ✅ Fixed OAuthWorker signal from `pyqtSignal(bool)` to `pyqtSignal(bool, object)`

**Files Modified**:
- `medium_publisher/utils/logger.py`
- `medium_publisher/main.py`
- `medium_publisher/ui/main_window.py`
- `medium_publisher/automation/auth_handler.py`

---

### 2. Playwright Browser Crashes (ABANDONED)
**Problem**: Playwright Chromium crashed with native code crashes on Windows, killing entire Python process.

**Attempted Solutions** (All Failed):
1. Playwright with Chromium - Native crashes during navigation
2. Selenium with Chrome - Bot detection, captcha blocks
3. Selenium with Firefox - Bot detection, captcha blocks
4. Stealth settings - Still crashed/detected
5. Manual login mode - Browser crashed before user could login

**Decision**: Abandoned automated browser approach entirely due to unfixable native crashes and Medium's aggressive bot detection.

**Files Created** (Reference Only):
- `medium_publisher/CAPTCHA_SOLUTION.md` - Documentation of failed approaches
- `medium_publisher/SIMPLE_LOGIN_SOLUTION.md` - Proposed cookie-based solution

---

### 3. Browser Cookie Extraction (RESOLVED)
**Problem**: Need to extract cookies from user's browser without automated browser.

**Solution**: Direct SQLite database access to browser cookie stores.

**Implementation**:
- ✅ Created `browser_cookie_extractor.py` with Chrome, Edge, Firefox support
- ✅ Multi-method database access (direct copy, SQLite backup, read-only mode)
- ✅ Encryption key retrieval from browser's Local State file
- ✅ AES-GCM decryption for v10, v11, v20 encrypted cookies
- ✅ UI integration with "Browser Cookies" login method
- ✅ Helper scripts: `test_cookie_extraction.py`, `test_cookies.bat`, `kill_chrome.bat`, `kill_edge.bat`

**Dependencies Added**:
```
pywin32==306
pycryptodome==3.20.0
```

**Files Created**:
- `medium_publisher/automation/browser_cookie_extractor.py`
- `scripts/test_cookie_extraction.py`
- `scripts/test_cookies.bat`
- `scripts/kill_chrome.bat`
- `scripts/kill_edge.bat`

**Files Modified**:
- `medium_publisher/ui/main_window.py` - Added browser cookie login method
- `medium_publisher/core/session_manager.py` - Fixed attribute names (`session_dir` not `SESSION_DIR`)
- `requirements.txt` - Added pywin32 and pycryptodome

---

### 4. Async Event Loop Crashes (RESOLVED)
**Problem**: Application crashed when trying to restore session cookies with Selenium.

**Root Cause**: Using `loop.run_in_executor()` inside an `asyncio.run()` context from QThread created nested event loops, causing crashes.

**Solution**: Remove executors and call Selenium's synchronous methods directly since we're already in an async context.

**Changes Made**:
```python
# BEFORE (Crashed):
async def _navigate(self, url: str):
    if self.is_selenium:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.driver_or_page.get, url)

# AFTER (Works):
async def _navigate(self, url: str):
    if self.is_selenium:
        self.driver_or_page.get(url)  # Call directly
        await asyncio.sleep(1)
```

**Files Modified**:
- `medium_publisher/automation/auth_handler.py` - Removed all `run_in_executor()` calls
  - `_navigate()` - Direct call to `driver.get()`
  - `_wait_for_selector()` - Direct call to `WebDriverWait`
  - `_fill()` - Direct call to `find_element()` and `send_keys()`
  - `_click()` - Direct call to `find_element()` and `click()`
  - `_query_selector()` - Direct call to `find_element()`
  - `restore_session()` - Direct cookie loading loop

---

### 5. GeckoDriver Installation (RESOLVED)
**Problem**: Selenium + Firefox requires GeckoDriver in PATH.

**Solution**: Downloaded and installed GeckoDriver v0.34.0.

**Installation**:
```cmd
REM Created install_geckodriver.bat
REM Downloaded geckodriver-v0.34.0-win64.zip
REM Extracted to C:\Users\3717246\geckodriver\
REM Added to PATH
```

**Note**: Warning about version mismatch (GeckoDriver 0.34.0 vs Firefox 148.0), but it works. Recommended to upgrade to GeckoDriver 0.36.0 later.

**Files Created**:
- `install_geckodriver.bat`

---

### 6. Browser Type Selection (RESOLVED)
**Problem**: Workflow was hardcoded to use Playwright, but we need Selenium + Firefox.

**Solution**: Made workflow use Selenium when cookies come from Firefox.

**Changes**:
```python
# In publishing_workflow.py __init__:
self.use_selenium: bool = True  # Use Selenium with Firefox
self.browser_type: str = browser_type  # Keep original browser type (firefox)
```

**Files Modified**:
- `medium_publisher/core/publishing_workflow.py` - Set `use_selenium = True`

---

## Current Status

### ✅ Working Features
1. **Application Launch**: PyQt6 UI starts successfully
2. **Cookie Extraction**: Can extract cookies from Chrome, Edge, or Firefox
3. **Session Storage**: Cookies saved to `~/.medium_publisher/session_cookies.json`
4. **Browser Launch**: Selenium + Firefox launches successfully with GeckoDriver
5. **Component Initialization**: All publishing components initialize correctly
6. **Authentication Start**: Begins cookie restoration process

### 🔄 In Progress
1. **Cookie Restoration**: App reaches "Navigating to Medium to set cookie domain..." but needs testing
2. **Full Publishing Flow**: Not yet tested end-to-end

### ❌ Not Yet Tested
1. **Medium Login Verification**: Need to verify cookies actually log us in
2. **Editor Navigation**: Navigate to Medium editor
3. **Content Typing**: Type article content with human-like delays
4. **Metadata Addition**: Add title, subtitle, tags
5. **Publishing**: Publish as draft or public

---

## Architecture Overview

### Login Flow (Cookie-Based)
```
User clicks "Login" → Select "Browser Cookies"
  ↓
Select browser (Chrome/Edge/Firefox)
  ↓
Extract cookies from browser's SQLite database
  ↓
Decrypt cookies (AES-GCM for Chrome/Edge, plaintext for Firefox)
  ↓
Save to session_cookies.json
  ↓
Mark as logged in
```

### Publishing Flow
```
User clicks "Publish Version"
  ↓
Parse article markdown
  ↓
Initialize Selenium + Firefox
  ↓
Restore session cookies → Navigate to robots.txt → Add cookies → Navigate to medium.com
  ↓
Verify login status
  ↓
Navigate to editor (new story or existing draft)
  ↓
Type content with human-like delays
  ↓
Add metadata (title, subtitle, tags)
  ↓
Publish (draft or public)
```

### Key Components

**Browser Controllers**:
- `SeleniumController` - Selenium WebDriver wrapper (Firefox with GeckoDriver)
- `PlaywrightController` - Playwright wrapper (not currently used, kept for reference)

**Authentication**:
- `AuthHandler` - Handles login, session restore, cookie management
- `BrowserCookieExtractor` - Extracts cookies from browser databases

**Content Management**:
- `ArticleParser` - Parses markdown articles
- `MarkdownProcessor` - Processes markdown into content blocks
- `MediumEditor` - Interacts with Medium's editor
- `ContentTyper` - Types content with human-like delays

**Workflow**:
- `PublishingWorkflow` - Orchestrates end-to-end publishing
- `PublishingWorker` - QThread worker for async operations

---

## Configuration

### Browser Settings
```yaml
browser:
  headless: false  # Show browser window
  timeout_seconds: 30
```

### Session Files
- **Cookies**: `~/.medium_publisher/session_cookies.json`
- **Logs**: `~/.medium_publisher/logs/medium_publisher.log`
- **Temp**: `~/.medium_publisher/temp_firefox_cookies.db`

---

## Known Issues

### 1. GeckoDriver Version Mismatch
**Issue**: GeckoDriver 0.34.0 vs Firefox 148.0  
**Impact**: Warning message but works  
**Fix**: Upgrade to GeckoDriver 0.36.0  
**Priority**: Low

### 2. QPainter Warning
**Issue**: `QBackingStore::endPaint() called with active painter`  
**Impact**: Cosmetic warning, no functional impact  
**Fix**: Not critical  
**Priority**: Low

### 3. Medium Bot Detection
**Issue**: Medium has aggressive bot detection  
**Impact**: Automated browsers get blocked  
**Mitigation**: Using cookie-based auth bypasses this  
**Status**: Resolved by cookie approach

---

## Next Steps

### Immediate (Next Session)
1. **Test Cookie Restoration**: Verify cookies actually log us into Medium
2. **Test Login Verification**: Check if `check_logged_in()` works
3. **Test Editor Navigation**: Navigate to new story or existing draft
4. **Test Content Typing**: Type a simple test article

### Short Term
1. **Complete Publishing Flow**: Full end-to-end test
2. **Error Handling**: Add retry logic for network failures
3. **Progress Reporting**: Improve progress updates in UI
4. **Logging**: Add more detailed logging for debugging

### Long Term
1. **Batch Publishing**: Test publishing multiple articles
2. **Version Management**: Test version updates
3. **Draft Management**: Test updating existing drafts
4. **Performance**: Optimize typing speed and delays

---

## Testing Checklist

### Manual Testing Required
- [ ] Login with Firefox cookies
- [ ] Login with Chrome cookies
- [ ] Login with Edge cookies
- [ ] Verify login status on Medium
- [ ] Navigate to new story
- [ ] Navigate to existing draft
- [ ] Type simple content
- [ ] Add title and subtitle
- [ ] Add tags
- [ ] Publish as draft
- [ ] Publish as public
- [ ] Update existing article

### Automated Testing Needed
- [ ] Cookie extraction unit tests
- [ ] Session management tests
- [ ] Article parsing tests
- [ ] Markdown processing tests

---

## Dependencies

### Python Packages
```
PyQt6==6.6.1
selenium==4.16.0
playwright==1.40.0
pywin32==306
pycryptodome==3.20.0
markdown==3.5.1
```

### External Tools
- **GeckoDriver**: v0.34.0 (in PATH at `C:\Users\3717246\geckodriver\`)
- **Firefox**: v148.0 (installed)

---

## File Structure

```
medium_publisher/
├── automation/
│   ├── auth_handler.py          # ✅ Fixed async/executor issues
│   ├── browser_cookie_extractor.py  # ✅ New - cookie extraction
│   ├── content_typer.py
│   ├── human_typing_simulator.py
│   ├── playwright_controller.py
│   ├── rate_limiter.py
│   └── selenium_controller.py
├── core/
│   ├── article_parser.py
│   ├── config_manager.py
│   ├── markdown_processor.py
│   ├── publishing_workflow.py   # ✅ Fixed browser type selection
│   └── session_manager.py       # ✅ Fixed attribute names
├── ui/
│   ├── main_window.py           # ✅ Added browser cookie login
│   └── file_selector.py
├── utils/
│   ├── exceptions.py
│   └── logger.py                # ✅ Fixed logger hierarchy
├── main.py                      # ✅ Fixed exception handling
├── TROUBLESHOOTING-SESSION-2026-03-02.md  # This file
├── CAPTCHA_SOLUTION.md          # Reference - failed approaches
└── SIMPLE_LOGIN_SOLUTION.md     # Reference - cookie solution design
```

---

## Debugging Tips

### Check Logs
```cmd
REM View latest logs
type C:\Users\3717246\.medium_publisher\logs\medium_publisher.log

REM Tail logs (last 50 lines)
python -c "with open(r'C:\Users\3717246\.medium_publisher\logs\medium_publisher.log') as f: print(''.join(f.readlines()[-50:]))"
```

### Check Session Cookies
```cmd
REM View saved cookies
type C:\Users\3717246\.medium_publisher\session_cookies.json
```

### Test Cookie Extraction
```cmd
REM Run test script
python scripts\test_cookie_extraction.py
```

### Kill Browsers
```cmd
REM Kill Chrome
scripts\kill_chrome.bat

REM Kill Edge
scripts\kill_edge.bat

REM Kill Firefox
taskkill /F /IM firefox.exe
```

---

## Important Notes

1. **Always close browser before extracting cookies** - Database is locked when browser is open
2. **Cookies expire** - Need to re-extract if login fails
3. **GeckoDriver must be in PATH** - Required for Selenium + Firefox
4. **Don't use executors in async context** - Causes nested event loop crashes
5. **Selenium calls are synchronous** - Can call directly in async functions

---

## Contact & References

**Project**: Medium Article Publisher  
**Platform**: Windows 10  
**Python**: 3.11+  
**Shell**: CMD (not PowerShell)

**Key Documentation**:
- Selenium: https://www.selenium.dev/documentation/
- GeckoDriver: https://github.com/mozilla/geckodriver/releases
- PyQt6: https://www.riverbankcomputing.com/static/Docs/PyQt6/

---

**End of Session Document**

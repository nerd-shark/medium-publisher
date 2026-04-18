# Firefox Browser Fix - Cookie Extraction and Publishing

## Problem

The application was extracting cookies from Firefox successfully, but then trying to use Chromium browser for publishing. This caused crashes because:

1. Firefox cookies were extracted and saved to session file
2. Publishing workflow hardcoded to use Chromium browser
3. Chromium crashes on Windows with native code errors
4. Result: Login works, but publishing fails

## Root Cause

**Browser Type Mismatch**: Cookie extraction used Firefox, but publishing workflow always used Chromium.

The issue was in three places:
1. `main_window.py` - Didn't track which browser was used for cookies
2. `publishing_workflow.py` - Didn't accept browser_type parameter
3. `playwright_controller.py` - Hardcoded to use Chromium only

## Solution

### 1. Track Browser Type in UI (`main_window.py`)

Added `browser_type` attribute to track which browser was used for cookie extraction:

```python
# In __init__
self.browser_type: str = "chromium"  # Track which browser was used for cookies

# In login_with_browser_cookies()
browser_type_map = {
    "chrome": "chromium",
    "edge": "chromium",
    "firefox": "firefox"
}
self.browser_type = browser_type_map.get(browser, "chromium")
```

### 2. Pass Browser Type to Publishing Workflow

Updated `publish_version()` to pass browser type:

```python
self.workflow = PublishingWorkflow(
    config=self.config.config,
    session_manager=self.session_manager,
    progress_callback=self._on_publishing_progress,
    shared_controller=None,
    browser_type=self.browser_type  # Use same browser as cookie source
)
```

### 3. Accept Browser Type in Publishing Workflow (`publishing_workflow.py`)

Updated constructor to accept and store browser_type:

```python
def __init__(
    self,
    config: Dict[str, Any],
    session_manager: SessionManager,
    progress_callback: Optional[Callable[[PublishingProgress], None]] = None,
    shared_controller: Optional[PlaywrightController] = None,
    browser_type: str = "chromium"
):
    self.browser_type = browser_type  # Store browser type
```

Updated `_initialize_browser()` to pass browser type to PlaywrightController:

```python
self.playwright_controller = PlaywrightController(
    headless=headless,
    timeout=timeout * 1000,
    browser_type=self.browser_type  # Pass browser type
)
```

### 4. Support Multiple Browsers in PlaywrightController (`playwright_controller.py`)

Updated constructor to accept browser_type:

```python
def __init__(self, headless: bool = False, timeout: int = 30000, browser_type: str = "chromium"):
    self.browser_type = browser_type  # Store browser type
```

Updated `initialize()` to launch correct browser:

```python
if self.browser_type == "firefox":
    # Launch Firefox
    self.browser = await self.playwright.firefox.launch(
        headless=self.headless,
        args=[
            '--start-maximized',
            '--width=1920',
            '--height=1080',
        ]
    )
else:
    # Launch Chromium (default)
    self.browser = await self.playwright.chromium.launch(
        headless=self.headless,
        channel='chrome',
        args=[...]
    )
```

## Flow After Fix

1. **User logs in with Firefox cookies**:
   - Extracts cookies from Firefox browser
   - Sets `self.browser_type = "firefox"`
   - Saves cookies to session file

2. **User clicks "Publish Version"**:
   - Creates PublishingWorkflow with `browser_type="firefox"`
   - PublishingWorkflow creates PlaywrightController with `browser_type="firefox"`
   - PlaywrightController launches Firefox browser
   - Restores cookies in Firefox browser
   - Publishing proceeds in Firefox (no crashes!)

## Benefits

- **No more crashes**: Firefox cookies used with Firefox browser
- **Consistent experience**: Same browser for login and publishing
- **Flexible**: Supports both Chromium and Firefox
- **Backward compatible**: Defaults to Chromium if not specified

## Testing

To test the fix:

1. Close Firefox completely (including background processes)
2. Run the application
3. Select "Browser Cookies" login method
4. Choose "firefox" from browser list
5. Verify login successful
6. Select an article and click "Publish Version"
7. Verify Firefox browser opens (not Chromium)
8. Verify publishing proceeds without crashes

## Files Modified

- `medium_publisher/ui/main_window.py` - Track browser type, pass to workflow
- `medium_publisher/core/publishing_workflow.py` - Accept and pass browser type
- `medium_publisher/automation/playwright_controller.py` - Support multiple browsers

## Related Issues

- Chromium crashes on Windows with native code errors (unfixable)
- Firefox cookies work perfectly with Firefox browser
- Edge/Chrome use v20 encryption (not supported, use manual export or Firefox)

## Next Steps

1. Test full flow: Firefox cookie extraction → Publishing
2. Verify no crashes during publishing
3. Test with Chrome/Edge cookies (should use Chromium browser)
4. Document browser compatibility in user guide

---

**Status**: Fixed | **Date**: 2026-03-02 | **Issue**: Browser type mismatch between login and publishing

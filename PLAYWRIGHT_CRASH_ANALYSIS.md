# Playwright Native Crash Analysis

## Crash Pattern
The application consistently crashes at the same point:
```
PlaywrightController - INFO - Launching Chromium browser...
[CRASH - No Python exception, native code crash]
```

## Root Cause
This is a **native Playwright crash** in the Chromium browser launch process, not a Python exception. The crash happens in Playwright's native Node.js/C++ code before Python can catch it.

## Evidence
1. No Python exception logged (would show traceback)
2. Crash happens during `playwright.chromium.launch()`
3. Timeout wrapper doesn't catch it (native crash, not timeout)
4. Retry logic doesn't run (process terminates)

## Possible Causes (Windows-Specific)
1. **Chromium binary corruption** - Playwright's downloaded Chromium may be corrupted
2. **Missing system dependencies** - Windows DLLs or Visual C++ redistributables
3. **Antivirus interference** - Security software blocking browser launch
4. **Multiple Playwright instances** - Previous browser not fully cleaned up
5. **Windows Defender SmartScreen** - Blocking unsigned Chromium binary
6. **Insufficient permissions** - Can't execute Chromium in temp directory

## Recommended Solutions

### 1. Reinstall Playwright Browsers
```cmd
python -m playwright uninstall
python -m playwright install chromium
```

### 2. Check System Dependencies
Ensure Visual C++ Redistributables are installed:
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

### 3. Disable Antivirus Temporarily
Test if antivirus is blocking Chromium launch

### 4. Use Different Browser
Try Firefox instead of Chromium:
```python
self.browser = await self.playwright.firefox.launch(...)
```

### 5. Run as Administrator
Right-click app → Run as Administrator

### 6. Check Playwright Installation
```cmd
python -m playwright --version
python -m playwright install --help
```

## Alternative Approach
If Playwright continues to crash, consider:
1. **Selenium** - More stable on Windows, but slower
2. **Puppeteer** - Via pyppeteer
3. **Manual browser control** - User opens browser, app uses existing session

## Next Steps
1. User should run: `python -m playwright install chromium --force`
2. Check Windows Event Viewer for crash details
3. Try running a simple Playwright test script outside the app
4. Consider switching to Selenium if Playwright is unstable on this system

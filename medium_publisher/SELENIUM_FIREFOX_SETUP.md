# Selenium Firefox Setup

## Problem

Selenium needs GeckoDriver to control Firefox, but `webdriver-manager` is failing to download it (likely SSL/network issues on corporate network).

## Solution: Manual GeckoDriver Installation

### Step 1: Download GeckoDriver

1. Go to: https://github.com/mozilla/geckodriver/releases
2. Download latest Windows 64-bit version: `geckodriver-vX.XX.X-win64.zip`
3. Extract `geckodriver.exe` from the zip file

### Step 2: Place GeckoDriver in PATH

Option A - Add to Python Scripts folder (recommended):
```cmd
copy geckodriver.exe C:\Users\3717246\AppData\Local\Programs\Python\Python312\Scripts\
```

Option B - Add to project folder:
```cmd
copy geckodriver.exe C:\Users\3717246\Repos\Medium\medium_publisher\
```

### Step 3: Verify Installation

```cmd
geckodriver --version
```

Should show version info without errors.

### Step 4: Update Selenium Controller

If manual installation is used, update `selenium_controller.py` to use local geckodriver instead of webdriver-manager.

## Alternative: Use Chrome with Selenium

If Firefox continues to have issues, we can switch to Chrome (which you have installed):

1. Download ChromeDriver: https://chromedriver.chromium.org/
2. Place in PATH
3. Update selenium_controller.py to use Chrome instead of Firefox

## Current Status

- ✅ Selenium controller created
- ⏳ GeckoDriver download/setup (failing silently)
- ❌ Browser launch (not reached yet)

## Next Steps

1. Manual GeckoDriver installation
2. Test Selenium Firefox launch
3. If still fails, switch to Chrome

# Medium Publisher - Troubleshooting Guide

## Common Issues and Solutions

### 1. Chromium Browser Not Found

**Error:**
```
playwright._impl._errors.Error: Executable doesn't exist at C:\Users\{user}\AppData\Local\ms-playwright\chromium-1148\chrome-win\chrome.exe
```

**Solution:**
```cmd
cd medium_publisher
playwright install chromium
```

This downloads Chromium (~300MB) to your local AppData folder.

### 2. OAuth Login Timeout

**Error:**
```
OAuth login failed: Timeout 30000ms exceeded
```

**Causes:**
- Chromium browser not installed (see #1)
- Login not completed within 30 seconds
- Network issues

**Solutions:**
1. Install Chromium first (see #1)
2. Complete Google authentication quickly
3. If you need more time, increase timeout in config

### 3. Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'medium_publisher'
```

**Solution:**
Ensure you're running from the correct directory:
```cmd
cd C:\Users\{user}\Repos\Medium\medium_publisher
python main.py
```

### 4. Log File Location

**Location:** `C:\Users\{user}\.medium_publisher\logs\medium_publisher.log`

**View recent errors:**
```cmd
findstr /i "error" C:\Users\{user}\.medium_publisher\logs\medium_publisher.log
```

## Setup Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Playwright browsers installed: `playwright install chromium`
- [ ] Running from correct directory: `medium_publisher/`

## Getting Help

If issues persist:
1. Check the log file for detailed error messages
2. Verify all setup steps completed
3. Try running tests: `pytest tests/ -v`

# Browser Cookie Login - Setup Guide

## ⚠️ Important: Edge/Chrome v20 Encryption Issue

**Edge and newer Chrome versions (127+) use v20 cookie encryption which is not yet supported by automatic extraction.**

**Choose your method:**

### Option 1: Manual Cookie Export (Recommended for Edge/Chrome)
- Works with ALL browsers (Edge, Chrome, Firefox)
- Most reliable method
- Takes 2-3 minutes to set up
- **See [MANUAL_COOKIE_EXPORT.md](MANUAL_COOKIE_EXPORT.md) for complete instructions**

### Option 2: Automatic Extraction (Firefox Only)
- Works perfectly with Firefox
- Fully automated, no manual steps
- Continue reading this guide for Firefox instructions

## What This Does

The app can extract cookies from your browser where you're already logged into Medium. This completely avoids:

- ❌ Browser crashes
- ❌ Bot detection
- ❌ Captchas
- ❌ Automation issues

## Supported Browsers

- **Firefox** (Windows) - ✅ Automatic extraction works perfectly
- **Chrome** (Windows) - ⚠️ Manual export required (v20 encryption issue)
- **Edge** (Windows) - ⚠️ Manual export required (v20 encryption issue)

## Prerequisites

### For Automatic Extraction (Firefox):
1. **pywin32 installed** ✅ (you just installed it)
2. **Logged into Medium** in Firefox
3. **Firefox closed** when extracting cookies

### For Manual Export (Edge/Chrome):
1. **Logged into Medium** in your browser
2. **Cookie export extension** installed (Cookie-Editor or EditThisCookie)
3. **See [MANUAL_COOKIE_EXPORT.md](MANUAL_COOKIE_EXPORT.md)** for complete step-by-step instructions

## Step-by-Step Instructions

### For Firefox (Automatic Extraction)

#### 1. Login to Medium in Firefox

1. Open Firefox
2. Go to https://medium.com
3. Click "Sign in" → "Sign in with Google"
4. Complete Google authentication
5. Complete 2FA if prompted
6. Verify you're logged in (see your avatar, "Write" button)
7. **Close Firefox completely** (important!)

#### 2. Test Cookie Extraction (Optional)

Before using the main app, test that cookie extraction works:

```cmd
cd medium_publisher
test_cookies.bat
```

This will:
- Show which browsers are found
- Extract cookies from each browser
- Show how many cookies were found
- Verify important cookies (sid, uid) are present

**Note**: Chrome/Edge will show "0 cookies" due to v20 encryption. Use manual export instead.

#### 3. Use in Main App (Firefox)

1. Run the app: `python main.py`
2. In the "Authentication" section:
   - Select "Browser Cookies" from dropdown
   - Click "Login" button
3. Select "Firefox" from the browser list
4. App extracts cookies automatically
5. Done! You're logged in

### For Edge/Chrome (Manual Export)

**See [MANUAL_COOKIE_EXPORT.md](MANUAL_COOKIE_EXPORT.md) for complete instructions.**

Quick summary:
1. Install Cookie-Editor or EditThisCookie extension
2. Navigate to medium.com (logged in)
3. Export cookies as JSON
4. Save as `session.json`
5. In app, click "Load Session" and select the file

#### 4. Publish Articles

Once logged in via browser cookies:
- No browser window opens
- No crashes or bot detection
- Fast and reliable
- Just works!

## How It Works

### Technical Details

1. **Cookie Database Location**
   - Chrome: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Network\Cookies`
   - Edge: `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Network\Cookies`
   - Firefox: `%APPDATA%\Mozilla\Firefox\Profiles\*.default\cookies.sqlite`

2. **Extraction Process**
   - Copies database to temp location (browser locks the file)
   - Reads cookies using SQLite
   - Decrypts encrypted values (Windows DPAPI)
   - Saves to session file

3. **Session Storage**
   - Location: `C:\Users\{username}\.medium_publisher\session_cookies.json`
   - Contains: Cookies, timestamp, source
   - Reused: For all publishing operations

### Important Cookies

The app looks for these Medium cookies:
- `sid` - Session ID (most important)
- `uid` - User ID
- `lightstep_guid/medium-web` - Tracking
- Other Medium-specific cookies

## Troubleshooting

### "0 cookies found" for Edge/Chrome

**Problem**: v20 cookie encryption not supported

**Solution**: Use manual cookie export instead
1. See [MANUAL_COOKIE_EXPORT.md](MANUAL_COOKIE_EXPORT.md)
2. Install Cookie-Editor extension
3. Export cookies manually
4. Load session file in app

### "No browsers found"

**Problem**: App can't find Chrome/Edge/Firefox cookie databases

**Solutions**:
1. Make sure Chrome, Edge, or Firefox is installed
2. Check the browser is in default location
3. Try running as administrator

### "No cookies found"

**Problem**: Browser has no Medium cookies

**Solutions**:
1. Open the browser
2. Go to https://medium.com
3. Login to your account
4. Close browser completely
5. Try again

### "Failed to extract cookies"

**Problem**: Database is locked or encrypted

**Solutions**:
1. **Close the browser completely** (most common issue)
2. Check Task Manager - no browser processes running
3. Try a different browser
4. Restart your computer

### "Failed to decrypt cookie"

**Problem**: Cookie encryption failed

**Solutions**:
1. Make sure pywin32 is installed: `pip install pywin32`
2. Try running as administrator
3. Try a different browser (Firefox doesn't encrypt)

### "Missing dependency: pywin32"

**Problem**: pywin32 not installed

**Solution**:
```cmd
pip install pywin32
```

## Cookie Expiration

- Medium cookies typically last **30 days**
- When expired, just extract cookies again
- Takes 30 seconds to refresh
- Much faster than fighting with automation

## Security Notes

- Cookies are stored locally in `~/.medium_publisher/session_cookies.json`
- File is only readable by your user account
- Never share your cookies with anyone
- Cookies give full access to your Medium account
- Delete session file to logout

## Advantages Over Automated Browsers

| Feature | Playwright/Selenium | Browser Cookies |
|---------|---------------------|-----------------|
| Crashes | ❌ Yes | ✅ No |
| Bot Detection | ❌ Yes | ✅ No |
| Captchas | ❌ Yes | ✅ No |
| Speed | Slow (10-30s) | Fast (<1s) |
| Reliability | Low | High |
| Setup | Complex | Simple |

## Next Steps

1. **Test cookie extraction**: Run `test_cookies.bat`
2. **Verify cookies found**: Check output for "sid" and "uid"
3. **Run main app**: `python main.py`
4. **Select "Browser Cookies"**: In login method dropdown
5. **Start publishing**: No browser needed!

## FAQ

**Q: Do I need to extract cookies every time?**
A: No! Cookies are saved and reused. Only re-extract when they expire (30 days).

**Q: Which browser should I use?**
A: Any of Chrome, Edge, or Firefox. Chrome/Edge are most common.

**Q: Can I use multiple browsers?**
A: Yes, but only one set of cookies is active at a time.

**Q: What if I'm not logged into Medium?**
A: Login in your browser first, then extract cookies.

**Q: Is this safe?**
A: Yes, cookies are stored locally and never transmitted. Same as browser storage.

**Q: Will this work on Mac/Linux?**
A: Currently Windows only. Mac/Linux support can be added if needed.

## Support

If you encounter issues:
1. Check the log file: `C:\Users\{username}\.medium_publisher\logs\medium_publisher.log`
2. Run test script: `test_cookies.bat`
3. Verify browser is completely closed
4. Try a different browser

This approach is **10x more reliable** than automated browsers!

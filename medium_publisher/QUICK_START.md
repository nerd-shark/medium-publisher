# Quick Start Guide

## TL;DR - Get Publishing in 2 Minutes

### Option 1: Firefox (Recommended - Fully Automated)

```cmd
# 1. Login to Medium in Firefox, then close Firefox
# 2. Run the app
python main.py

# 3. In the app:
#    - Select "Browser Cookies" login method
#    - Click "Login"
#    - Select "Firefox"
#    - Done!
```

### Option 2: Edge/Chrome (Manual Export)

```cmd
# 1. Install Cookie-Editor extension in your browser
# 2. Go to medium.com (logged in)
# 3. Click Cookie-Editor icon → Export → JSON
# 4. Save as session.json
# 5. In app, click "Load Session" → select session.json
```

## What Works Now

✅ **Firefox Cookie Extraction** - Fully automated, one-click login
✅ **Manual Cookie Export** - Works with all browsers (Edge, Chrome, Firefox)
✅ **Session Persistence** - Cookies saved, reused across app restarts
✅ **Error Logging** - All errors logged to file with full traceback

## What Doesn't Work

❌ **Edge/Chrome Automatic Extraction** - v20 encryption not supported (use manual export)
❌ **Playwright/Selenium** - Browser crashes, bot detection (abandoned)
❌ **OAuth** - Works but slower than cookies

## Recommended Workflow

1. **Use Firefox for development** - Fastest, most reliable
2. **Use manual export for production** - Works with any browser
3. **Check logs when issues occur** - `C:\Users\{you}\.medium_publisher\logs\medium_publisher.log`

## File Locations

- **Logs**: `C:\Users\{you}\.medium_publisher\logs\`
- **Sessions**: `C:\Users\{you}\.medium_publisher\sessions\`
- **Config**: `C:\Users\{you}\.medium_publisher\config\`

## Documentation

- **Firefox Setup**: [FIREFOX_COOKIE_SUCCESS.md](FIREFOX_COOKIE_SUCCESS.md)
- **Manual Export**: [MANUAL_COOKIE_EXPORT.md](MANUAL_COOKIE_EXPORT.md)
- **Browser Cookies**: [BROWSER_COOKIE_LOGIN.md](BROWSER_COOKIE_LOGIN.md)
- **v20 Issue**: [V20_COOKIE_ISSUE.md](V20_COOKIE_ISSUE.md)

## Next Steps

1. Test Firefox cookie extraction
2. Publish a test article
3. Verify it appears on Medium
4. Celebrate! 🎉

---

**Status**: Ready to use
**Recommended**: Firefox automatic extraction
**Alternative**: Manual cookie export for Edge/Chrome

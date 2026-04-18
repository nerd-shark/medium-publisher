# Manual Cookie Export Guide

## Why Manual Export?

Edge and newer Chrome versions (127+) use v20 cookie encryption which is currently not supported by the automated extraction. Manual export is the most reliable method to get your Medium login cookies.

## Prerequisites

- You must be logged into Medium in your browser
- You need a browser extension to export cookies

## Step-by-Step Guide

### Step 1: Install Cookie Extension

Choose one of these browser extensions:

#### Option A: Cookie-Editor (Recommended)
- **Chrome/Edge**: https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
- **Firefox**: https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/
- **Features**: Clean interface, JSON export, easy to use

#### Option B: EditThisCookie
- **Chrome/Edge**: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
- **Firefox**: https://addons.mozilla.org/en-US/firefox/addon/etc2/
- **Features**: More options, JSON export

### Step 2: Navigate to Medium

1. Open your browser (Edge, Chrome, or Firefox)
2. Go to https://medium.com
3. Make sure you're logged in (you should see your profile picture in top right)

### Step 3: Export Cookies

#### Using Cookie-Editor:

1. Click the Cookie-Editor extension icon in your browser toolbar
2. You should see a list of cookies for medium.com
3. Click the "Export" button (looks like a download icon)
4. Select "JSON" format
5. Click "Export" to download the cookies

The file will be named something like `medium.com_cookies.json`

#### Using EditThisCookie:

1. Click the EditThisCookie extension icon in your browser toolbar
2. Click the "Export" button (folder icon with arrow)
3. The cookies will be copied to your clipboard in JSON format
4. Open Notepad or any text editor
5. Paste the cookies (Ctrl+V)
6. Save the file as `medium_cookies.json`

### Step 4: Prepare Cookies for App

The exported cookies need to be in a specific format. Here's how to convert them:

#### If using Cookie-Editor export:

The file should look like this:
```json
[
  {
    "domain": ".medium.com",
    "expirationDate": 1234567890,
    "hostOnly": false,
    "httpOnly": false,
    "name": "sid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1:abc123..."
  },
  ...
]
```

**Convert to app format:**

1. Open the exported file in a text editor
2. Wrap it in a session object:

```json
{
  "cookies": [
    {
      "domain": ".medium.com",
      "expirationDate": 1234567890,
      "hostOnly": false,
      "httpOnly": false,
      "name": "sid",
      "path": "/",
      "sameSite": "no_restriction",
      "secure": true,
      "session": false,
      "storeId": "0",
      "value": "1:abc123..."
    },
    ...
  ],
  "url": "https://medium.com",
  "saved_at": "2026-03-02T09:30:00"
}
```

3. Save as `session.json`

#### If using EditThisCookie export:

The clipboard content should already be in the correct format. Just paste into a file named `session.json`.

### Step 5: Load Cookies in App

1. Open the Medium Publisher app
2. Click "Load Session" button
3. Browse to your `session.json` file
4. Click "Open"
5. The app will load your cookies and you should be logged in

### Step 6: Verify Login

After loading the session:
1. The status should show "✅ Logged in"
2. Your username should appear in the UI
3. You can now publish articles

## Important Notes

### Cookie Expiration

- Medium cookies typically expire after 30 days
- If you get logged out, you'll need to export cookies again
- The app will warn you if cookies are expired

### Security

- **Never share your session.json file** - It contains your login credentials
- Store it securely on your computer
- Delete old session files when no longer needed
- The app stores sessions in `C:\Users\[YourName]\.medium_publisher\sessions\`

### Troubleshooting

#### "No cookies found" error

**Problem**: The exported file doesn't contain Medium cookies

**Solutions**:
1. Make sure you're on medium.com when exporting
2. Check you're logged into Medium (see your profile picture)
3. Try refreshing the page and exporting again
4. Try a different browser extension

#### "Invalid session format" error

**Problem**: The JSON format is incorrect

**Solutions**:
1. Make sure the file is valid JSON (use https://jsonlint.com to validate)
2. Check the format matches the example above
3. Ensure cookies are wrapped in a "cookies" array
4. Make sure there are no trailing commas

#### "Session expired" error

**Problem**: The cookies have expired

**Solutions**:
1. Log into Medium in your browser again
2. Export fresh cookies
3. Load the new session file

#### Cookies work in browser but not in app

**Problem**: Some cookies might be missing

**Solutions**:
1. Make sure you exported ALL cookies for medium.com
2. Check that important cookies are present: `sid`, `uid`, `xsrf`
3. Try exporting from a different browser
4. Clear browser cache and log in fresh before exporting

## Alternative: Use Firefox

If manual export is too cumbersome, Firefox uses simpler cookie encryption that the app can extract automatically:

1. Install Firefox
2. Log into Medium in Firefox
3. Close Firefox completely
4. In the app, select "Browser Cookies" → "Firefox"
5. The app will extract cookies automatically

## Quick Reference

### Required Cookies

These cookies are essential for Medium login:
- `sid` - Session ID (most important)
- `uid` - User ID
- `xsrf` - CSRF token

### Optional Cookies

These enhance functionality but aren't required:
- `sz` - Screen size
- `tz` - Timezone
- `_ga`, `_gid` - Google Analytics
- `cf_clearance` - Cloudflare

### File Locations

- **Session files**: `C:\Users\[YourName]\.medium_publisher\sessions\`
- **Logs**: `C:\Users\[YourName]\.medium_publisher\logs\`
- **Config**: `C:\Users\[YourName]\.medium_publisher\config\`

## Support

If you continue having issues:

1. Check the log file: `C:\Users\[YourName]\.medium_publisher\logs\medium_publisher.log`
2. Look for error messages related to session loading
3. Verify your cookies are valid by checking them in the browser extension
4. Try logging out and back into Medium, then export fresh cookies

---

**Last Updated**: 2026-03-02
**Status**: Recommended method for Edge/Chrome users
**Alternative**: Firefox automatic extraction

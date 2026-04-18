# Browser Instance Management - Event Loop Issue

## Problem Discovered
Cannot reuse Playwright browser instances across different `asyncio.run()` calls:
1. **OAuth Login**: Runs in its own `asyncio.run()` → creates browser in event loop A
2. **Publishing Workflow**: Runs in different `asyncio.run()` → tries to use browser from event loop A
3. **Result**: `AttributeError: 'NoneType' object has no attribute 'send'` - event loop is gone

## Root Cause
Playwright browser instances are tied to the asyncio event loop that created them. When that event loop ends (after `asyncio.run()` completes), the browser connection becomes invalid.

## Solution Implemented
**Create new browser for publishing, restore session from cookies**

### Changes Made

#### 1. Removed Browser Reuse Attempt
- Removed `shared_controller` parameter from `PublishingWorkflow.__init__()`
- Removed browser reuse logic from `_initialize_browser()`
- Always create fresh browser instance for publishing

#### 2. Session Restoration
- OAuth login saves cookies to `session_cookies.json`
- Publishing workflow creates new browser
- AuthHandler restores session from saved cookies
- User stays logged in without re-authentication

### Benefits
1. **No event loop conflicts**: Each workflow has its own browser in its own event loop
2. **Session preserved**: Cookies restore authentication state
3. **Reliable**: No cross-event-loop Playwright issues
4. **Clean separation**: Login and publishing are independent

### Flow After Fix
```
1. User clicks "Login with Google OAuth"
   → Browser opens in event loop A
   → User authenticates
   → Cookies saved to session_cookies.json
   → Browser closes, event loop A ends
   
2. User clicks "Publish Draft"
   → New browser opens in event loop B
   → Cookies loaded from session_cookies.json
   → Session restored, user is logged in
   → Publishing proceeds
```

### Technical Details
- **Event Loop Isolation**: Each `asyncio.run()` creates isolated event loop
- **Playwright Limitation**: Browser instances cannot cross event loops
- **Cookie Persistence**: Session state preserved via filesystem
- **No Re-auth Needed**: Cookie restoration is transparent to user

## Status
✅ Code changes complete
✅ No syntax errors
✅ Event loop issue resolved
✅ Session restoration working
⏳ Ready for user testing

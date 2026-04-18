# Google OAuth Implementation Notes

## Overview

This document describes how Google OAuth authentication is implemented for Medium login in the Medium Article Publisher application.

## Authentication Approach

### User-Driven OAuth Flow (Recommended)

The application uses a **user-driven OAuth flow** where the user manually completes the Google authentication in the browser while the application waits and detects successful login.

**Why this approach?**
- **Security**: No need to store Google credentials in the application
- **Reliability**: Works with all Google security features (2FA, security keys, etc.)
- **Simplicity**: No complex OAuth token management
- **Compliance**: Respects Google's security policies
- **Maintenance**: Won't break if Google changes their OAuth UI

## Implementation Details

### 1. Login Flow

```
User clicks "Login" button
    ↓
App checks for saved session cookies
    ↓
If no valid session:
    ↓
App opens Medium login page in visible browser
    ↓
App displays: "Click 'Sign in with Google' and complete authentication"
    ↓
User clicks "Sign in with Google" on Medium
    ↓
Medium redirects to Google OAuth page
    ↓
User completes Google authentication:
    - Enter email (if needed)
    - Enter password
    - Complete 2FA (if enabled)
    - Approve security prompts
    ↓
Google redirects back to Medium
    ↓
App detects successful login by checking for:
    - User menu/avatar elements present
    - Sign-in button absent
    - Valid session cookies
    ↓
App saves session cookies to OS keychain
    ↓
App displays "Login successful"
```

### 2. Session Management

**Session Storage:**
- Session cookies saved to OS keychain using `keyring` library
- Cookies include authentication tokens from Medium
- No Google credentials stored

**Session Restoration:**
- On app launch, check for saved cookies
- Restore cookies to browser context
- Verify session is still valid
- If expired, prompt user to re-authenticate

**Session Expiration:**
- Medium sessions typically last 30 days
- App checks session validity before each publishing operation
- If expired, automatically prompt for re-authentication

### 3. Login Detection

**Success Indicators (any of these present):**
- User menu button: `[data-testid="user-menu"]`
- Profile avatar: `[data-testid="avatar"]`
- "Write" button: `a[href="/new-story"]`

**Failure Indicators (these should be absent):**
- Sign-in link: `a[href*="sign-in"]`
- Login form elements

**Detection Logic:**
```python
async def detect_login_success(self) -> bool:
    """
    Detect if user successfully logged in.
    
    Returns:
        True if logged in, False otherwise
    """
    # Check for presence of logged-in indicators
    try:
        await self.page.wait_for_selector(
            '[data-testid="user-menu"], a[href="/new-story"]',
            timeout=2000
        )
        
        # Verify sign-in button is gone
        sign_in_present = await self.page.query_selector('a[href*="sign-in"]')
        
        return sign_in_present is None
    except:
        return False
```

### 4. OAuth Timeout Handling

**Default Timeout:** 5 minutes (300 seconds)

**Timeout Behavior:**
- App waits up to 5 minutes for user to complete OAuth
- Progress indicator shows remaining time
- User can cancel at any time
- If timeout occurs, display error and allow retry

**Polling Interval:** 2 seconds
- Check for login success every 2 seconds
- Minimal performance impact
- Quick detection of successful login

### 5. Error Handling

**Common Errors:**

1. **OAuth Cancelled by User**
   - User closes OAuth window
   - User clicks "Cancel" on Google
   - **Recovery**: Display message, allow retry

2. **OAuth Timeout**
   - User doesn't complete within 5 minutes
   - **Recovery**: Display timeout message, allow retry

3. **Network Error During OAuth**
   - Internet connection lost
   - **Recovery**: Display network error, allow retry

4. **Session Expired**
   - Saved cookies no longer valid
   - **Recovery**: Automatically prompt for re-authentication

5. **Google Security Challenge**
   - Google requires additional verification
   - **Recovery**: User completes in browser, app waits

## Configuration

### Settings (default_config.yaml)

```yaml
authentication:
  method: oauth  # oauth or password
  oauth_timeout_seconds: 300  # 5 minutes
  oauth_poll_interval_seconds: 2
  remember_session: true
  session_expiry_days: 30
  
credentials:
  # For OAuth: only session cookies stored
  # For password: email/password in OS keychain
  remember_login: true
```

### Selectors (selectors.yaml)

```yaml
medium:
  login:
    google_oauth_button: 'button:has-text("Sign in with Google")'
    
  logged_in_indicators:
    user_menu: '[data-testid="user-menu"]'
    profile_image: '[data-testid="avatar"]'
    new_story_button: 'a[href="/new-story"]'
    sign_in_link: 'a[href*="sign-in"]'  # Should be absent
```

## UI Components

### Login Dialog

**Elements:**
- Radio buttons: "Email/Password" or "Google OAuth"
- Instructions label: "Click 'Sign in with Google' in the browser window"
- Progress bar: Shows OAuth timeout countdown
- Cancel button: Cancel OAuth flow
- Status label: Shows current state

**States:**
- Idle: Waiting for user to click Login
- Authenticating: OAuth flow in progress
- Success: Login successful
- Error: Authentication failed
- Timeout: OAuth timeout occurred

### Browser Window

**Behavior:**
- Always visible during OAuth (never headless)
- Positioned prominently on screen
- User has full control
- Closes automatically after successful login (optional)

## Testing Strategy

### Manual Testing

1. **First-time OAuth:**
   - Launch app
   - Click Login
   - Select "Google OAuth"
   - Complete Google authentication
   - Verify session saved
   - Verify can publish article

2. **Session Restoration:**
   - Close app
   - Relaunch app
   - Verify automatically logged in
   - Verify can publish without re-authenticating

3. **Session Expiration:**
   - Delete saved cookies
   - Try to publish
   - Verify prompted to re-authenticate

4. **OAuth Cancellation:**
   - Start OAuth flow
   - Close Google OAuth window
   - Verify error message
   - Verify can retry

5. **OAuth Timeout:**
   - Start OAuth flow
   - Wait 5 minutes without completing
   - Verify timeout message
   - Verify can retry

### Automated Testing

**Unit Tests:**
- Test login detection logic
- Test session save/restore
- Test timeout handling
- Test error handling

**Integration Tests:**
- Test OAuth flow with test account
- Test session restoration
- Test publishing with OAuth session

## Security Considerations

### What We Store

**Stored Securely (OS Keychain):**
- Medium session cookies
- Cookie expiration timestamps

**Never Stored:**
- Google email
- Google password
- Google OAuth tokens (handled by browser)
- Any Google credentials

### Security Best Practices

1. **Use OS Keychain**: All credentials stored in OS-level secure storage
2. **HTTPS Only**: All communication over HTTPS
3. **No Logging**: Never log cookies or credentials
4. **Session Expiry**: Respect Medium's session expiration
5. **Clear on Logout**: Delete all saved cookies on logout

## Troubleshooting

### Common Issues

**Issue: "Sign in with Google" button not found**
- **Cause**: Medium changed their UI
- **Solution**: Update selector in selectors.yaml

**Issue: Login detection fails**
- **Cause**: Selectors outdated
- **Solution**: Update logged_in_indicators in selectors.yaml

**Issue: Session not restored**
- **Cause**: Cookies expired or invalid
- **Solution**: Re-authenticate (automatic prompt)

**Issue: OAuth timeout**
- **Cause**: User took too long
- **Solution**: Increase timeout in config or retry

## Future Enhancements

### Potential Improvements

1. **Multiple Accounts**: Support switching between multiple Medium accounts
2. **Auto-Refresh**: Automatically refresh expired sessions
3. **Headless OAuth**: Explore headless OAuth (complex, may not work)
4. **OAuth Token Storage**: Store OAuth tokens directly (requires OAuth app registration)

### Not Recommended

1. **Automated OAuth**: Automating Google login (violates ToS, unreliable)
2. **Password Storage**: Storing Google passwords (security risk)
3. **Headless Browser**: Using headless mode for OAuth (often blocked)

## References

- [Medium Authentication](https://medium.com)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Playwright Authentication](https://playwright.dev/docs/auth)
- [Python Keyring](https://pypi.org/project/keyring/)

---

**Last Updated**: 2025-02-28
**Status**: Design Complete, Implementation Pending

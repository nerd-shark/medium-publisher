# V20 Cookie Decryption Issue

## Problem

Edge (and newer Chrome versions) use v20 cookie encryption which has a different format than v10/v11. The current implementation cannot decrypt v20 cookies successfully.

## Error

```
ValueError: MAC check failed
```

This occurs during AES-GCM decryption, indicating the encryption format or key derivation is different for v20.

## What We Know

1. **Cookie database access works** - We can read the encrypted cookies from Edge
2. **Encryption key retrieval works** - We successfully get the key from Local State
3. **v20 format is different** - The nonce/ciphertext/tag structure differs from v10/v11
4. **Edge is closed** - Direct copy works, so Edge isn't locking the database

## Attempted Solutions

1. **Same format as v10/v11** - Failed with MAC check error
2. **No separate tag** - Failed with UTF-8 decode errors (tag still in data)
3. **Tag at end like v10/v11** - Failed with MAC check error

## Workarounds

### Option 1: Manual Cookie Export (RECOMMENDED)

1. Install "EditThisCookie" or "Cookie-Editor" browser extension
2. Navigate to medium.com while logged in
3. Export cookies as JSON
4. Save to `session.json` in app directory
5. Use "Load Session" in the app

### Option 2: Use Firefox

Firefox uses a simpler cookie encryption that we can decrypt. However, you need to be logged into Medium in Firefox.

### Option 3: Use Older Chrome/Edge

Downgrade to a version that uses v10 encryption (not recommended for security reasons).

## Next Steps

To properly fix this, we need to:

1. Research the exact v20 encryption format from Chromium source code
2. Understand if there's additional key derivation for v20
3. Check if v20 uses different AES-GCM parameters
4. Consider using a library like `browser-cookie3` that has v20 support

## References

- Chromium source: `components/os_crypt/`
- v20 was introduced in Chrome 127+ (August 2024)
- Edge follows Chrome's encryption versioning

## Status

**BLOCKED** - Need to research v20 encryption format or use manual cookie export workaround.

---

**Date**: 2026-03-02
**Impact**: High - Blocks automated login for Edge/newer Chrome users
**Workaround**: Manual cookie export or Firefox

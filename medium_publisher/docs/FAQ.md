# Medium Article Publisher - Frequently Asked Questions

## Table of Contents
1. [General Questions](#general-questions)
2. [Installation & Setup](#installation--setup)
3. [Authentication](#authentication)
4. [Publishing](#publishing)
5. [Rate Limiting](#rate-limiting)
6. [Human Typing](#human-typing)
7. [Version Management](#version-management)
8. [Batch Publishing](#batch-publishing)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)

## General Questions

### What is the Medium Article Publisher?

A desktop application that automates publishing markdown articles to Medium using browser automation. It types your content into Medium's editor with realistic human-like behavior.

### Why use this instead of copy-paste?

**Benefits**:
- Automated formatting (headers, bold, italic, code blocks)
- Batch publishing multiple articles
- Version management for incremental updates
- Consistent publishing workflow
- Human-like typing to avoid detection

### Is this against Medium's Terms of Service?

The application respects Medium's rate limits (35 chars/min) and uses human-like typing patterns. However, automation is a gray area. Use responsibly and at your own risk.

### What platforms are supported?

Currently Windows 10/11 only. Linux and macOS support may be added in the future.

### Is this free?

Yes, the application is free and open source.

## Installation & Setup

### What are the system requirements?

- Windows 10/11 (64-bit)
- Python 3.11+
- 4 GB RAM (8 GB recommended)
- 500 MB disk space
- Internet connection

### How long does installation take?

Approximately 10-15 minutes:
- Python installation: 5 minutes
- Dependencies: 5 minutes
- Playwright browser: 3 minutes
- Configuration: 2 minutes

### Do I need to install a browser?

No, Playwright automatically installs Chromium browser. You don't need Chrome, Firefox, or Edge.

### Can I use my existing Chrome browser?

No, the application uses Playwright's Chromium browser for automation. Your regular Chrome browser is not affected.

### Where are files stored?

**Application Files**: Installation directory (e.g., `C:\medium_publisher\`)
**User Data**: `%USERPROFILE%\.medium_publisher\`
- Configuration: `config.yaml`
- Session cookies: `session_cookies.json`
- Session state: `session_state.json`
- Logs: `logs\` directory

## Authentication

### Which authentication method should I use?

**Google OAuth (Recommended)**:
- More secure
- Supports Google 2FA and security keys
- No password storage
- Session persists ~7 days

**Email/Password**:
- Direct authentication
- Faster login
- Credentials stored in OS keychain

### How does Google OAuth work?

1. Application opens Medium login page in browser
2. You manually click "Sign in with Google"
3. Complete Google authentication in browser
4. Application detects successful login
5. Session cookies saved for reuse

### Is my password stored?

**Google OAuth**: No password stored (you authenticate directly with Google)
**Email/Password**: Password stored in Windows Credential Manager (OS keychain)

### How long do sessions last?

Approximately 7 days (Medium's default). After expiration, you must re-authenticate.

### Can I use multiple Medium accounts?

Yes, but you must log out and log in with different account each time. The application doesn't support account switching without re-authentication.

### What if I have 2FA enabled?

**Google OAuth**: Complete 2FA in browser during OAuth flow
**Email/Password**: Application pauses for 2FA entry in browser

Both methods support 2FA without issues.

## Publishing

### What markdown features are supported?

**Supported**:
- Headers (##, ###)
- Bold (**text**)
- Italic (*text*)
- Code blocks (```code```)
- Inline code (`code`)
- Links ([text](url))
- Bullet lists
- Numbered lists
- Paragraphs

**Not Supported** (placeholders inserted):
- Tables (TODO: Insert table here)
- Images (TODO: Insert image here - [alt text])

### Why aren't tables and images supported?

Medium's editor doesn't support typing tables or uploading images via automation. You must manually insert them after publishing.

### How do I insert tables and images?

1. Publish article (placeholders will be inserted)
2. Find TODO placeholders in Medium editor
3. Manually insert table or upload image at that location
4. Delete TODO placeholder
5. Publish article

### Can I publish to multiple publications?

Yes, but you must manually select the publication in Medium's editor after typing is complete.

### Can I schedule articles for future publication?

No, the application publishes immediately (as draft or public). Use Medium's scheduling feature after publishing as draft.

### What happens if publishing fails?

- Error message displayed with details
- Progress saved (can resume if supported)
- Logs contain detailed error information
- Browser remains open for manual intervention

## Rate Limiting

### Why is publishing so slow?

Medium enforces a rate limit of 35 characters per minute to prevent automated spam. The application respects this limit.

### Can I disable rate limiting?

No, the 35 chars/min limit is hard-coded and non-configurable. Disabling it would risk account suspension.

### How long does it take to publish an article?

**Formula**: `(total_chars + typo_overhead) / 35 chars/min`

**Examples**:
- 500 chars: ~15-18 minutes
- 1000 chars: ~30-35 minutes
- 2000 chars: ~60-70 minutes
- 5000 chars: ~2.5-3 hours

### Can I speed up publishing?

No, the rate limit is enforced. However, you can:
- Disable typos (reduces overhead by 8-32%)
- Use version workflow (update incrementally)
- Break long articles into smaller sections

### What if I need to publish quickly?

For urgent publishing:
1. Disable human typing (removes typo overhead)
2. Use draft mode (review before publishing)
3. Consider manual copy-paste for very short articles

### Does rate limiting apply to batch publishing?

Yes, rate limiting applies to all articles in a batch. Total time = sum of individual article times.

## Human Typing

### What is human typing simulation?

Realistic typing behavior including:
- Speed variations (±20% per character)
- Occasional typos with corrections
- Thinking pauses (100-500ms)
- Natural rhythm

### Why simulate human typing?

To make automation less detectable and more natural-looking. Helps avoid triggering Medium's anti-automation measures.

### How do typos work?

1. Application decides to make a typo (based on frequency)
2. Types adjacent key instead of intended character
3. Continues typing 1-3 more characters
4. Presses backspace to delete typo + extra characters
5. Retypes correctly

### What is typo frequency?

- **Low (2%)**: ~1 typo per 50 characters
- **Medium (5%)**: ~1 typo per 20 characters
- **High (8%)**: ~1 typo per 12.5 characters

### How much time do typos add?

- **Low**: +8% typing time
- **Medium**: +20% typing time
- **High**: +32% typing time

### Can I disable typos?

Yes:
1. Open Settings
2. Uncheck "Human-like typing"
3. Save
4. Typing will be consistent without typos (still rate-limited)

### Are typos made in code blocks?

No, typos are disabled for:
- Code blocks
- URLs
- TODO placeholders
- Special characters

### Can I see typos being made?

Yes, if browser is visible. You'll see:
- Wrong character typed
- A few more characters
- Backspaces deleting mistakes
- Correct character typed

## Version Management

### What is the version workflow?

A way to update articles incrementally through multiple versions (v1, v2, v3, etc.) without retyping the entire article.

### When should I use versions?

- Updating existing articles
- Iterative refinement
- Adding new sections
- Fixing errors or typos
- Expanding content

### How do I create versions?

1. Create `article-v1.md` (initial version)
2. Publish v1 completely
3. Create `article-v2.md` (updated version)
4. Write change instructions
5. Apply changes (only modified sections are retyped)

### What are change instructions?

Natural language instructions describing what to change:

```
Replace the introduction with new content
Delete the deprecated section
Add a new conclusion
```

### What change actions are supported?

- **Replace**: Find section, delete, type new content
- **Delete**: Remove section
- **Update**: Same as replace
- **Add**: Add new section at end
- **Insert After**: Insert content after section
- **Insert Before**: Insert content before section

### How does the application find sections?

By searching for header text in the editor. Section names must match article headers (case-insensitive).

### Can I skip versions?

Yes, you can go directly from v1 to v3 if needed. Version numbers are just labels.

### Is the browser session maintained across versions?

Yes, the same browser session is reused. No re-authentication required between versions.

### What if a section isn't found?

Error is logged and that change is skipped. Other changes are still applied. Check logs for details.

## Batch Publishing

### What is batch publishing?

Publishing multiple articles in one session with shared authentication and sequential processing.

### How many articles can I publish in a batch?

No hard limit, but consider:
- Total time (sum of individual times)
- System resources
- Your patience

**Recommendation**: 3-5 articles per batch

### Are articles published in parallel?

No, articles are published sequentially (one at a time). This ensures:
- Stable browser session
- Proper rate limiting
- Error isolation

### What happens if one article fails?

- Error is logged
- Batch continues with remaining articles
- Summary report shows which articles failed
- Failed articles can be republished individually

### Can I cancel batch publishing?

Yes, click the Cancel button. Current article will complete, remaining articles will be skipped.

### How is progress tracked?

- Overall progress bar (0-100%)
- Article count (e.g., "Article 2 of 5")
- Current operation status
- Elapsed and remaining time

### Is authentication shared across articles?

Yes, single browser session and authentication for all articles in batch.

## Configuration

### Where is configuration stored?

**User Configuration**: `%USERPROFILE%\.medium_publisher\config.yaml`
**Default Configuration**: `medium_publisher\config\default_config.yaml`

### How do I change settings?

**Via UI** (Recommended):
1. Click Settings button (⚙️)
2. Modify settings
3. Click Save

**Via File**:
1. Edit `%USERPROFILE%\.medium_publisher\config.yaml`
2. Save file
3. Restart application

### What settings can I configure?

- Typing speed (10-100ms)
- Human typing (enabled/disabled)
- Typo frequency (low/medium/high)
- Default publish mode (draft/public)
- Browser visibility (visible/headless)
- Default article directory
- Remember login (enabled/disabled)

### Can I have different configurations for different projects?

Yes, manually:
1. Create multiple config files (e.g., `config_project1.yaml`)
2. Copy desired config before launching
3. Application loads from standard location

### How do I reset to defaults?

```cmd
REM Delete user configuration
del %USERPROFILE%\.medium_publisher\config.yaml

REM Restart application (recreates with defaults)
```

### Are credentials stored in configuration?

No, credentials are stored separately:
- **Session cookies**: `session_cookies.json`
- **Passwords**: Windows Credential Manager (OS keychain)

## Troubleshooting

### Application won't start

**Solutions**:
1. Verify Python installed: `python --version`
2. Activate virtual environment: `venv\Scripts\activate`
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Check logs: `%USERPROFILE%\.medium_publisher\logs\`

### Browser won't launch

**Solutions**:
1. Reinstall Playwright browser: `playwright install chromium --force`
2. Check antivirus isn't blocking
3. Verify disk space available
4. Check logs for specific error

### Authentication fails

**Solutions**:
1. Verify credentials are correct
2. Try logging in manually on Medium
3. Check internet connection
4. Clear session cookies and re-authenticate
5. Try different authentication method

### Content not typing

**Solutions**:
1. Verify browser is visible (not headless)
2. Check rate limiting isn't paused
3. Verify selectors are correct
4. Check logs for errors
5. Update `selectors.yaml` if Medium UI changed

### Settings not saving

**Solutions**:
1. Check file permissions on `%USERPROFILE%\.medium_publisher\`
2. Verify YAML syntax in config file
3. Check logs for validation errors
4. Delete and recreate config file

### Where are logs located?

`%USERPROFILE%\.medium_publisher\logs\`

**Log Files**:
- `medium_publisher.log`: Latest log
- `medium_publisher_YYYYMMDD.log`: Daily logs

### How do I enable debug logging?

1. Edit `medium_publisher\utils\logger.py`
2. Change `default_level="INFO"` to `default_level="DEBUG"`
3. Restart application
4. Reproduce issue
5. Check logs for detailed information

### How do I report a bug?

1. Check FAQ and troubleshooting guide
2. Collect diagnostic information:
   - Error message
   - Steps to reproduce
   - Logs
   - Screenshots
3. Search existing issues
4. Create new issue with details

### Can I get help?

Yes:
1. Read documentation thoroughly
2. Check FAQ and troubleshooting guide
3. Search community forums
4. Create issue with detailed information
5. Provide logs and diagnostic data

---

**Still Have Questions?** Check the [User Guide](USER_GUIDE.md) for detailed information or [Troubleshooting Guide](TROUBLESHOOTING.md) for specific issues.

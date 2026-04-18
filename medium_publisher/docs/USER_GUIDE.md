# Medium Article Publisher - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Publishing Your First Article](#publishing-your-first-article)
4. [Authentication Methods](#authentication-methods)
5. [Working with Versions](#working-with-versions)
6. [Batch Publishing](#batch-publishing)
7. [Understanding Rate Limiting](#understanding-rate-limiting)
8. [Human Typing Simulation](#human-typing-simulation)
9. [Configuration](#configuration)
10. [Tips and Best Practices](#tips-and-best-practices)

## Introduction

The Medium Article Publisher is a desktop application that automates publishing markdown articles to Medium. It uses browser automation to type your content into Medium's editor with realistic human-like behavior, including typing speed variations and occasional typos.

### Key Features

- **Markdown Support**: Write articles in markdown with frontmatter metadata
- **Human-Like Typing**: Realistic typing with speed variations and typos
- **Rate Limiting**: Enforces Medium's 35 characters/minute limit
- **Version Management**: Update articles incrementally through multiple versions
- **Batch Publishing**: Publish multiple articles in one session
- **Google OAuth**: Secure authentication via Google account
- **Session Management**: Resume interrupted publishing sessions

## Getting Started

### System Requirements

- Windows 10/11
- Python 3.11 or higher
- Internet connection
- Medium account (with or without Google OAuth)

### Installation

See [SETUP.md](SETUP.md) for detailed installation instructions.

### First Launch

1. Launch the application by running `python main.py`
2. The main window will appear with file selection and publishing options
3. Configure settings via the Settings button (⚙️ icon)

## Publishing Your First Article

### Step 1: Prepare Your Markdown File

Create a markdown file with YAML frontmatter:

```markdown
---
title: "My First Article"
subtitle: "A beginner's guide"
tags:
  - tutorial
  - beginner
  - medium
---

# Introduction

Your article content goes here...

## Section 1

More content...
```

**Required Frontmatter Fields**:
- `title`: Article title (max 200 characters)
- `subtitle`: Article subtitle (optional, max 300 characters)
- `tags`: Up to 5 tags (alphanumeric with hyphens/spaces)

### Step 2: Select Your Article

1. Click **"Select File"** button
2. Navigate to your markdown file
3. Select the file
4. The application will display:
   - File path
   - Character count
   - Estimated typing time (with typo overhead)

### Step 3: Authenticate with Medium

**Option A: Google OAuth (Recommended)**
1. Click **"Login"** button
2. Select **"Google OAuth"** from the dropdown
3. Browser window will open to Medium login page
4. Click **"Sign in with Google"** in the browser
5. Complete Google authentication (including 2FA if enabled)
6. Application will detect successful login automatically
7. Session cookies are saved for future use

**Option B: Email/Password**
1. Click **"Login"** button
2. Select **"Email/Password"** from the dropdown
3. Enter your Medium credentials
4. If 2FA is enabled, complete it in the browser
5. Credentials are stored securely in OS keychain

### Step 4: Publish

1. Click **"Publish Version"** button
2. Confirm the estimated time in the dialog
3. Watch the progress bar as the article is typed
4. When complete, review the article in the browser
5. Manually insert any tables or images (marked with TODO placeholders)
6. Click **"Publish"** in Medium's editor when ready

## Authentication Methods

### Google OAuth (Recommended)

**Advantages**:
- No password storage required
- Supports Google 2FA and security keys
- More secure authentication flow
- Session cookies persist across launches

**How It Works**:
1. Application opens Medium login page in visible browser
2. You manually click "Sign in with Google"
3. Complete Google OAuth flow in browser
4. Application detects successful login (polls for indicators)
5. Session cookies saved to `~/.medium_publisher/session_cookies.json`

**Session Duration**: ~7 days (Medium's default)

**Re-authentication**: Required when session expires

### Email/Password

**Advantages**:
- Direct authentication
- Faster login process

**How It Works**:
1. Enter email and password in application
2. Credentials stored in OS keychain (optional)
3. Application logs in automatically
4. Session cookies saved for reuse

**2FA Support**: Application pauses for manual 2FA entry in browser

## Working with Versions

The version workflow allows you to update articles incrementally without retyping the entire content.

### Version Workflow Overview

1. **Version 1**: Type complete article
2. **Version 2**: Apply changes based on instructions
3. **Version 3+**: Continue iterating

### Publishing Version 1

1. Select your markdown file (e.g., `article-v1.md`)
2. Select **"v1"** from version dropdown
3. Click **"Publish Version"**
4. Complete article is typed into Medium editor

### Updating to Version 2

1. Create `article-v2.md` with updated content
2. Select **"v2"** from version dropdown
3. Enter change instructions in the text area:

```
Replace the introduction section with new content
Add a new section after "Design Principles"
Update the conclusion
```

4. Click **"Apply Changes"**
5. Application will:
   - Parse your instructions
   - Find the specified sections
   - Delete old content
   - Type new content
   - Preserve unchanged sections

### Change Instruction Format

**Supported Actions**:
- `Replace [section] with [new content]`
- `Delete [section]`
- `Update [section]` (same as replace)
- `Add [new section]` (at end)
- `Insert [content] after [section]`
- `Insert [content] before [section]`

**Examples**:
```
Replace the "Getting Started" section with updated instructions
Delete the "Deprecated Features" section
Add a new "Advanced Topics" section
Insert troubleshooting tips after the "Installation" section
```

### Version Progression

- Browser session is maintained across versions
- No re-authentication required
- Session state tracks current version
- Can iterate through v1 → v2 → v3 → ... → v99

## Batch Publishing

Publish multiple articles in one session with shared authentication.

### How to Use Batch Publishing

1. Click **"Select Multiple"** button
2. Select multiple markdown files (Ctrl+Click or Shift+Click)
3. Review batch information:
   - Number of articles
   - Total character count
   - Total estimated time
4. Click **"Publish Batch"** button
5. Confirm the batch operation
6. Articles are published sequentially
7. Progress shows: "Article 1 of 3", "Article 2 of 3", etc.

### Batch Behavior

- **Sequential Processing**: Articles published one at a time
- **Shared Session**: Single browser session for all articles
- **Continue on Error**: Failures don't stop the batch
- **Summary Report**: Shows success/failure for each article

### Batch Summary

After completion, you'll see:
- Total articles processed
- Successful publications
- Failed publications (with error messages)
- Total time elapsed

## Understanding Rate Limiting

Medium enforces a rate limit to prevent automated spam. This application respects that limit.

### Rate Limit Details

- **Hard Limit**: 35 characters per minute (non-configurable)
- **Enforcement**: Sliding window approach
- **Wait Logic**: Application pauses when limit is reached
- **Resume**: Typing resumes when capacity is available

### Why Rate Limiting?

1. **Medium's Terms**: Prevents account suspension
2. **Human-Like Behavior**: Makes automation less detectable
3. **Quality Control**: Encourages thoughtful content

### Time Estimation

The application calculates estimated typing time before publishing:

**Formula**: `(total_chars + typo_overhead) / 35 chars/min * 60 seconds`

**Example** (1000 character article with medium typos):
- Base characters: 1000
- Typos (5%): 50 typos
- Typo overhead: 50 × 4 = 200 extra keystrokes
- Total keystrokes: 1200
- Estimated time: 1200 / 35 = 34.3 minutes

### Rate Limit Warning

Large articles may take significant time:
- 1000 chars: ~30-35 minutes
- 2000 chars: ~60-70 minutes
- 5000 chars: ~2.5-3 hours

**Recommendation**: Break long articles into smaller sections or use version workflow.

## Human Typing Simulation

The application simulates realistic human typing to avoid detection as automation.

### Typing Behaviors

1. **Speed Variation**: ±20% random variation per character
2. **Thinking Pauses**: Occasional 100-500ms pauses (10% chance)
3. **Typos**: Realistic typos with corrections
4. **Correction Delay**: Wait 1-3 characters before fixing typo

### Typo Simulation

**How It Works**:
1. Application decides to make a typo (based on frequency)
2. Types an adjacent key instead of intended character
3. Continues typing 1-3 more characters
4. Presses backspace to delete typo + extra characters
5. Retypes correctly

**QWERTY Keyboard Layout**:
- Typos use adjacent keys on QWERTY layout
- Case is preserved (uppercase typo for uppercase letter)
- Example: 'a' might become 'q', 's', 'w', or 'z'

### Typo Frequency Settings

Configure in Settings dialog:

- **Low (2%)**: 1 typo per 50 characters (~20 typos per 1000 chars)
- **Medium (5%)**: 1 typo per 20 characters (~50 typos per 1000 chars)
- **High (8%)**: 1 typo per 12.5 characters (~80 typos per 1000 chars)

### Typo Overhead

Each typo adds ~4 extra keystrokes:
- 1 wrong character
- 1-3 additional characters
- 1-4 backspaces
- 1 correct character

**Time Impact**:
- Low (2%): +8% typing time
- Medium (5%): +20% typing time
- High (8%): +32% typing time

### No Typos In

- Code blocks (```code```)
- URLs and links
- TODO placeholders
- Special characters

### Disabling Typos

1. Open Settings (⚙️ button)
2. Uncheck **"Human-like typing"**
3. Click **"Save"**
4. Typing will be consistent without typos (still rate-limited)

## Configuration

### Settings Dialog

Access via Settings button (⚙️) in main window.

### Typing Settings

- **Typing Speed**: 10-100ms per character (default: 30ms)
- **Human-like Typing**: Enable/disable typo simulation
- **Typo Frequency**: Low/Medium/High (when enabled)
- **Rate Limit**: 35 chars/min (non-configurable, display only)

### Publishing Settings

- **Default Mode**: Draft or Public
  - Draft: Article saved as draft (not published)
  - Public: Article published immediately

### Browser Settings

- **Browser Visibility**: Visible or Headless
  - Visible: See browser automation (recommended)
  - Headless: Browser runs in background (faster, but harder to debug)

### Paths Settings

- **Default Article Directory**: Where file selector starts
- Browse button to select directory
- Remembers last used directory

### Credentials Settings

- **Remember Login**: Save session cookies
  - Enabled: Session persists across launches
  - Disabled: Re-authenticate each launch

## Tips and Best Practices

### Writing Articles

1. **Use Frontmatter**: Always include title, subtitle, and tags
2. **Test Locally**: Preview markdown before publishing
3. **Keep It Concise**: Shorter articles publish faster
4. **Use Versions**: Update incrementally instead of republishing

### Authentication

1. **Use Google OAuth**: More secure and supports 2FA
2. **Save Sessions**: Enable "Remember Login" for convenience
3. **Re-authenticate Periodically**: Sessions expire after ~7 days

### Publishing

1. **Review Estimates**: Check estimated time before publishing
2. **Use Draft Mode**: Publish as draft first, review, then make public
3. **Manual Review**: Always review in browser before final publish
4. **Insert Media**: Manually add tables and images at TODO placeholders

### Version Updates

1. **Clear Instructions**: Be specific about sections to change
2. **Test Changes**: Review version 2 before version 3
3. **Incremental Updates**: Small changes are easier to manage
4. **Backup Versions**: Keep all version files for reference

### Batch Publishing

1. **Group Similar Articles**: Batch articles from same series
2. **Check Total Time**: Ensure you have time for full batch
3. **Monitor Progress**: Watch for errors in batch summary
4. **Resume on Failure**: Re-run failed articles individually

### Performance

1. **Close Other Browsers**: Reduce resource usage
2. **Stable Internet**: Ensure reliable connection
3. **Don't Interrupt**: Let publishing complete without interruption
4. **Check Logs**: Review logs for debugging issues

### Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

### FAQ

See [FAQ.md](FAQ.md) for frequently asked questions.

---

**Need Help?** Check the troubleshooting guide or FAQ for common issues and solutions.

# Medium Article Publisher - Configuration Reference

## Table of Contents
1. [Configuration Files](#configuration-files)
2. [Typing Configuration](#typing-configuration)
3. [Publishing Configuration](#publishing-configuration)
4. [Browser Configuration](#browser-configuration)
5. [Paths Configuration](#paths-configuration)
6. [Credentials Configuration](#credentials-configuration)
7. [Selector Configuration](#selector-configuration)
8. [Advanced Configuration](#advanced-configuration)

## Configuration Files

### Location

**User Configuration**: `~/.medium_publisher/config.yaml`
**Default Configuration**: `medium_publisher/config/default_config.yaml`
**Selectors**: `medium_publisher/config/selectors.yaml`

### Configuration Hierarchy

1. User configuration (`~/.medium_publisher/config.yaml`) - highest priority
2. Default configuration (`config/default_config.yaml`) - fallback values

### Configuration Format

YAML format with nested sections:

```yaml
typing:
  speed_ms: 30
  # ... more typing settings

publishing:
  default_mode: draft
  # ... more publishing settings
```

## Typing Configuration

### speed_ms

**Description**: Base delay between keystrokes in milliseconds
**Type**: Integer
**Range**: 10-100
**Default**: 30
**UI**: Typing Speed slider in Settings

**Effect**:
- Lower values = faster typing (less human-like)
- Higher values = slower typing (more human-like)
- Actual delay varies ±20% per character

**Examples**:
- 10ms: Very fast (600 chars/min theoretical, limited by rate limiter)
- 30ms: Moderate (200 chars/min theoretical, limited by rate limiter)
- 50ms: Slow (120 chars/min theoretical, limited by rate limiter)
- 100ms: Very slow (60 chars/min theoretical, limited by rate limiter)

**Note**: All speeds are limited by the 35 chars/min rate limit.

### paragraph_delay_ms

**Description**: Delay between paragraphs
**Type**: Integer
**Range**: 0-1000
**Default**: 100
**UI**: Not exposed (advanced setting)

**Effect**: Natural pause between paragraphs

### max_chars_per_minute

**Description**: Maximum characters per minute (rate limit)
**Type**: Integer
**Range**: Fixed at 35
**Default**: 35
**UI**: Display only (non-editable)

**Effect**: Hard limit enforced by sliding window algorithm

**Why 35?**: Medium's rate limit to prevent automated spam

### human_typing_enabled

**Description**: Enable human-like typing simulation
**Type**: Boolean
**Values**: true, false
**Default**: true
**UI**: "Human-like typing" checkbox in Settings

**Effect**:
- true: Enables typos, corrections, speed variations, thinking pauses
- false: Consistent typing without typos (still rate-limited)

### typo_frequency

**Description**: Frequency of typos when human typing is enabled
**Type**: String
**Values**: low, medium, high
**Default**: low
**UI**: "Typo Frequency" dropdown in Settings

**Effect**:
- low: 2% typo rate (~1 typo per 50 characters)
- medium: 5% typo rate (~1 typo per 20 characters)
- high: 8% typo rate (~1 typo per 12.5 characters)

**Time Overhead**:
- low: +8% typing time
- medium: +20% typing time
- high: +32% typing time

## Publishing Configuration

### default_mode

**Description**: Default publishing mode
**Type**: String
**Values**: draft, public
**Default**: draft
**UI**: "Default Mode" radio buttons in Settings

**Effect**:
- draft: Articles saved as draft (not published)
- public: Articles published immediately

**Recommendation**: Use draft mode for review before publishing

### auto_add_tags

**Description**: Automatically add tags from frontmatter
**Type**: Boolean
**Values**: true, false
**Default**: true
**UI**: Not exposed (always enabled)

**Effect**: Tags from frontmatter are added to Medium article

### max_tags

**Description**: Maximum number of tags
**Type**: Integer
**Range**: 1-5
**Default**: 5
**UI**: Not exposed (Medium's limit)

**Effect**: Only first 5 tags are used if more are provided

### remember_draft_url

**Description**: Remember last used draft URL
**Type**: Boolean
**Values**: true, false
**Default**: true
**UI**: Not exposed (always enabled)

**Effect**: Draft URL field pre-filled with last used URL

## Browser Configuration

### headless

**Description**: Run browser in headless mode (no visible window)
**Type**: Boolean
**Values**: true, false
**Default**: false
**UI**: "Browser Visibility" checkbox in Settings

**Effect**:
- false: Browser window visible (recommended)
- true: Browser runs in background (faster, harder to debug)

**Recommendation**: Use visible mode for first-time setup and debugging

### timeout_seconds

**Description**: Default timeout for browser operations
**Type**: Integer
**Range**: 10-120
**Default**: 30
**UI**: Not exposed (advanced setting)

**Effect**: Maximum wait time for page loads and element detection

## Paths Configuration

### last_directory

**Description**: Last directory used in file selector
**Type**: String
**Default**: "" (empty)
**UI**: Automatically updated when selecting files

**Effect**: File selector opens to this directory

### articles_directory

**Description**: Default directory for articles
**Type**: String
**Default**: "" (empty)
**UI**: "Default Article Directory" in Settings

**Effect**: File selector starts here if no last_directory

### last_draft_url

**Description**: Last used Medium draft URL
**Type**: String
**Default**: "" (empty)
**UI**: Automatically updated when entering draft URL

**Effect**: Draft URL field pre-filled with this value

## Credentials Configuration

### remember_login

**Description**: Save session cookies for reuse
**Type**: Boolean
**Values**: true, false
**Default**: false
**UI**: "Remember Login" checkbox in Settings

**Effect**:
- true: Session cookies saved to `~/.medium_publisher/session_cookies.json`
- false: Re-authenticate each launch

**Security**: Cookies stored in user home directory with restricted permissions

## Selector Configuration

### File: selectors.yaml

Contains CSS selectors for Medium's web interface. These may need updates if Medium changes their UI.

### Login Selectors

```yaml
medium:
  login:
    sign_in_button: 'a[href*="sign-in"]'
    google_oauth_button: 'button:has-text("Sign in with Google")'
    email_input: 'input[type="email"]'
    password_input: 'input[type="password"]'
    continue_button: 'button:has-text("Continue")'
```

### Logged In Indicators

```yaml
  logged_in_indicators:
    user_menu: '[data-testid="user-menu"]'
    profile_image: 'img[alt*="profile"]'
    new_story_button: 'a[href="/new-story"]'
```

### Editor Selectors

```yaml
  editor:
    new_story_link: 'a[href="/new-story"]'
    title_field: '[data-testid="storyTitle"]'
    content_area: '[data-testid="storyContent"]'
    publish_button: 'button:has-text("Publish")'
```

### Publishing Selectors

```yaml
  publishing:
    tags_input: 'input[placeholder*="tags"]'
    subtitle_input: 'input[placeholder*="subtitle"]'
    draft_button: 'button:has-text("Save as draft")'
    public_button: 'button:has-text("Publish now")'
```

### Draft Selectors

```yaml
  draft:
    editor_content: '[contenteditable="true"]'
    clear_all: 'button[aria-label="Clear"]'
```

### Keyboard Shortcuts

```yaml
formatting:
  bold: "Control+B"
  italic: "Control+I"
  code: "Control+Alt+6"
  header_2: "Control+Alt+2"
  header_3: "Control+Alt+3"
  link: "Control+K"
```

## Advanced Configuration

### Manual Configuration File Editing

1. Locate user configuration:
   ```cmd
   cd %USERPROFILE%\.medium_publisher
   notepad config.yaml
   ```

2. Edit values in YAML format

3. Save and restart application

### Configuration Validation

The application validates configuration on startup:
- Type checking (integer, boolean, string)
- Range checking (min/max values)
- Enum validation (valid options)

Invalid values are replaced with defaults and logged.

### Resetting Configuration

To reset to defaults:

```cmd
REM Delete user configuration
del %USERPROFILE%\.medium_publisher\config.yaml

REM Restart application (will recreate with defaults)
```

### Configuration Backup

Backup your configuration:

```cmd
REM Backup
copy %USERPROFILE%\.medium_publisher\config.yaml config_backup.yaml

REM Restore
copy config_backup.yaml %USERPROFILE%\.medium_publisher\config.yaml
```

### Environment-Specific Configuration

For different environments (e.g., testing vs production):

1. Create multiple configuration files:
   - `config_test.yaml`
   - `config_prod.yaml`

2. Copy desired config before launching:
   ```cmd
   copy config_test.yaml %USERPROFILE%\.medium_publisher\config.yaml
   python main.py
   ```

### Logging Configuration

Logging is configured in code, not in YAML. To adjust log levels:

1. Edit `medium_publisher/utils/logger.py`
2. Change `default_level` in `LoggerConfig`
3. Restart application

**Log Levels**:
- DEBUG: Detailed debugging information
- INFO: General information (default)
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

### Session State Configuration

Session state is stored in:
- `~/.medium_publisher/session_state.json`

Contains:
- Current version
- Completed versions
- Article path
- Draft URL
- Progress information

**Manual Editing**: Not recommended (managed by application)

### Cookie Storage Configuration

Session cookies are stored in:
- `~/.medium_publisher/session_cookies.json`

Contains:
- Medium session cookies
- Expiration timestamps

**Security**: File has restricted permissions (user read/write only)

**Manual Editing**: Not recommended (managed by application)

## Configuration Examples

### Fast Typing (Testing)

```yaml
typing:
  speed_ms: 10
  human_typing_enabled: false
  max_chars_per_minute: 35  # Still enforced
```

**Effect**: Fastest possible typing (limited by rate limiter)

### Maximum Human-Like Behavior

```yaml
typing:
  speed_ms: 50
  human_typing_enabled: true
  typo_frequency: high
  paragraph_delay_ms: 200
```

**Effect**: Very realistic typing with frequent typos

### Production Publishing

```yaml
publishing:
  default_mode: public

browser:
  headless: true
  timeout_seconds: 60

credentials:
  remember_login: true
```

**Effect**: Automated publishing with saved credentials

### Development/Testing

```yaml
publishing:
  default_mode: draft

browser:
  headless: false
  timeout_seconds: 30

credentials:
  remember_login: false
```

**Effect**: Visible browser, draft mode, no saved credentials

## Troubleshooting Configuration

### Configuration Not Loading

**Symptom**: Settings changes don't persist

**Solution**:
1. Check file permissions on `~/.medium_publisher/`
2. Verify YAML syntax (use online YAML validator)
3. Check application logs for validation errors

### Invalid Configuration Values

**Symptom**: Application uses defaults despite custom config

**Solution**:
1. Check logs for validation errors
2. Verify value types (integer vs string)
3. Verify value ranges (e.g., speed_ms: 10-100)

### Selectors Not Working

**Symptom**: Application can't find Medium UI elements

**Solution**:
1. Medium may have changed their UI
2. Update `selectors.yaml` with new selectors
3. Use browser developer tools to find correct selectors
4. Report issue for official update

---

**Need Help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common configuration issues.

# Medium Article Publisher - Configuration Reference

## Table of Contents
1. [Configuration Files](#configuration-files)
2. [Typing Configuration](#typing-configuration)
3. [Publishing Configuration](#publishing-configuration)
4. [Safety Configuration](#safety-configuration)
5. [Navigation Configuration](#navigation-configuration)
6. [UI Configuration](#ui-configuration)
7. [Assets Configuration](#assets-configuration)
8. [Advanced Configuration](#advanced-configuration)

## Configuration Files

### Location

**Default Configuration**: `config/default_config.yaml`

### Configuration Format

YAML format with nested sections:

```yaml
typing:
  base_delay_ms: 150
  # ... more typing settings

publishing:
  default_mode: draft
  # ... more publishing settings
```

## Typing Configuration

### base_delay_ms

**Description**: Base delay between keystrokes in milliseconds
**Type**: Integer
**Default**: 150

**Effect**:
- Lower values = faster typing
- Higher values = slower, more human-like typing
- Actual delay varies based on `variation_percent`

### variation_percent

**Description**: Random variation applied to base delay
**Type**: Integer
**Default**: 30

**Effect**: Each keystroke delay is `base_delay_ms ± variation_percent%`. A value of 30 means delays range from 105ms to 195ms (with base of 150ms).

### human_typing_enabled

**Description**: Enable human-like typing simulation
**Type**: Boolean
**Default**: true

**Effect**:
- true: Enables speed variations, thinking pauses, paragraph pauses, and optional typos
- false: Consistent typing at base_delay_ms rate

### typo_frequency

**Description**: Frequency of intentional typos when human typing is enabled
**Type**: String
**Values**: "none", "low", "medium", "high"
**Default**: "none"

**Effect**:
- "none": No typos generated
- "low": Occasional typos (~2%)
- "medium": Moderate typos (~5%)
- "high": Frequent typos (~8%)

### immediate_correction_ratio

**Description**: Ratio of typos corrected immediately vs. deferred
**Type**: Float
**Range**: 0.0 - 1.0
**Default**: 0.70

**Effect**: 0.70 means 70% of typos are corrected immediately (backspace + retype), while 30% are deferred and corrected later in a batch.

### thinking_pause_min_ms / thinking_pause_max_ms

**Description**: Range for random "thinking" pauses between words or sentences
**Type**: Integer
**Default**: Configured in default_config.yaml

**Effect**: Simulates natural pauses where a human would think before continuing.

### paragraph_pause_min_ms / paragraph_pause_max_ms

**Description**: Range for pauses between paragraphs
**Type**: Integer
**Default**: Configured in default_config.yaml

**Effect**: Longer pauses between paragraphs to simulate reading/thinking between sections.

## Publishing Configuration

### default_mode

**Description**: Default publishing mode
**Type**: String
**Values**: "draft", "public"
**Default**: "draft"

**Effect**:
- "draft": Articles saved as draft (not published)
- "public": Articles published immediately

### max_tags

**Description**: Maximum number of tags per article
**Type**: Integer
**Default**: 5

**Effect**: Only first 5 tags from frontmatter are used (Medium's limit).

## Safety Configuration

### emergency_stop_hotkey

**Description**: Keyboard shortcut to immediately stop all automation
**Type**: String
**Default**: "ctrl+shift+escape"

**Effect**: Pressing this hotkey at any time raises `EmergencyStopError` and halts all typing/navigation. Monitored via pynput keyboard listener.

### countdown_seconds

**Description**: Countdown before typing begins
**Type**: Integer
**Default**: 3

**Effect**: Gives user time to position cursor or cancel before automation starts.

### focus_check_enabled

**Description**: Whether to verify the target window has focus before typing
**Type**: Boolean
**Default**: true

**Effect**:
- true: Typing pauses if the target window loses focus, raises `FocusLostError`
- false: Types regardless of window focus (not recommended)

## Navigation Configuration

### screen_confidence

**Description**: Minimum confidence threshold for screen recognition matches
**Type**: Float
**Range**: 0.0 - 1.0
**Default**: 0.8

**Effect**: When matching reference PNG images against the screen, matches below this confidence are rejected. Lower values = more permissive matching, higher values = stricter.

### poll_interval_seconds

**Description**: How often to poll the screen for state changes
**Type**: Integer
**Default**: 2

**Effect**: The NavigationStateMachine checks the screen every N seconds to detect page transitions.

### login_timeout_seconds

**Description**: Maximum time to wait for user to complete login
**Type**: Integer
**Default**: 300

**Effect**: If login is not detected within this time, a `NavigationError` is raised. The user completes OAuth manually in their browser.

### page_load_timeout_seconds

**Description**: Maximum time to wait for a page to load
**Type**: Integer
**Default**: 30

**Effect**: After navigation, the app waits up to this duration for the expected screen state to appear.

### google_account_email

**Description**: Google account email for login detection
**Type**: String
**Default**: "" (empty)

**Effect**: Used by the login flow to identify which Google account to expect during OAuth.

## UI Configuration

### always_on_top

**Description**: Keep application window above other windows
**Type**: Boolean
**Default**: true

**Effect**: The publisher window stays visible even when the browser has focus.

### remember_window_position

**Description**: Save and restore window position between sessions
**Type**: Boolean
**Default**: true

### remember_last_directory

**Description**: Remember the last directory used in file selection
**Type**: Boolean
**Default**: true

## Assets Configuration

### reference_images_dir

**Description**: Directory containing reference PNG images for screen recognition
**Type**: String
**Default**: "assets/medium/"

**Effect**: The ScreenRecognition module loads reference images from this directory to identify UI states (login buttons, editor fields, navigation elements).

**Contents**: PNG screenshots of Medium UI elements used for matching:
- Login page indicators
- Editor state indicators
- Navigation elements
- Button states

## Advanced Configuration

### Manual Configuration File Editing

1. Open the config file:
   ```cmd
   notepad config\default_config.yaml
   ```

2. Edit values in YAML format
3. Save and restart application

### Configuration Validation

The ConfigManager validates configuration on load:
- Type checking (integer, boolean, string, float)
- Range checking where applicable
- Missing keys filled with defaults

Invalid values are replaced with defaults and logged.

### Resetting Configuration

To reset to defaults, restore the original `config/default_config.yaml` from version control:

```cmd
git checkout -- config\default_config.yaml
```

## Configuration Examples

### Fast Typing (Testing)

```yaml
typing:
  base_delay_ms: 50
  variation_percent: 10
  human_typing_enabled: false
  typo_frequency: "none"
```

### Maximum Human-Like Behavior

```yaml
typing:
  base_delay_ms: 200
  variation_percent: 40
  human_typing_enabled: true
  typo_frequency: "medium"
  immediate_correction_ratio: 0.60
```

### Strict Safety

```yaml
safety:
  emergency_stop_hotkey: "ctrl+shift+escape"
  countdown_seconds: 5
  focus_check_enabled: true

navigation:
  screen_confidence: 0.9
  login_timeout_seconds: 600
```

## Troubleshooting Configuration

### Configuration Not Loading

**Symptom**: Settings changes don't take effect

**Solution**:
1. Verify YAML syntax (use online YAML validator)
2. Check application logs for validation errors
3. Ensure file is saved as UTF-8

### Screen Recognition Failing

**Symptom**: Navigation times out, states not detected

**Solution**:
1. Increase `login_timeout_seconds` or `page_load_timeout_seconds`
2. Lower `screen_confidence` (e.g., 0.7) if matches are close but rejected
3. Verify reference images in `assets/medium/` match your screen resolution
4. Check that display scaling matches the reference images

### Emergency Stop Not Working

**Symptom**: Hotkey doesn't stop automation

**Solution**:
1. Verify `emergency_stop_hotkey` is set correctly
2. Ensure pynput has keyboard access permissions
3. Try a different hotkey combination
4. Check that no other application is capturing the same hotkey

---

**Need Help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common configuration issues.

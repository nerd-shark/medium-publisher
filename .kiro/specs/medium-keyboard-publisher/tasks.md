# Implementation Plan: Medium Keyboard Publisher

## Overview

Rework the existing `medium_publisher/` desktop application from Playwright-based browser automation to OS-level keyboard/mouse control via pyautogui/pynput. Reuse core parsing, config, logging, and models. Build new Safety, Navigation, and Automation layers. Rework UI and ContentTyper. All code is Python 3.11+ with PyQt6 UI.

## Tasks

- [x] 1. Update project dependencies and configuration
  - [x] 1.1 Update `requirements.txt` to add pyautogui, pynput, Pillow, hypothesis; remove playwright, selenium, browser-cookie3
    - _Requirements: Constraints, Dependencies_
  - [x] 1.2 Update `config/default_config.yaml` with new schema (typing, safety, navigation, ui, assets sections); remove browser/rate-limiter settings
    - Reference design Configuration Schema section
    - _Requirements: 12.1, 12.11_
  - [x] 1.3 Add new exception classes to `utils/exceptions.py`: `EmergencyStopError`, `NavigationError`, `InputControlError`, `FocusLostError`
    - Extend existing `PublishingError` hierarchy
    - _Requirements: 13.1, 13.7_

- [x] 2. Implement new data models
  - [x] 2.1 Add `DeferredTypo`, `TypingProgress`, and `NavigationState` to `core/models.py`
    - `DeferredTypo`: block_index, char_offset, wrong_char, correct_char, surrounding_context
    - `TypingProgress`: total_blocks, current_block, total_chars, typed_chars, deferred_typo_count, review pass flags, estimated_remaining_seconds
    - `NavigationState`: Enum with START, LOGGED_OUT_HOME, SIGN_IN_SCREEN, GOOGLE_SIGN_IN, WAITING_2FA, LOGGED_IN_HOME, DRAFTS_PAGE, NEW_STORY_EDITOR, ERROR, READY
    - _Requirements: 3.3, 5.7, 14.8, 14.9_

  - [x] 2.2 Write property test for DeferredTypo round-trip (Property 17)
    - **Property 17: Deferred typo recording preserves all fields**
    - Record a deferred typo via `DeferredTypoTracker.record()` and retrieve via `get_all()` — all fields must match
    - **Validates: Requirements 5.7**

- [x] 3. Implement Safety Layer
  - [x] 3.1 Create `safety/emergency_stop.py` — EmergencyStop class
    - pynput `GlobalHotKeys` listener in background thread for configurable hotkey (default: Ctrl+Shift+Escape)
    - pyautogui `FAILSAFE = True` for mouse-to-corner detection
    - `trigger()`, `reset()`, `is_stopped()`, `pause()`, `resume()` methods
    - `release_all_keys()` called on trigger to release all held modifiers
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_
  - [x] 3.2 Create `safety/focus_window_detector.py` — FocusWindowDetector class
    - Platform-specific window detection using `win32gui` on Windows
    - `get_active_window_title()`, `capture_target_window()`, `is_target_focused()`
    - _Requirements: 6.9_
  - [x] 3.3 Write property tests for Safety Layer
    - **Property 19: Emergency stop releases all held modifier keys**
    - **Validates: Requirements 6.4**
    - **Property 20: Focus window change pauses typing**
    - **Validates: Requirements 6.9**
  - [x] 3.4 Write unit tests for EmergencyStop and FocusWindowDetector
    - Test trigger/reset/pause/resume state transitions
    - Test key release on trigger
    - Test window title comparison logic
    - _Requirements: 6.1–6.9_

- [x] 4. Checkpoint — Safety layer complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement OS Input Controller
  - [x] 5.1 Create `automation/os_input_controller.py` — OS_Input_Controller class
    - Inject `EmergencyStop` dependency; check `is_stopped()` before every keystroke/click
    - `type_character()`, `type_text()`, `press_key()`, `hotkey()`, `select_text_backwards()`
    - `click_at()`, `click_image()`, `scroll()`, `release_all_keys()`
    - Use pyautogui for keyboard/mouse, pynput for low-level key events where needed
    - Inject `FocusWindowDetector`; check `is_target_focused()` before actions
    - _Requirements: 4.1, 4.2, 4.16, 6.4, 6.9_
  - [x] 5.2 Write unit tests for OS_Input_Controller
    - Mock pyautogui/pynput calls; verify correct key sequences
    - Test emergency stop check before each action
    - Test focus window check integration
    - _Requirements: 4.1, 4.2_

- [x] 6. Implement DeferredTypoTracker
  - [x] 6.1 Create `automation/deferred_typo_tracker.py` — DeferredTypoTracker class
    - `record()`, `get_all()`, `clear()`, `count` property
    - Returns typos in document order (by block_index, then char_offset)
    - _Requirements: 5.7, 5.8_
  - [x] 6.2 Write property test for DeferredTypoTracker (Property 17)
    - **Property 17: Deferred typo recording preserves all fields**
    - **Validates: Requirements 5.7**

- [x] 7. Implement Screen Recognition and Navigation
  - [x] 7.1 Create `navigation/screen_recognition.py` — ScreenRecognition class
    - Wrap pyautogui `locateOnScreen()` with configurable confidence threshold
    - `find_on_screen()`, `is_visible()`, `wait_for()` (polling with timeout), `capture_reference()`, `set_confidence()`
    - Assets directory defaults to `assets/medium/` (6 reference images already exist)
    - _Requirements: 3.2, 3.3, 3.14, 3.17, 3.18_
  - [x] 7.2 Create `navigation/login_detector.py` — LoginDetector using ScreenRecognition
    - Check all 6 reference images to determine current page state
    - Map image matches to `NavigationState` enum values
    - _Requirements: 3.3, 3.4_
  - [x] 7.3 Create `navigation/navigation_state_machine.py` — NavigationStateMachine class
    - Inject ScreenRecognition, OS_Input_Controller, ConfigManager
    - `detect_current_state()` checks all 6 reference images
    - `navigate_to_editor()` drives full flow from START to READY
    - State handlers: `_handle_logged_out_home`, `_handle_sign_in_screen`, `_handle_google_sign_in`, `_handle_waiting_2fa`, `_handle_logged_in_home`, `_handle_drafts_page`
    - Open Medium.com via `webbrowser.open()`; poll every 2s; 5-min login timeout; 30s page load timeout
    - Log each state transition for debugging
    - _Requirements: 3.1–3.19_
  - [x] 7.4 Write property test for navigation state detection (Property 9)
    - **Property 9: Navigation state detection returns correct state**
    - Mock reference image visibility combinations; verify correct NavigationState returned
    - **Validates: Requirements 3.3, 3.4**
  - [x] 7.5 Write unit tests for Navigation layer
    - Test each state transition handler
    - Test timeout scenarios (30s page load, 5-min login)
    - Test 2FA wait and polling
    - Test error state when no image matches
    - _Requirements: 3.1–3.19_

- [x] 8. Checkpoint — Navigation layer complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Rework ContentTyper for OS-level input
  - [x] 9.1 Rework `automation/content_typer.py` — ContentTyper class
    - Replace Playwright `page.keyboard` calls with `OS_Input_Controller` methods
    - Remove rate limiter dependency (not needed for OS-level input)
    - Inject OS_Input_Controller, HumanTypingSimulator (reused), DeferredTypoTracker, ConfigManager
    - Implement all typing methods: `type_article()`, `type_title()`, `type_subtitle()`, `type_paragraph()`, `type_header()`, `type_code_block()`, `type_list()`, `type_link()`, `type_inline_formatting()`, `type_placeholder()`, `type_block_quote()`, `type_separator()`
    - `_type_with_typos()`: immediate typos corrected inline (70%), deferred typos recorded (30%)
    - `perform_review_pass()`: Ctrl+Home, then Ctrl+F for each deferred typo, find surrounding context, fix, Escape, next
    - Apply correct Medium shortcuts per formatting table in design
    - Code blocks, URLs, placeholders typed with `allow_typos=False`
    - _Requirements: 4.3–4.18, 5.1–5.14_
  - [x] 9.2 Write property tests for ContentTyper formatting (Properties 10, 11, 12)
    - **Property 10: Content formatting applies correct Medium shortcut**
    - **Validates: Requirements 4.6, 4.7, 4.8, 4.9, 4.12, 4.15**
    - **Property 11: List typing uses correct prefix per list type**
    - **Validates: Requirements 4.13, 4.14**
    - **Property 12: Protected content typed without typos**
    - **Validates: Requirements 4.10, 4.18, 5.14**
  - [x] 9.3 Write unit tests for ContentTyper
    - Test each content block type method
    - Test inline formatting with mixed bold/italic/code/link
    - Test review pass flow (Ctrl+Home, Ctrl+F, fix, Escape sequence)
    - Test placeholder handling (no formatting, no typos)
    - _Requirements: 4.3–4.18_

- [x] 10. Property tests for core parsing (reused modules)
  - [x] 10.1 Write property test for frontmatter round-trip (Property 1)
    - **Property 1: Frontmatter round-trip**
    - **Validates: Requirements 1.4, 2.1**
  - [x] 10.2 Write property tests for markdown parsing (Properties 2–7)
    - **Property 2: Header parsing preserves level and content**
    - **Validates: Requirements 2.2, 2.3, 2.4**
    - **Property 3: Inline formatting parsing preserves type and position**
    - **Validates: Requirements 2.5, 2.6, 2.8, 2.9**
    - **Property 4: Code block parsing preserves content**
    - **Validates: Requirements 2.7**
    - **Property 5: List parsing preserves items and type**
    - **Validates: Requirements 2.10, 2.11**
    - **Property 6: Paragraph breaks produce separate ContentBlocks**
    - **Validates: Requirements 2.12**
    - **Property 7: Placeholder detection for tables and images**
    - **Validates: Requirements 2.13, 2.14**
  - [x] 10.3 Write property test for file validation (Property 8)
    - **Property 8: File validation accepts .md and rejects invalid files**
    - **Validates: Requirements 1.3, 1.5**

- [x] 11. Property tests for typing simulation (reused HumanTypingSimulator)
  - [x] 11.1 Write property test for typing speed bounds (Property 13)
    - **Property 13: Typing speed variation stays within ±30% bounds**
    - **Validates: Requirements 5.1**
  - [x] 11.2 Write property test for typo generation (Property 14)
    - **Property 14: Typo generation produces adjacent QWERTY key**
    - **Validates: Requirements 5.4**
  - [x] 11.3 Write property test for typo frequency (Property 15)
    - **Property 15: Typo frequency approximates configured rate**
    - **Validates: Requirements 5.3**
  - [x] 11.4 Write property test for correction delay (Property 16)
    - **Property 16: Immediate correction delay is 1-3 characters**
    - **Validates: Requirements 5.6**
  - [x] 11.5 Write property test for estimated typing time (Property 18)
    - **Property 18: Estimated typing time accounts for all overhead**
    - **Validates: Requirements 5.15**

- [x] 12. Checkpoint — Core automation and property tests complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Update ConfigManager and SessionManager
  - [x] 13.1 Update `core/config_manager.py` to handle new config schema fields (typing, safety, navigation, ui, assets)
    - Remove browser/rate-limiter config handling
    - Add validation for new fields (e.g., confidence 0.0–1.0, countdown > 0)
    - _Requirements: 12.1–12.12_
  - [x] 13.2 Update `core/session_manager.py` with new state fields
    - Add `last_typed_block_index`, `deferred_typos`, `review_pass_completed`, `batch_articles`, `current_batch_index`
    - Serialize/deserialize DeferredTypo list for session persistence
    - _Requirements: 13.6, 10.1–10.5_
  - [x] 13.3 Write property test for config round-trip (Property 24)
    - **Property 24: Config save/load round-trip**
    - **Validates: Requirements 12.11, 12.12**

- [x] 14. Rework PyQt6 UI
  - [x] 14.1 Rework `ui/main_window.py` — MainWindow
    - Add Start Typing, Pause/Resume, Emergency Stop buttons
    - Add countdown display (3, 2, 1 before typing starts)
    - Add draft URL input field with validation
    - Add batch file selection support
    - Add always-on-top toggle (configurable)
    - Remove Playwright-specific controls (browser launch, cookie import, etc.)
    - Wire Emergency Stop button to `EmergencyStop.trigger()`
    - Wire Pause/Resume to `EmergencyStop.pause()`/`resume()`
    - Disable buttons when actions unavailable (e.g., Start when no file selected)
    - _Requirements: 14.1–14.10, 6.5, 6.8, 7.1_
  - [x] 14.2 Update `ui/file_selector.py` — multi-file selection for batch publishing
    - Add multi-file selection mode
    - Remember last directory across sessions
    - _Requirements: 1.2, 1.6, 1.7_
  - [x] 14.3 Update `ui/settings_dialog.py` — new settings fields
    - Add: typing speed, variation range, typo frequency, immediate/deferred ratio, emergency stop hotkey, countdown duration, Google account email, screen recognition confidence
    - Remove: browser/Playwright settings
    - _Requirements: 12.1–12.10_
  - [x] 14.4 Update `ui/progress_widget.py` — per-block progress and batch tracking
    - Show per-ContentBlock progress bar
    - Show estimated time remaining (accounting for typo overhead)
    - Show batch progress (Article N of M)
    - _Requirements: 14.8, 14.9, 10.3_
  - [x] 14.5 Write unit tests for UI components
    - Test button state management (enabled/disabled logic)
    - Test countdown display
    - Test draft URL validation in UI
    - Test multi-file selection
    - _Requirements: 14.1–14.10_

- [x] 15. Implement Draft URL Validation and Placeholder Listing
  - [x] 15.1 Add draft URL validation to `utils/validators.py`
    - Accept Medium draft/story URL patterns: `https://medium.com/p/<id>/edit`, `https://<publication>.medium.com/<slug>-<id>`
    - Reject non-matching URLs with descriptive error
    - _Requirements: 7.2, 7.3_
  - [x] 15.2 Add placeholder listing logic to completion notification
    - Scan typed ContentBlocks for `table_placeholder` and `image_placeholder` types
    - Display list of all placeholders for user to manually insert content
    - _Requirements: 8.1, 8.2, 8.3_
  - [x] 15.3 Add tag validation to `utils/validators.py`
    - Enforce max 5 tags, alphanumeric + hyphens + spaces only
    - _Requirements: 9.3, 9.4, 9.5_
  - [x] 15.4 Write property tests for validation (Properties 21, 22, 23)
    - **Property 21: Draft URL validation**
    - **Validates: Requirements 7.2**
    - **Property 22: Placeholder listing includes all placeholders**
    - **Validates: Requirements 8.2**
    - **Property 23: Tag validation enforces max 5 and valid characters**
    - **Validates: Requirements 9.1, 9.3, 9.4, 9.5**

- [x] 16. Checkpoint — UI and validation complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 17. Wire everything together — main application flow
  - [x] 17.1 Update `main.py` — application entry point
    - Initialize EmergencyStop, FocusWindowDetector, OS_Input_Controller, ScreenRecognition, NavigationStateMachine, DeferredTypoTracker, ContentTyper
    - Wire dependency injection chain per design architecture
    - Register `release_all_keys()` via `atexit` for abnormal exit safety
    - Set `pyautogui.FAILSAFE = True`
    - _Requirements: 6.1, 6.2, NFR-2.1_
  - [x] 17.2 Implement publishing workflow orchestration
    - File selection → parse → countdown → navigate to editor → type article → review pass → completion notification
    - Batch mode: sequential processing with pause between articles, user confirmation, skip on failure
    - Error handling: trigger emergency stop on unhandled exceptions, save typing progress, display error
    - _Requirements: 1.1–1.7, 8.1–8.4, 10.1–10.5, 13.1–13.7_
  - [x] 17.3 Remove obsolete Playwright/Selenium modules
    - Remove or archive: `automation/playwright_controller.py`, `automation/selenium_controller.py`, `automation/auth_handler.py`, `automation/browser_cookie_extractor.py`, `automation/rate_limiter.py`, `automation/medium_editor.py`
    - Remove `config/selectors.yaml` (CSS selectors no longer needed)
    - Clean up imports across codebase
    - _Requirements: Constraints (no browser automation libraries)_
  - [x] 17.4 Write integration tests for full typing flow
    - Test complete article typing with mocked OS input (verify key sequence order)
    - Test batch publishing flow (multiple articles, pause between, skip on failure)
    - Test error recovery (emergency stop mid-article, resume from last block)
    - _Requirements: 4.1–4.18, 10.1–10.5, 13.1–13.7_

- [x] 18. Final checkpoint — Full integration
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate the 24 universal correctness properties from the design document using `hypothesis`
- Unit tests validate specific examples, edge cases, and error conditions
- Reused modules (ArticleParser, MarkdownProcessor, ConfigManager, HumanTypingSimulator, Models, Logger, Exceptions) require no changes to core logic — only config schema updates and new exception types
- All OS-level input (pyautogui/pynput) is mocked in tests — no real keyboard/mouse events during testing
- Reference images at `medium_publisher/assets/medium/` (6 screenshots) are already in place

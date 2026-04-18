# Implementation Plan: Version Update Workflow

## Overview

Extend the Medium Keyboard Publisher with iterative version update capability. New components (`VersionDiffDetector`, `VersionUpdateTyper`, `UpdateResult`, `VersionFileInfo`) are built on top of existing infrastructure (`ChangeParser`, `MarkdownProcessor`, `ContentTyper`, `OS_Input_Controller`, `SessionManager`, `NavigationStateMachine`). The UI gains a "Version Update" group box with version selection, previous version picker, change instructions area, and apply changes button. A `VersionUpdateWorker` QThread runs the update workflow in the background. All code is Python 3.11+ with PyQt6 UI.

## Tasks

- [x] 1. Add new data models
  - [x] 1.1 Add `UpdateResult` and `VersionFileInfo` dataclasses to `core/models.py`
    - `UpdateResult`: success, total_instructions, applied_count, skipped_count, failed_count, applied_sections, skipped_sections, failed_sections
    - `VersionFileInfo`: path, version_number, article_name, filename
    - _Requirements: 2.6, 7.5, 10.2_

  - [ ]* 1.2 Write unit tests for `UpdateResult` and `VersionFileInfo`
    - Test result aggregation and summary formatting
    - Test VersionFileInfo construction from file paths
    - _Requirements: 2.6, 10.2_

- [x] 2. Implement VersionDiffDetector
  - [x] 2.1 Create `core/version_diff_detector.py` — VersionDiffDetector class
    - Inject `MarkdownProcessor` dependency
    - `detect_changes(old_file, new_file)` reads both files, calls `compare_versions()`, maps diff tuples to `ChangeInstruction` objects
    - `_diff_to_instruction()` maps: added → `ChangeAction.ADD`, modified → `ChangeAction.REPLACE`, deleted → `ChangeAction.DELETE`
    - `_sort_by_document_order()` sorts instructions by section position in document
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [ ]* 2.2 Write property test for diff detection and conversion (Property 2)
    - **Property 2: Diff detection and conversion correctness**
    - For any two markdown documents with named sections, verify added/modified/deleted classification and ChangeAction mapping
    - **Validates: Requirements 2.2, 2.3, 2.4, 2.5, 2.6**

  - [ ]* 2.3 Write unit tests for VersionDiffDetector
    - Test end-to-end diff with real markdown files (added, modified, deleted sections)
    - Test empty files, identical files, single-section files
    - Test document-order sorting
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 3. Implement VersionUpdateTyper
  - [x] 3.1 Create `automation/version_update_typer.py` — VersionUpdateTyper class
    - Inject `OS_Input_Controller`, `ContentTyper`, `ChangeParser`, `ConfigManager`
    - `apply_changes()` processes instructions in document order, returns `UpdateResult`
    - `_apply_single_change()` dispatches to `_handle_add`, `_handle_replace`, `_handle_delete`
    - `_find_section()` opens Ctrl+F, types search marker, closes dialog
    - `_select_and_delete()` selects char_count characters using Shift+Arrow, deletes
    - `_type_replacement()` delegates to `ContentTyper` with formatting
    - Skips instructions whose search marker is not found, logs warning
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

  - [ ]* 3.2 Write property test for document-order processing (Property 4)
    - **Property 4: Document-order processing invariant**
    - For any list of ChangeInstructions targeting distinct sections, verify processing in ascending document position order
    - **Validates: Requirements 4.5**

  - [ ]* 3.3 Write property test for formatting dispatch (Property 5)
    - **Property 5: Formatting dispatch correctness**
    - For any ContentBlock with recognized type, verify delegation to correct ContentTyper method
    - **Validates: Requirements 6.3**

  - [ ]* 3.4 Write unit tests for VersionUpdateTyper
    - Test Ctrl+F open/type/close sequence
    - Test select+delete character counting
    - Test skip on section not found
    - Test emergency stop handling during apply_changes
    - Test ADD, REPLACE, DELETE action handlers
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 4. Checkpoint — Core components complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Extend PublishingWorkflow with version update method
  - [x] 5.1 Add `execute_version_update()` method to `core/publishing_workflow.py`
    - Save session state (version, draft URL) via SessionManager
    - Navigate to draft URL via NavigationStateMachine
    - Delegate to `VersionUpdateTyper.apply_changes()`
    - Mark version complete in SessionManager
    - Return `UpdateResult` with applied/skipped/failed counts
    - Handle EmergencyStopError: release keys, save progress
    - Handle FocusLostError: pause workflow
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 8.1, 8.2, 8.3_

  - [x] 5.2 Create `VersionUpdateWorker` QThread in `core/publishing_workflow.py`
    - Signals: `status_update(str)`, `instruction_progress(int, int)`, `finished_signal(bool, str)`
    - `run()` calls `execute_version_update()` and emits signals
    - _Requirements: 7.1, 9.7_

  - [ ]* 5.3 Write unit tests for PublishingWorkflow.execute_version_update
    - Test full update orchestration with mocked dependencies
    - Test navigation failure handling
    - Test emergency stop mid-update saves progress
    - Test version completion marking in SessionManager
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_

- [x] 6. Checkpoint — Workflow orchestration complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Implement version file discovery and validation
  - [x] 7.1 Add version filename validation utility to `utils/validators.py`
    - Validate pattern `v{N}-{article-name}.md` where N is positive integer and article-name is non-empty kebab-case
    - Return parsed version number and article name on success
    - _Requirements: 1.2, 1.3_

  - [x] 7.2 Add `_auto_discover_versions()` and `_suggest_previous_version()` helper methods
    - These will be added to `ui/main_window.py` as part of the version update UI
    - `_auto_discover_versions()`: scan parent `versions/` directory for matching files, sort by version number ascending
    - `_suggest_previous_version()`: parse version number N from selected file, return path to `v{N-1}-{article-name}.md` if it exists
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [ ]* 7.3 Write property test for version filename validation (Property 1)
    - **Property 1: Version filename validation**
    - For any string, validator accepts iff it matches `v{N}-{article-name}.md` pattern
    - **Validates: Requirements 1.2**

  - [ ]* 7.4 Write property test for version file discovery and sorting (Property 8)
    - **Property 8: Version file discovery and sorting**
    - For any directory with mixed files, `_auto_discover_versions()` returns only matching files sorted by version number ascending
    - **Validates: Requirements 11.1, 11.2**

  - [ ]* 7.5 Write property test for previous version suggestion (Property 9)
    - **Property 9: Previous version suggestion**
    - For any selected file with version N > 1, suggest v{N-1} if it exists, else None
    - **Validates: Requirements 11.3, 11.4**

  - [ ]* 7.6 Write unit tests for version file discovery
    - Test discovery with mixed file types in directory
    - Test sorting with non-sequential version numbers
    - Test suggestion when previous version exists and when it doesn't
    - Test edge case: v1 selected (no previous version)
    - _Requirements: 1.2, 1.3, 11.1, 11.2, 11.3, 11.4_

- [x] 8. Checkpoint — Version discovery and validation complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Implement Version Update UI controls
  - [x] 9.1 Add `_build_version_update_group()` to `ui/main_window.py`
    - Version Selector: QComboBox with v1–v5 options
    - Previous Version Selector: QLineEdit + Browse button (file picker)
    - Change Instructions Area: QTextEdit for natural language instructions
    - Apply Changes button
    - Draft URL display from session state
    - Detected changes summary label
    - _Requirements: 1.1, 1.6, 1.7, 9.1, 9.2, 9.6, 9.8_

  - [x] 9.2 Implement `_on_version_changed()` show/hide logic
    - v1: hide version update controls, show standard typing workflow
    - v2+: show version update controls (previous version picker, change instructions area, Apply Changes button)
    - _Requirements: 1.4, 1.5, 9.3, 9.4_

  - [x] 9.3 Implement `_on_apply_changes()` handler
    - Validate inputs (either change instructions or previous version file provided)
    - If previous version file provided: call `VersionDiffDetector.detect_changes()`
    - If change instructions provided: call `ChangeParser.parse_instructions()`
    - Display detected/parsed changes for user confirmation
    - Start `VersionUpdateWorker` on confirmation
    - Show countdown before starting
    - Disable all input controls during workflow, show progress via ProgressWidget
    - _Requirements: 2.7, 3.1, 3.3, 3.4, 3.5, 7.1, 7.2, 9.5, 9.6, 9.7_

  - [x] 9.4 Implement session state restoration in UI
    - On launch, restore draft URL and version selector from SessionManager
    - Allow user to clear session via "New Session" action
    - _Requirements: 8.4, 8.5, 8.6_

  - [ ]* 9.5 Write property test for Apply Changes button enable logic (Property 7)
    - **Property 7: Apply Changes button enable logic**
    - Button enabled iff at least one of (has_change_instructions, has_previous_version_file) is True
    - **Validates: Requirements 9.5**

  - [ ]* 9.6 Write unit tests for Version Update UI
    - Test show/hide controls on version selection change
    - Test Apply Changes button enable/disable logic
    - Test auto-discovery integration when file selected
    - Test session state restoration populates UI fields
    - _Requirements: 1.1, 1.4, 1.5, 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 10. Checkpoint — UI complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Remaining property tests and session round-trip
  - [ ]* 11.1 Write property test for change instruction parsing (Property 3)
    - **Property 3: Change instruction parsing produces correct actions**
    - For any instruction string with recognized action keyword, verify correct ChangeAction and non-empty section identifier
    - **Validates: Requirements 3.2**

  - [ ]* 11.2 Write property test for session state round-trip (Property 6)
    - **Property 6: Session state persistence round-trip**
    - For any session state with version string, draft URL, and completed versions list, verify save/restore preserves all values
    - **Validates: Requirements 8.2, 8.3, 8.4**

- [x] 12. Integration and wiring
  - [x] 12.1 Wire VersionDiffDetector and VersionUpdateTyper into PublishingWorkflow
    - Inject new dependencies into PublishingWorkflow constructor
    - Ensure `execute_version_update()` creates and uses VersionDiffDetector and VersionUpdateTyper correctly
    - _Requirements: 7.1, 7.4_

  - [x] 12.2 Wire VersionUpdateWorker into MainWindow
    - Connect worker signals to UI slots (status, progress, completion)
    - Connect Apply Changes button to worker start
    - Handle worker completion: re-enable controls, show summary dialog
    - _Requirements: 7.1, 7.5, 9.7, 10.2_

  - [x] 12.3 Update `main.py` entry point with new dependency chain
    - Initialize VersionDiffDetector with MarkdownProcessor
    - Initialize VersionUpdateTyper with OS_Input_Controller, ContentTyper, ChangeParser, ConfigManager
    - Pass new dependencies to PublishingWorkflow
    - _Requirements: 7.1_

  - [ ]* 12.4 Write integration tests for end-to-end version update flow
    - Test full pipeline with mocked OS input: parse → detect → navigate → apply
    - Test both diff-based and manual instruction paths
    - Test session persistence across simulated restart
    - Test error recovery: skip failed instruction, continue with remaining
    - _Requirements: 7.1, 7.4, 7.5, 7.6, 10.1, 10.2, 10.3_

- [x] 13. Final checkpoint — Full integration
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate the 9 correctness properties from the design document using Hypothesis
- Unit tests validate specific examples, edge cases, and error conditions
- Reused modules (ChangeParser, MarkdownProcessor, ContentTyper, OS_Input_Controller, SessionManager, NavigationStateMachine, ConfigManager, EmergencyStop, FocusWindowDetector) require no changes
- All OS-level input (pyautogui) is mocked in tests — no real keyboard/mouse events during testing
- The design uses Python throughout, so all implementation tasks use Python 3.11+ with PyQt6

# Version Update Workflow — Requirements Document

## Introduction

This specification defines the requirements for adding iterative version update capability to the Medium Keyboard Publisher. The feature enables a content creator to update an existing Medium draft with a new version of an article by navigating to changed sections in the editor, selecting old content, deleting it, and typing replacement content with human-like behavior. Changes are detected either through manual change instructions parsed by the existing ChangeParser or through automatic diff-based comparison of two markdown version files using MarkdownProcessor.compare_versions(). The workflow supports repeated update cycles (v1 → v2 → v3 → v4, etc.) and integrates with the existing publishing pipeline, session management, and safety controls.

## Glossary

- **Version_File**: A markdown article file following the naming convention `v{N}-{article-name}.md` located in the article's `versions/` directory
- **Version_Update_Typer**: New component that orchestrates finding, selecting, deleting, and retyping changed sections in the Medium_Editor using OS-level keyboard automation
- **Change_Instruction**: A parsed directive produced by ChangeParser describing a single content modification (REPLACE, ADD, UPDATE, DELETE, INSERT_AFTER, INSERT_BEFORE) with section identifiers and search markers
- **Diff_Result**: A tuple of (change_type, section_identifier, new_content) produced by MarkdownProcessor.compare_versions() representing a detected difference between two Version_Files
- **Search_Marker**: A text string extracted from article content used with Ctrl+F to locate a specific section in the Medium_Editor
- **Version_Selector**: A UI dropdown control allowing the user to choose which version (v1–v5) to apply
- **Change_Instructions_Area**: A UI text area where the user describes what sections changed in natural language
- **Previous_Version_Selector**: A UI file picker for selecting the previous version file to enable automatic diff-based change detection
- **Draft_URL**: The Medium draft URL where the existing article lives, stored in session state across version updates
- **Update_Session**: A session context maintained by SessionManager that tracks the current version number, draft URL, and completed versions across multiple update cycles

## Requirements

### Requirement 1: Version File Selection and Validation

**User Story:** As a content creator, I want to select a specific version file from my article's versions directory, so that the publisher knows which version to apply to my existing draft.

#### Acceptance Criteria

1. THE MainWindow SHALL display a Version_Selector dropdown with options v1 through v5
2. WHEN the user selects a version number and a Markdown_File, THE Keyboard_Publisher SHALL validate that the selected file follows the naming convention `v{N}-{article-name}.md`
3. IF the selected file does not match the expected version naming convention, THEN THE Keyboard_Publisher SHALL display a warning but allow the user to proceed
4. WHEN the user selects version v1, THE Keyboard_Publisher SHALL treat the operation as a full article typing workflow using the existing PublishingWorkflow
5. WHEN the user selects version v2 or higher, THE Keyboard_Publisher SHALL enable the version update workflow requiring either change instructions or a previous version file for diff comparison
6. THE MainWindow SHALL display a Previous_Version_Selector file picker that allows the user to select the prior version file for automatic diff detection
7. THE MainWindow SHALL display a Change_Instructions_Area text input where the user can describe changes in natural language


### Requirement 2: Change Detection via Diff Comparison

**User Story:** As a content creator, I want the publisher to automatically detect what changed between two versions of my article, so that I do not have to manually describe every modification.

#### Acceptance Criteria

1. WHEN the user provides both a current Version_File and a previous Version_File, THE Keyboard_Publisher SHALL use MarkdownProcessor.compare_versions() to produce a list of Diff_Results
2. THE MarkdownProcessor.compare_versions() SHALL identify sections that were added, modified, or deleted by comparing section maps derived from ContentBlock headers
3. WHEN a section exists in the new version but not the previous version, THE Keyboard_Publisher SHALL classify the Diff_Result as "added" with the full new section content
4. WHEN a section exists in both versions but the content differs, THE Keyboard_Publisher SHALL classify the Diff_Result as "modified" with the updated section content
5. WHEN a section exists in the previous version but not the new version, THE Keyboard_Publisher SHALL classify the Diff_Result as "deleted"
6. WHEN diff comparison produces Diff_Results, THE Keyboard_Publisher SHALL convert each Diff_Result into a Change_Instruction compatible with the Version_Update_Typer
7. THE Keyboard_Publisher SHALL display the detected changes to the user for confirmation before applying them to the Medium_Editor

### Requirement 3: Change Detection via Manual Instructions

**User Story:** As a content creator, I want to describe changes in natural language, so that I can direct the publisher to update specific sections without needing the previous version file.

#### Acceptance Criteria

1. WHEN the user enters text in the Change_Instructions_Area, THE Keyboard_Publisher SHALL pass the text to ChangeParser.parse_instructions() to produce a list of Change_Instructions
2. THE ChangeParser SHALL parse instructions supporting REPLACE, ADD, UPDATE, DELETE, INSERT_AFTER, and INSERT_BEFORE actions with section identifiers
3. FOR EACH Change_Instruction, THE Keyboard_Publisher SHALL call ChangeParser.extract_search_markers() with the current article content to locate the target section in the markdown
4. IF a referenced section is not found in the article content, THEN THE Keyboard_Publisher SHALL display a warning identifying the unmatched section and allow the user to revise the instructions
5. THE Keyboard_Publisher SHALL allow the user to use either diff-based detection or manual instructions, but not require both simultaneously


### Requirement 4: Navigate to Sections in Medium Editor

**User Story:** As a content creator, I want the publisher to navigate to the correct section in my Medium draft, so that changes are applied at the right location.

#### Acceptance Criteria

1. WHEN applying a Change_Instruction, THE Version_Update_Typer SHALL open the browser's find dialog using Ctrl+F
2. THE Version_Update_Typer SHALL type the Search_Marker text into the find dialog to locate the target section in the Medium_Editor
3. WHEN the find dialog locates the Search_Marker, THE Version_Update_Typer SHALL close the find dialog using Escape and position the cursor at the found location
4. IF the Search_Marker is not found in the Medium_Editor after searching, THEN THE Version_Update_Typer SHALL log a warning, skip the current Change_Instruction, and proceed to the next one
5. THE Version_Update_Typer SHALL process Change_Instructions in document order (top to bottom) to avoid cursor position drift from earlier modifications

### Requirement 5: Select and Delete Old Content

**User Story:** As a content creator, I want the publisher to select and remove the old content at the target section, so that it can be replaced with the updated version.

#### Acceptance Criteria

1. WHEN a REPLACE or UPDATE Change_Instruction targets a section, THE Version_Update_Typer SHALL select the old section content using Shift+Arrow key combinations via OS_Input_Controller.select_text_backwards()
2. WHEN old content is selected, THE Version_Update_Typer SHALL delete the selected content using the Delete or Backspace key via OS_Input_Controller.press_key()
3. THE Version_Update_Typer SHALL calculate the character count of the old section content to determine how many characters to select for deletion
4. WHEN a DELETE Change_Instruction targets a section, THE Version_Update_Typer SHALL select and delete the section content including its header without typing replacement content
5. IF the calculated selection length does not match the expected old content length, THEN THE Version_Update_Typer SHALL log a warning and proceed with the best-effort deletion

### Requirement 6: Type Replacement Content

**User Story:** As a content creator, I want the publisher to type the new content at the deletion point with human-like behavior, so that the update appears natural.

#### Acceptance Criteria

1. WHEN old content has been deleted for a REPLACE or UPDATE instruction, THE Version_Update_Typer SHALL type the new content at the current cursor position using ContentTyper
2. THE Version_Update_Typer SHALL type replacement content with the same human-like typing behavior as the initial article typing, including variable speed, typo simulation, and formatting shortcuts
3. WHEN the new content contains markdown formatting (headers, bold, italic, code, links, lists), THE Version_Update_Typer SHALL apply the corresponding Medium formatting shortcuts through ContentTyper
4. WHEN an ADD or INSERT_AFTER instruction is processed, THE Version_Update_Typer SHALL position the cursor after the referenced section and type the new content
5. WHEN an INSERT_BEFORE instruction is processed, THE Version_Update_Typer SHALL position the cursor before the referenced section and type the new content
6. THE Version_Update_Typer SHALL preserve all unchanged sections in the Medium_Editor by only modifying targeted sections


### Requirement 7: Version Update Workflow Orchestration

**User Story:** As a content creator, I want the version update process to be orchestrated end-to-end, so that I can apply all changes to my draft in a single automated session.

#### Acceptance Criteria

1. WHEN the user clicks "Apply Changes", THE Keyboard_Publisher SHALL execute the version update workflow: navigate to draft URL → process each Change_Instruction sequentially → report completion
2. THE Keyboard_Publisher SHALL display a countdown (3, 2, 1) before starting the version update, consistent with the existing typing workflow
3. WHEN navigating to the draft, THE Keyboard_Publisher SHALL open the stored Draft_URL in the browser and wait for the Medium_Editor to be ready using the existing NavigationStateMachine
4. FOR EACH Change_Instruction, THE Keyboard_Publisher SHALL execute the sequence: find section → select old content → delete → type new content → proceed to next
5. WHEN all Change_Instructions have been processed, THE Keyboard_Publisher SHALL display a completion notification listing the changes applied and any skipped instructions
6. IF an error occurs during a Change_Instruction, THEN THE Keyboard_Publisher SHALL log the error, skip the failed instruction, and continue with the remaining instructions
7. IF the Emergency_Stop is triggered during the version update, THEN THE Keyboard_Publisher SHALL immediately halt all input, release held keys, and save the current progress to SessionManager

### Requirement 8: Session State for Version Tracking

**User Story:** As a content creator, I want the publisher to remember my draft URL and current version across update cycles, so that I can apply v2, v3, v4 updates without re-entering information.

#### Acceptance Criteria

1. WHEN version v1 typing completes, THE SessionManager SHALL store the Draft_URL provided by the user for subsequent version updates
2. THE SessionManager SHALL track the current_version identifier (e.g., "v1", "v2") and update it when a version update completes
3. WHEN a version update completes, THE SessionManager SHALL add the completed version to the versions_completed list via mark_version_complete()
4. THE SessionManager SHALL persist the Update_Session state (draft URL, current version, completed versions) to disk so it survives application restarts
5. WHEN the user launches the application with an existing Update_Session, THE Keyboard_Publisher SHALL restore the session state and pre-populate the Draft_URL and Version_Selector with the last known values
6. THE Keyboard_Publisher SHALL allow the user to clear the Update_Session and start fresh via a "New Session" action

### Requirement 9: UI Controls for Version Update Workflow

**User Story:** As a content creator, I want dedicated UI controls for the version update workflow, so that I can easily manage iterative article refinements.

#### Acceptance Criteria

1. THE MainWindow SHALL display a "Version Update" group box containing the Version_Selector, Previous_Version_Selector, Change_Instructions_Area, and an "Apply Changes" button
2. THE Version_Selector SHALL be a dropdown with options: v1, v2, v3, v4, v5
3. WHEN the user selects v1 in the Version_Selector, THE MainWindow SHALL hide the version update controls and show only the standard typing workflow controls
4. WHEN the user selects v2 or higher in the Version_Selector, THE MainWindow SHALL show the version update controls (Previous_Version_Selector, Change_Instructions_Area, Apply Changes button)
5. THE "Apply Changes" button SHALL be enabled only when the user has provided either change instructions text or selected a previous version file for diff comparison
6. THE MainWindow SHALL display a summary of detected or parsed changes before the user confirms the update
7. WHEN the version update workflow is running, THE MainWindow SHALL disable all input controls and display progress through the ProgressWidget
8. THE MainWindow SHALL display the current Draft_URL from the session state, and allow the user to edit it before applying changes


### Requirement 10: Version Update Error Handling and Recovery

**User Story:** As a content creator, I want errors during version updates handled gracefully, so that a failed update does not corrupt my existing draft.

#### Acceptance Criteria

1. IF a Change_Instruction fails to locate its target section in the Medium_Editor, THEN THE Version_Update_Typer SHALL skip that instruction, log the failure, and continue with the next instruction
2. WHEN the version update workflow completes (with or without skipped instructions), THE Keyboard_Publisher SHALL display a summary showing: instructions applied, instructions skipped, and reasons for skips
3. IF the application crashes or Emergency_Stop is triggered during a version update, THEN THE SessionManager SHALL persist the index of the last successfully applied Change_Instruction for manual recovery
4. THE Keyboard_Publisher SHALL log each Change_Instruction execution (start, success, skip, failure) with sufficient detail for debugging
5. IF the Focus_Window changes during the version update, THEN THE Keyboard_Publisher SHALL pause the update and notify the user to refocus the Medium_Editor, consistent with the existing safety behavior

### Requirement 11: Article Version Directory Discovery

**User Story:** As a content creator, I want the publisher to understand my article directory structure, so that it can find version files automatically.

#### Acceptance Criteria

1. WHEN the user selects a Version_File, THE Keyboard_Publisher SHALL detect the parent `versions/` directory and list all available version files matching the pattern `v{N}-{article-name}.md`
2. THE Keyboard_Publisher SHALL sort discovered version files by version number in ascending order (v1, v2, v3, v4)
3. WHEN the user selects a version v{N} file, THE Keyboard_Publisher SHALL automatically suggest v{N-1} as the previous version file in the Previous_Version_Selector
4. IF the expected previous version file does not exist in the versions directory, THEN THE Keyboard_Publisher SHALL leave the Previous_Version_Selector empty and require the user to provide change instructions manually


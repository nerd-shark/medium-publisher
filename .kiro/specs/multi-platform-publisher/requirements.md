# Multi-Platform Article Publisher - Requirements

## Introduction

This specification extends the Medium Article Publisher to support multiple publishing platforms (Medium and Substack) through a unified interface. The application will use a platform abstraction layer to enable publishing to different platforms while maintaining a consistent user experience.

## Glossary

- **Platform**: A publishing service (Medium, Substack, etc.)
- **Platform Interface**: Abstract interface defining common publishing operations
- **Platform Implementation**: Concrete implementation for a specific platform
- **Platform Selector**: UI component for choosing target platform
- **Platform Configuration**: Platform-specific settings and credentials
- **Multi-Platform Session**: Publishing session that may target different platforms

## User Stories

### US-MP-1: Select Publishing Platform

**As a** content creator  
**I want to** select which platform to publish to (Medium or Substack)  
**So that** I can publish the same content to different audiences

**Acceptance Criteria**:

**THE** system **SHALL** provide a platform selector dropdown in the UI

**THE** system **SHALL** support "Medium" and "Substack" as platform options

**WHEN** the user selects a platform, **THE** system **SHALL** update the UI to show platform-specific options

**THE** system **SHALL** remember the last selected platform across sessions

**THE** system **SHALL** validate that the selected platform is configured before publishing

**WHERE** a platform is not configured, **THE** system **SHALL** prompt the user to configure it

### US-MP-2: Configure Platform-Specific Settings

**As a** content creator  
**I want to** configure settings for each platform independently  
**So that** I can customize behavior per platform

**Acceptance Criteria**:

**THE** system **SHALL** provide separate configuration sections for each platform

**THE** system **SHALL** allow configuration of platform-specific authentication methods

**THE** system **SHALL** allow configuration of platform-specific publishing options

**THE** system **SHALL** save platform configurations independently

**THE** system **SHALL** validate platform configurations before use

### US-MP-3: Authenticate with Multiple Platforms

**As a** content creator  
**I want to** authenticate with both Medium and Substack  
**So that** I can publish to either platform without re-authenticating

**Acceptance Criteria**:

**THE** system **SHALL** support authentication for Medium (email/password + Google OAuth)

**THE** system **SHALL** support authentication for Substack (email/password)

**THE** system **SHALL** store session cookies separately for each platform

**THE** system **SHALL** allow simultaneous authentication to multiple platforms

**THE** system **SHALL** restore sessions independently for each platform

**WHERE** a session expires, **THE** system **SHALL** prompt re-authentication for that platform only

### US-MP-4: Publish to Selected Platform

**As a** content creator  
**I want to** publish articles to my selected platform  
**So that** I can reach my audience on that platform

**Acceptance Criteria**:

**WHEN** the user clicks "Publish", **THE** system **SHALL** publish to the selected platform

**THE** system **SHALL** use platform-specific publishing workflow

**THE** system **SHALL** apply platform-specific formatting rules

**THE** system **SHALL** handle platform-specific metadata (tags for Medium, categories for Substack)

**THE** system **SHALL** provide platform-specific progress updates

**THE** system **SHALL** return platform-specific draft URLs

### US-MP-5: Switch Between Platforms

**As a** content creator  
**I want to** switch between platforms without restarting the application  
**So that** I can publish the same article to multiple platforms

**Acceptance Criteria**:

**THE** system **SHALL** allow changing the selected platform at any time

**WHEN** the platform is changed, **THE** system **SHALL** update the UI immediately

**THE** system **SHALL** preserve article selection when switching platforms

**THE** system **SHALL** clear platform-specific state (draft URL) when switching

**THE** system **SHALL** validate authentication for the new platform

### US-MP-6: Platform-Specific Draft URLs

**As a** content creator  
**I want to** provide draft URLs specific to each platform  
**So that** I can update existing drafts on the correct platform

**Acceptance Criteria**:

**THE** system **SHALL** validate draft URLs match the selected platform

**WHERE** a Medium draft URL is provided and Substack is selected, **THE** system **SHALL** display an error

**WHERE** a Substack draft URL is provided and Medium is selected, **THE** system **SHALL** display an error

**THE** system **SHALL** remember the last draft URL per platform

**THE** system **SHALL** clear draft URL when switching platforms

### US-MP-7: Platform-Specific Error Handling

**As a** content creator  
**I want to** receive platform-specific error messages  
**So that** I can troubleshoot issues effectively

**Acceptance Criteria**:

**WHERE** a platform-specific error occurs, **THE** system **SHALL** display the platform name in the error message

**THE** system **SHALL** provide platform-specific troubleshooting guidance

**THE** system **SHALL** log platform-specific errors separately

**THE** system **SHALL** allow retry with the same platform

**THE** system **SHALL** allow switching to a different platform after error

## Platform-Specific Requirements

### Medium Platform

**THE** system **SHALL** support Medium's rich text editor via browser automation

**THE** system **SHALL** support Medium authentication (email/password + Google OAuth)

**THE** system **SHALL** support Medium's tag system (max 5 tags)

**THE** system **SHALL** support Medium's subtitle field

**THE** system **SHALL** support Medium's draft/public publishing modes

**THE** system **SHALL** use Medium-specific CSS selectors

**THE** system **SHALL** apply Medium-specific keyboard shortcuts

### Substack Platform

**THE** system **SHALL** support Substack's editor via browser automation

**THE** system **SHALL** support Substack authentication (email/password)

**THE** system **SHALL** support Substack's category system

**THE** system **SHALL** support Substack's custom domain URLs

**THE** system **SHALL** support Substack's draft/send publishing modes

**THE** system **SHALL** use Substack-specific CSS selectors

**THE** system **SHALL** apply Substack-specific keyboard shortcuts

## Non-Functional Requirements

### NFR-MP-1: Extensibility

**THE** system **SHALL** use a platform abstraction layer for easy addition of new platforms

**THE** system **SHALL** isolate platform-specific code in separate modules

**THE** system **SHALL** define a clear platform interface contract

**THE** system **SHALL** allow adding new platforms without modifying core logic

### NFR-MP-2: Maintainability

**THE** system **SHALL** separate platform-specific configuration from core configuration

**THE** system **SHALL** use platform-specific selector files

**THE** system **SHALL** provide platform-specific logging

**THE** system **SHALL** document platform-specific requirements

### NFR-MP-3: Performance

**THE** system **SHALL** maintain the same performance characteristics per platform

**THE** system **SHALL** not degrade performance when multiple platforms are configured

**THE** system **SHALL** load platform implementations on-demand

### NFR-MP-4: Reliability

**THE** system **SHALL** handle platform-specific failures independently

**THE** system **SHALL** not affect other platforms when one platform fails

**THE** system **SHALL** maintain separate session state per platform

## Constraints

- Must maintain backward compatibility with existing Medium-only functionality
- Must support Windows 10/11
- Requires Python 3.11+
- Requires Chromium browser (installed by Playwright)
- Requires internet connection for platform access
- Limited by each platform's rate limits and terms of service

## Assumptions

- User has valid accounts on platforms they wish to use
- User's markdown files follow consistent frontmatter format
- Platform editor structures remain relatively stable
- User has permission to automate their own accounts

## Dependencies

- Playwright (browser automation)
- PyQt6 (desktop UI)
- markdown2 or mistune (markdown parsing)
- python-dotenv (configuration management)
- keyring (secure credential storage)
- Existing Medium Article Publisher codebase

## Success Criteria

- User can publish to both Medium and Substack from the same application
- User can switch between platforms without restarting
- Platform-specific features work correctly (tags, categories, etc.)
- Application maintains separate authentication for each platform
- Code is extensible for adding future platforms
- Existing Medium functionality continues to work without regression

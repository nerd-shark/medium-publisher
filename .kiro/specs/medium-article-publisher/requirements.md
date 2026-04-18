# Medium Article Publisher - Requirements

## Introduction

This specification defines the requirements for a desktop application that automates publishing markdown articles to Medium. The application will read markdown files from the local filesystem, parse their content and metadata, and use browser automation to type the content into Medium's editor with proper formatting.

## Glossary

- **Markdown File**: Source article file in markdown format with YAML frontmatter
- **Medium Editor**: Medium's web-based rich text editor for creating articles
- **Browser Automation**: Programmatic control of a web browser to interact with web pages
- **Playwright**: Browser automation library for controlling Chromium, Firefox, and WebKit
- **Frontmatter**: YAML metadata at the beginning of markdown files (title, subtitle, tags, etc.)
- **Article Template**: Predefined structure for different article types (technical, tutorial, opinion)
- **Publishing Session**: Single execution of the application to publish one or more articles
- **Draft Mode**: Publishing article as draft (not public) for review
- **Public Mode**: Publishing article as public (immediately visible)
- **OAuth**: Open Authorization protocol for secure authentication via third-party providers
- **Google OAuth**: Authentication method using Google account credentials
- **Session Cookies**: Browser cookies that maintain authenticated session state

## User Stories

### US-1: Select Markdown File for Publishing

**As a** content creator  
**I want to** select a markdown file from my filesystem  
**So that** I can publish it to Medium

**Acceptance Criteria**:

**WHEN** the user launches the application, **THE** system **SHALL** display a file selection dialog

**WHEN** the user selects a markdown file, **THE** system **SHALL** validate the file has .md extension

**WHEN** the user selects a valid markdown file, **THE** system **SHALL** parse the frontmatter and display article metadata (title, subtitle, tags)

**IF** the selected file is not a valid markdown file, **THEN THE** system **SHALL** display an error message and allow reselection

**THE** system **SHALL** remember the last selected directory for convenience

**THE** system **SHALL** provide an optional field for Medium draft URL

**WHERE** a draft URL is provided, **THE** system **SHALL** navigate to that draft instead of creating a new story

**WHERE** no draft URL is provided, **THE** system **SHALL** create a new story on Medium

### US-2: Authenticate with Medium

**As a** content creator  
**I want to** authenticate with my Medium account  
**So that** I can publish articles under my account

**Acceptance Criteria**:

**THE** system **SHALL** provide a login interface for Medium credentials

**WHEN** the user enters email and password, **THE** system **SHALL** authenticate with Medium using browser automation

**WHEN** authentication succeeds, **THE** system **SHALL** store session cookies for reuse

**IF** authentication fails, **THEN THE** system **SHALL** display an error message and allow retry

**THE** system **SHALL** support "Remember Me" functionality to persist login across sessions

**WHERE** the user has two-factor authentication enabled, **THE** system **SHALL** pause and allow manual 2FA entry

### US-2A: Authenticate with Medium via Google OAuth

**As a** content creator with Google-linked Medium account  
**I want to** authenticate using my Google account  
**So that** I can publish articles without managing separate Medium credentials

**Acceptance Criteria**:

**THE** system **SHALL** detect and support Google OAuth login on Medium

**WHEN** the user clicks "Login" button, **THE** system **SHALL** open Medium login page in visible browser

**THE** system **SHALL** display instructions to user: "Click 'Sign in with Google' and complete authentication"

**THE** system **SHALL** wait for user to complete Google OAuth flow manually

**WHERE** user has Google 2FA enabled, **THE** system **SHALL** allow user to complete 2FA in browser

**WHERE** user has security keys enabled, **THE** system **SHALL** allow user to use security keys

**WHEN** OAuth flow completes successfully, **THE** system **SHALL** detect successful login

**WHEN** login is detected, **THE** system **SHALL** save session cookies securely

**THE** system **SHALL** restore session from saved cookies on subsequent launches

**THE** system **SHALL** support both traditional email/password and Google OAuth methods

**THE** system **SHALL** not store Google credentials (user authenticates directly with Google)

**IF** session cookies expire, **THEN THE** system **SHALL** prompt user to re-authenticate

### US-3: Parse Markdown Content

**As a** content creator  
**I want to** have my markdown content parsed correctly  
**So that** formatting is preserved when published to Medium

**Acceptance Criteria**:

**THE** system **SHALL** parse YAML frontmatter to extract metadata (title, subtitle, tags, keywords)

**THE** system **SHALL** parse markdown headers (##, ###) and convert to Medium heading formats

**THE** system **SHALL** parse bold text (**text**) and convert to Medium bold formatting

**THE** system **SHALL** parse italic text (*text*) and convert to Medium italic formatting

**THE** system **SHALL** parse code blocks (```language```) and convert to Medium code blocks

**THE** system **SHALL** parse inline code (`code`) and convert to Medium inline code

**THE** system **SHALL** parse links ([text](url)) and convert to Medium links

**THE** system **SHALL** parse bullet lists and convert to Medium bullet lists

**THE** system **SHALL** parse numbered lists and convert to Medium numbered lists

**THE** system **SHALL** preserve paragraph breaks (double newlines)

**WHEN** markdown tables are detected, **THE** system **SHALL** insert a "TODO: Insert table here" placeholder

**WHEN** markdown images are detected, **THE** system **SHALL** insert a "TODO: Insert image here - [alt text]" placeholder

### US-4: Type Content into Medium Editor

**As a** content creator  
**I want to** have my article content typed into Medium's editor automatically  
**So that** I don't have to manually copy-paste and format

**Acceptance Criteria**:

**WHERE** no draft URL is provided, **THE** system **SHALL** navigate to Medium's new story page

**WHERE** a draft URL is provided, **THE** system **SHALL** navigate to the specified draft URL

**THE** system **SHALL** validate the draft URL is a valid Medium draft or story URL

**THE** system **SHALL** clear existing content in the editor before typing (if draft URL provided)

**THE** system **SHALL** type the article title into the title field

**THE** system **SHALL** type the article content paragraph by paragraph with appropriate delays

**WHEN** typing headers, **THE** system **SHALL** apply Medium's heading format using keyboard shortcuts

**WHEN** typing bold text, **THE** system **SHALL** apply Medium's bold format using keyboard shortcuts

**WHEN** typing code blocks, **THE** system **SHALL** apply Medium's code block format

**THE** system **SHALL** simulate human-like typing with configurable delays between keystrokes

**WHERE** human-like typing is enabled, **THE** system **SHALL** introduce realistic typos during typing

**WHERE** human-like typing is enabled, **THE** system **SHALL** correct typos using backspace after 1-3 additional characters

**THE** system **SHALL** vary typing speed randomly within configured range

**THE** system **SHALL** add occasional pauses (100-500ms) to simulate thinking

**THE** system **SHALL** handle special characters and unicode correctly

### US-5: Preview Before Publishing

**As a** content creator  
**I want to** preview the article in Medium's editor before publishing  
**So that** I can verify formatting is correct and manually insert tables/images

**Acceptance Criteria**:

**WHEN** content typing is complete, **THE** system **SHALL** pause and display a preview notification

**THE** system **SHALL** keep the browser window visible for manual review

**WHERE** TODO placeholders exist, **THE** system **SHALL** notify user to manually insert tables/images

**THE** system **SHALL** provide options to: publish as draft, publish as public, or cancel

**WHEN** the user selects "publish as draft", **THE** system **SHALL** click Medium's "Publish" button and select "Draft"

**WHEN** the user selects "publish as public", **THE** system **SHALL** click Medium's "Publish" button and select "Public"

**WHEN** the user selects "cancel", **THE** system **SHALL** close the browser without publishing

### US-6: Add Article Metadata

**As a** content creator  
**I want to** have article metadata (tags, subtitle) added automatically  
**So that** my articles are properly categorized

**Acceptance Criteria**:

**WHEN** publishing, **THE** system **SHALL** add tags from frontmatter to Medium's tag field

**THE** system **SHALL** add subtitle from frontmatter to Medium's subtitle field

**THE** system **SHALL** support up to 5 tags (Medium's limit)

**IF** more than 5 tags are provided, **THEN THE** system **SHALL** use the first 5 tags

**THE** system **SHALL** validate tags are alphanumeric with hyphens/spaces only

### US-7: Handle Errors Gracefully

**As a** content creator  
**I want to** have errors handled gracefully  
**So that** I don't lose work if something goes wrong

**Acceptance Criteria**:

**IF** Medium's page structure changes, **THEN THE** system **SHALL** display an error message with details

**IF** network connection is lost, **THEN THE** system **SHALL** pause and wait for reconnection

**IF** browser crashes, **THEN THE** system **SHALL** log the error and allow retry

**THE** system **SHALL** save progress (typed content) before each major operation

**THE** system **SHALL** provide a log file for debugging issues

### US-8: Configure Application Settings

**As a** content creator  
**I want to** configure application settings  
**So that** I can customize behavior to my preferences

**Acceptance Criteria**:

**THE** system **SHALL** provide a settings interface for configuration

**THE** system **SHALL** allow configuration of typing speed (delay between keystrokes)

**THE** system **SHALL** enforce rate limit of 35 characters per minute (non-configurable)

**THE** system **SHALL** display rate limit warning in settings

**THE** system **SHALL** allow configuration of human-like typing simulation (typos enabled/disabled)

**THE** system **SHALL** allow configuration of typo frequency (low/medium/high)

**THE** system **SHALL** allow configuration of default publish mode (draft vs public)

**THE** system **SHALL** allow configuration of browser visibility (headless vs visible)

**THE** system **SHALL** allow configuration of default article directory

**THE** system **SHALL** save settings to a configuration file

### US-9: Batch Publish Multiple Articles

**As a** content creator  
**I want to** publish multiple articles in one session  
**So that** I can efficiently publish a series of articles

**Acceptance Criteria**:

**THE** system **SHALL** allow selection of multiple markdown files

**WHEN** multiple files are selected, **THE** system **SHALL** publish them sequentially

**THE** system **SHALL** display progress for each article (1 of 3, 2 of 3, etc.)

**IF** one article fails, **THEN THE** system **SHALL** continue with remaining articles

**THE** system **SHALL** provide a summary report of successful and failed publications

### US-11: Iterative Version Updates

**As a** content creator  
**I want to** update an article through multiple versions incrementally  
**So that** I can refine content without retyping the entire article

**Acceptance Criteria**:

**WHEN** publishing version 1, **THE** system **SHALL** type the complete article content

**WHEN** version 1 is complete, **THE** system **SHALL** pause and wait for user instructions

**THE** system **SHALL** provide an interface for user to describe changes for next version

**WHEN** user provides change instructions, **THE** system **SHALL** parse the instructions

**THE** system **SHALL** identify sections to modify based on instructions

**THE** system **SHALL** navigate to the specified sections in the editor

**THE** system **SHALL** select and delete old content

**THE** system **SHALL** type new content with human-like behavior

**THE** system **SHALL** preserve unchanged sections

**THE** system **SHALL** support multiple iteration cycles (v1 → v2 → v3 → etc.)

**THE** system **SHALL** maintain context of current version number

**WHEN** all versions are complete, **THE** system **SHALL** allow final publishing

**As a** content creator  
**I want to** have a user-friendly desktop interface  
**So that** I can easily use the application

**Acceptance Criteria**:

**THE** system **SHALL** provide a native desktop window (not web-based)

**THE** system **SHALL** display application status (idle, authenticating, publishing, complete)

**THE** system **SHALL** display a log of operations for transparency

**THE** system **SHALL** provide clear buttons for main actions (Select File, Login, Publish)

**THE** system **SHALL** disable buttons when actions are not available

**THE** system **SHALL** provide keyboard shortcuts for common actions

**THE** system **SHALL** remember window size and position across sessions

## Non-Functional Requirements

### NFR-1: Performance

**THE** system **SHALL** type content at a configurable speed (default 30-50ms per character)

**THE** system **SHALL** vary typing speed randomly (±20%) to simulate human typing

**THE** system **SHALL** enforce a rate limit of maximum 35 characters per minute

**THE** system **SHALL** calculate and display estimated typing time before publishing (accounting for typos and corrections)

**THE** system **SHALL** complete authentication within 30 seconds

**THE** system **SHALL** handle articles up to 50,000 words

### NFR-2: Reliability

**THE** system **SHALL** have error handling for all network operations

**THE** system **SHALL** retry failed operations up to 3 times

**THE** system **SHALL** maintain session state across application restarts

### NFR-3: Usability

**THE** system **SHALL** provide clear error messages with actionable guidance

**THE** system **SHALL** provide progress indicators for long-running operations

**THE** system **SHALL** follow platform UI conventions (Windows)

### NFR-4: Security

**THE** system **SHALL** store credentials securely using OS keychain

**THE** system **SHALL** not log passwords or sensitive data

**THE** system **SHALL** clear session data on logout

### NFR-5: Maintainability

**THE** system **SHALL** use modular architecture for easy updates

**THE** system **SHALL** separate UI logic from automation logic

**THE** system **SHALL** provide comprehensive logging for debugging

## Constraints

- Must run on Windows 10/11
- Requires Python 3.11+
- Requires Chromium browser (installed by Playwright)
- Requires internet connection for Medium access
- Limited by Medium's rate limits and terms of service

## Assumptions

- User has valid Medium account
- User's markdown files follow consistent frontmatter format
- Medium's editor structure remains relatively stable
- User has permission to automate their own account

## Dependencies

- Playwright (browser automation)
- PyQt6 (desktop UI)
- markdown2 or mistune (markdown parsing)
- python-dotenv (configuration management)
- keyring (secure credential storage)

## Success Criteria

- User can publish a markdown article to Medium in under 2 minutes
- Application handles 95% of markdown formatting correctly
- Application provides clear feedback for all operations
- Application recovers gracefully from common errors
- User satisfaction with automation vs manual process

# Testing Checklist for Packaged Application

This checklist ensures the packaged Medium Article Publisher application works correctly on clean Windows machines.

## Pre-Testing Setup

### Test Environment

- [ ] Windows 10 or Windows 11
- [ ] No Python installed
- [ ] No development tools installed
- [ ] Fresh Windows installation or VM
- [ ] Internet connection available
- [ ] At least 1GB free disk space

### Test Files

- [ ] Sample markdown files prepared
- [ ] Test Medium account credentials
- [ ] Google account for OAuth testing (if applicable)

## Installation Testing

### Standalone Executable

- [ ] Copy `dist\` directory to test machine
- [ ] Verify all files present
- [ ] Check file sizes are reasonable
- [ ] No missing DLLs or dependencies

### Installer Testing

- [ ] Run installer as administrator
- [ ] Verify installation directory created
- [ ] Check Start menu shortcuts created
- [ ] Verify desktop shortcut (if selected)
- [ ] Check configuration files copied
- [ ] Verify documentation included

## Application Launch

### First Launch

- [ ] Application starts without errors
- [ ] No console window appears (GUI mode)
- [ ] Main window displays correctly
- [ ] All UI elements visible
- [ ] No missing icons or images
- [ ] Status bar shows "Ready"

### Configuration

- [ ] Default configuration loads
- [ ] Settings dialog opens
- [ ] All settings display correctly
- [ ] Settings can be modified
- [ ] Settings persist after restart

## Playwright Setup

### Browser Installation

- [ ] Run `setup_playwright.cmd`
- [ ] Chromium downloads successfully
- [ ] Installation completes without errors
- [ ] Browser files created in correct location
- [ ] No permission errors

### Browser Verification

- [ ] Application can launch browser
- [ ] Browser window appears
- [ ] Navigation works
- [ ] No browser errors in logs

## Core Functionality

### File Selection

- [ ] File selection dialog opens
- [ ] Can browse directories
- [ ] Can select .md files
- [ ] Invalid files rejected
- [ ] Selected file path displays
- [ ] Last directory remembered

### Article Parsing

- [ ] Markdown file parses correctly
- [ ] Frontmatter extracted
- [ ] Title displays
- [ ] Subtitle displays
- [ ] Tags display
- [ ] Character count accurate
- [ ] Estimated time calculated

### Authentication

#### Email/Password Login

- [ ] Login dialog appears
- [ ] Can enter credentials
- [ ] Login succeeds with valid credentials
- [ ] Login fails with invalid credentials
- [ ] Error messages display
- [ ] Session cookies saved
- [ ] Remember me works
- [ ] Can logout

#### Google OAuth Login

- [ ] OAuth flow initiates
- [ ] Browser opens to Google login
- [ ] Can complete Google authentication
- [ ] 2FA works (if enabled)
- [ ] Security keys work (if enabled)
- [ ] Login detected successfully
- [ ] Session cookies saved
- [ ] Session restored on restart

### Publishing Workflow

#### Single Article

- [ ] Publish button enabled after file selection
- [ ] Confirmation dialog shows estimated time
- [ ] Progress bar updates
- [ ] Status messages display
- [ ] Browser navigates to Medium
- [ ] Title typed correctly
- [ ] Content typed with formatting
- [ ] Bold formatting applied
- [ ] Italic formatting applied
- [ ] Headers applied (H2, H3)
- [ ] Code blocks inserted
- [ ] Links inserted
- [ ] Placeholders for tables/images
- [ ] Tags added
- [ ] Subtitle added
- [ ] Preview pause works
- [ ] Can publish as draft
- [ ] Can publish as public
- [ ] Success message displays
- [ ] Draft URL shown

#### Version Updates

- [ ] Version selector displays (v1-v5)
- [ ] Change instructions input works
- [ ] Can apply version changes
- [ ] Sections identified correctly
- [ ] Content replaced correctly
- [ ] New content added correctly
- [ ] Deleted content removed
- [ ] Multiple versions work (v1 → v2 → v3)
- [ ] Session maintained across versions

#### Batch Publishing

- [ ] Can select multiple files
- [ ] Batch info displays
- [ ] Total time estimated
- [ ] Confirmation shows all files
- [ ] Articles publish sequentially
- [ ] Progress shows current article
- [ ] Continue on error works
- [ ] Summary report displays
- [ ] Success/failure counts correct

### Rate Limiting

- [ ] Typing speed configurable
- [ ] Rate limit enforced (35 chars/min)
- [ ] Time estimates accurate
- [ ] No rate limit errors
- [ ] Sliding window works correctly

### Human Typing Simulation

- [ ] Typos generated (if enabled)
- [ ] Typos corrected automatically
- [ ] Typing speed varies
- [ ] Thinking pauses occur
- [ ] No typos in code blocks
- [ ] No typos in URLs
- [ ] Overhead calculated correctly

## Error Handling

### Network Errors

- [ ] Handles network disconnection
- [ ] Waits for reconnection
- [ ] Resumes after reconnection
- [ ] Error messages clear

### Browser Errors

- [ ] Handles browser crash
- [ ] Can retry operations
- [ ] Cleanup works correctly
- [ ] No zombie processes

### Content Errors

- [ ] Validates markdown content
- [ ] Handles malformed files
- [ ] Validates frontmatter
- [ ] Error messages helpful

### Authentication Errors

- [ ] Handles invalid credentials
- [ ] Handles expired sessions
- [ ] Handles OAuth timeout
- [ ] Can re-authenticate

## Logging

### Log Display

- [ ] Logs display in UI
- [ ] Color coding works
- [ ] Auto-scroll works
- [ ] Can clear logs
- [ ] Max lines enforced

### Log Files

- [ ] Log files created
- [ ] Logs written correctly
- [ ] Log rotation works
- [ ] No permission errors

## Session Management

### State Persistence

- [ ] Session state saved
- [ ] Session restored on restart
- [ ] Version tracking works
- [ ] Progress tracking works
- [ ] Can clear session

### Cookies

- [ ] Cookies saved correctly
- [ ] Cookies restored correctly
- [ ] Cookies cleared on logout
- [ ] No cookie errors

## UI Testing

### Main Window

- [ ] Window resizable
- [ ] Window position remembered
- [ ] All buttons work
- [ ] All inputs work
- [ ] Keyboard shortcuts work
- [ ] Tab order correct

### Settings Dialog

- [ ] Opens correctly
- [ ] All settings editable
- [ ] Save button works
- [ ] Cancel button works
- [ ] Changes persist

### Progress Widget

- [ ] Progress bar updates
- [ ] Status messages update
- [ ] Time estimates update
- [ ] Cancel button works
- [ ] Elapsed time accurate
- [ ] Remaining time accurate

### File Selector

- [ ] Dialog opens
- [ ] File filtering works
- [ ] Directory navigation works
- [ ] Selection works
- [ ] Cancel works

## Performance

### Startup Time

- [ ] Application starts in < 5 seconds
- [ ] No long delays
- [ ] Responsive immediately

### Memory Usage

- [ ] Memory usage reasonable (< 500MB)
- [ ] No memory leaks
- [ ] Stable over time

### CPU Usage

- [ ] CPU usage reasonable
- [ ] No excessive CPU usage
- [ ] Responsive during typing

## Cleanup and Uninstall

### Application Cleanup

- [ ] Can close application cleanly
- [ ] No processes left running
- [ ] No temporary files left
- [ ] Logs cleaned up (if configured)

### Uninstaller (If Using Installer)

- [ ] Uninstaller runs
- [ ] Application files removed
- [ ] Start menu shortcuts removed
- [ ] Desktop shortcut removed
- [ ] User data handling correct
- [ ] Registry entries cleaned (if any)

## Documentation

### Included Documentation

- [ ] README present
- [ ] Installation instructions clear
- [ ] Usage guide helpful
- [ ] Troubleshooting guide useful
- [ ] API documentation accessible

### Help System

- [ ] Help menu works (if implemented)
- [ ] Documentation opens correctly
- [ ] Links work

## Security

### Credentials

- [ ] Credentials stored securely
- [ ] No plaintext passwords
- [ ] Keyring integration works
- [ ] Credentials cleared on logout

### Network Security

- [ ] HTTPS used for all connections
- [ ] Certificates validated
- [ ] No security warnings

## Edge Cases

### Unusual Scenarios

- [ ] Very large articles (> 10,000 words)
- [ ] Articles with special characters
- [ ] Articles with unicode
- [ ] Empty articles
- [ ] Articles with only frontmatter
- [ ] Multiple simultaneous instances
- [ ] Rapid button clicking
- [ ] Canceling operations
- [ ] Closing during operations

## Final Verification

### Overall Quality

- [ ] No crashes during testing
- [ ] No data loss
- [ ] No corruption
- [ ] Performance acceptable
- [ ] User experience smooth
- [ ] Error messages helpful
- [ ] Documentation accurate

### Sign-Off

- [ ] All critical tests passed
- [ ] All high-priority tests passed
- [ ] Known issues documented
- [ ] Ready for release

---

**Tester Name**: _______________
**Test Date**: _______________
**Application Version**: _______________
**Windows Version**: _______________
**Test Environment**: _______________

**Notes**:

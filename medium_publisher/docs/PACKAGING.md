# Packaging and Distribution Guide

This guide explains how to package and distribute the Medium Article Publisher application for Windows.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Building the Executable](#building-the-executable)
3. [Testing the Executable](#testing-the-executable)
4. [Creating the Installer](#creating-the-installer)
5. [Creating Desktop Shortcuts](#creating-desktop-shortcuts)
6. [Distribution](#distribution)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Python 3.11+**
   - Download from: https://www.python.org/downloads/
   - Ensure Python is added to PATH during installation

2. **PyInstaller**
   - Installed automatically by build script
   - Manual install: `pip install pyinstaller`

3. **Inno Setup 6.x** (Optional - for installer)
   - Download from: https://jrsoftware.org/isinfo.php
   - Required only if creating an installer

### Project Setup

1. Clone the repository
2. Create virtual environment:
   ```cmd
   python -m venv venv
   ```

3. Activate virtual environment:
   ```cmd
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

5. Install Playwright browsers:
   ```cmd
   playwright install chromium
   ```

## Building the Executable

### Automated Build (Recommended)

Run the build script:

```cmd
build.cmd
```

This script will:
1. Install PyInstaller
2. Clean previous builds
3. Build the executable using PyInstaller
4. Verify the build

### Manual Build

If you prefer to build manually:

```cmd
pyinstaller medium_publisher.spec
```

### Build Output

After successful build:
- **Executable**: `dist\MediumArticlePublisher.exe`
- **Build files**: `build\` directory (can be deleted)
- **Size**: ~50-100 MB (without Playwright browsers)

## Testing the Executable

### Local Testing

1. Navigate to the dist directory:
   ```cmd
   cd dist
   ```

2. Run the executable:
   ```cmd
   MediumArticlePublisher.exe
   ```

3. Verify:
   - Application launches without errors
   - UI displays correctly
   - Configuration files are loaded
   - Logging works

### Clean Machine Testing

**IMPORTANT**: Test on a clean Windows machine without Python or development tools installed.

#### Test Environment Setup

1. **Virtual Machine** (Recommended)
   - Use Windows 10/11 VM
   - No Python installed
   - No development tools
   - Fresh Windows installation

2. **Physical Machine**
   - Borrow a non-developer machine
   - Or use Windows Sandbox

#### Test Procedure

1. Copy the entire `dist\` directory to the test machine

2. Run `MediumArticlePublisher.exe`

3. Install Playwright browsers:
   ```cmd
   setup_playwright.cmd
   ```

4. Test all features:
   - [ ] File selection
   - [ ] Article parsing
   - [ ] Configuration settings
   - [ ] Login (both methods)
   - [ ] Publishing workflow
   - [ ] Version updates
   - [ ] Batch publishing
   - [ ] Error handling

5. Check for missing dependencies:
   - DLL errors
   - Import errors
   - Runtime errors

#### Common Issues

**Issue**: "VCRUNTIME140.dll not found"
**Solution**: Install Visual C++ Redistributable
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Issue**: "Playwright browser not found"
**Solution**: Run `setup_playwright.cmd`

**Issue**: Application crashes on startup
**Solution**: Check Windows Event Viewer for error details

## Creating the Installer

### Prerequisites

Install Inno Setup 6.x from https://jrsoftware.org/isinfo.php

### Automated Installer Creation

Run the installer creation script:

```cmd
create_installer.cmd
```

This script will:
1. Verify executable exists
2. Check Inno Setup installation
3. Create placeholder files (LICENSE.txt, icon.ico)
4. Build installer using Inno Setup
5. Verify installer creation

### Manual Installer Creation

If you prefer to build manually:

```cmd
iscc installer.iss
```

### Installer Output

After successful build:
- **Installer**: `installer_output\MediumArticlePublisher_Setup_v0.1.0.exe`
- **Size**: ~50-100 MB
- **Type**: Windows executable installer

### Installer Features

The installer includes:
- Application executable
- Configuration files
- Documentation
- Playwright setup script
- Start menu shortcuts
- Optional desktop shortcut
- Uninstaller

### Customizing the Installer

Edit `installer.iss` to customize:
- Application name and version
- Publisher information
- Installation directory
- Shortcuts
- License agreement
- Pre/post-installation scripts

## Creating Desktop Shortcuts

### Automated Shortcut Creation

Run the VBScript:

```cmd
cscript create_shortcut.vbs
```

This creates a shortcut on the user's desktop pointing to the executable.

### Manual Shortcut Creation

1. Right-click on desktop
2. Select "New" → "Shortcut"
3. Browse to `dist\MediumArticlePublisher.exe`
4. Name: "Medium Article Publisher"
5. Click "Finish"

### Shortcut Properties

Recommended settings:
- **Target**: `path\to\dist\MediumArticlePublisher.exe`
- **Start in**: `path\to\dist`
- **Run**: Normal window
- **Icon**: Custom icon (if available)

## Distribution

### Distribution Methods

#### 1. Standalone Executable

**Pros**:
- No installation required
- Portable
- Easy to update

**Cons**:
- Requires manual Playwright setup
- No Start menu integration
- No uninstaller

**Distribution**:
1. Zip the `dist\` directory
2. Include `setup_playwright.cmd`
3. Include README with instructions
4. Upload to file sharing service or GitHub releases

#### 2. Installer Package

**Pros**:
- Professional installation experience
- Automatic shortcuts
- Uninstaller included
- Can bundle Playwright setup

**Cons**:
- Larger file size
- Requires admin privileges
- More complex to create

**Distribution**:
1. Build installer using `create_installer.cmd`
2. Test installer on clean machine
3. Upload to website or GitHub releases
4. Provide download link to users

### File Hosting Options

- **GitHub Releases**: Free, version tracking, changelog
- **Google Drive**: Easy sharing, no size limits
- **Dropbox**: Simple links, good for teams
- **OneDrive**: Microsoft integration
- **Self-hosted**: Full control, custom domain

### Version Numbering

Follow Semantic Versioning (SemVer):
- **Major.Minor.Patch** (e.g., 1.0.0)
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes

Update version in:
- `main.py` (app version)
- `installer.iss` (installer version)
- `README.md` (documentation)

## Troubleshooting

### Build Issues

#### PyInstaller Errors

**Error**: "Module not found"
**Solution**: Add module to `hiddenimports` in `medium_publisher.spec`

**Error**: "Failed to execute script"
**Solution**: Run with `--debug all` flag to see detailed errors

**Error**: "UPX is not available"
**Solution**: Install UPX or set `upx=False` in spec file

#### Missing Dependencies

**Error**: DLL not found
**Solution**: 
1. Check if DLL is in `dist\` directory
2. Add to `binaries` in spec file
3. Install Visual C++ Redistributable

### Runtime Issues

#### Application Won't Start

1. Check Windows Event Viewer
2. Run from command prompt to see errors
3. Verify all dependencies are included
4. Test on clean machine

#### Playwright Issues

**Error**: "Browser not found"
**Solution**: Run `setup_playwright.cmd`

**Error**: "Browser download failed"
**Solution**: 
1. Check internet connection
2. Check firewall settings
3. Manually download browser

### Installer Issues

#### Inno Setup Errors

**Error**: "File not found"
**Solution**: Verify all source files exist

**Error**: "Invalid script"
**Solution**: Check `installer.iss` syntax

**Error**: "Compilation failed"
**Solution**: Check Inno Setup compiler output for details

## Best Practices

### Before Release

- [ ] Test on multiple Windows versions (10, 11)
- [ ] Test on clean machines without Python
- [ ] Verify all features work
- [ ] Check for memory leaks
- [ ] Test error handling
- [ ] Verify logging works
- [ ] Test uninstaller (if using installer)
- [ ] Update documentation
- [ ] Update version numbers
- [ ] Create release notes

### Security

- [ ] Sign executable with code signing certificate
- [ ] Scan for viruses/malware
- [ ] Use HTTPS for downloads
- [ ] Verify file integrity (checksums)
- [ ] Don't include sensitive data in build

### Documentation

- [ ] Include README in distribution
- [ ] Provide installation instructions
- [ ] Document system requirements
- [ ] Include troubleshooting guide
- [ ] Provide contact information

## Additional Resources

- **PyInstaller Documentation**: https://pyinstaller.org/
- **Inno Setup Documentation**: https://jrsoftware.org/ishelp/
- **Playwright Documentation**: https://playwright.dev/python/
- **PyQt6 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt6/

## Support

For issues or questions:
1. Check this documentation
2. Review troubleshooting section
3. Check GitHub issues
4. Contact support

---

**Last Updated**: 2025-03-01
**Version**: 0.1.0

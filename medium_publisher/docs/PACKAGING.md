# Packaging and Distribution Guide

This guide explains how to package and distribute the Medium Keyboard Publisher for Windows.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Building the Executable](#building-the-executable)
3. [Testing the Executable](#testing-the-executable)
4. [Creating the Installer](#creating-the-installer)
5. [Distribution](#distribution)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Python 3.11+**
   - Download from: https://www.python.org/downloads/
   - Ensure Python is added to PATH during installation

2. **PyInstaller**
   - Installed automatically by build script
   - Manual install: `pip install pyinstaller`

3. **Inno Setup 6.x** (Optional — for installer)
   - Download from: https://jrsoftware.org/isinfo.php
   - Required only if creating a Windows installer

### Project Setup

1. Clone the repository
2. From the workspace root (folder containing `medium_publisher/`):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r medium_publisher/requirements.txt
   ```

## Building the Executable

### Automated Build (Recommended)

Run the build script from the `medium_publisher/` directory:

```cmd
build.cmd
```

This script will:
1. Install PyInstaller if not present
2. Clean previous builds
3. Build the executable using PyInstaller with `medium_publisher.spec`
4. Verify the build output

### Manual Build

```cmd
cd medium_publisher
pyinstaller medium_publisher.spec
```

### Build Output

After successful build:
- **Executable**: `dist\MediumArticlePublisher.exe`
- **Build files**: `build\` directory (can be deleted)
- **Size**: ~80-150 MB (includes PyQt6, Pillow, pyautogui, and all dependencies)

### What Gets Bundled

PyInstaller bundles:
- Python interpreter
- All pip dependencies (PyQt6, pyautogui, pynput, Pillow, pywin32, etc.)
- Reference PNG images from `assets/medium/`
- Default configuration from `config/`
- Application source code (compiled to .pyc)

No external browser or browser engine is bundled — the app uses the user's existing browser via OS-level input.

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
   - PyQt6 GUI displays correctly
   - Settings dialog opens and saves
   - File selection works
   - Logging works

### Testing on Another Machine

Test on a Windows machine to verify all DLLs are bundled:

1. Copy the `dist\` directory to the test machine
2. Run `MediumArticlePublisher.exe`
3. Test all features:
   - [ ] Application launches
   - [ ] File selection works
   - [ ] Article parsing displays info
   - [ ] Settings persist
   - [ ] Screen recognition finds reference images
   - [ ] OS-level typing works
   - [ ] Emergency stop triggers correctly

#### Common Issues

**Issue**: "VCRUNTIME140.dll not found"
**Solution**: Install Visual C++ Redistributable (https://aka.ms/vs/17/release/vc_redist.x64.exe)

**Issue**: Application crashes on startup
**Solution**: Run from command prompt to see error output; check Windows Event Viewer

**Issue**: pyautogui fails with DPI error
**Solution**: Right-click exe → Properties → Compatibility → "Override high DPI scaling" → "Application"

## Creating the Installer

### Prerequisites

Install Inno Setup 6.x from https://jrsoftware.org/isinfo.php

### Automated Installer Creation

Run from the `medium_publisher/` directory:

```cmd
create_installer.cmd
```

This script will:
1. Verify the executable exists in `dist\`
2. Check Inno Setup installation
3. Create placeholder files (LICENSE.txt, icon.ico) if missing
4. Compile the installer using `installer.iss`
5. Output the installer to `installer_output\`

### Manual Installer Creation

```cmd
iscc installer.iss
```

### Installer Output

- **Installer**: `installer_output\MediumArticlePublisher_Setup_v0.1.0.exe`
- **Size**: ~80-150 MB

### Installer Features

The installer includes:
- Application executable and bundled dependencies
- Reference PNG images for screen recognition
- Default configuration files
- Documentation
- Start menu shortcuts
- Optional desktop shortcut
- Uninstaller

### Customizing the Installer

Edit `installer.iss` to customize:
- Application name and version
- Publisher information
- Installation directory
- Shortcuts and icons
- License agreement

## Distribution

### Distribution Methods

#### 1. Standalone Executable (Portable)

**Pros**: No installation required, portable, easy to update
**Cons**: No Start menu integration, no uninstaller

**Steps**:
1. Zip the `dist\` directory
2. Include a README with instructions
3. Upload to file sharing or GitHub releases

#### 2. Installer Package

**Pros**: Professional install experience, shortcuts, uninstaller
**Cons**: Larger file, requires admin privileges

**Steps**:
1. Build installer using `create_installer.cmd`
2. Test on a clean machine
3. Upload to distribution channel

### Version Numbering

Follow Semantic Versioning: **Major.Minor.Patch** (e.g., 1.0.0)

Update version in:
- `main.py` (app version constant)
- `installer.iss` (installer version)
- `README.md`

## Troubleshooting

### Build Issues

**Error**: "Module not found"
**Solution**: Add module to `hiddenimports` in `medium_publisher.spec`

**Error**: "Failed to execute script"
**Solution**: Run with `--debug all` flag for detailed errors

**Error**: Missing DLL in dist
**Solution**: Add to `binaries` list in spec file; install Visual C++ Redistributable

### Runtime Issues

**Error**: Application won't start on target machine
**Solution**: Run from command prompt to see error; check for missing DLLs

**Error**: pyautogui import fails in packaged app
**Solution**: Ensure `pyautogui`, `pynput`, and `Pillow` are in `hiddenimports`

**Error**: Reference images not found
**Solution**: Verify `assets/medium/` is included in the PyInstaller `datas` list in the spec file

### Installer Issues

**Error**: "File not found" during Inno Setup compilation
**Solution**: Verify all source files referenced in `installer.iss` exist

**Error**: Installer fails on target machine
**Solution**: Check that Visual C++ Redistributable is installed

## Best Practices

### Before Release

- [ ] Test on Windows 10 and Windows 11
- [ ] Test at 100% and 150% display scaling
- [ ] Verify all reference images are bundled
- [ ] Check emergency stop works in packaged version
- [ ] Test file selection and article parsing
- [ ] Verify logging works (log file created)
- [ ] Update version numbers
- [ ] Create release notes

### Security

- [ ] Don't include sensitive data in build
- [ ] Sign executable with code signing certificate (if available)
- [ ] Provide checksums for downloads

---

**Last Updated**: 2025-03-01

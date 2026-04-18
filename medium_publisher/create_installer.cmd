@echo off
REM Create installer script for Medium Article Publisher
REM This script builds the Windows installer using Inno Setup

echo ========================================
echo Medium Article Publisher - Create Installer
echo ========================================
echo.

REM Check if executable exists
if not exist dist\MediumArticlePublisher.exe (
    echo ERROR: Executable not found!
    echo Please run build.cmd first to create the executable.
    echo.
    pause
    exit /b 1
)

REM Check if Inno Setup is installed
where iscc >nul 2>&1
if errorlevel 1 (
    echo ERROR: Inno Setup not found!
    echo.
    echo Please install Inno Setup 6.x from:
    echo https://jrsoftware.org/isinfo.php
    echo.
    echo After installation, add Inno Setup to your PATH or run:
    echo "C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer.iss
    echo.
    pause
    exit /b 1
)

echo Step 1: Creating placeholder files...

REM Create LICENSE.txt if it doesn't exist
if not exist LICENSE.txt (
    echo MIT License > LICENSE.txt
    echo. >> LICENSE.txt
    echo Copyright (c) 2025 Medium Publisher >> LICENSE.txt
    echo. >> LICENSE.txt
    echo Permission is hereby granted, free of charge... >> LICENSE.txt
)

REM Create icon.ico placeholder if it doesn't exist
if not exist icon.ico (
    echo Note: Using default icon. Create icon.ico for custom icon.
)

echo.
echo Step 2: Building installer with Inno Setup...
iscc installer.iss
if errorlevel 1 (
    echo ERROR: Installer build failed
    pause
    exit /b 1
)
echo.

echo Step 3: Verifying installer...
if not exist installer_output\MediumArticlePublisher_Setup_v0.1.0.exe (
    echo ERROR: Installer not found in installer_output\
    pause
    exit /b 1
)
echo.

echo ========================================
echo Installer created successfully!
echo ========================================
echo.
echo Installer location: installer_output\MediumArticlePublisher_Setup_v0.1.0.exe
echo.
echo Next steps:
echo 1. Test the installer on a clean Windows machine
echo 2. Verify all features work correctly
echo 3. Distribute the installer to users
echo.
pause

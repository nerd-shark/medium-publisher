@echo off
REM Build script for Medium Article Publisher
REM This script builds the Windows executable using PyInstaller

echo ========================================
echo Medium Article Publisher - Build Script
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo ERROR: Virtual environment not activated!
    echo Please run: venv\Scripts\activate
    echo.
    pause
    exit /b 1
)

echo Step 1: Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo.

echo Step 2: Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

echo Step 3: Building executable...
pyinstaller medium_publisher.spec
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)
echo.

echo Step 4: Verifying build...
if not exist dist\MediumArticlePublisher.exe (
    echo ERROR: Executable not found in dist\
    pause
    exit /b 1
)
echo.

echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\MediumArticlePublisher.exe
echo.
echo Next steps:
echo 1. Test the executable: dist\MediumArticlePublisher.exe
echo 2. Install Playwright browsers: playwright install chromium
echo 3. Create installer (optional): Run create_installer.cmd
echo.
pause

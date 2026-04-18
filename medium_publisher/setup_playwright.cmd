@echo off
REM Post-installation script for Medium Article Publisher
REM This script installs Playwright browsers after the application is installed

echo ========================================
echo Medium Article Publisher - Setup
echo ========================================
echo.
echo This script will download and install the Chromium browser
echo required for Medium Article Publisher to function.
echo.
echo Download size: ~300MB
echo Installation time: 2-5 minutes
echo.
pause

echo Installing Playwright Chromium browser...
echo.

REM Try to use playwright from the system
playwright install chromium
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install Playwright browser
    echo.
    echo Please ensure:
    echo 1. You have an active internet connection
    echo 2. You have sufficient disk space (~300MB)
    echo 3. Playwright is installed (pip install playwright)
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Chromium browser installed successfully.
echo You can now run Medium Article Publisher.
echo.
pause

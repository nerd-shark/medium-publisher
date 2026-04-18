@echo off
echo ========================================
echo GeckoDriver Installation Script
echo ========================================
echo.

REM Create directory for GeckoDriver
set INSTALL_DIR=%USERPROFILE%\geckodriver
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Installing GeckoDriver to: %INSTALL_DIR%
echo.

REM Download GeckoDriver (Windows 64-bit)
echo Downloading GeckoDriver v0.34.0...
curl -L -o "%INSTALL_DIR%\geckodriver.zip" https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-win64.zip

REM Extract
echo Extracting...
tar -xf "%INSTALL_DIR%\geckodriver.zip" -C "%INSTALL_DIR%"

REM Clean up zip
del "%INSTALL_DIR%\geckodriver.zip"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo GeckoDriver installed to: %INSTALL_DIR%
echo.
echo NEXT STEPS:
echo 1. Add to PATH manually:
echo    - Open System Properties ^> Environment Variables
echo    - Edit PATH variable
echo    - Add: %INSTALL_DIR%
echo.
echo 2. OR run this command in a NEW terminal:
echo    setx PATH "%%PATH%%;%INSTALL_DIR%"
echo.
echo 3. Close and reopen your terminal
echo 4. Test with: geckodriver --version
echo.
pause

@echo off
echo Killing all Chrome processes...
taskkill /F /IM chrome.exe /T 2>nul
if %errorlevel% equ 0 (
    echo Chrome processes killed successfully
) else (
    echo No Chrome processes found
)
echo.
echo You can now extract cookies.
pause

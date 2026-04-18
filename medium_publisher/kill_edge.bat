@echo off
echo Killing all Edge processes...
taskkill /F /IM msedge.exe /T 2>nul
if %errorlevel% equ 0 (
    echo Edge processes killed successfully
) else (
    echo No Edge processes found
)
echo.
echo You can now extract cookies.
pause

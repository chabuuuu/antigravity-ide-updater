@echo off
echo ===================================================
echo   Installing Antigravity IDE Updater (Windows)
echo ===================================================

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found on system.
    echo Please install Python 3 and try again.
    pause
    exit /b 1
)

python "%~dp0install.py"
pause

@echo off
echo ==============================================
echo   Cai dat Antigravity IDE Updater (Windows)
echo ==============================================

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Khong tim thay Python tren he thong.
    echo Vui long cai dat Python 3 va thu lai.
    pause
    exit /b 1
)

python "%~dp0install.py"
pause

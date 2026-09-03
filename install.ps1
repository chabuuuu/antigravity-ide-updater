# PowerShell Installer for Antigravity IDE Updater
Write-Host "=== Cai dat Antigravity IDE Updater (Windows PowerShell) ===" -ForegroundColor Cyan

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[LOI] Khong tim thay Python tren he thong. Vui long cai dat Python 3." -ForegroundColor Red
    Exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& python "$ScriptDir\install.py"

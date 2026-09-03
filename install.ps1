# PowerShell Installer for Antigravity IDE Updater
Write-Host "=== Installing Antigravity IDE Updater (Windows PowerShell) ===" -ForegroundColor Cyan

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[ERROR] Python 3 was not found. Please install Python 3." -ForegroundColor Red
    Exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& python "$ScriptDir\install.py"

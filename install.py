#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Cross-Platform Installer for Antigravity IDE Updater
Creates desktop entries, command wrappers, and shortcuts on Linux & Windows.
"""

import os
import sys
import platform
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_MAIN = ROOT_DIR / "main.py"
ICON_PATH = ROOT_DIR / "assets" / "icon.png"
HOME = Path.home()
SYSTEM = platform.system().lower()


def install_linux():
    print("🐧 Installing Antigravity IDE Updater for Linux...")

    # 1. Ensure executable permission
    os.chmod(SRC_MAIN, 0o755)

    # 2. Create command symlink in ~/.local/bin
    local_bin = HOME / ".local/bin"
    local_bin.mkdir(parents=True, exist_ok=True)
    symlink_path = local_bin / "antigravity-ide-updater"

    if symlink_path.is_symlink() or symlink_path.exists():
        symlink_path.unlink()
    symlink_path.symlink_to(SRC_MAIN)
    print(f"  ✓ Command symlink created at: {symlink_path}")

    # 3. Create .desktop entry in ~/.local/share/applications
    apps_dir = HOME / ".local/share/applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    desktop_file = apps_dir / "antigravity-ide-updater.desktop"

    content = f"""[Desktop Entry]
Name=Antigravity IDE Updater
Comment=Automated updater for Antigravity IDE with zero data loss
GenericName=IDE Updater
Exec="{sys.executable}" "{SRC_MAIN}"
Icon={ICON_PATH}
Type=Application
Terminal=false
Categories=Utility;Development;IDE;
StartupNotify=true
"""
    desktop_file.write_text(content, encoding="utf-8")
    os.chmod(desktop_file, 0o755)
    print(f"  ✓ Application menu entry created: {desktop_file}")

    # 4. Create Desktop shortcut if Desktop directory exists
    desktop_dir = HOME / "Desktop"
    if desktop_dir.exists():
        user_desktop_file = desktop_dir / "antigravity-ide-updater.desktop"
        user_desktop_file.write_text(content, encoding="utf-8")
        os.chmod(user_desktop_file, 0o755)
        if shutil.which("gio"):
            subprocess.run(["gio", "set", str(user_desktop_file), "metadata::trusted", "true"], check=False, stderr=subprocess.DEVNULL)
        print(f"  ✓ Desktop shortcut created: {user_desktop_file}")

    if shutil.which("update-desktop-database"):
        subprocess.run(["update-desktop-database", str(apps_dir)], check=False, stderr=subprocess.DEVNULL)

    print("\n🎉 Installation completed! You can now run 'antigravity-ide-updater' in your terminal or launch it from the Application Menu.")


def install_windows():
    print("🪟 Installing Antigravity IDE Updater for Windows...")

    local_app_data = Path(os.environ.get("LOCALAPPDATA", str(HOME / "AppData/Local")))
    bin_dir = local_app_data / "Programs" / "AntigravityIDEUpdater"
    bin_dir.mkdir(parents=True, exist_ok=True)

    # 1. Create cmd wrapper so user can type 'antigravity-ide-updater'
    cmd_wrapper = bin_dir / "antigravity-ide-updater.cmd"
    python_exe = sys.executable
    cmd_content = f'@echo off\r\n"{python_exe}" "{SRC_MAIN}" %*\r\n'
    cmd_wrapper.write_text(cmd_content, encoding="utf-8")
    print(f"  ✓ Command wrapper created at: {cmd_wrapper}")

    # 2. Create Desktop and Start Menu shortcuts via PowerShell
    desktop_dir = HOME / "Desktop"
    start_menu = Path(os.environ.get("APPDATA", str(HOME / "AppData/Roaming"))) / "Microsoft/Windows/Start Menu/Programs"

    ps_script = f'''
    $WshShell = New-Object -comObject WScript.Shell

    # Desktop Shortcut
    $DesktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"), "Antigravity IDE Updater.lnk")
    $Shortcut = $WshShell.CreateShortcut($DesktopPath)
    $Shortcut.TargetPath = "{python_exe}"
    $Shortcut.Arguments = '"{SRC_MAIN}"'
    $Shortcut.IconLocation = "{ICON_PATH}"
    $Shortcut.Save()

    # Start Menu Shortcut
    $StartMenuDir = "{start_menu}"
    if (Test-Path $StartMenuDir) {{
        $StartPath = [System.IO.Path]::Combine($StartMenuDir, "Antigravity IDE Updater.lnk")
        $Shortcut2 = $WshShell.CreateShortcut($StartPath)
        $Shortcut2.TargetPath = "{python_exe}"
        $Shortcut2.Arguments = '"{SRC_MAIN}"'
        $Shortcut2.IconLocation = "{ICON_PATH}"
        $Shortcut2.Save()
    }}
    '''
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=False)
    print("  ✓ Desktop and Start Menu shortcuts created.")

    print("\n🎉 Installation completed! You can now launch the app from Desktop or Start Menu.")


if __name__ == "__main__":
    if "windows" in SYSTEM:
        install_windows()
    else:
        install_linux()

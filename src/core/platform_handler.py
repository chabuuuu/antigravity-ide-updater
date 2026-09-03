# -*- coding: utf-8 -*-
"""
Platform Handler for Antigravity IDE Updater
Quản lý các đường dẫn, nhận diện hệ điều hành (Linux, Windows, macOS)
và các thao tác đặc thù cho từng nền tảng.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


class PlatformHandler:
    def __init__(self):
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.home = Path.home()
        self._init_paths()

    def _init_paths(self):
        if self.is_windows():
            local_app_data = Path(os.environ.get("LOCALAPPDATA", str(self.home / "AppData/Local")))
            app_data = Path(os.environ.get("APPDATA", str(self.home / "AppData/Roaming")))
            program_files = Path(os.environ.get("ProgramFiles", "C:/Program Files"))

            # Kiểm tra vị trí cài đặt trên Windows
            candidate_1 = local_app_data / "Programs" / "Antigravity IDE"
            candidate_2 = program_files / "Antigravity IDE"

            self.install_dir = candidate_1 if candidate_1.exists() or not candidate_2.exists() else candidate_2
            self.product_json = self.install_dir / "resources" / "app" / "product.json"
            self.launcher_bin = self.install_dir / "antigravity-ide.exe"
            if not self.launcher_bin.exists():
                alt_bin = self.install_dir / "bin" / "antigravity-ide.cmd"
                if alt_bin.exists():
                    self.launcher_bin = alt_bin

            self.user_config_dir = app_data / "Antigravity IDE"
            self.user_extensions_dir = self.home / ".antigravity-ide"
            self.cache_dir = local_app_data / "antigravity-ide-updater"
            self.backup_dir = local_app_data / "antigravity-ide-updater" / "backups"

        elif self.is_macos():
            self.install_dir = Path("/Applications/Antigravity IDE.app")
            self.product_json = self.install_dir / "Contents" / "Resources" / "app" / "product.json"
            self.launcher_bin = self.install_dir / "Contents" / "MacOS" / "Electron"
            self.user_config_dir = self.home / "Library" / "Application Support" / "Antigravity IDE"
            self.user_extensions_dir = self.home / ".antigravity-ide"
            self.cache_dir = self.home / "Library" / "Caches" / "antigravity-ide-updater"
            self.backup_dir = self.home / "Library" / "Application Support" / "antigravity-ide-updater" / "backups"

        else:  # Linux / Unix
            self.install_dir = self.home / "Antigravity IDE"
            self.product_json = self.install_dir / "resources" / "app" / "product.json"
            self.launcher_bin = self.install_dir / "bin" / "antigravity-ide"
            self.user_config_dir = self.home / ".config" / "Antigravity IDE"
            self.user_extensions_dir = self.home / ".antigravity-ide"
            self.cache_dir = self.home / ".cache" / "antigravity-ide-updater"
            self.backup_dir = self.home / ".local" / "share" / "antigravity-ide" / "backups"
            self.local_bin_link = self.home / ".local" / "bin" / "antigravity-ide"
            self.desktop_entry = self.home / ".local" / "share" / "applications" / "antigravity-ide.desktop"

    def is_windows(self):
        return "windows" in self.system

    def is_linux(self):
        return "linux" in self.system

    def is_macos(self):
        return "darwin" in self.system

    def is_arm(self):
        return "arm" in self.machine or "aarch64" in self.machine

    def get_url_pattern(self):
        """Trả về regex pattern khớp với URL download tương ứng hệ điều hành"""
        if self.is_windows():
            arch = "arm64" if self.is_arm() else "x64"
            return rf'(https://[^\s"\'<>]*windows-{arch}/Antigravity(?:%20|\+)IDE\.exe)'
        elif self.is_macos():
            arch = "arm" if self.is_arm() else "x64"
            return rf'(https://[^\s"\'<>]*darwin-{arch}/Antigravity(?:%20|\+)IDE\.dmg)'
        else:  # Linux
            arch = "arm" if self.is_arm() else "x64"
            return rf'(https://[^\s"\'<>]*linux-{arch}/Antigravity(?:%20|\+)IDE\.tar\.gz)'

    def is_ide_running(self):
        """Kiểm tra tiến trình Antigravity IDE đang hoạt động"""
        try:
            if self.is_windows():
                out = subprocess.check_output(
                    ["tasklist", "/FI", "IMAGENAME eq antigravity-ide.exe"],
                    stderr=subprocess.DEVNULL,
                    text=True
                )
                return "antigravity-ide.exe" in out.lower()
            else:
                out = subprocess.check_output(
                    ["pgrep", "-f", "antigravity-ide"],
                    stderr=subprocess.DEVNULL,
                    text=True
                ).strip()
                pids = [p for p in out.split() if p and p != str(os.getpid())]
                return len(pids) > 0
        except Exception:
            return False

    def close_ide(self):
        """Đóng an toàn tiến trình IDE"""
        try:
            if self.is_windows():
                subprocess.run(["taskkill", "/F", "/IM", "antigravity-ide.exe"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(["pkill", "-f", "antigravity-ide"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    def launch_ide(self):
        """Khởi động Antigravity IDE"""
        if self.launcher_bin.exists():
            if self.is_windows():
                os.startfile(str(self.launcher_bin))
            else:
                subprocess.Popen([str(self.launcher_bin)], start_new_session=True)
            return True
        return False

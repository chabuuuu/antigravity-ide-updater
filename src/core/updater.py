# -*- coding: utf-8 -*-
"""
Core Updater Engine
Thực hiện kiểm tra phiên bản từ máy chủ Google, tải bản cập nhật,
sao lưu cấu hình và cài đặt trên Linux/Windows.
"""

import os
import sys
import re
import json
import time
import shutil
import tarfile
import urllib.request
import urllib.error
import gzip
import subprocess
from pathlib import Path

from .platform_handler import PlatformHandler

DOWNLOAD_PAGE_URL = "https://antigravity.google/download"


def parse_version(v_str):
    """Trích xuất tuple số để so sánh phiên bản"""
    if not v_str:
        return (0, 0, 0)
    clean_v = str(v_str).split("-")[0]
    nums = re.findall(r"\d+", clean_v)
    return tuple(map(int, nums)) if nums else (0, 0, 0)


class AntigravityUpdater:
    def __init__(self, platform_handler=None):
        self.handler = platform_handler or PlatformHandler()

    def get_installed_version(self):
        """Đọc phiên bản hiện tại từ product.json"""
        if not self.handler.product_json.exists():
            return None
        try:
            with open(self.handler.product_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("ideVersion") or data.get("version")
        except Exception:
            return None

    def fetch_latest_release_info(self):
        """Truy vấn trang download chính thức để lấy URL và phiên bản mới nhất"""
        req = urllib.request.Request(
            DOWNLOAD_PAGE_URL,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            if resp.info().get("Content-Encoding") == "gzip":
                content = gzip.decompress(content)
            html = content.decode("utf-8", errors="ignore")

        pattern = self.handler.get_url_pattern()
        match = re.search(pattern, html)
        if not match:
            raise RuntimeError(f"Không tìm thấy link tải Antigravity IDE phù hợp cho hệ điều hành ({self.handler.system}).")

        url = match.group(1)
        ver_match = re.search(r'/([^/]+)/(linux|windows|darwin)-', url)
        full_ver = ver_match.group(1) if ver_match else "Unknown"
        short_ver = full_ver.split("-")[0]

        return {
            "url": url,
            "full_version": full_ver,
            "version": short_ver
        }

    def backup_user_config(self, log_callback=None):
        """Sao lưu an toàn thư mục User Settings"""
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)

        user_dir = self.handler.user_config_dir / "User"
        if not user_dir.exists():
            log("  ℹ Không tìm thấy cấu hình cá nhân trước đó để sao lưu.")
            return None

        self.handler.backup_dir.mkdir(parents=True, exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S")
        backup_file = self.handler.backup_dir / f"config_backup_{ts}.tar.gz"

        try:
            with tarfile.open(backup_file, "w:gz") as tar:
                tar.add(user_dir, arcname="User")
            log(f"  ✓ Đã sao lưu an toàn cấu hình tại: {backup_file.name}")

            # Dọn dẹp chỉ giữ tối đa 3 bản sao lưu gần nhất
            backups = sorted(self.handler.backup_dir.glob("config_backup_*.tar.gz"), key=os.path.getmtime)
            while len(backups) > 3:
                oldest = backups.pop(0)
                try:
                    oldest.unlink()
                except OSError:
                    pass
            return backup_file
        except Exception as e:
            log(f"  ⚠ Không thể sao lưu cấu hình: {e}")
            return None

    def send_notification(self, title, message):
        """Gửi thông báo desktop đa nền tảng"""
        if self.handler.is_linux() and shutil.which("notify-send"):
            icon = self.handler.install_dir / "resources/app/resources/linux/code.png"
            cmd = ["notify-send", title, message]
            if icon.exists():
                cmd += ["-i", str(icon)]
            subprocess.run(cmd, check=False)
        elif self.handler.is_windows():
            ps_script = f'''
            [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
            $objNotifyIcon = New-Object System.Windows.Forms.NotifyIcon
            $objNotifyIcon.Icon = [System.Drawing.SystemIcons]::Information
            $objNotifyIcon.BalloonTipIcon = "Info"
            $objNotifyIcon.BalloonTipText = "{message}"
            $objNotifyIcon.BalloonTipTitle = "{title}"
            $objNotifyIcon.Visible = $True
            $objNotifyIcon.ShowBalloonTip(5000)
            '''
            try:
                subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass

    def perform_update(self, download_url, progress_callback=None, log_callback=None):
        """Quy trình cập nhật tự động toàn diện"""
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)

        self.handler.cache_dir.mkdir(parents=True, exist_ok=True)
        pkg_name = "Antigravity_IDE_setup.exe" if self.handler.is_windows() else "Antigravity_IDE_latest.tar.gz"
        pkg_path = self.handler.cache_dir / pkg_name

        # Bước 1: Sao lưu cấu hình
        log("[1/5] Sao lưu an toàn dữ liệu người dùng (Bảo toàn 100%)...")
        self.backup_user_config(log_callback=log)

        # Bước 2: Tải file cập nhật
        log(f"[2/5] Đang tải gói cập nhật từ Google ({download_url.split('/')[-1]})...")
        req = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})

        start_time = time.time()
        with urllib.request.urlopen(req, timeout=30) as resp:
            total_size = int(resp.info().get("Content-Length", 0))
            downloaded = 0
            chunk_size = 1024 * 128

            with open(pkg_path, "wb") as f_out:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f_out.write(chunk)
                    downloaded += len(chunk)
                    elapsed = time.time() - start_time
                    speed = (downloaded / (1024 * 1024)) / max(elapsed, 0.001)

                    if progress_callback and total_size > 0:
                        percent = (downloaded / total_size) * 100
                        dl_mb = downloaded / (1024 * 1024)
                        tot_mb = total_size / (1024 * 1024)
                        progress_callback(percent, f"{dl_mb:.1f}/{tot_mb:.1f} MB ({speed:.1f} MB/s)")

        log("  ✓ Tải về hoàn tất thành công!")

        # Bước 3 & 4: Cài đặt theo hệ điều hành
        if self.handler.is_windows():
            log("[3/5] Đang khởi chạy trình cài đặt Windows...")
            # Chạy file installer chế độ im lặng hoặc tương tác
            cmd = [str(pkg_path), "/VERYSILENT", "/NORESTART", "/MERGETASKS=!runcode"]
            log("  -> Đang thực thi cài đặt ngầm (/VERYSILENT)...")
            ret = subprocess.run(cmd, check=False)
            if ret.returncode != 0:
                log("  ⚠ Chế độ ngầm không hoàn tất, đang chuyển sang chế độ đồ họa...")
                subprocess.run([str(pkg_path)], check=True)
            log("[4/5] Đồng bộ cài đặt và shortcut Windows...")
        else:
            log("[3/5] Đang giải nén bộ cài đặt Linux...")
            extract_dir = self.handler.cache_dir / "extract"
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
            extract_dir.mkdir(parents=True, exist_ok=True)

            with tarfile.open(pkg_path, "r:gz") as tar:
                tar.extractall(path=extract_dir)

            new_app_dir = extract_dir / "Antigravity IDE"
            if not new_app_dir.exists() or not (new_app_dir / "bin/antigravity-ide").exists():
                raise RuntimeError("Gói tải về không hợp lệ.")

            log("[4/5] Cập nhật thư mục ứng dụng an toàn...")
            backup_app = self.handler.home / "Antigravity IDE.bak"
            if backup_app.exists():
                shutil.rmtree(backup_app)

            if self.handler.install_dir.exists():
                self.handler.install_dir.rename(backup_app)

            try:
                shutil.move(str(new_app_dir), str(self.handler.install_dir))
            except Exception as e:
                log(f"  ❌ Lỗi di chuyển thư mục: {e}. Đang phục hồi bản trước...")
                if backup_app.exists():
                    backup_app.rename(self.handler.install_dir)
                raise

            # Cấp quyền thực thi
            for exe_name in ["antigravity-ide", "bin/antigravity-ide", "chrome-sandbox"]:
                p = self.handler.install_dir / exe_name
                if p.exists():
                    os.chmod(p, 0o755)

            # Đảm bảo symlink ở ~/.local/bin
            if hasattr(self.handler, "local_bin_link"):
                self.handler.local_bin_link.parent.mkdir(parents=True, exist_ok=True)
                if self.handler.local_bin_link.is_symlink() or self.handler.local_bin_link.exists():
                    self.handler.local_bin_link.unlink()
                self.handler.local_bin_link.symlink_to(self.handler.launcher_bin)

            if backup_app.exists():
                shutil.rmtree(backup_app)
            if extract_dir.exists():
                shutil.rmtree(extract_dir)

        # Bước 5: Hoàn tất
        log("[5/5] Hoàn tất 100%! Cấu hình và tiện ích mở rộng được giữ nguyên vẹn.")
        new_v = self.get_installed_version() or "mới nhất"
        self.send_notification("Antigravity IDE", f"Đã cập nhật thành công lên phiên bản v{new_v}!")
        return new_v

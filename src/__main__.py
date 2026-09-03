# -*- coding: utf-8 -*-
"""
Main entry point for Antigravity IDE Updater
"""

import os
import sys
import argparse

from .core.platform_handler import PlatformHandler
from .core.updater import AntigravityUpdater, parse_version


def main():
    parser = argparse.ArgumentParser(description="Antigravity IDE Auto-Updater (Linux & Windows)")
    parser.add_argument("--check", "-c", action="store_true", help="Kiểm tra phiên bản mới")
    parser.add_argument("--update", "-u", action="store_true", help="Tự động cập nhật không cần giao diện đồ họa")
    parser.add_argument("--gui", "-g", action="store_true", help="Mở giao diện đồ họa (mặc định nếu có màn hình)")
    args = parser.parse_args()

    handler = PlatformHandler()
    updater = AntigravityUpdater(handler)

    # Nếu không chỉ định --check hoặc --update, ưu tiên mở GUI
    has_display = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY") or handler.is_windows())
    if not args.check and not args.update and (args.gui or has_display):
        try:
            from .gui.app import create_gui
            create_gui(handler)
            return
        except Exception as e:
            print(f"Không thể khởi chạy giao diện đồ họa ({e}), chuyển sang chế độ dòng lệnh.\n")

    # CLI Mode
    print("=" * 55)
    print("  Antigravity IDE Auto-Updater (CLI Mode)")
    print(f"  Hệ điều hành: {handler.system.capitalize()} ({'ARM64' if handler.is_arm() else 'x64'})")
    print("=" * 55)

    local_v = updater.get_installed_version()
    print(f"Phiên bản hiện tại trên máy : v{local_v or 'Chưa phát hiện'}")

    print("Đang kết nối tới máy chủ cập nhật chính thức...")
    try:
        info = updater.fetch_latest_release_info()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)

    remote_v = info["version"]
    print(f"Phiên bản mới nhất trên web : v{remote_v}")

    local_t = parse_version(local_v)
    remote_t = parse_version(remote_v)
    has_update = (remote_t > local_t) or (not local_v)

    if has_update:
        print(f"\n=> ⚡ Đã có phiên bản mới: v{remote_v}!")
    else:
        print("\n=> ✓ Bạn đang ở phiên bản mới nhất!")

    if args.update or (has_update and input("\nBạn có muốn cập nhật ngay bây giờ? [Y/n]: ").strip().lower() in ("y", "yes", "")):
        if handler.is_ide_running():
            print("Antigravity IDE đang chạy. Đang tự động đóng...")
            handler.close_ide()

        print("\nBắt đầu cập nhật (Dữ liệu cá nhân được bảo vệ 100%)...")
        new_v = updater.perform_update(info["url"])
        print(f"\n🎉 Cập nhật thành công lên Antigravity IDE v{new_v}!")


if __name__ == "__main__":
    main()

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
    parser.add_argument("--check", "-c", action="store_true", help="Check for available updates")
    parser.add_argument("--update", "-u", action="store_true", help="Update automatically in non-interactive CLI mode")
    parser.add_argument("--gui", "-g", action="store_true", help="Force graphical user interface (GUI) mode")
    args = parser.parse_args()

    handler = PlatformHandler()
    updater = AntigravityUpdater(handler)

    # Launch GUI if no explicit CLI action requested and display is present
    has_display = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY") or handler.is_windows())
    if not args.check and not args.update and (args.gui or has_display):
        try:
            from .gui.app import create_gui
            create_gui(handler)
            return
        except Exception as e:
            print(f"Could not launch graphical interface ({e}), falling back to CLI mode.\n")

    # CLI Mode
    print("=" * 55)
    print("  Antigravity IDE Auto-Updater (CLI Mode)")
    print(f"  Platform: {handler.system.capitalize()} ({'ARM64' if handler.is_arm() else 'x64'})")
    print("=" * 55)

    local_v = updater.get_installed_version()
    print(f"Current installed version : v{local_v or 'Not detected'}")

    print("Connecting to official release server...")
    try:
        info = updater.fetch_latest_release_info()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    remote_v = info["version"]
    print(f"Latest release available  : v{remote_v}")

    local_t = parse_version(local_v)
    remote_t = parse_version(remote_v)
    has_update = (remote_t > local_t) or (not local_v)

    if has_update:
        print(f"\n=> ⚡ New version available: v{remote_v}!")
    else:
        print("\n=> ✓ You are using the latest version!")

    if args.update or (has_update and input("\nWould you like to update now? [Y/n]: ").strip().lower() in ("y", "yes", "")):
        if handler.is_ide_running():
            print("Antigravity IDE is running. Closing processes gracefully...")
            handler.close_ide()

        print("\nStarting update (100% User Data Safe)...")
        new_v = updater.perform_update(info["url"])
        print(f"\n🎉 Successfully updated to Antigravity IDE v{new_v}!")
        print("User data (settings, keybindings, extensions) is 100% preserved.")


if __name__ == "__main__":
    main()

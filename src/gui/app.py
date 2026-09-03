# -*- coding: utf-8 -*-
"""
Modern Tkinter GUI for Antigravity IDE Updater
Hoạt động nhất quán trên cả Windows và Linux.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from ..core.updater import AntigravityUpdater, parse_version
from ..core.platform_handler import PlatformHandler


def create_gui(platform_handler=None):
    handler = platform_handler or PlatformHandler()
    updater = AntigravityUpdater(handler)

    root = tk.Tk()
    root.title("Antigravity IDE Updater")
    root.geometry("640x550")
    root.minsize(580, 500)

    # Chọn phông chữ tùy theo hệ điều hành
    font_family = "Segoe UI" if handler.is_windows() else "Noto Sans"

    # Màu sắc hiện đại (Dark Theme)
    BG_COLOR = "#181920"
    PANEL_BG = "#21222c"
    CARD_BG = "#282a36"
    TEXT_COLOR = "#f8f8f2"
    MUTED_TEXT = "#6272a4"
    ACCENT_GREEN = "#50fa7b"
    ACCENT_BLUE = "#8be9fd"
    ACCENT_ORANGE = "#ffb86c"
    ACCENT_RED = "#ff5555"
    BTN_BG = "#44475a"

    root.configure(bg=BG_COLOR)

    # Thử gắn icon
    icon_path = Path(__file__).resolve().parent.parent.parent / "assets" / "icon.png"
    if not icon_path.exists():
        icon_path = handler.install_dir / "resources/app/resources/linux/code.png"

    if icon_path.exists():
        try:
            img = tk.PhotoImage(file=str(icon_path))
            root.iconphoto(True, img)
        except Exception:
            pass

    # Styling ttk Progressbar
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TProgressbar", thickness=14, troughcolor=CARD_BG, background=ACCENT_GREEN)

    # Header
    header = tk.Frame(root, bg=BG_COLOR)
    header.pack(fill="x", padx=20, pady=(15, 8))

    tk.Label(
        header,
        text="Antigravity IDE Updater",
        font=(font_family, 16, "bold"),
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(anchor="w")

    platform_desc = f"Hệ điều hành: {handler.system.capitalize()} ({'ARM64' if handler.is_arm() else 'x64'})"
    tk.Label(
        header,
        text=f"Kiểm tra & tự động cập nhật an toàn dữ liệu 100% | {platform_desc}",
        font=(font_family, 9),
        fg=MUTED_TEXT,
        bg=BG_COLOR
    ).pack(anchor="w", pady=(2, 0))

    # Version Card
    card = tk.Frame(root, bg=CARD_BG, highlightbackground="#383a4c", highlightthickness=1)
    card.pack(fill="x", padx=20, pady=8)

    tk.Label(card, text="Phiên bản trên máy:", font=(font_family, 10), fg=MUTED_TEXT, bg=CARD_BG).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 3))
    lbl_installed = tk.Label(card, text="Đang đọc...", font=(font_family, 11, "bold"), fg=TEXT_COLOR, bg=CARD_BG)
    lbl_installed.grid(row=0, column=1, sticky="w", padx=10, pady=(12, 3))

    tk.Label(card, text="Phiên bản mới nhất:", font=(font_family, 10), fg=MUTED_TEXT, bg=CARD_BG).grid(row=1, column=0, sticky="w", padx=15, pady=3)
    lbl_latest = tk.Label(card, text="Chưa kiểm tra", font=(font_family, 11, "bold"), fg=ACCENT_BLUE, bg=CARD_BG)
    lbl_latest.grid(row=1, column=1, sticky="w", padx=10, pady=3)

    tk.Label(card, text="Trạng thái:", font=(font_family, 10), fg=MUTED_TEXT, bg=CARD_BG).grid(row=2, column=0, sticky="w", padx=15, pady=(3, 12))
    lbl_status = tk.Label(card, text="Đang khởi tạo...", font=(font_family, 10, "bold"), fg=ACCENT_ORANGE, bg=CARD_BG)
    lbl_status.grid(row=2, column=1, sticky="w", padx=10, pady=(3, 12))

    # Safety Banner
    shield = tk.Frame(root, bg="#1d2d25", highlightbackground="#2a503a", highlightthickness=1)
    shield.pack(fill="x", padx=20, pady=(0, 8))
    tk.Label(
        shield,
        text="🔒 Cam kết an toàn dữ liệu: Cấu hình cá nhân, phím tắt, tiện ích mở rộng và dự án được bảo toàn nguyên vẹn 100%.",
        font=(font_family, 8),
        fg=ACCENT_GREEN,
        bg="#1d2d25",
        wraplength=570,
        justify="left"
    ).pack(anchor="w", padx=12, pady=7)

    # Progress Area
    p_frame = tk.Frame(root, bg=BG_COLOR)
    p_frame.pack(fill="x", padx=20, pady=(0, 4))

    lbl_progress_info = tk.Label(p_frame, text="", font=(font_family, 9), fg=MUTED_TEXT, bg=BG_COLOR)
    lbl_progress_info.pack(anchor="w", pady=(0, 4))

    progress_bar = ttk.Progressbar(p_frame, style="TProgressbar", mode="determinate")
    progress_bar.pack(fill="x")

    # Log Area
    log_frame = tk.Frame(root, bg=PANEL_BG)
    log_frame.pack(fill="both", expand=True, padx=20, pady=(6, 10))

    log_text = tk.Text(
        log_frame,
        bg=PANEL_BG,
        fg=TEXT_COLOR,
        font=("Consolas" if handler.is_windows() else "Monospace", 8),
        relief="flat",
        height=7,
        padx=10,
        pady=6
    )
    log_text.pack(fill="both", expand=True)

    def append_log(line):
        log_text.insert(tk.END, line + "\n")
        log_text.see(tk.END)

    # Action Buttons
    btn_frame = tk.Frame(root, bg=BG_COLOR)
    btn_frame.pack(fill="x", padx=20, pady=(0, 15))

    btn_check = tk.Button(
        btn_frame,
        text="🔍 Kiểm tra",
        font=(font_family, 10, "bold"),
        bg=BTN_BG,
        fg=TEXT_COLOR,
        relief="flat",
        padx=14,
        pady=6
    )
    btn_check.pack(side="left", padx=(0, 8))

    btn_update = tk.Button(
        btn_frame,
        text="🚀 Cập nhật ngay",
        font=(font_family, 10, "bold"),
        bg=ACCENT_GREEN,
        fg="#181920",
        relief="flat",
        padx=16,
        pady=6,
        state="disabled"
    )
    btn_update.pack(side="left", padx=(0, 8))

    btn_launch = tk.Button(
        btn_frame,
        text="▶ Khởi động IDE",
        font=(font_family, 10),
        bg=BTN_BG,
        fg=TEXT_COLOR,
        relief="flat",
        padx=14,
        pady=6
    )
    btn_launch.pack(side="right")

    release_info = {}

    def refresh_installed_ver():
        curr = updater.get_installed_version()
        if curr:
            lbl_installed.config(text=f"v{curr}", fg=TEXT_COLOR)
        else:
            lbl_installed.config(text="Chưa phát hiện", fg=ACCENT_ORANGE)

    def check_updates(quiet=False):
        btn_check.config(state="disabled")
        lbl_status.config(text="Đang kết nối đến Google...", fg=ACCENT_ORANGE)
        append_log("Đang kiểm tra thông tin phiên bản mới từ https://antigravity.google...")

        def _worker():
            try:
                info = updater.fetch_latest_release_info()
                release_info.clear()
                release_info.update(info)

                local_v = updater.get_installed_version()
                remote_v = info["version"]

                def _success():
                    lbl_latest.config(text=f"v{remote_v}")
                    btn_check.config(state="normal")

                    has_update = False
                    if not local_v:
                        has_update = True
                        lbl_status.config(text="Chưa cài đặt. Bấm Cập nhật để cài mới.", fg=ACCENT_ORANGE)
                    else:
                        local_t = parse_version(local_v)
                        remote_t = parse_version(remote_v)
                        if remote_t > local_t:
                            has_update = True
                            lbl_status.config(text=f"⚡ Đã có bản mới (v{remote_v})!", fg=ACCENT_BLUE)
                            append_log(f"-> Đã có bản cập nhật: v{remote_v} (Hiện tại: v{local_v})")
                        else:
                            lbl_status.config(text="✓ Bạn đang sử dụng phiên bản mới nhất!", fg=ACCENT_GREEN)
                            append_log(f"-> Đang ở phiên bản mới nhất: v{local_v}")

                    if has_update:
                        btn_update.config(state="normal", text="🚀 Cập nhật ngay", bg=ACCENT_GREEN)
                    else:
                        btn_update.config(state="normal", text="🔄 Cài đặt đè lại", bg=BTN_BG)

                root.after(0, _success)
            except Exception as e:
                def _error():
                    btn_check.config(state="normal")
                    lbl_status.config(text="Lỗi kết nối", fg=ACCENT_RED)
                    append_log(f"❌ Không thể kiểm tra: {e}")
                    if not quiet:
                        messagebox.showerror("Lỗi", f"Không thể lấy thông tin cập nhật:\n{e}")
                root.after(0, _error)

        threading.Thread(target=_worker, daemon=True).start()

    def do_update():
        if not release_info.get("url"):
            messagebox.showwarning("Thông báo", "Vui lòng kiểm tra cập nhật trước.")
            return

        if handler.is_ide_running():
            ans = messagebox.askyesno(
                "Antigravity IDE đang chạy",
                "Antigravity IDE đang được mở. Bạn có muốn tự động đóng ứng dụng để tiến hành cập nhật không?"
            )
            if ans:
                append_log("Đang đóng tiến trình IDE...")
                handler.close_ide()
            else:
                append_log("⚠ Hủy cập nhật vì ứng dụng chưa được đóng.")
                return

        btn_update.config(state="disabled")
        btn_check.config(state="disabled")
        btn_launch.config(state="disabled")
        progress_bar["value"] = 0
        lbl_status.config(text="Đang cập nhật...", fg=ACCENT_BLUE)

        def _worker():
            try:
                def _prog(pct, txt):
                    root.after(0, lambda: (
                        progress_bar.configure(value=pct),
                        lbl_progress_info.configure(text=txt)
                    ))

                def _log(m):
                    root.after(0, lambda: append_log(m))

                new_v = updater.perform_update(
                    release_info["url"],
                    progress_callback=_prog,
                    log_callback=_log
                )

                def _finish():
                    refresh_installed_ver()
                    progress_bar["value"] = 100
                    lbl_progress_info.config(text="Hoàn thành 100%!")
                    lbl_status.config(text="✓ Cập nhật thành công!", fg=ACCENT_GREEN)
                    btn_check.config(state="normal")
                    btn_update.config(state="normal", text="🔄 Cài đặt đè lại", bg=BTN_BG)
                    btn_launch.config(state="normal")
                    messagebox.showinfo(
                        "Thành công",
                        f"Đã cập nhật Antigravity IDE lên phiên bản v{new_v} thành công!\nToàn bộ dữ liệu của bạn đã được bảo vệ nguyên vẹn."
                    )

                root.after(0, _finish)
            except Exception as e:
                def _fail():
                    btn_check.config(state="normal")
                    btn_update.config(state="normal")
                    btn_launch.config(state="normal")
                    lbl_status.config(text="Cập nhật thất bại", fg=ACCENT_RED)
                    append_log(f"❌ Thất bại: {e}")
                    messagebox.showerror("Lỗi", f"Quá trình cập nhật thất bại:\n{e}")
                root.after(0, _fail)

        threading.Thread(target=_worker, daemon=True).start()

    def do_launch():
        if handler.launch_ide():
            root.destroy()
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy file khởi động Antigravity IDE.")

    btn_check.config(command=lambda: check_updates(quiet=False))
    btn_update.config(command=do_update)
    btn_launch.config(command=do_launch)

    refresh_installed_ver()
    root.after(300, lambda: check_updates(quiet=True))
    root.mainloop()

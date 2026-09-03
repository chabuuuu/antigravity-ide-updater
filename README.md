# 🚀 Antigravity IDE Updater

> **Trình kiểm tra và tự động cập nhật Antigravity IDE đa nền tảng (Linux & Windows)**  
> *Đảm bảo bảo toàn 100% dữ liệu cấu hình, phím tắt, tiện ích mở rộng (extensions) và dự án đang làm việc.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-brightgreen.svg)]()

---

## 📖 Giới thiệu (Overview)

**Antigravity IDE** là môi trường phát triển AI-first tiên tiến được phát triển trên nền tảng VS Code. Tuy nhiên, việc kiểm tra và cập nhật các bản phát hành mới thủ công trên Linux hoặc Windows đôi khi phức tạp và tiềm ẩn nguy cơ cấu hình bị ghi đè nếu không thao tác đúng.

**Antigravity IDE Updater** được xây dựng nhằm giải quyết triệt để vấn đề này:
* 🔍 **Tự động dò tìm phiên bản:** Tự động kết nối đến máy chủ Google (`https://antigravity.google/download`) để so sánh phiên bản hiện tại và phiên bản mới nhất.
* ⚡ **Cập nhật 1-Click tự động:** Tải về, giải nén, thiết lập quyền thực thi và đồng bộ lối tắt hệ thống chỉ với một cú nhấp chuột.
* 🔒 **Bảo toàn dữ liệu 100% (Zero Data Loss):** Toàn bộ cài đặt cá nhân, theme, phím tắt, lịch sử chat và danh sách extension được giữ nguyên vẹn tuyệt đối.
* 🖥️ **Đa nền tảng (Cross-Platform):** Hoạt động đồng nhất trên cả **Linux** (Ubuntu, Debian, Fedora, Arch...) và **Windows** (Windows 10, Windows 11).
* 🎨 **Hỗ trợ cả Giao diện đồ họa (GUI) & Dòng lệnh (CLI):** Cung cấp giao diện Dark mode trực quan kèm thanh tiến trình tải chi tiết, hoặc có thể chạy ngầm thông qua terminal.

---

## 🔒 Cơ chế Bảo toàn Dữ liệu (Zero Data Loss Architecture)

Một trong những ưu tiên hàng đầu của công cụ là **tuyệt đối không làm mất dữ liệu của người dùng**:

```
[ Antigravity IDE Core Binaries ]             [ User Data & Configurations ]
    (Được Updater cập nhật)                          (ĐƯỢC BẢO VỆ NGUYÊN VẸN)
           │                                                    │
   ┌───────┴──────────────┐                           ┌─────────┴─────────────┐
   │ Linux:               │                           │ Linux:                │
   │  ~/Antigravity IDE   │                           │  ~/.config/Antigravity│
   │ Windows:             │                           │  ~/.antigravity-ide   │
   │  %LOCALAPPDATA%\...  │                           │ Windows:              │
   └──────────────────────┘                           │  %APPDATA%\Antigravity│
                                                      │  %USERPROFILE%\.ant...│
                                                      └───────────────────────┘
```

1. **Tách biệt dữ liệu:** Cấu hình người dùng (`settings.json`, `keybindings.json`, `snippets`) và tiện ích mở rộng (extensions) được lưu trữ hoàn toàn bên ngoài thư mục chứa mã chạy của IDE. Bộ cập nhật chỉ thay thế các file thực thi của IDE.
2. **Snapshot sao lưu tự động:** Trước mỗi lần cập nhật, hệ thống tự động nén thư mục cấu hình người dùng vào thư mục `backups/` an toàn (lưu tối đa 3 bản gần nhất).
3. **Cơ chế Rollback nguyên vẹn:** Trong quá trình cập nhật thư mục ứng dụng, bản cài đặt cũ được chuyển thành thư mục dự phòng (`.bak`). Nếu có bất kỳ lỗi gián đoạn nào (mất mạng, lỗi giải nén), hệ thống sẽ tự động khôi phục bản cũ ngay lập tức.
4. **Phát hiện tiến trình đang chạy:** Nếu IDE đang mở, ứng dụng sẽ cảnh báo và cho phép đóng an toàn trước khi thay thế tệp, tránh xung đột file lock.

---

## 📥 Cài đặt Dễ Dàng (Easy Installation)

### 1. Trên Linux

Mở terminal và chạy lệnh cài đặt một chạm:

```bash
git clone https://github.com/chabuuuu/antigravity-ide-updater.git
cd antigravity-ide-updater
./install.sh
```

> **Sau khi cài đặt:**
> * Bạn có thể tìm thấy **Antigravity IDE Updater** trong Menu ứng dụng hoặc trên màn hình Desktop.
> * Lệnh `antigravity-ide-updater` được thêm vào đường dẫn hệ thống để gọi trực tiếp từ terminal.

---

### 2. Trên Windows

1. Tải hoặc clone repository về máy:
   ```cmd
   git clone https://github.com/chabuuuu/antigravity-ide-updater.git
   cd antigravity-ide-updater
   ```
2. Chạy tệp **`install.bat`** (hoặc chuột phải vào `install.ps1` chọn *Run with PowerShell*).

> **Sau khi cài đặt:**
> * Lối tắt **Antigravity IDE Updater** sẽ xuất hiện trên màn hình Desktop và Start Menu.
> * Lệnh `antigravity-ide-updater` có thể được gọi từ Command Prompt / PowerShell.

---

### 3. Cài đặt Phổ quát qua Python (Mọi hệ điều hành)

Nếu máy đã có Python 3:

```bash
python install.py
```

---

## 🚀 Hướng dẫn Sử dụng (Usage)

### 1. Giao diện đồ họa (GUI Mode)

Chỉ cần chạy lệnh hoặc mở từ icon Desktop:

```bash
antigravity-ide-updater
```

* **Kiểm tra cập nhật:** Bấm nút **`🔍 Kiểm tra`** để xem phiên bản mới nhất từ máy chủ Google.
* **Tiến hành cập nhật:** Bấm nút **`🚀 Cập nhật ngay`**. Thanh tiến trình sẽ hiển thị phần trăm, dung lượng đã tải và tốc độ tải thực tế.
* **Mở IDE:** Sau khi hoàn tất, bạn có thể bấm ngay nút **`▶ Khởi động IDE`** để bắt đầu làm việc.

---

### 2. Chế độ Dòng lệnh (CLI Mode)

Thích hợp cho người dùng thích thao tác nhanh trong terminal hoặc tích hợp vào cronjob / script tự động:

* **Kiểm tra phiên bản mà không mở giao diện:**
  ```bash
  antigravity-ide-updater --check
  ```
  *Kết quả mẫu:*
  ```text
  =======================================================
    Antigravity IDE Auto-Updater (CLI Mode)
    Hệ điều hành: Linux (x64)
  =======================================================
  Phiên bản hiện tại trên máy : v2.5.5
  Đang kết nối tới máy chủ cập nhật chính thức...
  Phiên bản mới nhất trên web : v2.5.5

  => ✓ Bạn đang ở phiên bản mới nhất!
  ```

* **Cập nhật tự động trực tiếp từ dòng lệnh:**
  ```bash
  antigravity-ide-updater --update
  ```

* **Xem trợ giúp:**
  ```bash
  antigravity-ide-updater --help
  ```

---

## 📂 Cấu trúc Thư mục Dự án (Project Structure)

```text
antigravity-ide-updater/
├── assets/
│   └── icon.png                  # Icon đại diện của ứng dụng
├── src/
│   ├── __init__.py
│   ├── __main__.py               # Điểm khởi chạy chính (CLI & GUI routing)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── platform_handler.py   # Xử lý khác biệt giữa Linux, Windows, macOS
│   │   └── updater.py            # Core engine: tải, kiểm tra ver, sao lưu, cài đặt
│   └── gui/
│       ├── __init__.py
│       └── app.py                # Giao diện đồ họa Tkinter (Dark theme hiện đại)
├── install.py                    # Trình cài đặt tự động đa nền tảng
├── install.sh                    # Trình cài đặt 1-click cho Linux
├── install.bat                   # Trình cài đặt 1-click cho Windows
├── install.ps1                   # Trình cài đặt PowerShell cho Windows
├── main.py                       # Entrypoint ngắn gọn
├── requirements.txt              # Danh sách thư viện tùy chọn
├── setup.py                      # Tích hợp pip install
├── LICENSE                       # Giấy phép MIT
└── README.md                     # Tài liệu hướng dẫn sử dụng
```

---

## ⚙️ Yêu cầu Hệ thống (Prerequisites)

* **Hệ điều hành:** Linux (mọi bản phân phối có hỗ trợ X11/Wayland) hoặc Windows 10/11.
* **Môi trường:** Python 3.8 trở lên (có sẵn thư viện `tkinter`, mặc định đi kèm bản cài Python chuẩn).
* Không bắt buộc cài đặt thêm bất kỳ thư viện bên thứ ba nào (`requests`, `beautifulsoup4`...) vì toàn bộ tính năng sử dụng thư viện chuẩn của Python (`urllib`, `tarfile`, `gzip`, `threading`).

---

## 📄 Bản quyền (License)

Dự án được phân phối dưới giấy phép **MIT License**. Xem chi tiết tại tệp [LICENSE](LICENSE).

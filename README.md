# 🚀 Antigravity IDE Updater

> **Cross-platform auto-updater and version manager for Google Antigravity IDE (Linux & Windows)**  
> *Engineered with a 100% Zero Data Loss guarantee for user settings, keybindings, extensions, and active projects.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-brightgreen.svg)]()

---

## 📖 Overview

**Antigravity IDE** is an advanced AI-first integrated development environment built on top of VS Code. However, checking for official releases and upgrading manually on Linux and Windows can be tedious and carries the risk of accidentally overwriting user configurations or custom extensions.

**Antigravity IDE Updater** solves this with an automated, reliable utility:
* 🔍 **Automated Version Discovery:** Directly queries the official Google distribution endpoints (`https://antigravity.google/download`) to detect the latest stable release.
* ⚡ **1-Click Seamless Update:** Downloads the official release package, verifies integrity, swaps binaries atomically, sets file permissions, and refreshes system shortcuts automatically.
* 🔒 **100% Zero Data Loss Guarantee:** Your personal configuration, themes, custom keybindings, chat history, and installed extensions are completely isolated and guaranteed safe.
* 🖥️ **Cross-Platform:** Works identically on both **Linux** (Ubuntu, Debian, Fedora, Arch, etc.) and **Windows** (Windows 10, Windows 11).
* 🎨 **GUI & CLI Dual Mode:** Includes a responsive Dark Mode GUI with real-time download progress and speed meters, as well as a non-interactive CLI mode for script automation.

---

## 🔒 Zero Data Loss Architecture

User data integrity is the primary design requirement of this updater.

```
[ Application Binaries ]                     [ User Data & Configurations ]
(Targeted for upgrade)                              (100% UNTOUCHED & PRESERVED)
         │                                                        │
 ┌───────┴──────────────┐                               ┌─────────┴─────────────┐
 │ Linux:               │                               │ Linux:                │
 │  ~/Antigravity IDE   │                               │  ~/.config/Antigravity│
 │ Windows:             │                               │  ~/.antigravity-ide   │
 │  %LOCALAPPDATA%\...  │                               │ Windows:              │
 └──────────────────────┘                               │  %APPDATA%\Antigravity│
                                                        │  %USERPROFILE%\.ant...│
                                                        └───────────────────────┘
```

1. **Storage Decoupling:** User configurations (`settings.json`, `keybindings.json`, snippets) and installed extensions reside outside the application installation folder. The updater strictly touches the application core files.
2. **Automated Pre-Update Snapshots:** Before any upgrade starts, the updater archives your user configuration directory into an encrypted/compressed snapshot in `backups/` (retaining the 3 most recent backups).
3. **Atomic Swapping & Instant Rollback:** The existing application folder is renamed to a backup directory (`.bak`) before the new build is moved into place. If any failure occurs (network disruption, extraction error), the updater immediately rolls back to the previous working build.
4. **Active Process Safeguard:** If Antigravity IDE is currently running, the updater prompts the user to close it safely before proceeding, avoiding locked files or corrupted runtime states.

---

## 📥 Easy Installation

### 1. On Linux

Open a terminal and run the one-step installer:

```bash
git clone https://github.com/chabuuuu/antigravity-ide-updater.git
cd antigravity-ide-updater
./install.sh
```

> **What this does:**
> * Creates an executable symlink in `~/.local/bin/antigravity-ide-updater`.
> * Installs a desktop entry in `~/.local/share/applications/antigravity-ide-updater.desktop`.
> * Adds a desktop shortcut directly to your Desktop.

---

### 2. On Windows

1. Clone or download the repository:
   ```cmd
   git clone https://github.com/chabuuuu/antigravity-ide-updater.git
   cd antigravity-ide-updater
   ```
2. Double-click **`install.bat`** (or right-click `install.ps1` and select *Run with PowerShell*).

> **What this does:**
> * Creates a command wrapper in `%LOCALAPPDATA%\Programs\AntigravityIDEUpdater\`.
> * Installs a shortcut on your Desktop and in the Windows Start Menu.

---

### 3. Universal Python Installation (Any Platform)

If Python 3 is installed:

```bash
python install.py
```

---

## 🚀 Usage

### 1. Graphical User Interface (GUI Mode)

Launch the application from your desktop shortcut or via terminal:

```bash
antigravity-ide-updater
```

* **Check for Updates:** Click **`🔍 Check for Updates`** to check Google's release server.
* **Perform Upgrade:** Click **`🚀 Update Now`**. The real-time progress bar will display the percentage, downloaded megabytes, and current download speed.
* **Launch IDE:** Once completed, click **`▶ Launch IDE`** to immediately open Antigravity IDE.

---

### 2. Command Line Interface (CLI Mode)

Ideal for quick terminal checks or integration into recurring scripts / cron jobs:

* **Check installed vs latest version:**
  ```bash
  antigravity-ide-updater --check
  ```
  *Sample output:*
  ```text
  =======================================================
    Antigravity IDE Auto-Updater (CLI Mode)
    Platform: Linux (x64)
  =======================================================
  Current installed version : v2.5.5
  Connecting to official release server...
  Latest release available  : v2.5.5

  => ✓ You are using the latest version!
  ```

* **Perform silent upgrade directly in terminal:**
  ```bash
  antigravity-ide-updater --update
  ```

* **Display help information:**
  ```bash
  antigravity-ide-updater --help
  ```

---

## 📂 Project Structure

```text
antigravity-ide-updater/
├── assets/
│   └── icon.png                  # Application icon asset
├── src/
│   ├── __init__.py
│   ├── __main__.py               # Main CLI/GUI dispatcher
│   ├── core/
│   │   ├── __init__.py
│   │   ├── platform_handler.py   # Cross-platform path and OS abstractions
│   │   └── updater.py            # Core engine: checks, downloads, backups, upgrades
│   └── gui/
│       ├── __init__.py
│       └── app.py                # Modern Tkinter dark-theme GUI
├── install.py                    # Universal cross-platform installer
├── install.sh                    # 1-Click Linux shell installer
├── install.bat                   # 1-Click Windows batch installer
├── install.ps1                   # Windows PowerShell installer
├── main.py                       # Root executable wrapper
├── requirements.txt              # Optional dependencies
├── setup.py                      # Pip packaging configuration
├── LICENSE                       # MIT License
└── README.md                     # Comprehensive project documentation
```

---

## ⚙️ Requirements

* **Operating System:** Linux (X11 / Wayland desktop) or Windows 10/11.
* **Runtime:** Python 3.8+ (standard installation with `tkinter` included).
* No mandatory third-party dependencies are required. The entire codebase is implemented using the Python Standard Library (`urllib`, `tarfile`, `gzip`, `threading`, `subprocess`).

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

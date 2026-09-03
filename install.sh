#!/usr/bin/env bash
set -e

echo "=== Cài đặt Antigravity IDE Updater (Linux) ==="

# Kiểm tra Python 3
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Lỗi: Python 3 chưa được cài đặt. Vui lòng cài đặt python3 trước."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/install.py"

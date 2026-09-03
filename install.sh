#!/usr/bin/env bash
set -e

echo "=== Installing Antigravity IDE Updater (Linux) ==="

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Error: Python 3 is required. Please install python3 first."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/install.py"

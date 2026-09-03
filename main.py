#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

# Đảm bảo import được module trong src
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.__main__ import main

if __name__ == "__main__":
    main()

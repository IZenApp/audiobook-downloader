#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎧 Audiobook Downloader - Console Launcher
Запуск консольной версии загрузчика аудиокниг
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Запуск консольной версии"""
    launcher_path = Path(__file__).parent / "src" / "launchers" / "console.py"
    
    try:
        result = subprocess.run([sys.executable, str(launcher_path)], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска: {e}")
        return e.returncode
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

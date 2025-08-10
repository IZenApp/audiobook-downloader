#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎧 Audiobook Downloader - GUI Launcher
Запуск графической версии загрузчика аудиокниг
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Запуск GUI версии"""
    # Путь к основному GUI модулю
    launcher_path = Path(__file__).parent.parent / "src" / "launchers" / "gui_launcher.py"
    
    try:
        result = subprocess.run([sys.executable, str(launcher_path)], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска GUI: {e}")
        return e.returncode
    except Exception as e:
        print(f"❌ Ошибка GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
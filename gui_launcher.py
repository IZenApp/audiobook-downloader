#!/usr/bin/env python3
"""
🪟 Audiobook Downloader - GUI Launcher
Обертка для запуска GUI версии из корневой папки
"""

import subprocess
import sys
import os

def main():
    """Обёртка для запуска GUI интерфейса."""
    try:
        # Путь к основному скрипту
        script_path = os.path.join(os.path.dirname(__file__), 'launchers', 'gui_launcher.py')
        
        # Запускаем основной скрипт с теми же аргументами
        result = subprocess.run([sys.executable, script_path] + sys.argv[1:], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска: {e}")
        return 1
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
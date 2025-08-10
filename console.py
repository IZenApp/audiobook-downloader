#!/usr/bin/env python3
"""
🎧 Audiobook Downloader - Console Launcher
Обертка для запуска консольной версии из корневой папки
"""

import subprocess
import sys
import os

def main():
    """Обёртка для запуска консольного интерфейса."""
    try:
        # Путь к основному скрипту
        script_path = os.path.join(os.path.dirname(__file__), 'launchers', 'console.py')
        
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎧 Audiobook Downloader - GUI Version
Графическая версия загрузчика аудиокниг
"""

import sys
from pathlib import Path

# Добавляем корневую папку в путь
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def main():
    """Главная функция GUI версии"""
    try:
        from src.gui import main as gui_main
        return gui_main()
    except ImportError as e:
        print(f"❌ Ошибка импорта GUI: {e}")
        print("💡 Возможно, не установлен tkinter")
        return 1
    except Exception as e:
        print(f"❌ Ошибка GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

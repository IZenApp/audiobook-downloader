#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎧 Audiobook Downloader - Console Version
Консольная версия загрузчика аудиокниг
"""

import sys
from pathlib import Path

# Добавляем корневую папку в путь
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def main():
    """Главная функция консольной версии"""
    try:
        from src.audiobook_downloader.core import main as core_main
        return core_main()
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return 1
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Тестовый скрипт для проверки работоспособности
"""

import sys
from pathlib import Path

# Добавляем корневую папку в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_parsing():
    """Тест парсинга файла books.txt"""
    print("🧪 Тестирование парсинга...")
    
    try:
        from src.utils.simple_downloader_v3 import SimpleDownloader
        
        downloader = SimpleDownloader()
        books = downloader.load_books()
        
        print(f"✅ Найдено {len(books)} книг")
        
        if books:
            first_book = books[0]
            print(f"📖 Первая книга: {first_book.author} - {first_book.title}")
        
        assert len(books) > 0, "Список книг должен содержать хотя бы одну книгу"
        
    except Exception as e:
        print(f"❌ Ошибка парсинга: {e}")
        assert False, f"Ошибка парсинга: {e}"

def test_dependencies():
    """Тест зависимостей"""
    print("🧪 Тестирование зависимостей...")
    
    required_modules = [
        'yt_dlp',
        'googlesearch',
        'requests',
        'rich'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"\n📦 Установите недостающие пакеты:")
        print(f"pip install {' '.join(missing)}")
        assert False, f"Отсутствуют модули: {missing}"
    
    assert len(missing) == 0, "Все необходимые модули должны быть установлены"

def main():
    """Главная функция тестирования"""
    print("🎧 Тестирование Audiobook Downloader v2.0")
    print("=" * 50)
    
    # Тест зависимостей
    deps_ok = test_dependencies()
    print()
    
    # Тест парсинга
    if deps_ok:
        parsing_ok = test_parsing()
    else:
        parsing_ok = False
    
    print("\n" + "=" * 50)
    if deps_ok and parsing_ok:
        print("🎉 Все тесты пройдены! Можно запускать скрипт.")
        print("🚀 Запуск: ./scripts/launcher.sh")
        print("🖥️ Консоль: python console.py")
        print("🪟 GUI: python gui_launcher.py")
    else:
        print("⚠️ Обнаружены проблемы. Исправьте их перед запуском.")

if __name__ == "__main__":
    main()

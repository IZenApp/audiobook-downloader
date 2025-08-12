#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для проверки парсера книг
"""

import sys
from pathlib import Path

# Добавляем путь к исходному коду
sys.path.insert(0, str(Path(__file__).parent / "src"))

from audiobook_downloader.core import AudiobookParser

def main():
    """Тестирование парсера"""
    books_file = Path(__file__).parent / "data" / "books.txt"
    
    try:
        parser = AudiobookParser(str(books_file))
        books = parser.parse()
        
        print(f"✅ Успешно парсированы {len(books)} книги:")
        print("=" * 80)
        
        for i, book in enumerate(books, 1):
            print(f"{i:2d}. ID: {book.id}")
            print(f"    Автор: {book.author}")
            print(f"    Название: {book.title}")
            if book.subtitle:
                print(f"    Подзаголовок: {book.subtitle}")
            print(f"    Полное название: {book.full_title}")
            print(f"    Поисковый запрос: {book.search_query}")
            print("-" * 80)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()

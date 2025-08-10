#!/usr/bin/env python3
"""
🎧 Simple Audiobook Downloader v3
Автономная простая версия загрузчика
"""

import os
import sys
import re
import logging
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

try:
    import yt_dlp
    from rich.console import Console
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.panel import Panel
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Установите зависимости: pip install yt-dlp rich")
    sys.exit(1)

console = Console()
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Book:
    """Информация о книге"""
    author: str
    title: str
    category: str = ""

class SimpleDownloader:
    """Простой загрузчик аудиокниг"""
    
    def __init__(self, books_file: str = None):
        # Определяем пути относительно корня проекта
        current_dir = Path(__file__).parent
        root_dir = current_dir.parent.parent
        
        self.books_file = books_file or str(root_dir / "data" / "books.txt")
        self.download_dir = str(root_dir / "downloads")
        self.mp3_dir = str(root_dir / "downloads" / "mp3_audiobooks")
        
        # Создаем директории
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.mp3_dir, exist_ok=True)
        
        # Настройки yt-dlp для MP3
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.mp3_dir, '%(uploader)s-%(title)s.%(ext)s'),
            'noplaylist': True,
            'extract_flat': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    
    def load_books(self) -> List[Book]:
        """Загрузка списка книг"""
        books = []
        current_category = ""
        
        try:
            with open(self.books_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Пропускаем комментарии и пустые строки
                    if not line or line.startswith('#'):
                        continue
                    
                    # Определяем категорию
                    if line.startswith('##'):
                        current_category = line.replace('##', '').strip()
                        continue
                    
                    # Парсим книгу
                    if ' - ' in line:
                        parts = line.split(' - ', 1)
                        if len(parts) == 2:
                            author = parts[0].strip()
                            title = parts[1].strip()
                            books.append(Book(author=author, title=title, category=current_category))
                    
        except FileNotFoundError:
            console.print(f"[red]❌ Файл {self.books_file} не найден[/red]")
        except Exception as e:
            logger.error(f"Ошибка загрузки книг: {e}")
        
        return books
    
    def search_youtube(self, book: Book) -> List[str]:
        """Поиск на YouTube"""
        search_queries = [
            f"ytsearch3:{book.author} {book.title} аудиокнига",
            f"ytsearch2:{book.author} {book.title} полная версия",
            f"ytsearch2:аудиокнига {book.author} {book.title}",
        ]
        
        urls = []
        
        for query in search_queries:
            try:
                console.print(f"[dim]🔍 Поиск: {query.split(':')[1][:50]}...[/dim]")
                
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    search_results = ydl.extract_info(query, download=False)
                    
                    if 'entries' in search_results and search_results['entries']:
                        for entry in search_results['entries']:
                            if entry and 'webpage_url' in entry:
                                duration = entry.get('duration', 0)
                                title = entry.get('title', '').lower()
                                
                                # Фильтруем по длительности (больше 30 минут)
                                if duration and duration > 1800:
                                    # Проверяем релевантность
                                    author_words = book.author.lower().split()
                                    if any(word in title for word in author_words if len(word) > 2):
                                        urls.append(entry['webpage_url'])
                                        console.print(f"[green]   ✅ Найдено: {entry.get('title', '')[:60]}...[/green]")
                                        
                                        if len(urls) >= 2:  # Ограничиваем количество
                                            break
                
                if len(urls) >= 2:
                    break
                    
            except Exception as e:
                logger.debug(f"Ошибка поиска: {e}")
                continue
        
        return urls
    
    def download_book(self, book: Book) -> bool:
        """Скачивание одной книги"""
        console.print(f"🔍 Поиск: {book.author} - {book.title}")
        
        urls = self.search_youtube(book)
        
        if not urls:
            console.print(f"[red]❌ Не найдено: {book.author} - {book.title}[/red]")
            return False
        
        # Создаем красивое имя файла
        safe_author = re.sub(r'[^\w\s-]', '', book.author).strip()
        safe_title = re.sub(r'[^\w\s-]', '', book.title).strip()
        filename = f"{safe_author}-{safe_title}.%(ext)s"
        
        # Настройки для конкретной книги с MP3 конвертацией
        download_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.mp3_dir, filename),
            'noplaylist': True,
            'extract_flat': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        # Скачиваем первый найденный результат
        try:
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([urls[0]])
            
            console.print(f"[green]✅ Успешно скачано: {book.author} - {book.title}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Ошибка скачивания: {e}[/red]")
            logger.error(f"Ошибка скачивания {book.title}: {e}")
            return False
    
    def download_books(self, books: List[Book]):
        """Скачивание списка книг"""
        if not books:
            console.print("[yellow]⚠️ Список книг пуст[/yellow]")
            return
        
        successful = 0
        total = len(books)
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("Скачивание...", total=total)
            
            for i, book in enumerate(books):
                if self.download_book(book):
                    successful += 1
                
                progress.advance(task)
        
        console.print(f"\n🎉 Завершено! Успешно: {successful}/{total}")
    
    def run(self):
        """Основной цикл"""
        books = self.load_books()
        
        if not books:
            console.print("[red]❌ Список книг пуст[/red]")
            return
        
        console.print(f"✅ Найдено {len(books)} книг в файле")
        
        # Показываем список книг
        console.print("\n📚 Список книг:")
        for i, book in enumerate(books, 1):
            console.print(f"{i}. {book.author} - {book.title}")
        
        # Выбираем режим
        console.print("\nВыберите режим:")
        console.print("1. Скачать все книги")
        console.print("2. Скачать диапазон книг")
        console.print("3. Скачать одну книгу")
        
        try:
            choice = input("\nВаш выбор (1-3): ").strip()
            
            if choice == "1":
                self.download_books(books)
            elif choice == "2":
                start = int(input("Начать с книги №: ")) - 1
                end = int(input("Закончить на книге №: "))
                if 0 <= start < len(books) and start < end <= len(books):
                    self.download_books(books[start:end])
                else:
                    console.print("[red]❌ Неверный диапазон[/red]")
            elif choice == "3":
                book_num = int(input("Номер книги: ")) - 1
                if 0 <= book_num < len(books):
                    self.download_books([books[book_num]])
                else:
                    console.print("[red]❌ Неверный номер книги[/red]")
            else:
                console.print("[red]❌ Неверный выбор[/red]")
                
        except (ValueError, KeyboardInterrupt):
            console.print("\n[yellow]⚠️ Отменено[/yellow]")

def main():
    """Главная функция"""
    try:
        console.print(Panel.fit(
            "🎧 Simple Audiobook Downloader v3\n"
            "Автономная версия с поиском на YouTube",
            title="🚀 Запуск"
        ))
        
        downloader = SimpleDownloader()
        downloader.run()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Остановлено пользователем[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e}[/red]")
        logger.error(f"Ошибка в main: {e}", exc_info=True)

if __name__ == "__main__":
    main()

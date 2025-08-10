#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎧 Улучшенная версия загрузчика с обработкой ошибок YouTube
"""

import sys
import time
from pathlib import Path

# Добавляем пути для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from audiobook_downloader.core import AudiobookDownloader, BookInfo
    from utils.youtube_handler import YouTubeErrorHandler, ImprovedSearcher, create_improved_ydl_options
    from config.downloader_config import YDL_CONFIG
    import yt_dlp
    from rich.console import Console
    from rich.progress import Progress
    from rich.panel import Panel
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

console = Console()

class RobustAudiobookDownloader(AudiobookDownloader):
    """Улучшенная версия загрузчика с лучшей обработкой ошибок"""
    
    def __init__(self, download_dir: str = "downloads"):
        super().__init__(download_dir)
        self.error_handler = YouTubeErrorHandler()
        self.searcher = ImprovedSearcher()
        
    def download_book_robust(self, book: BookInfo) -> bool:
        """Улучшенная загрузка книги с обработкой ошибок"""
        if book.id in self.downloaded_books:
            console.print(f"[yellow]⏭️ Книга уже скачана: {book.full_title}[/yellow]")
            return True
        
        console.print(f"[cyan]🔍 Поиск: {book.full_title}[/cyan]")
        
        # Используем улучшенный поиск
        try:
            book_info = {
                'author': book.author,
                'title': book.title,
                'narrator': book.narrator
            }
            
            urls = self.searcher.search_with_fallbacks(book_info, max_results=5)
            
            if not urls:
                console.print(f"[red]❌ Не найдено результатов для: {book.full_title}[/red]")
                return False
            
            console.print(f"[green]✅ Найдено {len(urls)} потенциальных источников[/green]")
            
            # Пробуем скачать с каждого URL
            for i, url in enumerate(urls, 1):
                console.print(f"[blue]🔗 Попытка {i}/{len(urls)}: {url[:60]}...[/blue]")
                
                if self.download_from_url_robust(url, book):
                    console.print(f"[green]✅ Успешно скачано: {book.full_title}[/green]")
                    return True
                
                # Пауза между попытками
                if i < len(urls):
                    time.sleep(3)
            
            console.print(f"[red]❌ Не удалось скачать: {book.full_title}[/red]")
            return False
            
        except Exception as e:
            console.print(f"[red]💥 Критическая ошибка: {e}[/red]")
            return False
    
    def download_from_url_robust(self, url: str, book: BookInfo) -> bool:
        """Улучшенная загрузка с URL с обработкой ошибок"""
        target_dir = self._get_category_dir(book.category)
        
        # Создаем красивое имя файла
        safe_title = self._create_safe_filename(book)
        output_file = target_dir / f"{safe_title}.%(ext)s"
        
        # Создаем улучшенные опции для yt-dlp
        ydl_opts = create_improved_ydl_options(target_dir)
        ydl_opts['outtmpl'] = str(output_file)
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                console.print(f"[dim]   🔄 Попытка {attempt + 1}/{max_attempts}[/dim]")
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Получаем информацию о видео
                    info = ydl.extract_info(url, download=False)
                    
                    if not info:
                        console.print("[red]   ❌ Не удалось получить информацию о видео[/red]")
                        continue
                    
                    # Проверяем длительность
                    duration = info.get('duration', 0)
                    if duration < 1800:  # Меньше 30 минут
                        console.print(f"[yellow]   ⚠️ Видео слишком короткое ({duration//60} мин)[/yellow]")
                        return False
                    
                    console.print(f"[green]   ⏱️ Длительность: {duration//3600}ч {(duration%3600)//60}м[/green]")
                    
                    # Скачиваем
                    ydl.download([url])
                    
                    # Сохраняем прогресс
                    self.downloaded_books[book.id] = book.full_title
                    self._save_progress()
                    
                    console.print(f"[green]   ✅ Файл сохранен в {target_dir}[/green]")
                    return True
                    
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)
                console.print(f"[red]   ❌ Ошибка загрузки: {error_msg[:100]}...[/red]")
                
                # Проверяем, связано ли с блокировкой YouTube
                if self.error_handler.is_youtube_blocked(error_msg):
                    console.print("[yellow]   🚫 Обнаружена блокировка YouTube[/yellow]")
                    
                    if self.error_handler.should_retry(url, "youtube_block"):
                        delay = self.error_handler.get_retry_delay(attempt)
                        console.print(f"[dim]   ⏳ Ожидание {delay:.1f}с перед повтором...[/dim]")
                        time.sleep(delay)
                        continue
                    else:
                        console.print("[red]   🛑 Превышено количество попыток для этого URL[/red]")
                        return False
                else:
                    # Другая ошибка - пробуем еще раз
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                        continue
                    else:
                        return False
                        
            except Exception as e:
                console.print(f"[red]   💥 Неожиданная ошибка: {e}[/red]")
                if attempt < max_attempts - 1:
                    time.sleep(2)
                    continue
                else:
                    return False
        
        return False

def main():
    """Главная функция с улучшенным обработчиком"""
    console.print(Panel(
        "[bold blue]🎧 Audiobook Downloader v2.0 (Robust Edition)[/bold blue]\n"
        "[dim]Улучшенная версия с обходом блокировок YouTube[/dim]",
        title="🚀 Запуск",
        border_style="blue"
    ))
    
    try:
        from audiobook_downloader.core import AudiobookParser
        
        # Инициализация
        parser = AudiobookParser("data/books.txt")
        books = parser.parse()
        
        console.print(f"[green]✅ Найдено {len(books)} книг в файле[/green]")
        
        # Создаем улучшенный загрузчик
        downloader = RobustAudiobookDownloader()
        
        # Интерактивный режим
        console.print("\n[bold]Выберите режим:[/bold]")
        console.print("1. Скачать все книги")
        console.print("2. Скачать диапазон книг")
        console.print("3. Скачать одну книгу")
        
        choice = console.input("\n[bold]Ваш выбор (1-3): [/bold]")
        
        if choice == "1":
            # Все книги
            with Progress() as progress:
                task = progress.add_task("[green]Скачивание...", total=len(books))
                successful = 0
                
                for book in books:
                    if downloader.download_book_robust(book):
                        successful += 1
                    progress.advance(task)
                
            console.print(f"\n[green]🎉 Завершено! Успешно: {successful}/{len(books)}[/green]")
            
        elif choice == "2":
            # Диапазон
            start = int(console.input("[bold]Начать с книги №: [/bold]"))
            end = int(console.input("[bold]Закончить на книге №: [/bold]"))
            
            filtered_books = [book for book in books if start <= book.id <= end]
            
            with Progress() as progress:
                task = progress.add_task("[green]Скачивание...", total=len(filtered_books))
                successful = 0
                
                for book in filtered_books:
                    if downloader.download_book_robust(book):
                        successful += 1
                    progress.advance(task)
                
            console.print(f"\n[green]🎉 Завершено! Успешно: {successful}/{len(filtered_books)}[/green]")
            
        elif choice == "3":
            # Одна книга
            book_id = int(console.input("[bold]Номер книги: [/bold]"))
            book = next((b for b in books if b.id == book_id), None)
            
            if book:
                if downloader.download_book_robust(book):
                    console.print("[green]✅ Книга успешно скачана![/green]")
                else:
                    console.print("[red]❌ Не удалось скачать книгу[/red]")
            else:
                console.print("[red]❌ Книга с таким номером не найдена[/red]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 Остановлено пользователем[/yellow]")
    except Exception as e:
        console.print(f"[red]💥 Критическая ошибка: {e}[/red]")

if __name__ == "__main__":
    main()

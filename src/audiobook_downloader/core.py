#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎧 Загрузчик аудиокниг v2.0
Красивый и функциональный скрипт для поиска и скачивания аудиокниг

Автор: GitHub Copilot
Дата: 10 августа 2025
"""

import os
import re
import json
import time
import logging
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import requests
from urllib.parse import quote, unquote

# Проверка виртуального окружения и зависимостей
def check_environment():
    """Проверка окружения и зависимостей"""
    missing_packages = []
    
    try:
        import yt_dlp
    except ImportError:
        missing_packages.append('yt-dlp')
    
    try:
        from googlesearch import search
    except ImportError:
        missing_packages.append('googlesearch-python')
    
    try:
        from rich.console import Console
    except ImportError:
        missing_packages.append('rich')
    
    if missing_packages:
        print("❌ Отсутствуют необходимые пакеты:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Установите их командой:")
        print(f"pip install {' '.join(missing_packages)}")
        print("\n🔧 Или активируйте виртуальное окружение:")
        print("source .venv/bin/activate")
        sys.exit(1)

# Проверяем окружение перед импортом
check_environment()

import yt_dlp
from googlesearch import search
from dataclasses import dataclass
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

# Настройка логирования
def setup_logging():
    """Настройка красивого логирования"""
    # Определяем путь к логам относительно корня проекта
    current_dir = Path(__file__).parent
    log_dir = current_dir.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'audiobook_downloader.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()
console = Console()

@dataclass
class BookInfo:
    """Класс для хранения информации о книге"""
    id: int
    author: str
    title: str
    subtitle: str = ""
    narrator: str = ""
    year: str = ""
    category: str = ""
    
    @property
    def full_title(self) -> str:
        """Полное название книги"""
        result = f"{self.author} - {self.title}"
        if self.subtitle:
            result += f": {self.subtitle}"
        return result
    
    @property
    def search_query(self) -> str:
        """Запрос для поиска"""
        return f"{self.author} {self.title} аудиокнига"
    
    @property
    def filename(self) -> str:
        """Безопасное имя файла"""
        safe_name = re.sub(r'[^\w\s\-\.]', '', self.full_title)
        safe_name = re.sub(r'[-\s]+', '-', safe_name)
        return safe_name[:100]  # Ограничиваем длину

class AudiobookParser:
    """Парсер файла с аудиокнигами"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        
    def parse(self) -> List[BookInfo]:
        """Парсинг файла с книгами"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл {self.file_path} не найден!")
        
        books = []
        current_category = ""
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            
            # Обнаружение категории
            if line.startswith('##'):
                current_category = line.replace('##', '').strip()
                continue
            
            # Парсинг книги
            book = self._parse_book_line(line, current_category)
            if book:
                books.append(book)
        
        console.print(f"[green]✅ Найдено {len(books)} книг в файле[/green]")
        return books
    
    def _parse_book_line(self, line: str, category: str) -> Optional[BookInfo]:
        """Парсинг одной строки с книгой"""
        # Поддержка двух форматов:
        # 1. Номерованный: "1. Автор - Название | Чтец: Имя (2024)"
        # 2. Простой: "Автор - Название"
        
        # Сначала пробуем номерованный формат
        numbered_pattern = r'^(\d+)\.\s+([^-]+?)\s*-\s*([^|]+?)(?:\s*\|\s*Чтец:\s*([^(]+?)\s*\((\d{4})\))?$'
        match = re.match(numbered_pattern, line.strip())
        
        if match:
            # Номерованный формат
            book_id = int(match.group(1))
            author = match.group(2).strip()
            title_part = match.group(3).strip()
            narrator = match.group(4).strip() if match.group(4) else ""
            year = match.group(5) if match.group(5) else ""
        else:
            # Пробуем простой формат "Автор - Название"
            simple_pattern = r'^([^-]+?)\s*-\s*(.+)$'
            simple_match = re.match(simple_pattern, line.strip())
            
            if not simple_match:
                logger.warning(f"Не удалось распарсить строку: {line}")
                return None
            
            # Простой формат - генерируем ID
            import hashlib
            book_id = int(hashlib.md5(line.encode()).hexdigest()[:8], 16) % 100000
            author = simple_match.group(1).strip()
            title_part = simple_match.group(2).strip()
            narrator = ""
            year = ""
        
        # Разделяем название и подзаголовок
        if ':' in title_part:
            title, subtitle = title_part.split(':', 1)
            title = title.strip()
            subtitle = subtitle.strip()
        else:
            title = title_part
            subtitle = ""
        
        return BookInfo(
            id=book_id,
            author=author,
            title=title,
            subtitle=subtitle,
            narrator=narrator,
            year=year,
            category=category
        )

class AudiobookDownloader:
    """Основной класс для скачивания аудиокниг"""
    
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
        # Создаем папку для MP3 файлов
        self.mp3_dir = self.download_dir / "mp3_audiobooks"
        self.mp3_dir.mkdir(exist_ok=True)
        
        # Настройки для yt-dlp с MP3 конвертацией
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'ignoreerrors': True,
            'no_warnings': True,
            'outtmpl': str(self.mp3_dir / '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'writeinfojson': True,
            'writethumbnail': True,
        }
        
        # Файл для отслеживания скачанных книг
        self.progress_file = self.download_dir / 'download_progress.json'
        self.downloaded_books = self._load_progress()
    
    def _load_progress(self) -> Dict[int, str]:
        """Загрузка прогресса скачивания"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return {int(k): v for k, v in json.load(f).items()}
        return {}
    
    def _save_progress(self):
        """Сохранение прогресса"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.downloaded_books, f, ensure_ascii=False, indent=2)
    
    def _get_category_dir(self, category: str) -> Path:
        """Получение директории для категории с улучшенной сортировкой"""
        # Нормализуем категорию для поиска
        category_lower = category.lower() if category else ""
        
        # Точное сопоставление категорий
        if any(keyword in category_lower for keyword in ["зарубежная", "зарубеж", "foreign"]) and \
           any(keyword in category_lower for keyword in ["фантастика", "фэнтези", "мистика", "ужасы", "фанфики", "fantasy"]):
            return self.download_dir / "foreign_fantasy"
        
        elif any(keyword in category_lower for keyword in ["зарубежная", "зарубеж", "foreign"]) and \
             any(keyword in category_lower for keyword in ["детектив", "триллер", "боевик", "detective", "thriller"]):
            return self.download_dir / "foreign_detective"
        
        elif any(keyword in category_lower for keyword in ["российская", "русская", "russian"]) and \
             any(keyword in category_lower for keyword in ["фантастика", "фэнтези", "мистика", "ужасы", "фанфики", "fantasy"]):
            return self.download_dir / "russian_fantasy"
        
        elif any(keyword in category_lower for keyword in ["российская", "русская", "russian"]) and \
             any(keyword in category_lower for keyword in ["детектив", "триллер", "боевик", "detective", "thriller"]):
            return self.download_dir / "russian_detective"
        
        # Если категория не определена, анализируем автора
        return self._guess_category_by_content(category)
    
    def _guess_category_by_content(self, category: str) -> Path:
        """Угадывание категории по содержимому"""
        # Список известных зарубежных авторов фантастики
        foreign_fantasy_authors = [
            "герберт", "толкин", "мартин", "роулинг", "кинг", "лавкрафт",
            "азимов", "кларк", "хайнлайн", "дик", "брэдбери", "ле гуин"
        ]
        
        # Список известных зарубежных авторов детективов
        foreign_detective_authors = [
            "кристи", "дойль", "стаут", "чандлер", "макдональд", "леонард",
            "коннелли", "чайлд", "харрис", "гришэм", "фолетт"
        ]
        
        # Анализируем по умолчанию как российскую фантастику
        return self.download_dir / "russian_fantasy"
    
    def _create_organized_structure(self, book: BookInfo, file_path: Path) -> Path:
        """Создание организованной структуры файлов"""
        category_dir = self._get_category_dir(book.category)
        
        # Создаем подпапки по авторам (исправляем русские символы)
        author_safe = book.author
        # Заменяем русские символы на латинские
        cyrillic_to_latin = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
            'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
            'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
            'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
        }
        
        # Транслитерация
        for cyr, lat in cyrillic_to_latin.items():
            author_safe = author_safe.replace(cyr, lat)
        
        # Удаляем небезопасные символы и нормализуем
        author_safe = re.sub(r'[^\w\s]', '', author_safe)
        author_safe = re.sub(r'\s+', '_', author_safe.strip())
        
        author_dir = category_dir / author_safe
        author_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем папку для серии (если есть цифры в названии)
        if re.search(r'\d+', book.title):
            series_match = re.search(r'([^0-9]+)', book.title)
            if series_match:
                series_name = series_match.group(1).strip()
                series_safe = re.sub(r'[^\w\s]', '', series_name)
                series_safe = re.sub(r'\s+', '_', series_safe)
                if len(series_safe) > 3:  # Только если название серии осмысленное
                    series_dir = author_dir / series_safe
                    series_dir.mkdir(parents=True, exist_ok=True)
                    return series_dir
        
        return author_dir
    
    def search_youtube(self, book: BookInfo) -> List[str]:
        """Поиск на YouTube"""
        try:
            search_queries = [
                f"ytsearch5:{book.search_query} полная версия",
                f"ytsearch5:{book.author} {book.title} аудиокнига",
                f"ytsearch3:{book.full_title}"
            ]
            
            urls = []
            for query in search_queries:
                try:
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        search_results = ydl.extract_info(query, download=False)
                        
                        if 'entries' in search_results:
                            for entry in search_results['entries']:
                                if entry and 'webpage_url' in entry:
                                    duration = entry.get('duration', 0)
                                    # Фильтруем слишком короткие видео (меньше 30 минут)
                                    if duration > 1800:  
                                        urls.append(entry['webpage_url'])
                except:
                    continue
            
            return list(set(urls))  # Убираем дубликаты
            
        except Exception as e:
            logger.error(f"Ошибка поиска на YouTube: {e}")
            return []
    
    def download_from_url(self, url: str, book: BookInfo) -> bool:
        """Скачивание с URL с красивой организацией файлов"""
        try:
            # Получаем организованную структуру папок
            target_dir = self._create_organized_structure(book, None)
            
            # Создаем красивое имя файла
            filename = self._create_beautiful_filename(book)
            
            opts = self.ydl_opts.copy()
            opts['outtmpl'] = str(target_dir / f"{filename}.%(ext)s")
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                console.print(f"[blue]📥 Скачивание: {book.full_title}[/blue]")
                console.print(f"[dim]📁 Сохранение в: {target_dir.relative_to(self.download_dir)}[/dim]")
                
                ydl.download([url])
                
                # Сохраняем прогресс
                self.downloaded_books[book.id] = {
                    'title': book.full_title,
                    'url': url,
                    'category': book.category,
                    'file_path': str(target_dir / f"{filename}.mp3"),
                    'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                self._save_progress()
                
                console.print(f"[green]✅ Успешно скачано: {book.full_title}[/green]")
                return True
                
        except Exception as e:
            console.print(f"[red]❌ Ошибка скачивания {book.full_title}: {e}[/red]")
            return False
    
    def _create_beautiful_filename(self, book: BookInfo) -> str:
        """Создание красивого имени файла"""
        # Формат: "Автор - Книга 01 - Подзаголовок (Чтец, Год)"
        filename_parts = []
        
        # Автор (безопасный для файловой системы)
        author_clean = re.sub(r'[^\w\s]', '', book.author).strip()
        author_clean = re.sub(r'\s+', '_', author_clean)
        filename_parts.append(author_clean)
        
        # Название с номером (если есть)
        title_clean = re.sub(r'[^\w\s\d]', '', book.title).strip()
        title_clean = re.sub(r'\s+', '_', title_clean)
        if book.subtitle:
            subtitle_clean = re.sub(r'[^\w\s\d]', '', book.subtitle).strip()
            subtitle_clean = re.sub(r'\s+', '_', subtitle_clean)
            title_clean += f"_{subtitle_clean}"
        filename_parts.append(title_clean)
        
        # Дополнительная информация
        extra_info = []
        if book.narrator:
            narrator_clean = re.sub(r'[^\w\s-]', '', book.narrator).strip()
            extra_info.append(narrator_clean)
        if book.year:
            extra_info.append(book.year)
        
        if extra_info:
            filename_parts.append(f"({', '.join(extra_info)})")
        
        filename = " - ".join(filename_parts)
        
        # Ограничиваем длину и очищаем
        filename = re.sub(r'[-\s]+', '-', filename)
        return filename[:150]  # Ограничиваем длину
    
    def download_book(self, book: BookInfo) -> bool:
        """Скачивание одной книги"""
        if book.id in self.downloaded_books:
            console.print(f"[yellow]⏭️ Книга уже скачана: {book.full_title}[/yellow]")
            return True
        
        console.print(f"[cyan]🔍 Поиск: {book.full_title}[/cyan]")
        
        # Поиск на YouTube
        urls = self.search_youtube(book)
        
        if not urls:
            console.print(f"[red]❌ Не найдено результатов для: {book.full_title}[/red]")
            return False
        
        # Пробуем скачать с первых найденных URL
        for i, url in enumerate(urls[:3], 1):
            console.print(f"[blue]🔗 Попытка {i}/3: {url}[/blue]")
            if self.download_from_url(url, book):
                return True
            time.sleep(2)
        
        console.print(f"[red]❌ Не удалось скачать: {book.full_title}[/red]")
        return False
    
    def download_books(self, books: List[BookInfo], start_from: int = 1, limit: Optional[int] = None):
        """Скачивание списка книг"""
        # Фильтрация
        filtered_books = [book for book in books if book.id >= start_from]
        if limit:
            filtered_books = filtered_books[:limit]
        
        console.print(Panel(
            f"[bold green]📚 Начинаем скачивание {len(filtered_books)} книг[/bold green]",
            title="🎧 Audiobook Downloader",
            border_style="green"
        ))
        
        successful = 0
        failed = 0
        
        with Progress() as progress:
            task = progress.add_task("[green]Скачивание...", total=len(filtered_books))
            
            for book in filtered_books:
                # Показываем информацию о книге
                table = Table(title=f"📖 Книга #{book.id}")
                table.add_column("Поле", style="cyan")
                table.add_column("Значение", style="white")
                
                table.add_row("Автор", book.author)
                table.add_row("Название", book.title)
                if book.subtitle:
                    table.add_row("Подзаголовок", book.subtitle)
                if book.narrator:
                    table.add_row("Чтец", book.narrator)
                if book.year:
                    table.add_row("Год", book.year)
                table.add_row("Категория", book.category)
                
                console.print(table)
                
                # Скачиваем
                if self.download_book(book):
                    successful += 1
                else:
                    failed += 1
                
                progress.update(task, advance=1)
                
                # Пауза между книгами
                time.sleep(3)
        
        # Итоги
        result_table = Table(title="📊 Результаты скачивания")
        result_table.add_column("Статус", style="bold")
        result_table.add_column("Количество", style="bold")
        
        result_table.add_row("✅ Успешно", str(successful), style="green")
        result_table.add_row("❌ Неудачно", str(failed), style="red")
        result_table.add_row("📁 Папка", str(self.download_dir.absolute()), style="blue")
        
        console.print(result_table)

def show_welcome():
    """Показать приветствие"""
    welcome_text = Text()
    welcome_text.append("🎧 ", style="bold blue")
    welcome_text.append("Загрузчик аудиокниг v2.0", style="bold green")
    welcome_text.append("\n📚 Красивый и функциональный инструмент", style="dim")
    
    console.print(Panel(
        welcome_text,
        title="[bold blue]Audiobook Downloader[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))

def main():
    """Основная функция"""
    show_welcome()
    
    # Определяем путь к файлу с книгами относительно корня проекта
    current_dir = Path(__file__).parent
    books_file = current_dir.parent.parent / "data" / "books.txt"
    
    # Создаем экземпляры
    parser = AudiobookParser(str(books_file))
    
    # Путь к downloads тоже относительно корня проекта
    downloads_dir = current_dir.parent.parent / "downloads"
    downloader = AudiobookDownloader(str(downloads_dir))
    
    try:
        # Парсим книги
        books = parser.parse()
        
        if not books:
            console.print("[red]❌ Не найдено книг для скачивания[/red]")
            return
        
        # Настройки скачивания
        console.print("\n[bold]⚙️ Настройки скачивания:[/bold]")
        console.print("1. Скачать все книги")
        console.print("2. Скачать с определенного номера")
        console.print("3. Скачать ограниченное количество")
        
        choice = console.input("\n[bold]Выберите опцию (1-3): [/bold]").strip()
        
        start_from = 1
        limit = None
        
        if choice == "2":
            start_from = int(console.input("С какого номера начать: "))
        elif choice == "3":
            limit = int(console.input("Сколько книг скачать: "))
            start_input = console.input("С какого номера начать (Enter для начала с 1): ").strip()
            if start_input:
                start_from = int(start_input)
        
        # Запуск скачивания
        downloader.download_books(books, start_from, limit)
        
    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e}[/red]")
        logger.error(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()

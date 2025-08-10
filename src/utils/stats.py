#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📊 Статистика загрузчика аудиокниг v3
Анализ MP3 файлов
"""

import os
import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

class MP3Stats:
    def __init__(self, downloads_dir: str = None):
        # Определяем путь относительно корня проекта
        if downloads_dir is None:
            current_dir = Path(__file__).parent
            root_dir = current_dir.parent.parent
            self.downloads_dir = root_dir / "downloads"
        else:
            self.downloads_dir = Path(downloads_dir)
        self.mp3_dir = self.downloads_dir / "mp3_audiobooks"
    
    def format_size(self, size_bytes):
        """Форматирование размера файла"""
        if size_bytes < 1024*1024:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024*1024*1024:
            return f"{size_bytes/(1024*1024):.1f} MB"
        else:
            return f"{size_bytes/(1024*1024*1024):.1f} GB"
    
    def show_stats(self):
        """Показать красивую статистику MP3 файлов"""
        console.print("\n" + "="*50)
        console.print("📊 СТАТИСТИКА MP3 АУДИОКНИГ", style="bold green", justify="center")
        console.print("="*50)
        
        # Проверяем существование папки
        if not self.mp3_dir.exists():
            console.print(f"[red]❌ Папка не найдена: {self.mp3_dir}[/red]")
            return
        
        # Находим все MP3 файлы
        mp3_files = list(self.mp3_dir.glob("*.mp3"))
        
        if not mp3_files:
            console.print(f"[yellow]📊 Нет MP3 файлов в папке: {self.mp3_dir}[/yellow]")
            return
        
        # Анализируем файлы
        total_files = len(mp3_files)
        total_size = 0
        dates = []
        file_info = []
        
        for mp3_file in mp3_files:
            if mp3_file.exists():
                size = mp3_file.stat().st_size
                total_size += size
                
                # Дата модификации
                mod_time = datetime.datetime.fromtimestamp(mp3_file.stat().st_mtime)
                dates.append(mod_time)
                
                file_info.append({
                    'name': mp3_file.name,
                    'size': size,
                    'date': mod_time
                })
        
        # Создаём сводку
        overview_text = Text()
        overview_text.append("🎵 Всего MP3 файлов: ", style="bold")
        overview_text.append(str(total_files), style="bold green")
        overview_text.append(f"\n💾 Общий размер: ", style="bold")
        overview_text.append(self.format_size(total_size), style="bold blue")
        
        if dates:
            last_date = max(dates).strftime('%d.%m.%Y %H:%M')
            overview_text.append(f"\n📅 Последний файл: ", style="bold")
            overview_text.append(last_date, style="bold magenta")
        
        overview_panel = Panel(overview_text, title="📊 Общая статистика", border_style="green")
        console.print(overview_panel)
        
        # Таблица файлов
        if total_files <= 20:  # Показываем детали только если файлов немного
            files_table = Table(title="📋 Список файлов")
            files_table.add_column("Название", style="cyan", max_width=40)
            files_table.add_column("Размер", style="bold")
            files_table.add_column("Дата", style="dim")
            
            # Сортируем по дате (новые сверху)
            file_info.sort(key=lambda x: x['date'], reverse=True)
            
            for info in file_info:
                name = info['name']
                if len(name) > 40:
                    name = name[:37] + "..."
                
                files_table.add_row(
                    name,
                    self.format_size(info['size']),
                    info['date'].strftime('%d.%m %H:%M')
                )
            
            console.print("\n")
            console.print(files_table)
        
        # Дополнительная статистика
        if total_files > 1:
            avg_size = total_size / total_files
            console.print(f"\n[dim]💡 Средний размер файла: {self.format_size(avg_size)}[/dim]")
        
        console.print(f"\n[dim]📂 Путь к файлам: {self.mp3_dir}[/dim]")

def main():
    """Главная функция для запуска статистики"""
    stats = MP3Stats()
    stats.show_stats()

if __name__ == "__main__":
    main()

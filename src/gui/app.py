#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎧 Audiobook Downloader GUI
Графический интерфейс для загрузчика аудиокниг
"""

import sys
import os
import json
import threading
from pathlib import Path
from typing import List, Optional
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from tkinter.font import Font
import queue

# Добавляем корневую папку в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

# Проверка зависимостей
def check_gui_dependencies():
    """Проверка зависимостей для GUI"""
    missing = []
    
    try:
        import tkinter as tk
    except ImportError:
        missing.append("tkinter (встроенный в Python)")
    
    try:
        from src.audiobook_downloader.core import AudiobookDownloader, BookInfo
    except ImportError as e:
        missing.append(f"audiobook_downloader: {e}")
    
    if missing:
        error_msg = "❌ Отсутствуют зависимости:\n" + "\n".join(f"- {m}" for m in missing)
        error_msg += "\n\n💡 Убедитесь что:\n"
        error_msg += "1. Активировано виртуальное окружение: source .venv/bin/activate\n"
        error_msg += "2. Установлены зависимости: pip install -r requirements.txt\n"
        error_msg += "3. Существует модуль audiobook_downloader"
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Ошибка зависимостей", error_msg)
            root.destroy()
        except:
            print(error_msg)
        
        sys.exit(1)

# Проверяем зависимости
check_gui_dependencies()

try:
    from src.audiobook_downloader import AudiobookParser, AudiobookDownloader, BookInfo
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("📁 Убедитесь что пакет audiobook_downloader доступен")
    sys.exit(1)

class AudiobookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎧 Audiobook Downloader v2.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Настройка стиля
        self.setup_styles()
        
        # Переменные
        self.books = []
        self.downloader = None
        self.download_thread = None
        self.queue = queue.Queue()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Запуск проверки очереди
        self.check_queue()
        
    def setup_styles(self):
        """Настройка стилей"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цвета
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Info.TLabel', foreground='blue')
        
    def create_widgets(self):
        """Создание виджетов"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Конфигурация растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🎧 Audiobook Downloader v2.0", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Панель управления файлом
        file_frame = ttk.LabelFrame(main_frame, text="📚 Файл с книгами", padding="5")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        self.file_var = tk.StringVar(value="data/books.txt")
        ttk.Label(file_frame, text="Файл:").grid(row=0, column=0, padx=(0, 5))
        ttk.Entry(file_frame, textvariable=self.file_var, state='readonly').grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(file_frame, text="Выбрать", command=self.select_file).grid(row=0, column=2)
        ttk.Button(file_frame, text="Загрузить", command=self.load_books).grid(row=0, column=3, padx=(5, 0))
        
        # Панель со списком книг
        books_frame = ttk.LabelFrame(main_frame, text="📖 Список книг", padding="5")
        books_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        books_frame.columnconfigure(0, weight=1)
        books_frame.rowconfigure(0, weight=1)
        
        # Treeview для книг
        columns = ('ID', 'Автор', 'Название', 'Чтец', 'Год', 'Категория')
        self.books_tree = ttk.Treeview(books_frame, columns=columns, show='headings', height=15)
        
        # Настройка колонок
        self.books_tree.heading('ID', text='ID')
        self.books_tree.heading('Автор', text='Автор')
        self.books_tree.heading('Название', text='Название')
        self.books_tree.heading('Чтец', text='Чтец')
        self.books_tree.heading('Год', text='Год')
        self.books_tree.heading('Категория', text='Категория')
        
        self.books_tree.column('ID', width=50)
        self.books_tree.column('Автор', width=150)
        self.books_tree.column('Название', width=250)
        self.books_tree.column('Чтец', width=150)
        self.books_tree.column('Год', width=60)
        self.books_tree.column('Категория', width=100)
        
        # Скроллбар для списка
        scrollbar = ttk.Scrollbar(books_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        
        self.books_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Панель управления скачиванием
        control_frame = ttk.LabelFrame(main_frame, text="⚙️ Управление скачиванием", padding="5")
        control_frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Настройки скачивания
        ttk.Label(control_frame, text="Начать с книги:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.start_var = tk.StringVar(value="1")
        ttk.Entry(control_frame, textvariable=self.start_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(control_frame, text="Количество книг:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.limit_var = tk.StringVar(value="")
        ttk.Entry(control_frame, textvariable=self.limit_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        # Кнопки управления
        self.download_btn = ttk.Button(control_frame, text="🚀 Начать скачивание", command=self.start_download)
        self.download_btn.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ Остановить", command=self.stop_download, state='disabled')
        self.stop_btn.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Прогресс
        ttk.Label(control_frame, text="Прогресс:").grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        self.progress_var = tk.StringVar(value="Готов к работе")
        ttk.Label(control_frame, textvariable=self.progress_var, style='Info.TLabel').grid(row=5, column=0, columnspan=2, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(control_frame, mode='determinate')
        self.progress_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 10))
        
        # Статистика
        self.stats_var = tk.StringVar(value="Статистика появится здесь")
        ttk.Label(control_frame, textvariable=self.stats_var, style='Info.TLabel').grid(row=7, column=0, columnspan=2, sticky=tk.W)
        
        # Панель логов
        log_frame = ttk.LabelFrame(main_frame, text="📝 Логи", padding="5")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Растягивание последней строки
        main_frame.rowconfigure(3, weight=1)
        
    def select_file(self):
        """Выбор файла с книгами"""
        filename = filedialog.askopenfilename(
            title="Выберите файл с книгами",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_var.set(filename)
            
    def load_books(self):
        """Загрузка списка книг"""
        try:
            file_path = self.file_var.get()
            if not os.path.exists(file_path):
                messagebox.showerror("Ошибка", f"Файл {file_path} не найден!")
                return
                
            parser = AudiobookParser(file_path)
            self.books = parser.parse()
            
            # Очистка и заполнение таблицы
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)
                
            for book in self.books:
                self.books_tree.insert('', 'end', values=(
                    book.id,
                    book.author,
                    f"{book.title}{': ' + book.subtitle if book.subtitle else ''}",
                    book.narrator,
                    book.year,
                    book.category.split()[-1] if book.category else ""  # Последнее слово категории
                ))
            
            self.log(f"✅ Загружено {len(self.books)} книг")
            messagebox.showinfo("Успех", f"Загружено {len(self.books)} книг")
            
        except Exception as e:
            self.log(f"❌ Ошибка загрузки: {e}")
            messagebox.showerror("Ошибка", f"Ошибка загрузки файла: {e}")
            
    def start_download(self):
        """Начало скачивания"""
        if not self.books:
            messagebox.showwarning("Предупреждение", "Сначала загрузите список книг!")
            return
            
        try:
            start_from = int(self.start_var.get()) if self.start_var.get() else 1
            limit = int(self.limit_var.get()) if self.limit_var.get() else None
            
            # Фильтрация книг
            filtered_books = [book for book in self.books if book.id >= start_from]
            if limit:
                filtered_books = filtered_books[:limit]
                
            if not filtered_books:
                messagebox.showwarning("Предупреждение", "Нет книг для скачивания!")
                return
                
            # UI изменения
            self.download_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.progress_bar.config(maximum=len(filtered_books))
            self.progress_bar.config(value=0)
            
            # Создание загрузчика с правильным путем
            downloads_dir = Path(__file__).parent / "downloads"
            self.downloader = AudiobookDownloader(str(downloads_dir))
            
            # Запуск в отдельном потоке
            self.download_thread = threading.Thread(
                target=self.download_worker,
                args=(filtered_books,),
                daemon=True
            )
            self.download_thread.start()
            
            self.log(f"🚀 Начато скачивание {len(filtered_books)} книг")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Неверные числовые значения!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка запуска: {e}")
            
    def download_worker(self, books: List[BookInfo]):
        """Рабочий поток скачивания"""
        successful = 0
        failed = 0
        
        for i, book in enumerate(books, 1):
            try:
                # Отправка обновления в главный поток
                self.queue.put(('progress', i, len(books), book.full_title))
                
                # Скачивание книги
                if self.downloader.download_book(book):
                    successful += 1
                    self.queue.put(('success', book.full_title))
                else:
                    failed += 1
                    self.queue.put(('error', book.full_title))
                    
            except Exception as e:
                failed += 1
                self.queue.put(('error', f"{book.full_title}: {e}"))
                
        # Завершение
        self.queue.put(('complete', successful, failed))
        
    def stop_download(self):
        """Остановка скачивания"""
        # Здесь можно добавить логику остановки
        self.download_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress_var.set("Остановлено пользователем")
        self.log("⏹️ Скачивание остановлено")
        
    def check_queue(self):
        """Проверка очереди сообщений"""
        try:
            while True:
                message = self.queue.get_nowait()
                self.process_message(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
            
    def process_message(self, message):
        """Обработка сообщения из очереди"""
        msg_type = message[0]
        
        if msg_type == 'progress':
            _, current, total, title = message
            self.progress_bar.config(value=current)
            self.progress_var.set(f"Скачивание {current}/{total}")
            self.log(f"📥 [{current}/{total}] {title}")
            
        elif msg_type == 'success':
            _, title = message
            self.log(f"✅ Успешно: {title}")
            
        elif msg_type == 'error':
            _, error = message
            self.log(f"❌ Ошибка: {error}")
            
        elif msg_type == 'complete':
            _, successful, failed = message
            self.download_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.progress_var.set("Завершено")
            self.stats_var.set(f"✅ Успешно: {successful} | ❌ Ошибок: {failed}")
            self.log(f"🎉 Скачивание завершено! Успешно: {successful}, Ошибок: {failed}")
            messagebox.showinfo("Готово", f"Скачивание завершено!\nУспешно: {successful}\nОшибок: {failed}")
            
    def log(self, message: str):
        """Добавление сообщения в лог"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

def main():
    """Главная функция GUI"""
    root = tk.Tk()
    app = AudiobookGUI(root)
    
    # Центрирование окна
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

# 💻 Source Code

Исходный код Audiobook Downloader.

## 📁 Структура

```
src/
├── audiobook_downloader/   # Основной движок
│   ├── __init__.py
│   └── core.py            # Ядро программы
├── config/                # Конфигурация
│   ├── __init__.py
│   ├── downloader_config.py
│   └── README.md
├── gui/                   # Графический интерфейс
│   ├── __init__.py
│   └── app.py            # Tkinter приложение
├── launchers/             # Точки входа
│   ├── console.py        # Консольный launcher
│   └── gui_launcher.py   # GUI launcher
└── utils/                 # Утилиты
    ├── __init__.py
    ├── simple_downloader_v3.py  # Простой загрузчик
    ├── stats.py          # Статистика
    └── youtube_handler.py # Работа с YouTube
```

## 🧩 Модули

### 🎯 Core (`audiobook_downloader/`)
- **Основная логика** программы
- Парсинг списков книг
- YouTube поиск и загрузка
- MP3 конвертация

### ⚙️ Config (`config/`)
- Настройки программы
- Конфигурация yt-dlp
- Пути и параметры

### 🖥️ GUI (`gui/`)
- Графический интерфейс
- Tkinter приложение
- Удобное управление

### 🚀 Launchers (`launchers/`)
- Точки входа в программу
- Обработка аргументов
- Инициализация

### 🛠️ Utils (`utils/`)
- Вспомогательные утилиты
- Статистика файлов
- Работа с YouTube API

## 🎯 Точки входа

```bash
# Консольная версия
python src/launchers/console.py

# GUI версия  
python src/launchers/gui_launcher.py

# Простой загрузчик
python src/utils/simple_downloader_v3.py

# Статистика
python src/utils/stats.py
```

## 🧪 Тестирование

```bash
# Запуск тестов
python -m pytest tests/

# Проверка зависимостей
python tests/test_core.py
```

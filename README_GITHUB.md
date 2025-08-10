# 🎧 Audiobook Downloader v3.0

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](README.md)

> Профессиональный загрузчик аудиокниг с красивой архитектурой и поддержкой MP3 конвертации

## ✨ Особенности

- 🎵 **MP3 конвертация** - автоматическое преобразование в MP3 (192 kbps)
- 📁 **Организованное хранение** - чистая структура файлов
- 🎯 **Множественные интерфейсы** - консоль, GUI, простая версия
- 🔍 **Умный поиск** - автоматический поиск на YouTube
- 🛡️ **Обход ограничений** - работа с заблокированным контентом
- 🏗️ **Профессиональная архитектура** - организованный код
- 📊 **Красивая статистика** - анализ загрузок
- 🔒 **Приватность** - ваши списки книг остаются локальными

## 🚀 Быстрая установка

```bash
# Клонирование репозитория
git clone https://github.com/ваш-username/audiobook-downloader.git
cd audiobook-downloader

# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка списка книг
cp data/books_example.txt data/books.txt
# Отредактируйте data/books.txt со своими книгами

# Установка ffmpeg (для MP3 конвертации)
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: скачайте с ffmpeg.org

# Запуск
./scripts/launcher.sh
```

## 📱 Интерфейсы

### 🎛️ Главное меню (рекомендуется)
```bash
./scripts/launcher.sh
```

### 🎧 Простая версия v3 (лучший выбор)
```bash
python src/utils/simple_downloader_v3.py
```

### 🖥️ Консольная версия
```bash
python console.py
```

### 🪟 GUI версия
```bash
python gui_launcher.py
```

## 📁 Архитектура

```
📦 audiobook-downloader/
├── 📄 console.py               # 🚀 Консольный лаунчер
├── 📄 gui_launcher.py         # 🪟 GUI лаунчер
│
├── 📁 src/                    # 🔧 Исходный код
│   ├── 📁 audiobook_downloader/ # 🎧 Основной движок
│   ├── 📁 config/             # ⚙️ Конфигурации
│   ├── 📁 gui/                # 🖼️ Графический интерфейс
│   ├── 📁 launchers/          # 🚀 Внутренние лаунчеры
│   └── 📁 utils/              # 🛠️ Утилиты
│       ├── simple_downloader_v3.py  # ⭐ Простая версия
│       ├── robust_downloader.py     # 💪 Продвинутая
│       └── stats.py                 # 📊 Статистика
│
├── 📁 data/                   # 📚 Данные
│   ├── books_example.txt      # 📖 Пример списка
│   └── books.txt             # 🔒 Ваш список (приватный)
│
├── 📁 downloads/             # ⬇️ MP3 файлы (приватные)
├── 📁 tests/                 # 🧪 Тестирование
├── 📁 scripts/               # 🔧 Bash скрипты
└── 📁 docs/                  # 📚 Документация
```

## 🎯 Использование

### Для начинающих
1. Запустите `./scripts/launcher.sh`
2. Выберите "3" - Простая версия v3
3. Выберите книги для скачивания
4. Получите MP3 файлы в `downloads/mp3_audiobooks/`

### Для разработчиков
```bash
# Тестирование
python tests/test_core.py

# Статистика
python src/utils/stats.py

# Прямой запуск компонентов
python src/utils/simple_downloader_v3.py
```

## 📥 Результат

- 📁 `downloads/mp3_audiobooks/` - MP3 файлы
- 🎵 `Автор-Название.mp3` - понятные имена
- 🎧 192 kbps качество
- 📊 Статистика загрузок

## 🔧 Требования

- **Python** 3.8+
- **ffmpeg** (для MP3 конвертации)
- **Интернет** соединение
- **ОС**: Windows, macOS, Linux

## 🛡️ Приватность

- ✅ Ваши списки книг остаются **локальными**
- ✅ Файл `data/books.txt` в `.gitignore`
- ✅ Папка `downloads/` не синхронизируется
- ✅ Логи и статистика приватны

## 🧪 Тестирование

```bash
# Проверка всех компонентов
python tests/test_core.py

# Тест простой версии
python src/utils/simple_downloader_v3.py --test

# Статистика
python src/utils/stats.py
```

## 📚 Документация

- 📖 [Полное руководство](README.md)
- ⚡ [Быстрый старт](QUICKSTART.md)
- 🔧 [Настройка после клонирования](SETUP.md)
- 📊 [Статус проекта](PROJECT_STATUS.md)
- 🆘 [Решение проблем](docs/TROUBLESHOOTING.md)

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Отправьте Pull Request

## 📄 Лицензия

MIT License - используйте свободно!

## ⭐ Поддержка

Если проект был полезен, поставьте звезду! ⭐

---

**🎧 Наслаждайтесь аудиокнигами в высоком качестве!**

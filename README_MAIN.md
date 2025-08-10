# 🎧 Audiobook Downloader v3.1

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Cross-Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/YOUR_USERNAME/audiobook-downloader)

> 🔥 **Мощный инструмент для автоматического поиска и скачивания аудиокниг с YouTube в MP3 формате**

## ✨ Особенности

- 🎵 **MP3 конвертация** - Высокое качество 192 kbps
- 📚 **Умный парсинг** - Простой формат `Автор - Название`
- 🔍 **YouTube поиск** - Автоматический поиск аудиокниг
- 📁 **Организация файлов** - Структурированное хранение по авторам
- 🖥️ **Множественные интерфейсы** - Консоль, GUI, скрипты
- 🌍 **Полная локализация** - Поддержка русских символов
- 🔒 **Приватность** - Ваши списки книг остаются локальными

## 🚀 Быстрый старт

### 1. Установка
```bash
git clone https://github.com/YOUR_USERNAME/audiobook-downloader.git
cd audiobook-downloader
chmod +x scripts/*.sh
./scripts/install.sh
```

### 2. Настройка
```bash
# Создайте свой список книг
cp data/books_example.txt data/books.txt
# Отредактируйте data/books.txt
```

### 3. Запуск
```bash
./scripts/launcher.sh
```

## 🎯 Интерфейсы

### 🖥️ Консольный (рекомендуется)
```bash
python console.py
```
- Rich UI с прогресс-барами
- Интерактивные меню
- Цветной вывод

### 🪟 Графический интерфейс
```bash
python gui_launcher.py
```
- Tkinter приложение
- Простое управление
- Drag & drop поддержка

### 🔧 Простой загрузчик
```bash
python src/utils/simple_downloader_v3.py
```
- Минималистичный интерфейс
- Быстрая настройка
- Автономная работа

## 📁 Структура проекта

```
audiobook-downloader/
├── 🚀 console.py              # Главный launcher
├── 🪟 gui_launcher.py         # GUI launcher
├── 📋 requirements.txt        # Зависимости
├── 📂 src/                    # Исходный код
│   ├── 🎧 audiobook_downloader/   # Основной движок
│   ├── ⚙️ config/                 # Конфигурация
│   ├── 🖥️ gui/                    # GUI интерфейс
│   ├── 🚀 launchers/              # Точки входа
│   └── 🛠️ utils/                  # Утилиты
├── 📂 scripts/                # Bash скрипты
├── 📂 tests/                  # Тесты
├── 📂 docs/                   # Документация
├── 📂 data/                   # Списки книг (приватно)
├── 📂 downloads/              # Загрузки (приватно)
└── 📂 logs/                   # Логи (приватно)
```

## 📚 Формат списка книг

Создайте файл `data/books.txt`:

```text
# Комментарии начинаются с #
## 🌍 Зарубежная фантастика

Фрэнк Герберт - Дюна
Толкин - Властелин колец
Азимов - Основание

## 🇷🇺 Российская фантастика

Лукьяненко - Ночной дозор
Стругацкие - Пикник на обочине
```

## 🎵 Результат

```
downloads/
└── russian_fantasy/
    └── Frenk_Gerbert/
        ├── Фрэнк_Герберт-Дюна.mp3     # 🎵 Аудио
        ├── Фрэнк_Герберт-Дюна.webp    # 🖼️ Обложка
        └── Фрэнк_Герберт-Дюна.info.json  # 📄 Метаданные
```

## 🔧 Требования

- **Python 3.11+**
- **ffmpeg** (для конвертации в MP3)
- **Интернет соединение**

### Автоматическая установка зависимостей
```bash
./scripts/install.sh
```

### Ручная установка
```bash
pip install -r requirements.txt
```

## 🧪 Тестирование

```bash
# Все тесты
python -m pytest tests/ -v

# Быстрая проверка
python tests/test_core.py
```

## 📊 Статистика

```bash
python src/utils/stats.py
```

```
📊 СТАТИСТИКА MP3 АУДИОКНИГ
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Название                ┃ Размер  ┃ Дата        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━┩
│ Фрэнк_Герберт-Дюна.mp3  │ 600 MB  │ 11.08 01:43 │
└─────────────────────────┴─────────┴─────────────┘
```

## 🔒 Приватность

### ✅ Что НЕ публикуется в git:
- 🚫 Ваши списки книг (`data/books.txt`)
- 🚫 Скачанные аудиофайлы (`downloads/`)
- 🚫 Логи активности (`logs/`)
- 🚫 Временные файлы и кэш

### ✅ Что публикуется:
- ✅ Исходный код программы
- ✅ Документация и примеры
- ✅ Скрипты установки
- ✅ Структура папок (пустые)

## 📖 Документация

- 📋 [**Руководство пользователя**](docs/USER_GUIDE.md)
- 🔧 [**Решение проблем**](docs/TROUBLESHOOTING.md)
- 🧩 [**Структура кода**](src/README.md)
- 📜 [**История изменений**](CHANGELOG.md)

## 🆘 Поддержка

### Частые проблемы
1. **Ошибка ffmpeg** → `./scripts/install.sh`
2. **Не находит книги** → Проверьте формат в `data/books.txt`
3. **Ошибки скачивания** → Проверьте логи `logs/audiobook_downloader.log`

### Отладка
```bash
# Проверка зависимостей
python tests/test_core.py

# Подробные логи
tail -f logs/audiobook_downloader.log

# Тестовое скачивание
python src/utils/simple_downloader_v3.py
```

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Проект распространяется под лицензией MIT. См. [LICENSE](LICENSE) для подробностей.

## 🎉 Благодарности

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - За отличный загрузчик
- [Rich](https://github.com/Textualize/rich) - За красивый консольный интерфейс
- [FFmpeg](https://ffmpeg.org/) - За конвертацию аудио

---

⭐ **Поставьте звезду, если проект был полезен!**

🔗 **[Скачать последнюю версию](https://github.com/YOUR_USERNAME/audiobook-downloader/releases)**

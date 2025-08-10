# 🎧 Audiobook Downloader v3.1

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Cross-Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/YOUR_USERNAME/audiobook-downloader)

> 🔥 **Мощный инструмент для автоматического поиска и скачивания аудиокниг с YouTube в MP3 формате**

## ✨ Особенности

- 🎵 **MP3 конвертация** - Высокое качество 192 kbps
- 📚 **Умный парсинг** - Простой формат `Автор - Название`
- 🔍 **YouTube поиск** - Автоматический поиск аудиокниг
- 📁 **Организация файлов** - Структурированное хранение по авторам и категориям
- 🖥️ **Множественные интерфейсы** - Консоль, GUI, простая версия
- 🌍 **Кириллица** - Полная поддержка русских символов с транслитерацией
- 🔒 **Приватность** - Ваши списки книг остаются локальными
- 🛡️ **Безопасность** - Никаких личных данных в репозитории

## 🚀 Быстрый старт

### 1. Установка
```bash
git clone https://github.com/YOUR_USERNAME/audiobook-downloader.git
cd audiobook-downloader
chmod +x scripts/*.sh
pip install -r requirements.txt
```

### 2. Настройка
```bash
# Создайте свой список книг
cp data/books_example.txt data/books.txt
# Отредактируйте data/books.txt своими книгами
```

### 3. Запуск
```bash
# 🎛️ Главное меню (рекомендуется)
./scripts/launcher.sh

# 🎧 Простая версия (лучший выбор для новичков)
python src/utils/simple_downloader_v3.py

# 🖥️ Консольная версия (полный функционал)
python console.py

# 🪟 GUI версия
python gui_launcher.py
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
- Tkinter GUI
- Простое управление
- Интуитивный интерфейс

### ⚡ Простая версия
```bash
python src/utils/simple_downloader_v3.py
```
- Минимальная настройка
- Быстрый старт
- Идеально для новичков

## 📁 Структура проекта

```
audiobook-downloader/
├── 📄 console.py               # Консольный лаунчер
├── 📄 gui_launcher.py         # GUI лаунчер  
├── 📄 README.md               # Документация
├── 📄 requirements.txt        # Зависимости
│
├── 📁 src/                    # Исходный код
│   ├── 📁 audiobook_downloader/ # Основной движок
│   ├── 📁 config/             # Конфигурация
│   ├── 📁 gui/                # Графический интерфейс
│   ├── 📁 launchers/          # Внутренние лаунчеры
│   └── 📁 utils/              # Утилиты
│       ├── simple_downloader_v3.py  # ⭐ Простая версия
│       ├── stats.py                 # 📊 Статистика
│       └── youtube_handler.py       # 📺 YouTube
│
├── 📁 data/                   # Данные пользователя
│   ├── books_example.txt      # 📖 Пример списка книг
│   └── books.txt              # 📝 Ваш список (создать)
│
├── 📁 downloads/              # Загрузки
│   ├── 📁 mp3_audiobooks/     # 🎵 Простые MP3
│   └── 📁 russian_fantasy/    # 📚 Структурированные по категориям
│       └── 📁 Author_Name/    # Папки авторов (транслитерация)
│
├── 📁 scripts/                # Bash скрипты
│   ├── launcher.sh            # 🎛️ Главное меню
│   └── install.sh             # ⚙️ Установка
│
├── 📁 tests/                  # Тестирование
├── 📁 docs/                   # Документация
└── 📁 logs/                   # Логи работы
```

## 💾 Результат работы

После запуска вы получите:
- 🎵 **MP3 файлы** в высоком качестве (192 kbps)
- 📁 **Организованную структуру** по авторам и категориям
- 🖼️ **Обложки книг** (webp формат)
- 📄 **Метаданные** (JSON файлы с информацией)
- 📊 **Статистику** загрузок

## 🔧 Требования

- **Python 3.11+**
- **ffmpeg** (для конвертации в MP3)
- **Интернет** соединение
- **4GB+ свободного места** (для загрузок)

### Установка ffmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Скачайте с https://ffmpeg.org/
```

## 📖 Формат списка книг

Создайте файл `data/books.txt` в простом формате:

```txt
# 📚 Мой список аудиокниг

## 🌍 Зарубежная фантастика
Фрэнк Герберт - Дюна
Толкин - Властелин колец
Азимов - Основание

## 🇷🇺 Российская фантастика  
Лукьяненко - Ночной дозор
Стругацкие - Пикник на обочине
```

## 📊 Статистика и мониторинг

```bash
# Анализ скачанных файлов
python src/utils/stats.py

# Логи работы
tail -f logs/audiobook_downloader.log

# Тестирование системы
python -m pytest tests/
```

## 🛠️ Расширенное использование

### 🔧 Консольные команды
```bash
# Скачать с определенного номера
python console.py --start 5

# Ограничить количество
python console.py --limit 3

# Простая версия с опциями
python src/utils/simple_downloader_v3.py --range 1-5
```

### 📁 Организация загрузок
- **Простые имена**: `downloads/mp3_audiobooks/Автор-Книга.mp3`
- **По категориям**: `downloads/russian_fantasy/Author_Name/Автор-Книга.mp3`
- **Метаданные**: `downloads/.../Автор-Книга.info.json`
- **Обложки**: `downloads/.../Автор-Книга.webp`

## 🆘 Решение проблем

### ❓ Частые проблемы
- **Нет ffmpeg**: `brew install ffmpeg` (macOS) или скачайте с официального сайта
- **Ошибки кодировки**: Используйте UTF-8 в файле `books.txt`
- **Медленная скорость**: Используйте VPN при блокировках YouTube

### 📚 Документация
- 📖 **Полная документация**: `docs/`
- ⚡ **Быстрый старт**: `QUICKSTART.md`
- 🔧 **Решение проблем**: `docs/TROUBLESHOOTING.md`
- 📝 **История изменений**: `CHANGELOG.md`

## 🤝 Контрибьюция

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add: AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📜 Лицензия

Проект распространяется под лицензией **MIT**. Подробности в файле [LICENSE](LICENSE).

## 🌟 Благодарности

- **yt-dlp** - за отличную библиотеку для загрузки с YouTube
- **Rich** - за красивый терминальный интерфейс
- **Python сообщество** - за поддержку и библиотеки

---

⭐ **Если проект был полезен, поставьте звезду!** ⭐

🚀 **Начните с: `./scripts/launcher.sh`**

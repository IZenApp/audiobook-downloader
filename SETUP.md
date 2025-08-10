# 🚀 Настройка после клонирования

После клонирования репозитория выполните следующие шаги:

## 1. 📚 Настройка списка книг

```bash
# Скопируйте пример и создайте свой список
cp data/books_example.txt data/books.txt

# Отредактируйте файл со своими книгами
nano data/books.txt
```

## 2. 🐍 Создание виртуального окружения

```bash
# Создание виртуального окружения
python3 -m venv .venv

# Активация
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

## 3. 🎵 Установка ffmpeg

### macOS:
```bash
brew install ffmpeg
```

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows:
Скачайте с [ffmpeg.org](https://ffmpeg.org/download.html)

## 4. 🚀 Первый запуск

```bash
# Запуск главного меню
./scripts/launcher.sh

# Или запуск простой версии
python src/utils/simple_downloader_v3.py
```

## 🔒 Приватность

Файл `data/books.txt` добавлен в `.gitignore` - ваши книги останутся приватными!

## 📁 Структура

- `data/books_example.txt` - пример формата файла
- `data/books.txt` - ваш личный список (создайте сами)
- `downloads/` - папка для скачанных MP3 файлов

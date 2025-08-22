# 🎧 Audiobook Downloader v3.1

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Cross-Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/YOUR_USERNAME/audiobook-downloader)

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

**🐧 Linux/macOS:**
```bash
git clone https://github.com/YOUR_USERNAME/audiobook-downloader.git
cd audiobook-downloader
chmod +x scripts/*.sh
pip install -r requirements.txt
```

**🪟 Windows:**
```cmd
git clone https://github.com/YOUR_USERNAME/audiobook-downloader.git
cd audiobook-downloader
pip install -r requirements.txt
```

### 2. Настройка
```bash
# Создайте свой список книг
cp data/books_example.txt data/books.txt
# Отредактируйте data/books.txt своими книгами
```

### 3. Запуск

**🐧 Linux/macOS:**
```bash
# 🎯 Самый простой способ - главное меню
./scripts/launcher.sh

# 🖥️ Или прямой запуск консольной версии
./scripts/run_console.sh

# 🪟 Или GUI версия
./scripts/run_gui.sh
```

**🪟 Windows:**
```cmd
# 🖥️ Консольная версия
python launchers\console.py

# 🪟 GUI версия
python launchers\gui_launcher.py
```

## 🎯 Интерфейсы

### 4. Выбор интерфейса

**🎯 Консольная версия (рекомендуется):**
```bash
./scripts/run_console.sh
```
- Rich UI с прогресс-барами
- Интерактивные меню
- Цветной вывод

### 🪟 Графический интерфейс
```bash
python launchers/gui_launcher.py
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
├── 📄 README.md               # Документация
├── 📄 requirements.txt        # Зависимости
│
├── 📁 config/                 # Конфигурация
├── 📁 data/                   # Списки книг, примеры
│   ├── books_example.txt      # Пример списка книг
│   └── README.md
├── 📁 docs/                   # Документация и гайды
│   ├── USER_GUIDE.md
│   ├── TROUBLESHOOTING.md
│   └── LICENSE
├── 📁 downloads/              # Скачанные аудиокниги
│   └── mp3_audiobooks/
├── 📁 launchers/              # Лаунчеры (альтернативные)
│   ├── console.py             # Консольный лаунчер
│   └── gui_launcher.py        # GUI лаунчер
├── 📁 logs/                   # Логи работы
│   └── audiobook_downloader.log
├── 📁 scripts/                # Скрипты запуска и установки
│   ├── launcher.sh            # Главное меню
│   ├── run_console.sh         # Быстрый запуск консоли
│   ├── run_gui.sh             # Быстрый запуск GUI
│   └── install.sh             # Установка зависимостей
├── 📁 src/                    # Исходный код
│   ├── audiobook_downloader/  # Основная логика
│   ├── config/                # Конфиг загрузчика
│   ├── gui/                   # GUI приложение
│   ├── launchers/             # Лаунчеры
│   └── utils/                 # Утилиты (YouTube, статистика и пр.)
├── 📁 tests/                  # Тесты
│   ├── test_core.py
│   └── test_parser.py
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

**🐧 Linux/macOS:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

**🪟 Windows (подробная инструкция):**

**Способ 1 (самый простой) - через Windows Package Manager:**
```cmd
winget install ffmpeg
```

**Способ 2 - ручная установка:**
1. Перейдите на [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Выберите "Windows" → "Windows builds by BtbN" или "gyan.dev"
3. Скачайте "release build" (архив .zip)
4. Распакуйте в папку `C:\ffmpeg`
5. Добавьте `C:\ffmpeg\bin` в системную переменную PATH:
   - Нажмите Win + R, введите `sysdm.cpl`
   - Вкладка "Дополнительно" → "Переменные среды"
   - В "Системные переменные" найдите "Path" → "Изменить"
   - "Создать" → введите `C:\ffmpeg\bin` → "ОК"
6. Перезапустите командную строку

**Способ 3 - локальная установка (не требует прав администратора):**
1. Создайте папку `ffmpeg` в корневой директории проекта
2. Скачайте ffmpeg и поместите `ffmpeg.exe` в эту папку
3. Структура: `audiobook-downloader/ffmpeg/ffmpeg.exe`

**Проверка установки:**
```cmd
ffmpeg -version
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
# Примеры запуска с параметрами
./scripts/run_console.sh --start 5  # Начать с 5-й книги
./scripts/run_console.sh --limit 3  # Скачать только 3 книги

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

**🐧 Linux/macOS:**
- **Нет ffmpeg**: `brew install ffmpeg` или `sudo apt install ffmpeg`
- **Права доступа**: `chmod +x scripts/*.sh`

**🪟 Windows:**
- **❌ Ошибка: "ffmpeg не найден"**
  - Убедитесь, что ffmpeg добавлен в PATH (способ 1 или 2 выше)
  - Или используйте локальную установку (способ 3)
  - Перезапустите командную строку после изменения PATH
- **❌ Ошибка: "Python не найден"**
  - Переустановите Python с галочкой "Add Python to PATH"
  - Или используйте полный путь: `C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python3X\python.exe`
- **❌ Проблемы с кодировкой (кракозябры в консоли)**
  ```cmd
  chcp 65001
  ```
- **❌ Ошибки при установке зависимостей**
  ```cmd
  python -m pip install --upgrade pip
  pip install -r requirements.txt --user
  ```
- **❌ Антивирус блокирует скачивание**
  - Добавьте папку проекта в исключения антивируса
  - Временно отключите реальную защиту при первом запуске

**Общие проблемы:**
- **Ошибки кодировки**: Используйте UTF-8 в файле `books.txt`
- **Медленная скорость**: Используйте VPN при блокировках YouTube

### 📚 Документация
- 📖 **Полная документация**: `docs/`
- 🔧 **Решение проблем**: `docs/TROUBLESHOOTING.md`

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

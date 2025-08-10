# 🎧 Audiobook Downloader v2.0 - Полное руководство

## 📁 Структура проекта
```
audiobook-downloader/
├── 🎯 Точки входа
│   ├── console.py              # Консольная версия
│   ├── gui_launcher.py         # GUI версия
│   └── utils/robust_downloader.py  # Улучшенная версия
├── 🔧 Скрипты
│   └── scripts/launcher.sh     # Главное меню
├── 📦 Пакеты
│   ├── audiobook_downloader/   # Основная логика
│   ├── gui/                    # Графический интерфейс
│   ├── utils/                  # Утилиты и обходы
│   └── config/                 # Настройки
└── 📚 Данные
    ├── data/books.txt          # Список книг
    ├── downloads/              # Скачанные файлы
    └── logs/                   # Логи
```

## 🚀 Способы запуска

### 1. Главное меню (рекомендуется)
```bash
./scripts/launcher.sh
```
- Красивое меню с выбором режимов
- Автоматическая активация окружения
- Встроенная справка

### 2. Прямой запуск
```bash
# Консольная версия (обычная)
python console.py

# GUI версия  
python gui_launcher.py

# Улучшенная версия (при проблемах с YouTube)
python utils/robust_downloader.py
```

### 3. Через скрипты
```bash
./scripts/run_console.sh    # Консоль
./scripts/run_gui.sh        # GUI
```

## 🎯 Режимы работы

### Консольный режим
- 🎨 Красивый интерфейс с Rich
- 📊 Прогресс-бары в реальном времени
- 🎯 Интерактивный выбор диапазона
- 📈 Статистика в реальном времени

### GUI режим
- 🖱️ Удобный графический интерфейс
- 📋 Таблица со списком всех книг
- ⚙️ Настройки начальной позиции и лимитов
- 📝 Лог операций в отдельном окне

### Улучшенный режим
- 🛡️ Обход блокировок YouTube
- 🔍 Множественные стратегии поиска
- 🔄 Автоматические повторы при ошибках
- 📊 Детальная отчетность по ошибкам

## 📚 Формат файла books.txt

```
# 🌍 Зарубежная фантастика
1. Дуглас Адамс - Автостопом по галактике | Чтец: Игорь Князев (2005)
2. Айзек Азимов - Основание | Чтец: Владимир Самойлов (2008)

# 🔍 Зарубежные детективы  
3. Агата Кристи - Убийство в Восточном экспрессе | Чтец: Татьяна Телегина (2010)
```

**Формат строки:**
`ID. Автор - Название | Чтец: Имя (Год)`

## 🗂️ Организация файлов

Скачанные файлы автоматически сортируются:

```
downloads/
├── foreign_fantasy/           # Зарубежная фантастика
│   └── Douglas_Adams/
│       └── Avtostopom_po_galaktike_Igor_Knyazev_2005.mp3
├── foreign_detective/         # Зарубежные детективы
│   └── Agatha_Christie/
├── russian_fantasy/           # Российская фантастика
│   └── Strugatsky_Brothers/
└── russian_detective/         # Российские детективы
    └── Boris_Akunin/
```

## 🚨 Решение проблем

### YouTube блокирует загрузки (HTTP 403)
```bash
# Используйте улучшенную версию
python utils/robust_downloader.py

# Или через меню: опция 3
./scripts/launcher.sh
```

### Проблемы с зависимостями
```bash
# Переустановка
./scripts/install.sh

# Проверка
python tests/test_core.py
```

### Проблемы с поиском
1. Убедитесь что названия точные
2. Проверьте интернет-соединение
3. Попробуйте позже (блокировки временные)

## 📊 Мониторинг и статистика

```bash
# Статистика скачиваний
python utils/stats.py

# Структура файлов
ls -la downloads/

# Логи ошибок
tail -f logs/audiobook_downloader.log
```

## ⚙️ Настройка

### Качество аудио
Отредактируйте `config/downloader_config.py`:
```python
YDL_CONFIG = {
    'audioquality': '320',  # Изменить качество
    'audioformat': 'mp3',   # Формат
}
```

### Поисковые запросы
Добавьте свои паттерны в `SEARCH_PATTERNS`.

### Источники
Настройте `TRUSTED_SOURCES` для приоритетных сайтов.

## 🔧 Продвинутое использование

### Запуск одной книги
```bash
python -c "
from audiobook_downloader import AudiobookParser
from utils.robust_downloader import RobustAudiobookDownloader

parser = AudiobookParser('data/books.txt')
books = parser.parse()
book = next(b for b in books if b.id == 1)

downloader = RobustAudiobookDownloader()
downloader.download_book_robust(book)
"
```

### Пакетная обработка
```python
# В Python скрипте
filtered_books = [b for b in books if 'фантастика' in b.category.lower()]
for book in filtered_books:
    downloader.download_book_robust(book)
```

## 📝 Логирование

Логи сохраняются в `logs/audiobook_downloader.log`:
- ✅ Успешные загрузки
- ❌ Ошибки и их причины  
- 🔍 Поисковые запросы
- ⏱️ Время выполнения операций

## 🔄 Обновление

```bash
# Получить последние изменения
git pull origin main

# Переустановить зависимости
./scripts/install.sh

# Проверить работоспособность
python tests/test_core.py
```

---
🎧 **Готово! Теперь вы знаете все возможности загрузчика!** 📚

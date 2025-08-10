# 📖 Документация Audiobook Downloader

## Содержание

1. [Быстрый старт](quick-start.md)
2. [API Documentation](api.md)
3. [Troubleshooting](troubleshooting.md)
4. [Примеры использования](examples.md)

## Архитектура проекта

### Основные компоненты

- **AudiobookParser** - парсинг списка книг
- **AudiobookDownloader** - загрузка файлов
- **BookInfo** - модель данных книги

### Поток данных

```
books.txt → Parser → BookInfo[] → Downloader → MP3 files
```

## Расширение функциональности

### Добавление нового источника

1. Создайте класс наследник от `BaseSearchProvider`
2. Реализуйте метод `search(query: str) -> List[str]`
3. Добавьте в `AudiobookDownloader.search_providers`

### Новые форматы файлов

Измените настройки `ydl_opts` в классе `AudiobookDownloader`:

```python
'audioformat': 'flac',  # Для FLAC
'audioquality': '0',    # Для lossless
```

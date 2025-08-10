# 📁 Config Directory

Эта папка содержит конфигурационные файлы для настройки работы Audiobook Downloader.

## Файлы конфигурации

### settings.json
```json
{
  "download_settings": {
    "quality": "192",
    "format": "mp3",
    "max_concurrent_downloads": 1,
    "retry_attempts": 3,
    "pause_between_downloads": 5
  },
  "search_settings": {
    "youtube_results_limit": 5,
    "google_results_limit": 10,
    "min_duration_seconds": 1800
  },
  "paths": {
    "downloads_dir": "../downloads",
    "logs_dir": "../logs",
    "data_dir": "../data"
  }
}
```

### filters.json
```json
{
  "title_filters": [
    "полная версия",
    "аудиокнига",
    "слушать онлайн"
  ],
  "excluded_keywords": [
    "трейлер",
    "обзор",
    "реклама",
    "отрывок"
  ],
  "preferred_narrators": [
    "Сергей Чонишвили",
    "Александр Клюквин",
    "Ксения Бржезовская"
  ]
}
```

## Использование

Эти файлы могут быть использованы для тонкой настройки поведения скрипта без изменения исходного кода.

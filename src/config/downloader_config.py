#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🛠️ Конфигурация для Audiobook Downloader
Настройки обходных путей для YouTube и альтернативных источников
"""

# Конфигурация yt-dlp для обхода блокировок YouTube с MP3 конвертацией
YDL_CONFIG = {
    'format': 'bestaudio/best',
    'ignoreerrors': True,
    'no_warnings': False,  # Включаем предупреждения для отладки
    'noplaylist': True,
    'extract_flat': False,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'writeinfojson': False,
    'writethumbnail': False,
    
    # Обходные пути для YouTube блокировок
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web'],
            'skip': ['dash', 'hls']
        }
    },
    
    # Дополнительные опции для стабильности
    'retries': 3,
    'socket_timeout': 30,
    'http_chunk_size': 1048576,  # 1MB chunks
}

# Альтернативные поисковые запросы
SEARCH_PATTERNS = [
    # Основной формат
    '"{author} {title}" {narrator} аудиокнига',
    # Без чтеца
    '"{author} {title}" аудиокнига полная',
    # Упрощенный
    '{author} {title} аудиокнига',
    # С дополнительными ключевыми словами
    '"{author} {title}" аудиокнига слушать',
    # Альтернативный формат
    'аудиокнига {author} {title}',
]

# Список надежных источников аудиокниг
TRUSTED_SOURCES = [
    'youtube.com',
    'youtu.be',
    'vk.com',
    'ok.ru',
    'archive.org',
    'soundcloud.com'
]

# Фильтры для улучшения поиска
SEARCH_FILTERS = [
    'длинн',  # длинная версия
    'полн',   # полная версия  
    'целик',  # целиком
    'весь',   # вся книга
    'часть 1', # первая часть
    'глава 1'  # первая глава
]

# Исключения (плохие результаты)
EXCLUDE_TERMS = [
    'краткое содержание',
    'пересказ',
    'анонс',
    'трейлер',
    'отрывок',
    'фрагмент'
]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 Утилиты для работы с YouTube и обходом блокировок
"""

import time
import random
import requests
from typing import List, Optional, Dict, Any
from pathlib import Path
import logging

class YouTubeErrorHandler:
    """Класс для обработки ошибок YouTube и поиска обходных путей"""
    
    def __init__(self):
        self.failed_attempts = {}
        self.max_retries = 3
        self.base_delay = 2
        
    def should_retry(self, url: str, error_type: str) -> bool:
        """Определяет, стоит ли повторить попытку"""
        key = f"{url}_{error_type}"
        current_attempts = self.failed_attempts.get(key, 0)
        
        if current_attempts >= self.max_retries:
            return False
            
        self.failed_attempts[key] = current_attempts + 1
        return True
    
    def get_retry_delay(self, attempt: int) -> float:
        """Получить задержку перед повтором с экспоненциальным бэкоффом"""
        delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
        return min(delay, 30)  # Максимум 30 секунд
    
    def is_youtube_blocked(self, error_msg: str) -> bool:
        """Проверка, связана ли ошибка с блокировкой YouTube"""
        blocking_indicators = [
            'HTTP Error 403',
            'HTTP Error 429',
            'Sign in to confirm',
            'Video unavailable',
            'Private video',
            'age-restricted',
            'SABR streaming'
        ]
        
        return any(indicator.lower() in error_msg.lower() for indicator in blocking_indicators)

class ImprovedSearcher:
    """Улучшенный поисковик с множественными стратегиями"""
    
    def __init__(self):
        self.error_handler = YouTubeErrorHandler()
        
    def search_with_fallbacks(self, book_info: dict, max_results: int = 10) -> List[str]:
        """Поиск с резервными стратегиями"""
        try:
            from googlesearch import search
        except ImportError:
            print("❌ Библиотека googlesearch-python не установлена")
            return []
        
        search_queries = self._generate_search_queries(book_info)
        all_results = []
        
        for i, query in enumerate(search_queries):
            try:
                print(f"🔍 Поиск {i+1}/{len(search_queries)}: {query[:50]}...")
                
                # Пробуем разные варианты API
                try:
                    # Новый API (только обязательные параметры)
                    results = list(search(query, num_results=max_results, sleep_interval=2))
                except TypeError:
                    try:
                        # Старый API
                        results = list(search(query, num=max_results, stop=max_results, pause=2))
                    except TypeError:
                        # Самый простой вариант
                        results = list(search(query))[:max_results]
                
                # Фильтруем результаты
                filtered_results = self._filter_results(results, book_info)
                all_results.extend(filtered_results)
                
                if len(all_results) >= 3:  # Достаточно результатов
                    break
                    
            except Exception as e:
                print(f"⚠️ Ошибка поиска: {e}")
                time.sleep(3)  # Пауза перед следующей попыткой
                continue
                time.sleep(3)  # Пауза перед следующей попыткой
                continue
        
        # Удаляем дубликаты, сохраняя порядок
        unique_results = []
        seen = set()
        for url in all_results:
            if url not in seen:
                unique_results.append(url)
                seen.add(url)
        
        return unique_results[:max_results]
    
    def _generate_search_queries(self, book_info: dict) -> List[str]:
        """Генерация множественных поисковых запросов"""
        author = book_info.get('author', '')
        title = book_info.get('title', '')
        narrator = book_info.get('narrator', '')
        
        queries = []
        
        # Основные запросы
        if narrator:
            queries.extend([
                f'"{author} {title}" {narrator} аудиокнига',
                f'аудиокнига {author} {title} {narrator}',
                f'{title} {author} читает {narrator}'
            ])
        
        # Запросы без чтеца
        queries.extend([
            f'"{author} {title}" аудиокнига полная',
            f'аудиокнига {author} {title} слушать онлайн',
            f'{title} {author} аудиокнига скачать'
        ])
        
        # Упрощенные запросы
        queries.extend([
            f'{author} {title} аудиокнига',
            f'{title} аудиокнига {author}'
        ])
        
        return queries
    
    def _filter_results(self, results: List[str], book_info: dict) -> List[str]:
        """Фильтрация результатов по релевантности"""
        filtered = []
        author = book_info.get('author', '').lower()
        title = book_info.get('title', '').lower()
        
        for url in results:
            # Проверяем, что URL содержит ключевые слова
            url_lower = url.lower()
            
            # Приоритет YouTube и другим надежным источникам
            trusted_sources = ['youtube.com', 'youtu.be', 'vk.com', 'ok.ru']
            is_trusted = any(source in url_lower for source in trusted_sources)
            
            # Проверяем релевантность
            has_author = any(word in url_lower for word in author.split())
            has_title = any(word in url_lower for word in title.split())
            has_audiobook = any(word in url_lower for word in ['аудиокнига', 'audiobook', 'audio'])
            
            # Исключаем плохие результаты
            exclude_terms = ['краткое', 'пересказ', 'анонс', 'трейлер']
            is_excluded = any(term in url_lower for term in exclude_terms)
            
            if is_trusted and (has_author or has_title) and has_audiobook and not is_excluded:
                filtered.append(url)
        
        return filtered

def create_improved_ydl_options(output_path: Path) -> Dict[str, Any]:
    """Создание улучшенных опций для yt-dlp с обходом блокировок"""
    
    return {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'no_warnings': False,
        'extractaudio': True,
        'audioformat': 'mp3',
        'audioquality': '192',
        'writeinfojson': False,
        'writethumbnail': False,
        'noplaylist': True,
        'extract_flat': False,
        
        # Обходные пути для YouTube
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'ios'],
                'skip': ['dash', 'hls'],
                'player_skip': ['configs'],
            }
        },
        
        # Настройки сети
        'retries': 5,
        'socket_timeout': 60,
        'http_chunk_size': 1048576,
        
        # User-Agent для обхода блокировок
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        }
    }

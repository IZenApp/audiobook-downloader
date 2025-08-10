#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎧 Audiobook Downloader Package
Пакет для загрузки аудиокниг из различных источников
"""

from .core import AudiobookParser, AudiobookDownloader, BookInfo

__version__ = "2.0.0"
__author__ = "Audiobook Downloader Team"
__description__ = "Автоматический загрузчик аудиокниг с поиском в Google и YouTube"

__all__ = [
    'AudiobookParser',
    'AudiobookDownloader', 
    'BookInfo'
]

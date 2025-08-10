# 🚨 Решение проблем с YouTube и Google Search

## Проблема: HTTP Error 403 Forbidden

YouTube активно блокирует автоматические загрузки. Мы создали несколько решений:

### 🔧 Решение 1: Простая версия (рекомендуется)

```bash
# Простая версия без Google Search - самый надежный способ
python utils/simple_downloader.py

# Или через меню: пункт 4
./scripts/launcher.sh
```

### 🔧 Решение 2: Улучшенный загрузчик

```bash
# Используйте улучшенную версию с обходом блокировок
python utils/robust_downloader.py

# Или через меню: пункт 3
./scripts/launcher.sh
```

## Проблема: Google Search API ошибки

Если видите `search() got an unexpected keyword argument 'num'`:

1. **Используйте простую версию** (без Google Search):
   ```bash
   python utils/simple_downloader.py
   ```

2. **Переустановите Google Search**:
   ```bash
   pip uninstall googlesearch-python
   pip install googlesearch-python==1.2.3
   ```

3. **Альтернативная библиотека**:
   ```bash
   pip install google
   ```

### 🔧 Решение 3: Обновление yt-dlp

```bash
# Обновите yt-dlp до последней версии
source .venv/bin/activate
pip install --upgrade yt-dlp
```

### 🔧 Решение 4: Ручной поиск

Если автоматический поиск не работает:

1. Найдите аудиокнигу вручную на YouTube
2. Скопируйте URL
3. Используйте yt-dlp напрямую:

```bash
yt-dlp -x --audio-format mp3 --audio-quality 192 "URL_ВИДЕО"
```

## Альтернативные источники

### VK.com
- Много русских аудиокниг
- Меньше блокировок

### Archive.org
- Свободные аудиокниги
- Стабильные ссылки

### SoundCloud
- Независимые загрузки
- Хорошее качество

## Советы по поиску

1. **Используйте точные названия** - копируйте названия из надежных источников
2. **Проверяйте длительность** - аудиокнига должна быть больше 30 минут  
3. **Ищите полные версии** - избегайте отрывков и пересказов
4. **Используйте имена чтецов** - это улучшает поиск

## Мониторинг статуса

```bash
# Проверить статус загрузки
python utils/stats.py

# Посмотреть логи
tail -f logs/audiobook_downloader.log
```

## Если ничего не помогает

1. Попробуйте позже - блокировки могут быть временными
2. Измените VPN/прокси если используете
3. Обновите весь проект:

```bash
git pull origin main
./scripts/install.sh
```

4. Используйте ручной режим загрузки

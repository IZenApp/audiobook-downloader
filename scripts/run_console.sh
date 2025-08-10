#!/bin/bash
# 🎧 Audiobook Downloader - Консольная версия

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🎧 Запуск консольной версии...${NC}"

# Переход в корневую папку проекта
cd "$(dirname "$0")/.."

# Активация виртуального окружения
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${GREEN}✅ Виртуальное окружение активировано${NC}"
else
    echo -e "${RED}❌ Виртуальное окружение не найдено!${NC}"
    echo -e "Запустите: ./scripts/install.sh"
    exit 1
fi

# Запуск консольной версии
python launchers/console.py

#!/bin/bash
# 🎧 Audiobook Downloader - Установка и настройка

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎧 Audiobook Downloader - Установка${NC}"
echo -e "${BLUE}======================================${NC}"

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 не найден!${NC}"
    echo -e "${YELLOW}📦 Установите Python 3.8+ и повторите попытку${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} найден${NC}"

# Проверка виртуального окружения
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}📦 Создание виртуального окружения...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✅ Виртуальное окружение создано${NC}"
fi

# Активация виртуального окружения
echo -e "${CYAN}🔧 Активация виртуального окружения...${NC}"
source .venv/bin/activate

# Обновление pip
echo -e "${CYAN}📥 Обновление pip...${NC}"
python -m pip install --upgrade pip

# Установка зависимостей
echo -e "${CYAN}📦 Установка зависимостей...${NC}"
pip install -r requirements.txt

# Проверка установки
echo -e "${CYAN}🧪 Проверка установки...${NC}"
python -c "import yt_dlp, googlesearch, rich; print('✅ Все зависимости установлены')"

# Создание необходимых директорий
echo -e "${CYAN}📁 Создание директорий...${NC}"
mkdir -p downloads logs config

# Создание файла .gitkeep для пустых папок
touch downloads/.gitkeep
touch logs/.gitkeep

echo -e "${GREEN}🎉 Установка завершена успешно!${NC}"
echo -e "${PURPLE}🚀 Запуск:${NC}"
echo -e "  ${CYAN}Консоль:${NC} ./scripts/run_console.sh"
echo -e "  ${CYAN}GUI:${NC}     ./scripts/run_gui.sh"
echo -e "  ${CYAN}Меню:${NC}    ./scripts/launcher.sh"

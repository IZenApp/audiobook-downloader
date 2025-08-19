#!/bin/bash

# 🎧 Audiobook Downloader - Главное меню
# Красивое меню для запуска всех версий загрузчика

# Цвета для красивого вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Функция для красивого заголовка
show_header() {
    clear
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${WHITE}                    🎧 Audiobook Downloader                   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${CYAN}                     Версия 3.1 - Полная                      ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Функция для показа меню
show_menu() {
    echo -e "${YELLOW}Выберите версию для запуска:${NC}"
    echo ""
    echo -e "${GREEN}1.${NC} ${WHITE}Консольная версия${NC} ${CYAN}(Основная, Rich интерфейс)${NC}"
    echo -e "${GREEN}2.${NC} ${WHITE}GUI версия${NC} ${CYAN}(Графический интерфейс)${NC}"
    echo -e "${GREEN}3.${NC} ${WHITE}Простая версия v3${NC} ${CYAN}(Рекомендуемая для MP3)${NC}"
    echo -e "${GREEN}4.${NC} ${WHITE}Продвинутая версия${NC} ${CYAN}(Обход блокировок YouTube)${NC}"
    echo ""
    echo -e "${YELLOW}5.${NC} ${WHITE}Помощь${NC} ${CYAN}(Документация)${NC}"
    echo -e "${RED}6.${NC} ${WHITE}Выход${NC}"
    echo ""
    echo -ne "${YELLOW}Ваш выбор [1-6]: ${NC}"
}

# Функция для активации виртуального окружения
activate_venv() {
    if [ -d ".venv" ]; then
        echo -e "${GREEN}🔌 Активация виртуального окружения...${NC}"
        source .venv/bin/activate
        return 0
    else
        echo -e "${RED}❌ Виртуальное окружение не найдено!${NC}"
        echo -e "${YELLOW}💡 Запустите: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt${NC}"
        return 1
    fi
}

# Функция для запуска команды с проверкой
run_command() {
    local cmd="$1"
    local description="$2"
    
    echo -e "${GREEN}🚀 Запуск: ${description}${NC}"
    echo -e "${CYAN}Команда: ${cmd}${NC}"
    echo ""
    
    if ! activate_venv; then
        return 1
    fi
    
    eval "$cmd"
    local exit_code=$?
    
    echo ""
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ Выполнено успешно!${NC}"
    else
        echo -e "${RED}❌ Ошибка выполнения (код: $exit_code)${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}Нажмите Enter для продолжения...${NC}"
    read
}

# Основной цикл меню
while true; do
    show_header
    show_menu
    
    read -r choice
    
    case $choice in
        1)
            run_command "python launchers/console.py" "Консольная версия"
            ;;
        2)
            run_command "python launchers/gui_launcher.py" "GUI версия"
            ;;
        3)
            run_command "python src/utils/simple_downloader_v3.py" "Простая версия v3 (Рекомендуемая для MP3)"
            ;;
        4)
            run_command "python src/utils/robust_downloader.py" "Продвинутая версия (Обход блокировок YouTube)"
            ;;
        5)
            show_header
            echo -e "${CYAN}📖 Документация:${NC}"
            echo ""
            echo -e "${WHITE}• README.md${NC} - Основное руководство"
            echo -e "${WHITE}• docs/USER_GUIDE.md${NC} - Подробная инструкция"
            echo -e "${WHITE}• docs/TROUBLESHOOTING.md${NC} - Решение проблем"
            echo ""
            echo -e "${YELLOW}🔗 Быстрые команды:${NC}"
            echo -e "${GREEN}source .venv/bin/activate${NC} - активация окружения"
            echo -e "${GREEN}python src/utils/simple_downloader_v3.py${NC} - самая надежная версия (MP3)"
            echo -e "${GREEN}python src/utils/robust_downloader.py${NC} - продвинутая с обходом блокировок"
            echo ""
            echo -e "${YELLOW}Нажмите Enter для продолжения...${NC}"
            read
            ;;
        6)
            echo -e "${GREEN}👋 До свидания!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Неверный выбор. Пожалуйста, введите число от 1 до 6.${NC}"
            echo -e "${YELLOW}Нажмите Enter для продолжения...${NC}"
            read
            ;;
    esac
done

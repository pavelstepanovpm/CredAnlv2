#!/bin/bash

# Единый скрипт для запуска системы аналитики кредитного портфеля
# Запускает бэкенд и фронтенд одновременно

set -e  # Остановка при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функция для вывода баннера
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                    🏦 СИСТЕМА АНАЛИТИКИ КРЕДИТНОГО ПОРТФЕЛЯ 🏦                    ║"
    echo "║                                                                              ║"
    echo "║  🚀 Запуск полной системы в режиме разработки                                ║"
    echo "║  📊 Backend: FastAPI + Quantlib                                              ║"
    echo "║  🎨 Frontend: React + TypeScript                                             ║"
    echo "║  💼 Trading Terminal Style Interface                                         ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${GREEN}🕐 Время запуска: $(date '+%d.%m.%Y %H:%M:%S')${NC}"
    echo "=================================================================================="
}

# Функция для проверки требований
check_requirements() {
    echo -e "${BLUE}🔍 Проверка требований системы...${NC}"
    
    # Проверка Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"
    else
        echo -e "${RED}❌ Python 3 не найден. Установите Python 3.8+${NC}"
        exit 1
    fi
    
    # Проверка Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        echo -e "${GREEN}✅ Node.js $NODE_VERSION${NC}"
    else
        echo -e "${RED}❌ Node.js не найден. Установите Node.js 16+${NC}"
        exit 1
    fi
    
    # Проверка npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        echo -e "${GREEN}✅ npm $NPM_VERSION${NC}"
    else
        echo -e "${RED}❌ npm не найден${NC}"
        exit 1
    fi
}

# Функция для установки зависимостей бэкенда
install_backend_deps() {
    echo -e "\n${BLUE}📦 Установка зависимостей бэкенда...${NC}"
    
    if [ ! -f "backend/requirements.txt" ]; then
        echo -e "${RED}❌ Файл backend/requirements.txt не найден${NC}"
        exit 1
    fi
    
    if python3 -m pip install -r backend/requirements.txt; then
        echo -e "${GREEN}✅ Зависимости бэкенда установлены${NC}"
    else
        echo -e "${RED}❌ Ошибка установки зависимостей бэкенда${NC}"
        exit 1
    fi
}

# Функция для установки зависимостей фронтенда
install_frontend_deps() {
    echo -e "\n${BLUE}📦 Установка зависимостей фронтенда...${NC}"
    
    if [ ! -d "frontend" ]; then
        echo -e "${RED}❌ Директория frontend не найдена${NC}"
        exit 1
    fi
    
    if [ ! -f "frontend/package.json" ]; then
        echo -e "${RED}❌ Файл frontend/package.json не найден${NC}"
        exit 1
    fi
    
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📥 Установка npm пакетов...${NC}"
        if npm install --legacy-peer-deps; then
            echo -e "${GREEN}✅ Зависимости фронтенда установлены${NC}"
        else
            echo -e "${RED}❌ Ошибка установки зависимостей фронтенда${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Зависимости фронтенда уже установлены${NC}"
    fi
    
    cd ..
}

# Функция для запуска бэкенда
start_backend() {
    echo -e "\n${BLUE}🚀 Запуск бэкенда...${NC}"
    
    # Запуск бэкенда в фоне
    python3 run_backend.py &
    BACKEND_PID=$!
    
    # Ждем запуска бэкенда
    sleep 3
    
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${GREEN}✅ Бэкенд запущен на http://localhost:8000${NC}"
        echo -e "${CYAN}📚 API документация: http://localhost:8000/docs${NC}"
    else
        echo -e "${RED}❌ Ошибка запуска бэкенда${NC}"
        exit 1
    fi
}

# Функция для запуска фронтенда
start_frontend() {
    echo -e "\n${BLUE}🎨 Запуск фронтенда...${NC}"
    
    cd frontend
    
    # Запуск фронтенда в фоне
    npm start &
    FRONTEND_PID=$!
    
    cd ..
    
    # Ждем запуска фронтенда
    sleep 5
    
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${GREEN}✅ Фронтенд запущен на http://localhost:3000${NC}"
    else
        echo -e "${RED}❌ Ошибка запуска фронтенда${NC}"
        exit 1
    fi
}

# Функция для мониторинга процессов
monitor_processes() {
    echo -e "\n${BLUE}👀 Мониторинг процессов...${NC}"
    echo -e "${YELLOW}💡 Нажмите Ctrl+C для остановки системы${NC}"
    echo "=================================================================================="
    
    # Обработчик сигналов для корректной остановки
    trap 'stop_system' INT TERM
    
    while true; do
        # Проверяем статус бэкенда
        if ! kill -0 $BACKEND_PID 2>/dev/null; then
            echo -e "${RED}❌ Бэкенд остановлен неожиданно${NC}"
            break
        fi
        
        # Проверяем статус фронтенда
        if ! kill -0 $FRONTEND_PID 2>/dev/null; then
            echo -e "${RED}❌ Фронтенд остановлен неожиданно${NC}"
            break
        fi
        
        sleep 1
    done
}

# Функция для остановки системы
stop_system() {
    echo -e "\n${YELLOW}🛑 Остановка системы...${NC}"
    
    if [ ! -z "$BACKEND_PID" ]; then
        echo -e "${BLUE}🔄 Остановка бэкенда...${NC}"
        kill $BACKEND_PID 2>/dev/null || true
        sleep 2
        kill -9 $BACKEND_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Бэкенд остановлен${NC}"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo -e "${BLUE}🔄 Остановка фронтенда...${NC}"
        kill $FRONTEND_PID 2>/dev/null || true
        sleep 2
        kill -9 $FRONTEND_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Фронтенд остановлен${NC}"
    fi
    
    echo -e "${GREEN}✅ Система остановлена${NC}"
    exit 0
}

# Основная функция
main() {
    print_banner
    
    # Проверка требований
    check_requirements
    
    # Установка зависимостей
    install_backend_deps
    install_frontend_deps
    
    # Запуск бэкенда
    start_backend
    
    # Запуск фронтенда
    start_frontend
    
    # Вывод информации о системе
    echo -e "\n${GREEN}================================================================================${NC}"
    echo -e "${GREEN}🎉 СИСТЕМА УСПЕШНО ЗАПУЩЕНА!${NC}"
    echo -e "${GREEN}================================================================================${NC}"
    echo -e "${CYAN}🌐 Фронтенд: http://localhost:3000${NC}"
    echo -e "${CYAN}🔧 Бэкенд API: http://localhost:8000${NC}"
    echo -e "${CYAN}📚 API документация: http://localhost:8000/docs${NC}"
    echo -e "${CYAN}🔍 Health check: http://localhost:8000/health${NC}"
    echo -e "${GREEN}================================================================================${NC}"
    echo -e "${YELLOW}💡 Система готова к работе!${NC}"
    echo -e "${YELLOW}🛑 Для остановки нажмите Ctrl+C${NC}"
    echo -e "${GREEN}================================================================================${NC}"
    
    # Мониторинг процессов
    monitor_processes
}

# Запуск основной функции
main "$@"

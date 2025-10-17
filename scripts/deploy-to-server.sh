#!/bin/bash

# Скрипт развертывания на удаленный сервер
# Использование: ./scripts/deploy-to-server.sh

set -e  # Остановить при ошибке

# Конфигурация
SERVER_HOST="${SERVER_HOST:-your-server.com}"
SERVER_USER="${SERVER_USER:-ubuntu}"
PROJECT_PATH="/opt/credit-analytics"
BRANCH="${BRANCH:-main}"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для вывода
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверка зависимостей
check_dependencies() {
    log_info "Проверка зависимостей..."
    
    if ! command -v git &> /dev/null; then
        log_error "Git не установлен"
        exit 1
    fi
    
    if ! command -v ssh &> /dev/null; then
        log_error "SSH не установлен"
        exit 1
    fi
    
    log_success "Все зависимости установлены"
}

# Проверка подключения к серверу
check_server_connection() {
    log_info "Проверка подключения к серверу $SERVER_HOST..."
    
    if ! ssh -o ConnectTimeout=10 -o BatchMode=yes $SERVER_USER@$SERVER_HOST exit 2>/dev/null; then
        log_error "Не удается подключиться к серверу $SERVER_HOST"
        log_info "Проверьте:"
        log_info "1. SSH ключи настроены"
        log_info "2. Сервер доступен"
        log_info "3. Пользователь $SERVER_USER существует"
        exit 1
    fi
    
    log_success "Подключение к серверу установлено"
}

# Отправка изменений в GitHub
push_to_github() {
    log_info "Отправка изменений в GitHub..."
    
    # Проверить статус Git
    if [[ -n $(git status --porcelain) ]]; then
        log_info "Обнаружены несохраненные изменения"
        
        # Добавить все изменения
        git add .
        
        # Создать коммит
        git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    # Отправить в GitHub
    if git push origin $BRANCH; then
        log_success "Изменения отправлены в GitHub"
    else
        log_error "Ошибка отправки в GitHub"
        exit 1
    fi
}

# Развертывание на сервере
deploy_to_server() {
    log_info "Развертывание на сервере..."
    
    ssh $SERVER_USER@$SERVER_HOST << EOF
        set -e
        
        echo "🔄 Переход в директорию проекта..."
        cd $PROJECT_PATH
        
        echo "📥 Получение изменений из GitHub..."
        git fetch origin
        git reset --hard origin/$BRANCH
        
        echo "🛑 Остановка контейнеров..."
        docker-compose down || true
        
        echo "🔨 Сборка новых образов..."
        docker-compose build --no-cache
        
        echo "🚀 Запуск контейнеров..."
        docker-compose up -d
        
        echo "🧹 Очистка неиспользуемых образов..."
        docker system prune -f
        
        echo "🔍 Проверка статуса..."
        docker-compose ps
        
        echo "📊 Проверка логов..."
        docker-compose logs --tail=10
EOF
    
    if [ $? -eq 0 ]; then
        log_success "Развертывание на сервере завершено"
    else
        log_error "Ошибка развертывания на сервере"
        exit 1
    fi
}

# Проверка работоспособности
health_check() {
    log_info "Проверка работоспособности приложения..."
    
    # Проверить доступность API
    if curl -s -f "https://$SERVER_HOST/api/health" > /dev/null; then
        log_success "API доступен"
    else
        log_warning "API недоступен, проверьте логи на сервере"
    fi
    
    # Проверить доступность фронтенда
    if curl -s -f "https://$SERVER_HOST" > /dev/null; then
        log_success "Фронтенд доступен"
    else
        log_warning "Фронтенд недоступен, проверьте логи на сервере"
    fi
}

# Основная функция
main() {
    echo "🚀 Развертывание системы аналитики кредитного портфеля"
    echo "=================================================="
    echo "Сервер: $SERVER_HOST"
    echo "Пользователь: $SERVER_USER"
    echo "Ветка: $BRANCH"
    echo "=================================================="
    
    # Выполнить все этапы
    check_dependencies
    check_server_connection
    push_to_github
    deploy_to_server
    health_check
    
    echo ""
    log_success "🎉 Развертывание завершено успешно!"
    echo ""
    echo "📋 Информация:"
    echo "   🌐 Приложение: https://$SERVER_HOST"
    echo "   🔧 API: https://$SERVER_HOST/api"
    echo "   📊 Документация: https://$SERVER_HOST/api/docs"
    echo ""
    echo "🔧 Управление на сервере:"
    echo "   ssh $SERVER_USER@$SERVER_HOST"
    echo "   cd $PROJECT_PATH"
    echo "   docker-compose logs -f"
    echo "   docker-compose ps"
}

# Обработка аргументов командной строки
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            SERVER_HOST="$2"
            shift 2
            ;;
        --user)
            SERVER_USER="$2"
            shift 2
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        --help)
            echo "Использование: $0 [опции]"
            echo ""
            echo "Опции:"
            echo "  --host HOST     Хост сервера (по умолчанию: your-server.com)"
            echo "  --user USER     Пользователь SSH (по умолчанию: ubuntu)"
            echo "  --branch BRANCH Ветка для развертывания (по умолчанию: main)"
            echo "  --help          Показать эту справку"
            echo ""
            echo "Переменные окружения:"
            echo "  SERVER_HOST     Хост сервера"
            echo "  SERVER_USER     Пользователь SSH"
            echo "  BRANCH          Ветка для развертывания"
            exit 0
            ;;
        *)
            log_error "Неизвестная опция: $1"
            echo "Используйте --help для справки"
            exit 1
            ;;
    esac
done

# Запуск основной функции
main

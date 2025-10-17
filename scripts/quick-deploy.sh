#!/bin/bash

# Быстрый скрипт развертывания для macOS
# Использование: ./scripts/quick-deploy.sh

set -e

# Конфигурация (настройте под ваш сервер)
SERVER_HOST="${SERVER_HOST:-your-server.com}"
SERVER_USER="${SERVER_USER:-ubuntu}"
PROJECT_PATH="/opt/credit-analytics"

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверка конфигурации
check_config() {
    if [[ "$SERVER_HOST" == "your-server.com" ]]; then
        log_error "Настройте SERVER_HOST в скрипте или переменной окружения"
        echo "Пример: export SERVER_HOST=192.168.1.100"
        exit 1
    fi
}

# Быстрое развертывание
quick_deploy() {
    log_info "🚀 Быстрое развертывание на $SERVER_HOST"
    
    # 1. Отправить в GitHub
    log_info "📤 Отправка в GitHub..."
    git add .
    git commit -m "Quick deploy: $(date)" || true
    git push origin main
    
    # 2. Развернуть на сервере
    log_info "🔄 Развертывание на сервере..."
    ssh $SERVER_USER@$SERVER_HOST << EOF
        cd $PROJECT_PATH
        git pull origin main
        docker-compose down
        docker-compose up -d
        docker system prune -f
EOF
    
    log_success "🎉 Развертывание завершено!"
    echo "🌐 Приложение: https://$SERVER_HOST"
}

# Основная функция
main() {
    check_config
    quick_deploy
}

main "$@"

#!/bin/bash

# Скрипт настройки вашего сервера 87.228.88.77
# Использование: ./scripts/setup-my-server.sh

set -e

# Конфигурация для вашего сервера
SERVER_HOST="87.228.88.77"
SERVER_USER="root"  # Подтверждено: работает с root
SSH_KEY="~/.ssh/DSkey_project"
PROJECT_PATH="/opt/credit-analytics"
DOMAIN="${DOMAIN:-87.228.88.77}"  # Можно изменить на ваш домен
EMAIL="${EMAIL:-admin@example.com}"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Проверка SSH подключения
check_ssh_connection() {
    log_info "Проверка SSH подключения к $SERVER_HOST..."
    
    # Попробуем разные пользователи
    for user in root ubuntu admin; do
        log_info "Пробуем подключиться как $user..."
        if ssh -i ~/.ssh/DSkey_project -o ConnectTimeout=10 $user@$SERVER_HOST "echo 'SSH подключение работает!'" 2>/dev/null; then
            SERVER_USER=$user
            log_success "SSH подключение работает с пользователем: $user"
            return 0
        fi
    done
    
    log_error "Не удается подключиться к серверу"
    log_info "Возможные причины:"
    log_info "1. SSH ключ не добавлен на сервер"
    log_info "2. Неправильный пользователь"
    log_info "3. Сервер недоступен"
    log_info ""
    log_info "Попробуйте добавить SSH ключ на сервер вручную:"
    echo "ssh-copy-id -i ~/.ssh/DSkey.pub $SERVER_USER@$SERVER_HOST"
    echo ""
    log_info "Или добавьте публичный ключ в ~/.ssh/authorized_keys на сервере:"
    cat ~/.ssh/DSkey.pub
    exit 1
}

# Настройка сервера
setup_server() {
    log_info "Настройка сервера $SERVER_HOST..."
    
    ssh -i ~/.ssh/DSkey_project $SERVER_USER@$SERVER_HOST << 'EOF'
        set -e
        
        echo "🔄 Обновление системы..."
        apt update && apt upgrade -y
        
        echo "🐳 Установка Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        usermod -aG docker $USER
        
        echo "🐙 Установка Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        
        echo "🌐 Установка Nginx..."
        apt install -y nginx
        
        echo "🔒 Установка дополнительных инструментов..."
        apt install -y git htop curl wget unzip ufw fail2ban
        
        echo "🔥 Настройка файрвола..."
        ufw --force enable
        ufw allow ssh
        ufw allow 80/tcp
        ufw allow 443/tcp
        
        echo "🛡️ Настройка fail2ban..."
        systemctl enable fail2ban
        systemctl start fail2ban
        
        echo "📁 Создание структуры проекта..."
        mkdir -p /opt/credit-analytics/{data/postgres,data/redis,logs,backups,scripts}
        chown -R $USER:$USER /opt/credit-analytics
        
        echo "✅ Настройка сервера завершена!"
EOF
    
    log_success "Сервер настроен успешно"
}

# Клонирование проекта
clone_project() {
    log_info "Клонирование проекта на сервер..."
    
    ssh -i ~/.ssh/DSkey_project $SERVER_USER@$SERVER_HOST << EOF
        cd $PROJECT_PATH
        
        # Клонировать репозиторий
        git clone https://github.com/pavelstepanovpm/CredAnlv2.git . || echo "Репозиторий уже существует"
        
        # Создать .env файл
        cat > .env << 'ENVEOF'
# Database
POSTGRES_DB=credit_analytics
POSTGRES_USER=credit_user
POSTGRES_PASSWORD=$(openssl rand -base64 32)

# Redis
REDIS_URL=redis://redis:6379

# Backend
DATABASE_URL=postgresql://credit_user:$(grep POSTGRES_PASSWORD .env | cut -d'=' -f2)@db:5432/credit_analytics
PYTHONPATH=/app

# Frontend
REACT_APP_API_URL=http://$DOMAIN/api

# Security
SECRET_KEY=$(openssl rand -base64 32)
ENVEOF
        
        echo "✅ Проект клонирован и настроен"
EOF
    
    log_success "Проект клонирован на сервер"
}

# Настройка Nginx
setup_nginx() {
    log_info "Настройка Nginx..."
    
    ssh -i ~/.ssh/DSkey_project $SERVER_USER@$SERVER_HOST << EOF
        # Удалить дефолтную конфигурацию
        rm -f /etc/nginx/sites-enabled/default
        
        # Создать конфигурацию для проекта
        cat > /etc/nginx/sites-available/credit-analytics << 'NGINXEOF'
server {
    listen 80;
    server_name $DOMAIN;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINXEOF
        
        # Активировать конфигурацию
        ln -s /etc/nginx/sites-available/credit-analytics /etc/nginx/sites-enabled/
        
        # Проверить конфигурацию
        nginx -t
        
        # Перезагрузить Nginx
        systemctl reload nginx
        
        echo "✅ Nginx настроен"
EOF
    
    log_success "Nginx настроен"
}

# Запуск приложения
start_application() {
    log_info "Запуск приложения..."
    
    ssh -i ~/.ssh/DSkey_project $SERVER_USER@$SERVER_HOST << EOF
        cd $PROJECT_PATH
        
        echo "🚀 Запуск Docker Compose..."
        docker-compose up -d
        
        echo "⏳ Ожидание запуска сервисов..."
        sleep 30
        
        echo "🔍 Проверка статуса..."
        docker-compose ps
        
        echo "📊 Проверка логов..."
        docker-compose logs --tail=10
EOF
    
    log_success "Приложение запущено"
}

# Проверка работоспособности
health_check() {
    log_info "Проверка работоспособности..."
    
    # Проверить доступность сервера
    if curl -s -f "http://$SERVER_HOST" > /dev/null; then
        log_success "Фронтенд доступен по адресу: http://$SERVER_HOST"
    else
        log_warning "Фронтенд недоступен, проверьте логи на сервере"
    fi
    
    # Проверить API
    if curl -s -f "http://$SERVER_HOST/api/health" > /dev/null; then
        log_success "API доступен по адресу: http://$SERVER_HOST/api"
    else
        log_warning "API недоступен, проверьте логи на сервере"
    fi
}

# Основная функция
main() {
    echo "🚀 Настройка сервера $SERVER_HOST"
    echo "=================================================="
    echo "Сервер: $SERVER_HOST"
    echo "Пользователь: $SERVER_USER"
    echo "Домен: $DOMAIN"
    echo "Путь проекта: $PROJECT_PATH"
    echo "=================================================="
    
    check_ssh_connection
    setup_server
    clone_project
    setup_nginx
    start_application
    health_check
    
    echo ""
    log_success "🎉 Настройка сервера завершена!"
    echo ""
    echo "📋 Информация:"
    echo "   🌐 Приложение: http://$SERVER_HOST"
    echo "   🔧 API: http://$SERVER_HOST/api"
    echo "   📊 Документация: http://$SERVER_HOST/api/docs"
    echo ""
    echo "🔧 Управление на сервере:"
    echo "   ssh -i ~/.ssh/DSkey_project $SERVER_USER@$SERVER_HOST"
    echo "   cd $PROJECT_PATH"
    echo "   docker-compose logs -f"
    echo "   docker-compose ps"
    echo ""
    echo "📝 Следующие шаги:"
    echo "1. Настроить GitHub Secrets для автоматического развертывания"
    echo "2. Настроить домен и SSL (если нужно)"
    echo "3. Протестировать развертывание"
}

# Обработка аргументов командной строки
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --email)
            EMAIL="$2"
            shift 2
            ;;
        --help)
            echo "Использование: $0 [опции]"
            echo ""
            echo "Опции:"
            echo "  --domain DOMAIN  Домен для приложения (по умолчанию: $DOMAIN)"
            echo "  --email EMAIL   Email для уведомлений (по умолчанию: $EMAIL)"
            echo "  --help          Показать эту справку"
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

#!/bin/bash

# Упрощенный скрипт настройки сервера 87.228.88.77
# Использование: ./scripts/setup-server-simple.sh

set -e

# Конфигурация
SERVER_HOST="87.228.88.77"
SERVER_USER="root"
SSH_KEY="~/.ssh/DSkey_project"
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

# Проверка SSH подключения
check_ssh() {
    log_info "Проверка SSH подключения к $SERVER_HOST..."
    
    if ssh -i ~/.ssh/DSkey_project -o ConnectTimeout=10 $SERVER_USER@$SERVER_HOST "echo 'SSH подключение работает!'"; then
        log_success "SSH подключение работает"
        return 0
    else
        log_error "SSH подключение не работает"
        exit 1
    fi
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
        if [ ! -d ".git" ]; then
            git clone https://github.com/pavelstepanovpm/CredAnlv2.git .
        else
            echo "Репозиторий уже существует, обновляем..."
            git pull origin main
        fi
        
        # Создать .env файл
        cat > .env << 'ENVEOF'
# Database
POSTGRES_DB=credit_analytics
POSTGRES_USER=credit_user
POSTGRES_PASSWORD=secure_password_123

# Redis
REDIS_URL=redis://redis:6379

# Backend
DATABASE_URL=postgresql://credit_user:secure_password_123@db:5432/credit_analytics
PYTHONPATH=/app

# Frontend
REACT_APP_API_URL=http://87.228.88.77/api

# Security
SECRET_KEY=your_secret_key_here_123
ENVEOF
        
        echo "✅ Проект клонирован и настроен"
EOF
    
    log_success "Проект клонирован на сервер"
}

# Настройка Nginx
setup_nginx() {
    log_info "Настройка Nginx..."
    
    ssh -i ~/.ssh/DSkey_project $SERVER_USER@$SERVER_HOST << 'EOF'
        # Удалить дефолтную конфигурацию
        rm -f /etc/nginx/sites-enabled/default
        
        # Создать конфигурацию для проекта
        cat > /etc/nginx/sites-available/credit-analytics << 'NGINXEOF'
server {
    listen 80;
    server_name 87.228.88.77;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
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
    
    # Подождать немного для запуска
    sleep 10
    
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
    echo "Путь проекта: $PROJECT_PATH"
    echo "=================================================="
    
    check_ssh
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
    echo "2. Протестировать развертывание"
    echo "3. Настроить домен и SSL (если нужно)"
}

# Запуск основной функции
main

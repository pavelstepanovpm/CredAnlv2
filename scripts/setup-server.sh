#!/bin/bash

# Скрипт настройки сервера Ubuntu для развертывания
# Использование: ./scripts/setup-server.sh

set -e  # Остановить при ошибке

# Конфигурация
PROJECT_PATH="/opt/credit-analytics"
DOMAIN="${DOMAIN:-your-domain.com}"
EMAIL="${EMAIL:-admin@your-domain.com}"

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

# Обновление системы
update_system() {
    log_info "Обновление системы..."
    
    sudo apt update
    sudo apt upgrade -y
    
    log_success "Система обновлена"
}

# Установка Docker
install_docker() {
    log_info "Установка Docker..."
    
    # Удалить старые версии
    sudo apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    
    # Установить зависимости
    sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
    
    # Добавить GPG ключ Docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Добавить репозиторий Docker
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Обновить пакеты
    sudo apt update
    
    # Установить Docker
    sudo apt install -y docker-ce docker-ce-cli containerd.io
    
    # Добавить пользователя в группу docker
    sudo usermod -aG docker $USER
    
    log_success "Docker установлен"
}

# Установка Docker Compose
install_docker_compose() {
    log_info "Установка Docker Compose..."
    
    # Получить последнюю версию
    COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    
    # Скачать и установить
    sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    log_success "Docker Compose установлен (версия: $COMPOSE_VERSION)"
}

# Установка дополнительных инструментов
install_tools() {
    log_info "Установка дополнительных инструментов..."
    
    sudo apt install -y \
        nginx \
        certbot \
        python3-certbot-nginx \
        git \
        htop \
        curl \
        wget \
        unzip \
        ufw \
        fail2ban
    
    log_success "Дополнительные инструменты установлены"
}

# Настройка файрвола
setup_firewall() {
    log_info "Настройка файрвола..."
    
    sudo ufw --force enable
    sudo ufw allow ssh
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw status
    
    log_success "Файрвол настроен"
}

# Настройка fail2ban
setup_fail2ban() {
    log_info "Настройка fail2ban..."
    
    sudo systemctl enable fail2ban
    sudo systemctl start fail2ban
    
    # Создать конфигурацию для SSH
    sudo tee /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
EOF
    
    sudo systemctl restart fail2ban
    
    log_success "fail2ban настроен"
}

# Создание структуры проекта
setup_project_structure() {
    log_info "Создание структуры проекта..."
    
    # Создать директорию
    sudo mkdir -p $PROJECT_PATH
    sudo chown $USER:$USER $PROJECT_PATH
    
    # Создать поддиректории
    mkdir -p $PROJECT_PATH/{data/postgres,data/redis,logs,backups,scripts}
    
    log_success "Структура проекта создана"
}

# Настройка Nginx
setup_nginx() {
    log_info "Настройка Nginx..."
    
    # Удалить дефолтную конфигурацию
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Создать конфигурацию для проекта
    sudo tee /etc/nginx/sites-available/credit-analytics << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    # SSL configuration (will be added by Certbot)
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

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

    # WebSocket support
    location /ws/ {
        proxy_pass http://localhost:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }
}
EOF
    
    # Активировать конфигурацию
    sudo ln -s /etc/nginx/sites-available/credit-analytics /etc/nginx/sites-enabled/
    
    # Проверить конфигурацию
    sudo nginx -t
    
    # Перезагрузить Nginx
    sudo systemctl reload nginx
    
    log_success "Nginx настроен"
}

# Получение SSL сертификата
setup_ssl() {
    log_info "Настройка SSL сертификата..."
    
    # Получить сертификат
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email $EMAIL
    
    # Настроить автоматическое обновление
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
    
    log_success "SSL сертификат настроен"
}

# Создание скриптов управления
create_management_scripts() {
    log_info "Создание скриптов управления..."
    
    # Скрипт мониторинга
    cat > $PROJECT_PATH/scripts/monitor.sh << 'EOF'
#!/bin/bash

echo "=== Статус контейнеров ==="
docker-compose ps

echo -e "\n=== Использование ресурсов ==="
docker stats --no-stream

echo -e "\n=== Использование диска ==="
df -h

echo -e "\n=== Использование памяти ==="
free -h

echo -e "\n=== Логи ошибок ==="
docker-compose logs --tail=10 | grep -i error
EOF

    # Скрипт резервного копирования
    cat > $PROJECT_PATH/scripts/backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/opt/credit-analytics/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Резервное копирование базы данных
docker-compose exec -T db pg_dump -U credit_user credit_analytics > $BACKUP_DIR/db_backup_$DATE.sql

# Резервное копирование файлов
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz data/

# Удалить старые резервные копии (старше 7 дней)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Резервное копирование завершено: $DATE"
EOF

    # Скрипт обновления
    cat > $PROJECT_PATH/scripts/update.sh << 'EOF'
#!/bin/bash

echo "🔄 Обновление приложения..."

# Получить изменения
git pull origin main

# Остановить контейнеры
docker-compose down

# Собрать новые образы
docker-compose build --no-cache

# Запустить контейнеры
docker-compose up -d

# Очистить неиспользуемые образы
docker system prune -f

echo "✅ Обновление завершено"
EOF

    # Сделать скрипты исполняемыми
    chmod +x $PROJECT_PATH/scripts/*.sh
    
    log_success "Скрипты управления созданы"
}

# Настройка автоматического резервного копирования
setup_backup_cron() {
    log_info "Настройка автоматического резервного копирования..."
    
    # Добавить задачу в crontab
    (crontab -l 2>/dev/null; echo "0 2 * * * $PROJECT_PATH/scripts/backup.sh") | crontab -
    
    log_success "Автоматическое резервное копирование настроено"
}

# Основная функция
main() {
    echo "🚀 Настройка сервера Ubuntu для развертывания"
    echo "=================================================="
    echo "Домен: $DOMAIN"
    echo "Email: $EMAIL"
    echo "Путь проекта: $PROJECT_PATH"
    echo "=================================================="
    
    # Выполнить все этапы
    update_system
    install_docker
    install_docker_compose
    install_tools
    setup_firewall
    setup_fail2ban
    setup_project_structure
    setup_nginx
    setup_ssl
    create_management_scripts
    setup_backup_cron
    
    echo ""
    log_success "🎉 Настройка сервера завершена!"
    echo ""
    echo "📋 Следующие шаги:"
    echo "1. Клонировать репозиторий:"
    echo "   cd $PROJECT_PATH"
    echo "   git clone https://github.com/pavelstepanovpm/CredAnlv2.git ."
    echo ""
    echo "2. Настроить переменные окружения:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    echo ""
    echo "3. Запустить приложение:"
    echo "   docker-compose up -d"
    echo ""
    echo "4. Проверить статус:"
    echo "   ./scripts/monitor.sh"
    echo ""
    echo "🔧 Полезные команды:"
    echo "   ./scripts/monitor.sh    # Мониторинг"
    echo "   ./scripts/backup.sh     # Резервное копирование"
    echo "   ./scripts/update.sh     # Обновление"
    echo ""
    echo "⚠️  Важно: Перезайдите в систему для применения группы docker"
    echo "   exit"
    echo "   ssh $USER@$(hostname)"
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
            echo "  --domain DOMAIN  Домен для SSL (по умолчанию: your-domain.com)"
            echo "  --email EMAIL    Email для Let's Encrypt (по умолчанию: admin@your-domain.com)"
            echo "  --help           Показать эту справку"
            echo ""
            echo "Переменные окружения:"
            echo "  DOMAIN           Домен для SSL"
            echo "  EMAIL            Email для Let's Encrypt"
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

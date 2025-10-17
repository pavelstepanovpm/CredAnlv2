# 🚀 End-to-End развертывание: macOS → Ubuntu Server

## 🎯 Архитектура развертывания

### Локальная среда (macOS):
- ✅ **Разработка** в Cursor
- ✅ **Git** для версионирования
- ✅ **Docker Desktop** для локального тестирования
- ✅ **SSH** для подключения к серверу

### Удаленный сервер (Ubuntu):
- ✅ **Docker** и **Docker Compose**
- ✅ **Nginx** для reverse proxy
- ✅ **SSL сертификаты** (Let's Encrypt)
- ✅ **Мониторинг** и логирование

## 📋 Пошаговый процесс

### 1. Подготовка локальной среды (macOS)

#### Проверка инструментов:
```bash
# Проверить Git
git --version

# Проверить Docker
docker --version
docker-compose --version

# Проверить SSH
ssh -V
```

#### Настройка SSH ключей:
```bash
# Сгенерировать SSH ключ (если нет)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Скопировать публичный ключ на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server.com

# Или вручную
cat ~/.ssh/id_ed25519.pub
# Скопировать содержимое в ~/.ssh/authorized_keys на сервере
```

### 2. Подготовка удаленного сервера (Ubuntu)

#### Установка Docker:
```bash
# Подключиться к серверу
ssh user@your-server.com

# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER

# Установить Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезайти в систему для применения групп
exit
ssh user@your-server.com
```

#### Установка дополнительных инструментов:
```bash
# Установить Nginx
sudo apt install nginx -y

# Установить Certbot для SSL
sudo apt install certbot python3-certbot-nginx -y

# Установить Git
sudo apt install git -y

# Установить htop для мониторинга
sudo apt install htop -y
```

### 3. Настройка проекта на сервере

#### Создание структуры:
```bash
# Создать директорию для проекта
sudo mkdir -p /opt/credit-analytics
sudo chown $USER:$USER /opt/credit-analytics
cd /opt/credit-analytics

# Клонировать репозиторий
git clone https://github.com/pavelstepanovpm/CredAnlv2.git .

# Создать директории для данных
mkdir -p data/postgres data/redis logs
```

#### Настройка переменных окружения:
```bash
# Создать .env файл
cat > .env << EOF
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
REACT_APP_API_URL=https://your-domain.com/api

# Security
SECRET_KEY=$(openssl rand -base64 32)
EOF
```

### 4. Настройка Nginx

#### Создание конфигурации:
```bash
# Создать конфигурацию Nginx
sudo tee /etc/nginx/sites-available/credit-analytics << EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL configuration (will be added by Certbot)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

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

    # WebSocket support (if needed)
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
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Получение SSL сертификата

```bash
# Получить SSL сертификат от Let's Encrypt
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Настроить автоматическое обновление
sudo crontab -e
# Добавить строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 6. Запуск приложения

```bash
# Перейти в директорию проекта
cd /opt/credit-analytics

# Запустить приложение
docker-compose up -d

# Проверить статус
docker-compose ps
docker-compose logs -f
```

## 🔧 Автоматизация развертывания

### GitHub Actions для автоматического развертывания:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_SSH_KEY }}
        script: |
          cd /opt/credit-analytics
          git pull origin main
          docker-compose down
          docker-compose build --no-cache
          docker-compose up -d
          docker system prune -f
```

### Скрипт для локального развертывания:

```bash
#!/bin/bash
# deploy-to-server.sh

SERVER_HOST="your-server.com"
SERVER_USER="your-username"
PROJECT_PATH="/opt/credit-analytics"

echo "🚀 Развертывание на сервер $SERVER_HOST"

# 1. Отправить изменения в GitHub
echo "📤 Отправка изменений в GitHub..."
git add .
git commit -m "Deploy: $(date)"
git push origin main

# 2. Подключиться к серверу и обновить
echo "🔄 Обновление на сервере..."
ssh $SERVER_USER@$SERVER_HOST << EOF
cd $PROJECT_PATH
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker system prune -f
EOF

echo "✅ Развертывание завершено!"
echo "🌐 Приложение доступно по адресу: https://your-domain.com"
```

## 📊 Мониторинг и логирование

### Настройка логирования:

```bash
# Создать конфигурацию для логирования
cat > docker-compose.override.yml << EOF
version: '3.8'

services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  frontend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
EOF
```

### Мониторинг ресурсов:

```bash
# Создать скрипт мониторинга
cat > monitor.sh << EOF
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

chmod +x monitor.sh
```

## 🔒 Безопасность

### Настройка файрвола:

```bash
# Настроить UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw status
```

### Резервное копирование:

```bash
# Создать скрипт резервного копирования
cat > backup.sh << EOF
#!/bin/bash

BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Резервное копирование базы данных
docker-compose exec -T db pg_dump -U credit_user credit_analytics > $BACKUP_DIR/db_backup_$DATE.sql

# Резервное копирование файлов
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz /opt/credit-analytics/data

# Удалить старые резервные копии (старше 7 дней)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Резервное копирование завершено: $DATE"
EOF

chmod +x backup.sh

# Добавить в crontab
crontab -e
# Добавить строку:
# 0 2 * * * /opt/credit-analytics/backup.sh
```

## 🚨 Устранение проблем

### Частые проблемы:

#### 1. Проблема с правами Docker:
```bash
# Решение
sudo usermod -aG docker $USER
newgrp docker
```

#### 2. Проблема с портами:
```bash
# Проверить занятые порты
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# Остановить конфликтующие сервисы
sudo systemctl stop apache2  # если установлен Apache
```

#### 3. Проблема с SSL:
```bash
# Проверить сертификат
sudo certbot certificates

# Обновить сертификат
sudo certbot renew --dry-run
```

#### 4. Проблема с базой данных:
```bash
# Проверить логи
docker-compose logs db

# Пересоздать базу данных
docker-compose down -v
docker-compose up -d
```

## 📋 Чек-лист развертывания

### Подготовка сервера:
- [ ] Ubuntu обновлен
- [ ] Docker установлен
- [ ] Docker Compose установлен
- [ ] Nginx установлен
- [ ] Certbot установлен
- [ ] SSH ключи настроены
- [ ] Файрвол настроен

### Настройка проекта:
- [ ] Репозиторий клонирован
- [ ] .env файл создан
- [ ] Nginx настроен
- [ ] SSL сертификат получен
- [ ] Docker Compose запущен

### Проверка:
- [ ] Приложение доступно по HTTPS
- [ ] API работает
- [ ] База данных подключена
- [ ] Логирование работает
- [ ] Мониторинг настроен
- [ ] Резервное копирование настроено

## 🎯 Итоговые команды

### Локально (macOS):
```bash
# Развертывание
./deploy-to-server.sh

# Или вручную
git push origin main
ssh user@server.com "cd /opt/credit-analytics && git pull && docker-compose up -d"
```

### На сервере (Ubuntu):
```bash
# Мониторинг
./monitor.sh

# Резервное копирование
./backup.sh

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f
```

**Полный end-to-end процесс от разработки на macOS до продакшена на Ubuntu!** 🚀

---
*Создано: 13 октября 2025*  
*Версия: 1.0.0*

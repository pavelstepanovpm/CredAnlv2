# 🚀 Настройка автоматического развертывания на сервер

## 🎯 Обзор процесса

### Что мы создали:
1. **Скрипт настройки сервера** - автоматическая подготовка Ubuntu
2. **Скрипт развертывания** - развертывание с macOS на сервер
3. **GitHub Actions** - автоматическое развертывание при push
4. **Быстрый скрипт** - для быстрого развертывания

## 📋 Пошаговая настройка

### 1. Подготовка сервера (Ubuntu)

#### Вариант A: Автоматическая настройка
```bash
# На сервере
curl -fsSL https://raw.githubusercontent.com/pavelstepanovpm/CredAnlv2/main/scripts/setup-server.sh | bash -s -- --domain your-domain.com --email your-email@example.com
```

#### Вариант B: Ручная настройка
```bash
# Подключиться к серверу
ssh user@your-server.com

# Запустить скрипт настройки
./scripts/setup-server.sh --domain your-domain.com --email your-email@example.com
```

### 2. Настройка SSH ключей

#### На macOS (локально):
```bash
# Сгенерировать SSH ключ (если нет)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Скопировать публичный ключ на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server.com

# Проверить подключение
ssh user@your-server.com "echo 'SSH подключение работает!'"
```

### 3. Настройка GitHub Secrets

#### Перейти в настройки репозитория:
1. GitHub → Settings → Secrets and variables → Actions
2. Добавить следующие секреты:

```
SERVER_HOST = your-server.com
SERVER_USER = ubuntu
SERVER_SSH_KEY = [содержимое ~/.ssh/id_ed25519]
PROJECT_PATH = /opt/credit-analytics
```

#### Как получить SSH ключ:
```bash
# На macOS
cat ~/.ssh/id_ed25519
# Скопировать содержимое и добавить как SERVER_SSH_KEY
```

### 4. Клонирование проекта на сервер

```bash
# На сервере
cd /opt/credit-analytics
git clone https://github.com/pavelstepanovpm/CredAnlv2.git .

# Создать .env файл
cp .env.example .env
nano .env
```

#### Пример .env файла:
```bash
# Database
POSTGRES_DB=credit_analytics
POSTGRES_USER=credit_user
POSTGRES_PASSWORD=your-secure-password

# Redis
REDIS_URL=redis://redis:6379

# Backend
DATABASE_URL=postgresql://credit_user:your-secure-password@db:5432/credit_analytics
PYTHONPATH=/app

# Frontend
REACT_APP_API_URL=https://your-domain.com/api

# Security
SECRET_KEY=your-secret-key
```

### 5. Первый запуск

```bash
# На сервере
cd /opt/credit-analytics
docker-compose up -d

# Проверить статус
docker-compose ps
docker-compose logs -f
```

## 🔄 Варианты развертывания

### 1. Автоматическое развертывание (GitHub Actions)

#### При push в main ветку:
```bash
# Локально на macOS
git add .
git commit -m "feat: новая функция"
git push origin main

# GitHub Actions автоматически:
# 1. Запустит тесты
# 2. Соберет Docker образы
# 3. Развернет на сервер
```

### 2. Ручное развертывание

#### Полный скрипт:
```bash
# Локально на macOS
./scripts/deploy-to-server.sh --host your-server.com --user ubuntu
```

#### Быстрый скрипт:
```bash
# Локально на macOS
export SERVER_HOST=your-server.com
export SERVER_USER=ubuntu
./scripts/quick-deploy.sh
```

### 3. Развертывание через SSH

```bash
# Локально на macOS
ssh user@your-server.com << 'EOF'
cd /opt/credit-analytics
git pull origin main
docker-compose down
docker-compose up -d
EOF
```

## 🔧 Управление на сервере

### Полезные команды:

```bash
# Подключиться к серверу
ssh user@your-server.com

# Перейти в директорию проекта
cd /opt/credit-analytics

# Проверить статус
docker-compose ps

# Просмотр логов
docker-compose logs -f

# Мониторинг
./scripts/monitor.sh

# Резервное копирование
./scripts/backup.sh

# Обновление
./scripts/update.sh

# Перезапуск
docker-compose restart

# Остановка
docker-compose down

# Запуск
docker-compose up -d
```

## 📊 Мониторинг и логирование

### Проверка работоспособности:

```bash
# Проверить API
curl https://your-domain.com/api/health

# Проверить фронтенд
curl https://your-domain.com

# Проверить логи
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Мониторинг ресурсов:

```bash
# Использование ресурсов
docker stats

# Использование диска
df -h

# Использование памяти
free -h

# Процессы
htop
```

## 🚨 Устранение проблем

### Частые проблемы:

#### 1. Ошибка SSH подключения:
```bash
# Проверить SSH ключи
ssh-add -l

# Пересоздать SSH ключ
ssh-keygen -t ed25519 -C "your-email@example.com"
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server.com
```

#### 2. Ошибка Docker:
```bash
# На сервере
sudo usermod -aG docker $USER
newgrp docker

# Перезапустить Docker
sudo systemctl restart docker
```

#### 3. Ошибка портов:
```bash
# Проверить занятые порты
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# Остановить конфликтующие сервисы
sudo systemctl stop apache2
```

#### 4. Ошибка SSL:
```bash
# Проверить сертификат
sudo certbot certificates

# Обновить сертификат
sudo certbot renew --dry-run
```

#### 5. Ошибка базы данных:
```bash
# Проверить логи
docker-compose logs db

# Пересоздать базу данных
docker-compose down -v
docker-compose up -d
```

## 🔒 Безопасность

### Настройка файрвола:
```bash
# На сервере
sudo ufw status
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Настройка fail2ban:
```bash
# На сервере
sudo systemctl status fail2ban
sudo fail2ban-client status sshd
```

### Резервное копирование:
```bash
# Автоматическое резервное копирование (настроено в setup-server.sh)
# Резервные копии создаются каждый день в 2:00
# Хранятся в /opt/credit-analytics/backups/
```

## 📋 Чек-лист развертывания

### Подготовка:
- [ ] Сервер Ubuntu настроен
- [ ] Docker и Docker Compose установлены
- [ ] Nginx настроен
- [ ] SSL сертификат получен
- [ ] SSH ключи настроены
- [ ] GitHub Secrets добавлены

### Проект:
- [ ] Репозиторий клонирован на сервер
- [ ] .env файл создан и настроен
- [ ] Docker Compose запущен
- [ ] Приложение доступно по HTTPS

### Автоматизация:
- [ ] GitHub Actions настроен
- [ ] Автоматическое развертывание работает
- [ ] Мониторинг настроен
- [ ] Резервное копирование настроено

## 🎯 Итоговые команды

### Локально (macOS):
```bash
# Быстрое развертывание
export SERVER_HOST=your-server.com
export SERVER_USER=ubuntu
./scripts/quick-deploy.sh

# Полное развертывание
./scripts/deploy-to-server.sh --host your-server.com --user ubuntu
```

### На сервере (Ubuntu):
```bash
# Мониторинг
./scripts/monitor.sh

# Резервное копирование
./scripts/backup.sh

# Обновление
./scripts/update.sh
```

### GitHub Actions:
```bash
# Автоматическое развертывание при push
git push origin main
```

**Полный end-to-end процесс от разработки на macOS до продакшена на Ubuntu!** 🚀

---
*Создано: 13 октября 2025*  
*Версия: 1.0.0*

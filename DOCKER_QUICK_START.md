# 🐳 Docker Quick Start - Система аналитики кредитного портфеля

## 🚀 Быстрый запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/pavelstepanovpm/CredAnlv2.git
cd CredAnlv2
```

### 2. Запустить развертывание
```bash
./deploy.sh
```

### 3. Открыть приложение
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Ручной запуск

### С Docker Compose:
```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Отдельные сервисы:
```bash
# Только бэкенд
docker-compose up backend db redis

# Только фронтенд
docker-compose up frontend
```

## 📦 Что включено

### Сервисы:
- **Backend** (FastAPI) - порт 8000
- **Frontend** (React) - порт 3000
- **PostgreSQL** - порт 5432
- **Redis** - порт 6379
- **Nginx** (опционально) - порт 80

### Образы:
- `credanlv2/backend:latest`
- `credanlv2/frontend:latest`
- `postgres:13-alpine`
- `redis:6-alpine`

## 🌐 Развертывание на сервере

### 1. Подготовка сервера
```bash
# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установить Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Развертывание
```bash
# Клонировать репозиторий
git clone https://github.com/pavelstepanovpm/CredAnlv2.git
cd CredAnlv2

# Настроить переменные окружения
cp .env.example .env
nano .env

# Запустить
./deploy.sh
```

### 3. Настройка домена (опционально)
```bash
# Настроить nginx для домена
sudo nano /etc/nginx/sites-available/credit-analytics

# Содержимое:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
    }
}
```

## 🔍 Мониторинг и управление

### Просмотр статуса:
```bash
docker-compose ps
```

### Просмотр логов:
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Вход в контейнер:
```bash
# Backend
docker-compose exec backend bash

# Database
docker-compose exec db psql -U credit_user -d credit_analytics
```

### Перезапуск:
```bash
# Все сервисы
docker-compose restart

# Конкретный сервис
docker-compose restart backend
```

## 🚨 Устранение проблем

### Проблема: Порты заняты
```bash
# Проверить занятые порты
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Остановить конфликтующие процессы
sudo kill -9 <PID>
```

### Проблема: Образы не собираются
```bash
# Очистить кэш Docker
docker system prune -a

# Пересобрать без кэша
docker-compose build --no-cache
```

### Проблема: База данных не запускается
```bash
# Проверить логи базы данных
docker-compose logs db

# Пересоздать том базы данных
docker-compose down -v
docker-compose up -d
```

## 📋 Полезные команды

```bash
# Обновление приложения
git pull
docker-compose down
docker-compose up -d

# Резервное копирование базы данных
docker-compose exec db pg_dump -U credit_user credit_analytics > backup.sql

# Восстановление базы данных
docker-compose exec -T db psql -U credit_user credit_analytics < backup.sql

# Мониторинг ресурсов
docker stats

# Очистка неиспользуемых образов
docker image prune -a
```

## 🎯 Итог

### ✅ Что получается:
- **Полная система** в Docker контейнерах
- **Автоматическая сборка** через GitHub Actions
- **Простое развертывание** одной командой
- **Масштабируемость** и изоляция сервисов

### 🔗 Полезные ссылки:
- **GitHub**: https://github.com/pavelstepanovpm/CredAnlv2
- **Docker Hub**: https://hub.docker.com
- **GitHub Container Registry**: https://ghcr.io

---
*Docker Quick Start: 13 октября 2025*

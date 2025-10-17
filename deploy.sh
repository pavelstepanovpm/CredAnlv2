#!/bin/bash

# Скрипт развертывания системы аналитики кредитного портфеля

echo "🚀 Развертывание системы аналитики кредитного портфеля"
echo "=================================================="

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

echo "✅ Docker и Docker Compose установлены"

# Создание .env файла если не существует
if [ ! -f .env ]; then
    echo "📝 Создание .env файла..."
    cat > .env << EOF
# Database
POSTGRES_DB=credit_analytics
POSTGRES_USER=credit_user
POSTGRES_PASSWORD=credit_pass

# Redis
REDIS_URL=redis://redis:6379

# Backend
DATABASE_URL=postgresql://credit_user:credit_pass@db:5432/credit_analytics
PYTHONPATH=/app

# Frontend
REACT_APP_API_URL=http://localhost:8000
EOF
    echo "✅ .env файл создан"
fi

# Остановка существующих контейнеров
echo "🛑 Остановка существующих контейнеров..."
docker-compose down

# Сборка образов
echo "🔨 Сборка Docker образов..."
docker-compose build --no-cache

# Запуск сервисов
echo "🚀 Запуск сервисов..."
docker-compose up -d

# Ожидание запуска
echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверка статуса
echo "🔍 Проверка статуса сервисов..."
docker-compose ps

# Проверка доступности
echo "🌐 Проверка доступности сервисов..."

# Проверка бэкенда
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend доступен на http://localhost:8000"
else
    echo "❌ Backend недоступен"
fi

# Проверка фронтенда
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend доступен на http://localhost:3000"
else
    echo "❌ Frontend недоступен"
fi

# Проверка базы данных
if docker-compose exec db pg_isready -U credit_user -d credit_analytics > /dev/null 2>&1; then
    echo "✅ База данных доступна"
else
    echo "❌ База данных недоступна"
fi

echo ""
echo "🎉 Развертывание завершено!"
echo ""
echo "📋 Доступные сервисы:"
echo "   🌐 Frontend: http://localhost:3000"
echo "   🔧 Backend API: http://localhost:8000"
echo "   📊 API Docs: http://localhost:8000/docs"
echo "   🗄️  Database: localhost:5432"
echo "   🔄 Redis: localhost:6379"
echo ""
echo "🔧 Управление:"
echo "   docker-compose logs -f          # Просмотр логов"
echo "   docker-compose down             # Остановка"
echo "   docker-compose restart          # Перезапуск"
echo "   docker-compose exec backend bash # Вход в контейнер бэкенда"

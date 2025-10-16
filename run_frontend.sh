#!/bin/bash

# Запуск фронтенда React/TypeScript

echo "🚀 Запуск фронтенда системы аналитики кредитного портфеля..."
echo "📊 Фронтенд будет доступен по адресу: http://localhost:3000"
echo "🔧 Убедитесь, что бэкенд запущен на порту 8000"

# Проверка и освобождение порта 3000
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️ Порт 3000 занят, освобождаем..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

cd frontend

# Очистка кэша npm
echo "🧹 Очистка кэша npm..."
npm cache clean --force

# Проверка наличия node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 Установка зависимостей..."
    npm install --legacy-peer-deps
fi

# Запуск в режиме разработки
echo "🎨 Запуск в режиме разработки..."
PORT=3000 npm start

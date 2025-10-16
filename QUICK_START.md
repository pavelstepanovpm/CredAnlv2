# 🚀 Быстрый старт системы аналитики кредитного портфеля

## ⚡ Запуск в одну команду

```bash
# Самый простой способ
python start.py
```

## 🎯 Альтернативные способы запуска

### Python скрипт (рекомендуется)
```bash
python start_system.py
```

### Bash скрипт
```bash
./start_system.sh
```

## 📋 Что происходит при запуске

1. **🔍 Проверка требований**
   - Python 3.8+
   - Node.js 16+
   - npm

2. **📦 Установка зависимостей**
   - Backend: `pip install -r backend/requirements.txt`
   - Frontend: `npm install` (в директории frontend)

3. **🚀 Запуск компонентов**
   - Backend: FastAPI сервер на порту 8000
   - Frontend: React приложение на порту 3000

4. **👀 Мониторинг**
   - Отслеживание состояния процессов
   - Автоматическая остановка при ошибках

## 🌐 Доступ к системе

После успешного запуска:

- **Фронтенд**: http://localhost:3000
- **API**: http://localhost:8000
- **Документация API**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## 🛑 Остановка системы

Нажмите `Ctrl+C` в терминале для корректной остановки всех процессов.

## 🔧 Ручной запуск компонентов

Если нужно запустить компоненты отдельно:

### Backend
```bash
python run_backend.py
```

### Frontend
```bash
cd frontend
npm start
```

## ❗ Возможные проблемы

### Конфликт зависимостей npm
```bash
# Если возникают ошибки с зависимостями
python fix_dependencies.py

# Или вручную:
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Python не найден
```bash
# Установите Python 3.8+
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python3
```

### Node.js не найден
```bash
# Установите Node.js 16+
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node
```

### npm не найден
```bash
# npm обычно устанавливается вместе с Node.js
# Если нет, установите отдельно:
curl -L https://npmjs.org/install.sh | sh
```

### Порт занят
```bash
# Проверьте, что порты 3000 и 8000 свободны
lsof -i :3000
lsof -i :8000

# Остановите процессы, использующие эти порты
kill -9 <PID>
```

### TypeScript конфликты
```bash
# Если возникают ошибки с TypeScript
cd frontend
npm install --legacy-peer-deps --force
```

## 📊 Структура после запуска

```
🏦 Система аналитики кредитного портфеля
├── 🎨 Frontend (React/TypeScript) → http://localhost:3000
├── 🔧 Backend (FastAPI/Quantlib) → http://localhost:8000
├── 📚 API Documentation → http://localhost:8000/docs
└── 🔍 Health Check → http://localhost:8000/health
```

## 🎉 Готово!

Система готова к работе! Откройте браузер и перейдите на http://localhost:3000

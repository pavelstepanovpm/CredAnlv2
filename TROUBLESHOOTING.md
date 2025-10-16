# 🔧 Устранение проблем системы аналитики кредитного портфеля

## 🚨 Частые проблемы и решения

### 1. Конфликт зависимостей npm

**Проблема**: Ошибки типа `ERESOLVE could not resolve` при установке npm пакетов

**Решение**:
```bash
# Автоматическое исправление
python3 fix_dependencies.py

# Или вручную:
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### 2. TypeScript версии конфликты

**Проблема**: `react-scripts` требует TypeScript 4.x, а установлен 5.x

**Решение**:
- В `package.json` уже исправлено: `"typescript": "^4.9.5"`
- Используйте флаг `--legacy-peer-deps` при установке

### 3. Python не найден

**Проблема**: `python: command not found`

**Решение**:
```bash
# Используйте python3 вместо python
python3 start_system.py

# Или создайте алиас
alias python=python3
```

### 4. Node.js не найден

**Проблема**: `node: command not found`

**Решение**:
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node

# Проверка
node --version
npm --version
```

### 5. Порт занят

**Проблема**: `EADDRINUSE: address already in use`

**Решение**:
```bash
# Проверить, что порты свободны
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Остановить процессы
kill -9 <PID>

# Или использовать другие порты
export PORT=3001  # Для фронтенда
```

### 6. Права доступа

**Проблема**: `Permission denied` при запуске скриптов

**Решение**:
```bash
# Сделать скрипты исполняемыми
chmod +x *.sh
chmod +x *.py

# Или запускать через python3
python3 start_system.py
```

### 7. Модули не найдены

**Проблема**: `ModuleNotFoundError` в Python

**Решение**:
```bash
# Установить зависимости
pip3 install -r backend/requirements.txt

# Или через python3 -m pip
python3 -m pip install -r backend/requirements.txt
```

### 8. npm install не работает

**Проблема**: Ошибки при `npm install`

**Решение**:
```bash
# Очистить кэш npm
npm cache clean --force

# Удалить node_modules и переустановить
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps --force

# Или использовать yarn
yarn install
```

## 🛠️ Скрипты для диагностики

### Проверка системы
```bash
# Проверить версии
python3 --version
node --version
npm --version

# Проверить порты
lsof -i :3000
lsof -i :8000

# Проверить процессы
ps aux | grep python
ps aux | grep node
```

### Очистка системы
```bash
# Очистить все зависимости
python3 fix_dependencies.py

# Или вручную:
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps

# Backend
pip3 cache purge
pip3 install -r backend/requirements.txt --upgrade
```

## 🔍 Логи и отладка

### Просмотр логов
```bash
# Backend логи
python3 run_backend.py 2>&1 | tee backend.log

# Frontend логи
cd frontend
npm start 2>&1 | tee frontend.log
```

### Отладка npm
```bash
# Подробные логи npm
npm install --legacy-peer-deps --verbose

# Проверить конфликты
npm ls --depth=0
```

### Отладка Python
```bash
# Проверить установленные пакеты
pip3 list

# Проверить зависимости
pip3 check
```

## 🚀 Альтернативные способы запуска

### Если основной скрипт не работает
```bash
# Запуск компонентов отдельно
python3 run_backend.py &
cd frontend && npm start &

# Или через screen/tmux
screen -S backend python3 run_backend.py
screen -S frontend cd frontend && npm start
```

### Docker (если доступен)
```bash
# Создать Dockerfile для каждого компонента
# Запустить через docker-compose
```

## 📋 Чек-лист диагностики

- [ ] Python 3.8+ установлен
- [ ] Node.js 16+ установлен
- [ ] npm установлен
- [ ] Порты 3000 и 8000 свободны
- [ ] Права доступа на скрипты
- [ ] Зависимости установлены
- [ ] Нет конфликтов версий
- [ ] Файлы проекта на месте

## 🆘 Если ничего не помогает

1. **Полная переустановка**:
   ```bash
   # Удалить все зависимости
   rm -rf frontend/node_modules
   pip3 uninstall -r backend/requirements.txt -y
   
   # Переустановить
   python3 fix_dependencies.py
   ```

2. **Проверить системные требования**:
   - macOS: 10.15+
   - Ubuntu: 18.04+
   - Windows: 10+

3. **Обратиться за помощью**:
   - Проверить логи ошибок
   - Собрать информацию о системе
   - Описать шаги воспроизведения

## 💡 Профилактика проблем

1. **Регулярно обновляйте зависимости**
2. **Используйте виртуальные окружения для Python**
3. **Следите за версиями Node.js и npm**
4. **Делайте бэкапы рабочей конфигурации**
5. **Используйте `--legacy-peer-deps` для npm**

## 🎯 Быстрые команды

```bash
# Полное исправление
python3 fix_dependencies.py

# Быстрый запуск
python3 start.py

# Проверка системы
python3 start_system.py

# Только бэкенд
python3 run_backend.py

# Только фронтенд
cd frontend && npm start
```


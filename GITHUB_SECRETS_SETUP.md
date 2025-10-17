# 🔐 Настройка GitHub Secrets - Пошаговая инструкция

## 🎯 Что такое GitHub Secrets?

**GitHub Secrets** - это зашифрованные переменные окружения, которые можно использовать в GitHub Actions для хранения чувствительных данных.

### Зачем нужны Secrets:
- 🔐 **Безопасность** - пароли и токены не видны в коде
- 🔄 **Переиспользование** - одни секреты для разных workflow
- 🛡️ **Контроль доступа** - только workflow могут использовать секреты
- 📝 **Аудит** - логи использования секретов

## 📋 Пошаговая настройка

### 1. Перейти в настройки репозитория
1. Откройте ваш репозиторий на GitHub
2. Нажмите на вкладку **"Settings"**
3. В левом меню выберите **"Secrets and variables"**
4. Нажмите **"Actions"**

### 2. Добавить новый секрет
1. Нажмите **"New repository secret"**
2. Заполните форму:
   - **Name**: название секрета (например, `DOCKER_PASSWORD`)
   - **Secret**: значение секрета (например, ваш пароль)
3. Нажмите **"Add secret"**

## 🔧 Необходимые секреты для нашего проекта

### Для Docker Hub:
```
DOCKER_USERNAME = ваш-username
DOCKER_PASSWORD = ваш-пароль-или-токен
```

### Для GitHub Container Registry:
```
GITHUB_TOKEN = автоматически доступен
```

### Для развертывания на сервер:
```
SERVER_HOST = ip-адрес-сервера
SERVER_USER = username-на-сервере
SERVER_SSH_KEY = приватный-ssh-ключ
```

### Для уведомлений:
```
SLACK_WEBHOOK = webhook-url-для-slack
EMAIL_USERNAME = email-для-уведомлений
EMAIL_PASSWORD = пароль-для-email
```

## 🐳 Настройка Docker Hub

### 1. Создать аккаунт на Docker Hub
1. Перейти на [hub.docker.com](https://hub.docker.com)
2. Зарегистрироваться или войти
3. Создать репозиторий для вашего проекта

### 2. Создать Access Token
1. Перейти в **Account Settings** → **Security**
2. Нажать **"New Access Token"**
3. Выбрать права доступа: **Read, Write, Delete**
4. Скопировать токен

### 3. Добавить секреты в GitHub
```
DOCKER_USERNAME = ваш-dockerhub-username
DOCKER_PASSWORD = ваш-access-token
```

## 🔑 Настройка SSH для развертывания

### 1. Сгенерировать SSH ключ
```bash
# На вашем компьютере
ssh-keygen -t ed25519 -C "github-actions@yourproject.com"

# Создаст файлы:
# ~/.ssh/id_ed25519 (приватный ключ)
# ~/.ssh/id_ed25519.pub (публичный ключ)
```

### 2. Добавить публичный ключ на сервер
```bash
# Скопировать публичный ключ на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server.com

# Или вручную:
cat ~/.ssh/id_ed25519.pub
# Скопировать содержимое в ~/.ssh/authorized_keys на сервере
```

### 3. Добавить приватный ключ в GitHub Secrets
```bash
# Показать приватный ключ
cat ~/.ssh/id_ed25519

# Скопировать содержимое и добавить как секрет SERVER_SSH_KEY
```

## 📧 Настройка уведомлений

### Slack уведомления:
1. Создать Slack App на [api.slack.com](https://api.slack.com)
2. Добавить Incoming Webhooks
3. Получить Webhook URL
4. Добавить как секрет `SLACK_WEBHOOK`

### Email уведомления:
```
EMAIL_USERNAME = your-email@gmail.com
EMAIL_PASSWORD = app-specific-password
```

## 🧪 Тестирование секретов

### Простой workflow для тестирования:
```yaml
name: Test Secrets

on:
  workflow_dispatch:  # Запуск вручную

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: Test Docker Hub login
      run: |
        echo "Testing Docker Hub credentials..."
        echo "Username: ${{ secrets.DOCKER_USERNAME }}"
        # Не выводите пароль в логах!
        
    - name: Test SSH connection
      run: |
        echo "Testing SSH connection..."
        echo "${{ secrets.SERVER_SSH_KEY }}" > /tmp/ssh_key
        chmod 600 /tmp/ssh_key
        ssh -i /tmp/ssh_key -o StrictHostKeyChecking=no ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} "echo 'SSH connection successful'"
```

## 🚨 Безопасность секретов

### ✅ Что можно делать:
- Использовать секреты в workflow
- Передавать секреты в Docker контейнеры
- Использовать секреты в переменных окружения

### ❌ Что НЕЛЬЗЯ делать:
- Выводить секреты в логах
- Коммитить секреты в код
- Передавать секреты в публичные репозитории
- Использовать секреты в комментариях

### 🛡️ Лучшие практики:
1. **Минимизируйте права** - давайте только необходимые права
2. **Регулярно обновляйте** токены и пароли
3. **Используйте App Passwords** вместо основных паролей
4. **Мониторьте использование** секретов
5. **Удаляйте неиспользуемые** секреты

## 📋 Чек-лист настройки

### Обязательные секреты:
- [ ] `DOCKER_USERNAME` - для публикации образов
- [ ] `DOCKER_PASSWORD` - для публикации образов
- [ ] `SERVER_HOST` - для развертывания
- [ ] `SERVER_USER` - для развертывания
- [ ] `SERVER_SSH_KEY` - для развертывания

### Опциональные секреты:
- [ ] `SLACK_WEBHOOK` - для уведомлений
- [ ] `EMAIL_USERNAME` - для email уведомлений
- [ ] `EMAIL_PASSWORD` - для email уведомлений
- [ ] `API_TOKEN` - для внешних API

### Проверка:
- [ ] Все секреты добавлены
- [ ] SSH ключ работает
- [ ] Docker Hub доступен
- [ ] Уведомления работают

## 🔧 Примеры использования

### В workflow файле:
```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}

- name: Deploy to server
  uses: appleboy/ssh-action@v0.1.5
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SERVER_SSH_KEY }}
    script: |
      cd /opt/my-app
      git pull origin main
      docker-compose up -d
```

### В переменных окружения:
```yaml
- name: Set environment variables
  run: |
    echo "DATABASE_URL=${{ secrets.DATABASE_URL }}" >> $GITHUB_ENV
    echo "API_KEY=${{ secrets.API_KEY }}" >> $GITHUB_ENV
```

## 🎯 Итоговые выводы

### GitHub Secrets позволяют:
- ✅ **Безопасно хранить** чувствительные данные
- ✅ **Автоматизировать** развертывание
- ✅ **Интегрироваться** с внешними сервисами
- ✅ **Контролировать доступ** к ресурсам

### Для полноценного CI/CD нужно:
1. **Docker Hub** секреты - для публикации образов
2. **SSH секреты** - для развертывания на сервер
3. **API секреты** - для интеграций
4. **Уведомления** - для мониторинга

**Secrets - это ключ к безопасной автоматизации!**

---
*Создано: 13 октября 2025*  
*Версия: 1.0.0*

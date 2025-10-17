# ⚙️ GitHub Actions и Docker Registry - Полное руководство

## 🎯 Что такое GitHub Actions?

### Определение:
**GitHub Actions** - это платформа для автоматизации CI/CD (Continuous Integration/Continuous Deployment) прямо в GitHub.

### Основные возможности:
- ✅ **Автоматическая сборка** при push/PR
- ✅ **Автоматическое тестирование** кода
- ✅ **Автоматическое развертывание** на серверы
- ✅ **Сборка Docker образов** и публикация в Registry
- ✅ **Уведомления** о статусе сборки
- ✅ **Планировщик задач** (cron jobs)

## 🏗️ Архитектура GitHub Actions

### Компоненты:
1. **Workflow** - файл с инструкциями (.github/workflows/*.yml)
2. **Job** - набор шагов, выполняемых на одном runner
3. **Step** - отдельная команда или действие
4. **Runner** - виртуальная машина (Ubuntu, Windows, macOS)
5. **Action** - переиспользуемый компонент

### Схема работы:
```
Push в GitHub → Trigger Workflow → Запуск Runner → Выполнение Jobs → Результат
```

## 📋 Структура Workflow файла

### Базовый пример:
```yaml
name: My Workflow                    # Название workflow

on:                                  # Триггеры (когда запускать)
  push:                              # При push
    branches: [ main ]               # В ветку main
  pull_request:                      # При PR
    branches: [ main ]               # В ветку main

jobs:                                # Задачи
  build:                             # Название задачи
    runs-on: ubuntu-latest           # ОС для runner
    steps:                           # Шаги выполнения
    - name: Checkout code            # Название шага
      uses: actions/checkout@v3      # Использовать готовое действие
    - name: Run tests                # Другой шаг
      run: npm test                  # Выполнить команду
```

## 🐳 Что такое Docker Registry?

### Определение:
**Docker Registry** - это хранилище для Docker образов, где можно публиковать, скачивать и управлять образами.

### Популярные Registry:
1. **Docker Hub** (docker.io) - публичный, бесплатный
2. **GitHub Container Registry** (ghcr.io) - интегрирован с GitHub
3. **AWS ECR** - Amazon Web Services
4. **Google Container Registry** - Google Cloud
5. **Azure Container Registry** - Microsoft Azure

## 🔄 GitHub Actions + Docker Registry

### Workflow для сборки и публикации образов:

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io                    # Registry для образов
  IMAGE_NAME: ${{ github.repository }} # Название образа

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read                   # Чтение кода
      packages: write                  # Запись в Registry

    steps:
    # 1. Получить код
    - name: Checkout repository
      uses: actions/checkout@v3

    # 2. Настроить Docker Buildx
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    # 3. Войти в Registry
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}  # GitHub username
        password: ${{ secrets.GITHUB_TOKEN }} # Автоматический токен

    # 4. Собрать и отправить образ
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .                     # Контекст сборки
        push: true                     # Отправить в Registry
        tags: |
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

## 🛠️ Практические примеры

### 1. Простая сборка образа

```yaml
name: Build Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t my-app:latest .
        docker run --rm my-app:latest npm test
```

### 2. Сборка и публикация в Docker Hub

```yaml
name: Build and Push to Docker Hub

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          username/my-app:latest
          username/my-app:${{ github.sha }}
```

### 3. Мультиплатформенная сборка

```yaml
name: Multi-platform Build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        platforms: linux/amd64,linux/arm64  # Мультиплатформа
        push: true
        tags: ghcr.io/username/my-app:latest
```

## 🔐 Настройка секретов (Secrets)

### Что такое Secrets:
**Secrets** - это зашифрованные переменные окружения для хранения чувствительных данных.

### Как добавить Secrets:
1. Перейти в репозиторий → Settings → Secrets and variables → Actions
2. Нажать "New repository secret"
3. Добавить:
   - `DOCKER_USERNAME` - имя пользователя Docker Hub
   - `DOCKER_PASSWORD` - пароль или токен
   - `SERVER_SSH_KEY` - SSH ключ для сервера
   - `API_TOKEN` - токен для внешних API

### Использование в Workflow:
```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

## 🚀 Автоматическое развертывание

### Развертывание на VPS:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_SSH_KEY }}
        script: |
          cd /opt/my-app
          git pull origin main
          docker-compose down
          docker-compose up -d
```

### Развертывание на AWS:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment
```

## 📊 Мониторинг и уведомления

### Уведомления в Slack:

```yaml
name: Notify on Deploy

on:
  workflow_run:
    workflows: ["Deploy to Production"]
    types: [completed]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
    - name: Notify Slack
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#deployments'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Отправка email:

```yaml
- name: Send email notification
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "Deployment Status: ${{ job.status }}"
    body: "Deployment completed with status: ${{ job.status }}"
    to: admin@company.com
```

## 🔧 Продвинутые возможности

### Матричная сборка:

```yaml
name: Matrix Build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14, 16, 18]
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
    - name: Run tests
      run: npm test
```

### Кэширование зависимостей:

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Install dependencies
  run: npm ci
```

### Условное выполнение:

```yaml
- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  run: echo "Deploying to staging"

- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: echo "Deploying to production"
```

## 📋 Лучшие практики

### 1. Безопасность:
- ✅ Используйте Secrets для чувствительных данных
- ✅ Минимизируйте права доступа
- ✅ Регулярно обновляйте токены
- ✅ Используйте официальные Actions

### 2. Производительность:
- ✅ Кэшируйте зависимости
- ✅ Используйте матричную сборку для тестирования
- ✅ Оптимизируйте Docker образы
- ✅ Параллелизируйте независимые задачи

### 3. Мониторинг:
- ✅ Настройте уведомления
- ✅ Логируйте важные события
- ✅ Мониторьте время выполнения
- ✅ Отслеживайте использование ресурсов

## 🎯 Итоговые выводы

### GitHub Actions - это:
- ✅ **Платформа CI/CD** встроенная в GitHub
- ✅ **Автоматизация** сборки, тестирования, развертывания
- ✅ **Бесплатная** для публичных репозиториев
- ✅ **Интеграция** с Docker Registry

### Docker Registry - это:
- ✅ **Хранилище** для Docker образов
- ✅ **Публикация** готовых образов
- ✅ **Версионирование** образов
- ✅ **Распространение** между серверами

### Workflow:
1. **Код** → GitHub
2. **GitHub Actions** → сборка образа
3. **Docker Registry** → хранение образа
4. **Сервер** → скачивание и запуск

**GitHub Actions автоматизирует весь процесс от кода до развертывания!**

---
*Создано: 13 октября 2025*  
*Версия: 1.0.0*

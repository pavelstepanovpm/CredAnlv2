# ⚡ GitHub Actions & Docker Registry - Шпаргалка

## 🎯 Основные понятия

| Понятие | Описание |
|---------|----------|
| **GitHub Actions** | Платформа CI/CD в GitHub |
| **Workflow** | Файл .yml с инструкциями |
| **Job** | Набор шагов на одном runner |
| **Step** | Отдельная команда |
| **Runner** | Виртуальная машина |
| **Docker Registry** | Хранилище Docker образов |

## 🚀 Базовый Workflow

```yaml
name: My Workflow
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - run: echo "Hello World"
```

## 🐳 Docker Registry варианты

| Registry | URL | Особенности |
|----------|-----|-------------|
| **Docker Hub** | docker.io | Публичный, бесплатный |
| **GitHub Container Registry** | ghcr.io | Интегрирован с GitHub |
| **AWS ECR** | amazonaws.com | Amazon Web Services |
| **Google GCR** | gcr.io | Google Cloud |

## 🔧 Основные Actions

### Получение кода:
```yaml
- uses: actions/checkout@v3
```

### Настройка языков:
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.9'

- uses: actions/setup-node@v3
  with:
    node-version: '16'
```

### Docker:
```yaml
- uses: docker/setup-buildx-action@v2
- uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
- uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: username/app:latest
```

## 🔐 Секреты (Secrets)

### Добавление секретов:
1. Repository → Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `DOCKER_PASSWORD`
4. Value: `your-password`

### Использование:
```yaml
- name: Login
  run: echo ${{ secrets.DOCKER_PASSWORD }}
```

## 📋 Полный пример

```yaml
name: Build and Deploy

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

## 🎯 Триггеры (Triggers)

```yaml
on:
  push:                    # При push
    branches: [ main ]
  pull_request:            # При PR
    branches: [ main ]
  schedule:                # По расписанию
    - cron: '0 0 * * *'
  workflow_dispatch:       # Вручную
  release:                 # При релизе
    types: [published]
```

## 🔄 Условное выполнение

```yaml
- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  run: echo "Staging deploy"

- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: echo "Production deploy"
```

## 📊 Матричная сборка

```yaml
strategy:
  matrix:
    node-version: [14, 16, 18]
    os: [ubuntu-latest, windows-latest]
```

## 🚨 Частые проблемы

| Проблема | Решение |
|----------|---------|
| "Permission denied" | Проверить права в permissions |
| "Secret not found" | Добавить секрет в Settings |
| "Docker build failed" | Проверить Dockerfile |
| "Push failed" | Проверить логин в Registry |

## 📋 Чек-лист

### Настройка:
- [ ] Создать .github/workflows/*.yml
- [ ] Добавить секреты в Settings
- [ ] Настроить Docker Registry
- [ ] Протестировать workflow

### Секреты:
- [ ] `DOCKER_USERNAME`
- [ ] `DOCKER_PASSWORD`
- [ ] `SERVER_HOST`
- [ ] `SERVER_SSH_KEY`

### Workflow:
- [ ] Триггеры настроены
- [ ] Jobs определены
- [ ] Steps добавлены
- [ ] Условия проверены

## 🎯 Итог

### GitHub Actions:
- ✅ **Автоматизация** CI/CD
- ✅ **Интеграция** с Docker
- ✅ **Безопасность** через Secrets
- ✅ **Масштабируемость** и гибкость

### Docker Registry:
- ✅ **Хранение** образов
- ✅ **Версионирование** образов
- ✅ **Распространение** между серверами
- ✅ **Интеграция** с CI/CD

**GitHub Actions + Docker Registry = Полная автоматизация разработки!**

---
*Шпаргалка: 13 октября 2025*

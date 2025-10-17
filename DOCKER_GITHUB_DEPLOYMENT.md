# 🐳 Docker, GitHub и развертывание - Полное руководство

## 🎯 Ответы на ваши вопросы

### ❌ GitHub НЕ хранит Docker контейнеры
- **GitHub** хранит только **код** (Dockerfile, docker-compose.yml)
- **Docker образы** хранятся в **Docker Registry** (Docker Hub, GitHub Container Registry)
- **Контейнеры** - это **запущенные экземпляры** образов

### ✅ Правильный подход к развертыванию
1. **Код** хранится в GitHub
2. **Docker образы** хранятся в Registry
3. **На сервере** образы скачиваются и запускаются

## 🏗️ Архитектура Docker + GitHub

### Что где хранится:

| Компонент | Где хранится | Назначение |
|-----------|--------------|------------|
| **Код приложения** | GitHub | Исходный код, Dockerfile |
| **Docker образы** | Docker Registry | Готовые к запуску образы |
| **Контейнеры** | Сервер | Запущенные приложения |

### Docker Registry варианты:
- **Docker Hub** (docker.io) - публичный, бесплатный
- **GitHub Container Registry** (ghcr.io) - интегрирован с GitHub
- **AWS ECR** - Amazon
- **Google Container Registry** - Google Cloud
- **Azure Container Registry** - Microsoft

## 🚀 Правильный workflow развертывания

### 1. Разработка (локально)
```bash
# Создать Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
EOF

# Собрать образ локально
docker build -t my-app:latest .

# Протестировать локально
docker run -p 8000:8000 my-app:latest
```

### 2. Публикация образа
```bash
# Войти в Docker Hub
docker login

# Собрать образ с тегом для Registry
docker build -t username/my-app:latest .

# Отправить в Docker Hub
docker push username/my-app:latest
```

### 3. Развертывание на сервере
```bash
# На сервере скачать образ
docker pull username/my-app:latest

# Запустить контейнер
docker run -d -p 8000:8000 --name my-app username/my-app:latest
```

## 🔧 GitHub Actions для автоматизации

### Автоматическая сборка и публикация:

```yaml
# .github/workflows/docker.yml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
  pull_request:
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

## 📦 Docker Compose для сложных приложений

### docker-compose.yml:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

volumes:
  postgres_data:
```

### Развертывание с Docker Compose:
```bash
# На сервере
git clone https://github.com/username/my-app.git
cd my-app
docker-compose up -d
```

## 🌐 Развертывание на разных платформах

### 1. VPS/Сервер (DigitalOcean, Linode, etc.)
```bash
# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Клонировать репозиторий
git clone https://github.com/username/my-app.git
cd my-app

# Запустить приложение
docker-compose up -d
```

### 2. AWS (Elastic Beanstalk, ECS, EKS)
```bash
# AWS CLI
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Собрать и отправить в ECR
docker build -t my-app .
docker tag my-app:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
```

### 3. Google Cloud (Cloud Run, GKE)
```bash
# Google Cloud CLI
gcloud auth configure-docker

# Собрать и отправить
docker build -t gcr.io/PROJECT-ID/my-app .
docker push gcr.io/PROJECT-ID/my-app

# Развернуть на Cloud Run
gcloud run deploy --image gcr.io/PROJECT-ID/my-app --platform managed
```

### 4. Azure (Container Instances, AKS)
```bash
# Azure CLI
az acr login --name myregistry

# Собрать и отправить
docker build -t myregistry.azurecr.io/my-app:latest .
docker push myregistry.azurecr.io/my-app:latest
```

## 🔄 CI/CD Pipeline с GitHub Actions

### Полный pipeline:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run tests
      run: |
        docker-compose -f docker-compose.test.yml up --abort-on-container-exit

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build and push
      run: |
        docker build -t my-app:${{ github.sha }} .
        docker push my-app:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      run: |
        ssh user@server "docker pull my-app:${{ github.sha }} && docker stop my-app && docker rm my-app && docker run -d --name my-app my-app:${{ github.sha }}"
```

## 🛠️ Практический пример для нашего проекта

### Dockerfile для бэкенда:
```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установить системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копировать requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копировать код
COPY . .

# Открыть порт
EXPOSE 8000

# Запустить приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile для фронтенда:
```dockerfile
# frontend/Dockerfile
FROM node:16-alpine

WORKDIR /app

# Копировать package.json
COPY package*.json ./
RUN npm ci --only=production

# Копировать код
COPY . .

# Собрать приложение
RUN npm run build

# Установить nginx
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/creditdb
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: creditdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 📋 Чек-лист развертывания

### Подготовка:
- [ ] Dockerfile создан
- [ ] docker-compose.yml настроен
- [ ] Код в GitHub
- [ ] Docker Registry настроен

### Локальное тестирование:
- [ ] `docker build` работает
- [ ] `docker run` запускается
- [ ] `docker-compose up` работает
- [ ] Приложение доступно

### Развертывание:
- [ ] Образ опубликован в Registry
- [ ] Сервер настроен (Docker установлен)
- [ ] Образ скачан на сервер
- [ ] Контейнер запущен
- [ ] Приложение доступно

## 🚨 Частые ошибки

### Ошибка 1: "Image not found"
```bash
# Проблема: образ не найден
# Решение: проверить тег и Registry
docker pull username/my-app:latest
```

### Ошибка 2: "Port already in use"
```bash
# Проблема: порт занят
# Решение: изменить порт или остановить конфликтующий контейнер
docker run -p 8001:8000 my-app
```

### Ошибка 3: "Permission denied"
```bash
# Проблема: нет прав на Docker
# Решение: добавить пользователя в группу docker
sudo usermod -aG docker $USER
```

## 🎯 Итоговые выводы

### ❌ GitHub НЕ хранит:
- Docker контейнеры
- Docker образы
- Запущенные приложения

### ✅ GitHub хранит:
- Исходный код
- Dockerfile
- docker-compose.yml
- CI/CD конфигурации

### ✅ Правильный workflow:
1. **Код** → GitHub
2. **Образ** → Docker Registry
3. **Контейнер** → Сервер (скачивается и запускается)

### ✅ Для развертывания нужно:
1. Скачать образ с Registry
2. Запустить контейнер на сервере
3. Настроить сеть и порты

**GitHub хранит код, Docker Registry хранит образы, сервер запускает контейнеры!**

---
*Создано: 13 октября 2025*  
*Версия: 1.0.0*

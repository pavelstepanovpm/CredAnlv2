# ⚡ Быстрый старт развертывания

## 🎯 За 5 минут от кода до продакшена

### 1. Настройка сервера (Ubuntu)
```bash
# Подключиться к серверу
ssh user@your-server.com

# Автоматическая настройка
curl -fsSL https://raw.githubusercontent.com/pavelstepanovpm/CredAnlv2/main/scripts/setup-server.sh | bash -s -- --domain your-domain.com --email your-email@example.com
```

### 2. Настройка SSH ключей (macOS)
```bash
# Сгенерировать ключ
ssh-keygen -t ed25519 -C "your-email@example.com"

# Скопировать на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server.com
```

### 3. Настройка GitHub Secrets
1. GitHub → Settings → Secrets and variables → Actions
2. Добавить:
   - `SERVER_HOST` = your-server.com
   - `SERVER_USER` = ubuntu
   - `SERVER_SSH_KEY` = содержимое `~/.ssh/id_ed25519`

### 4. Клонирование проекта
```bash
# На сервере
cd /opt/credit-analytics
git clone https://github.com/pavelstepanovpm/CredAnlv2.git .
cp .env.example .env
nano .env  # Настроить переменные
```

### 5. Первый запуск
```bash
# На сервере
docker-compose up -d
```

## 🚀 Развертывание

### Автоматическое (GitHub Actions):
```bash
git push origin main  # Автоматически развернет на сервер
```

### Ручное:
```bash
# Быстрое развертывание
export SERVER_HOST=your-server.com
./scripts/quick-deploy.sh

# Полное развертывание
./scripts/deploy-to-server.sh --host your-server.com --user ubuntu
```

## 🔧 Управление

### На сервере:
```bash
cd /opt/credit-analytics
./scripts/monitor.sh    # Мониторинг
./scripts/backup.sh     # Резервное копирование
./scripts/update.sh     # Обновление
```

### Локально:
```bash
# Проверить статус
ssh user@your-server.com "cd /opt/credit-analytics && docker-compose ps"

# Просмотр логов
ssh user@your-server.com "cd /opt/credit-analytics && docker-compose logs -f"
```

## 📊 Проверка

```bash
# API
curl https://your-domain.com/api/health

# Фронтенд
curl https://your-domain.com

# Логи
ssh user@your-server.com "cd /opt/credit-analytics && docker-compose logs"
```

## 🎯 Готово!

**Ваше приложение доступно по адресу: https://your-domain.com**

---
*Быстрый старт: 13 октября 2025*

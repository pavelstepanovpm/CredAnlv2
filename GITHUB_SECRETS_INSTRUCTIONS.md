# 🔐 Настройка GitHub Secrets для автоматического развертывания

## 🎯 Цель
Настроить GitHub Secrets для автоматического развертывания на сервер 87.228.88.77 при каждом push в main ветку.

## 📋 Необходимые секреты

### 1. SERVER_HOST
- **Значение**: `87.228.88.77`
- **Описание**: IP адрес вашего сервера

### 2. SERVER_USER
- **Значение**: `root`
- **Описание**: Пользователь для SSH подключения

### 3. SERVER_SSH_KEY
- **Значение**: Содержимое приватного SSH ключа
- **Описание**: Приватный ключ для аутентификации

### 4. PROJECT_PATH
- **Значение**: `/opt/credit-analytics`
- **Описание**: Путь к проекту на сервере

## 🔧 Пошаговая настройка

### Шаг 1: Получить приватный SSH ключ
```bash
# На вашем Mac
cat ~/.ssh/DSkey_project
```

### Шаг 2: Перейти в настройки GitHub
1. Откройте ваш репозиторий на GitHub
2. Нажмите на вкладку **"Settings"**
3. В левом меню выберите **"Secrets and variables"**
4. Нажмите **"Actions"**

### Шаг 3: Добавить секреты

#### SERVER_HOST:
1. Нажмите **"New repository secret"**
2. **Name**: `SERVER_HOST`
3. **Secret**: `87.228.88.77`
4. Нажмите **"Add secret"**

#### SERVER_USER:
1. Нажмите **"New repository secret"**
2. **Name**: `SERVER_USER`
3. **Secret**: `root`
4. Нажмите **"Add secret"**

#### SERVER_SSH_KEY:
1. Нажмите **"New repository secret"**
2. **Name**: `SERVER_SSH_KEY`
3. **Secret**: [вставьте содержимое приватного ключа]
4. Нажмите **"Add secret"**

#### PROJECT_PATH:
1. Нажмите **"New repository secret"**
2. **Name**: `PROJECT_PATH`
3. **Secret**: `/opt/credit-analytics`
4. Нажмите **"Add secret"`

## ✅ Проверка настройки

После добавления всех секретов, вы должны увидеть:

| Name | Updated |
|------|---------|
| SERVER_HOST | Just now |
| SERVER_USER | Just now |
| SERVER_SSH_KEY | Just now |
| PROJECT_PATH | Just now |

## 🚀 Тестирование автоматического развертывания

### Вариант 1: Push в main ветку
```bash
# Сделать небольшое изменение
echo "# Test deployment" >> README.md
git add README.md
git commit -m "test: автоматическое развертывание"
git push origin main
```

### Вариант 2: Запуск вручную
1. Перейдите в **Actions** в вашем репозитории
2. Выберите workflow **"Deploy to Production Server"**
3. Нажмите **"Run workflow"**
4. Выберите ветку **main**
5. Нажмите **"Run workflow"**

## 📊 Мониторинг развертывания

### Просмотр логов:
1. Перейдите в **Actions**
2. Выберите последний запуск
3. Нажмите на job **"deploy"**
4. Просмотрите логи выполнения

### Проверка результата:
- **Frontend**: http://87.228.88.77:3002
- **Backend**: http://87.228.88.77:8001/docs

## 🔧 Устранение проблем

### Проблема: "Permission denied"
**Решение**: Проверьте, что SERVER_SSH_KEY содержит полный приватный ключ

### Проблема: "Connection refused"
**Решение**: Проверьте SERVER_HOST и SERVER_USER

### Проблема: "No such file or directory"
**Решение**: Проверьте PROJECT_PATH

## 🎯 Результат

После настройки GitHub Secrets:
- ✅ **Автоматическое развертывание** при push в main
- ✅ **Тестирование** перед развертыванием
- ✅ **Сборка Docker образов** и публикация в Registry
- ✅ **Развертывание на сервер** через SSH
- ✅ **Проверка работоспособности** после развертывания

---
*Инструкция создана: 17 октября 2025*

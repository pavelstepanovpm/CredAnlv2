# 🔐 Ручная настройка GitHub Secrets

## 🎯 Цель
Настроить GitHub Secrets для автоматического развертывания через веб-интерфейс GitHub.

## 📋 Необходимые секреты

| Название | Значение | Описание |
|----------|----------|----------|
| `SERVER_HOST` | `87.228.88.77` | IP адрес сервера |
| `SERVER_USER` | `root` | Пользователь SSH |
| `SERVER_SSH_KEY` | [содержимое ключа] | Приватный SSH ключ |
| `PROJECT_PATH` | `/opt/credit-analytics` | Путь к проекту |

## 🔧 Пошаговая настройка

### Шаг 1: Получить SSH ключ
```bash
# На вашем Mac выполните:
cat ~/.ssh/DSkey_project
```

**Скопируйте весь вывод, включая:**
```
-----BEGIN OPENSSH PRIVATE KEY-----
[содержимое ключа]
-----END OPENSSH PRIVATE KEY-----
```

### Шаг 2: Открыть настройки репозитория
1. Перейдите на https://github.com/pavelstepanovpm/CredAnlv2
2. Нажмите на вкладку **"Settings"** (в верхнем меню)
3. В левом меню выберите **"Secrets and variables"**
4. Нажмите **"Actions"**

### Шаг 3: Добавить секреты

#### SERVER_HOST
1. Нажмите **"New repository secret"**
2. **Name**: `SERVER_HOST`
3. **Secret**: `87.228.88.77`
4. Нажмите **"Add secret"**

#### SERVER_USER
1. Нажмите **"New repository secret"**
2. **Name**: `SERVER_USER`
3. **Secret**: `root`
4. Нажмите **"Add secret"**

#### SERVER_SSH_KEY
1. Нажмите **"New repository secret"**
2. **Name**: `SERVER_SSH_KEY`
3. **Secret**: [вставьте содержимое SSH ключа из Шага 1]
4. Нажмите **"Add secret"**

#### PROJECT_PATH
1. Нажмите **"New repository secret"**
2. **Name**: `PROJECT_PATH`
3. **Secret**: `/opt/credit-analytics`
4. Нажмите **"Add secret"**

## ✅ Проверка настройки

После добавления всех секретов, вы должны увидеть:

| Name | Updated |
|------|---------|
| SERVER_HOST | Just now |
| SERVER_USER | Just now |
| SERVER_SSH_KEY | Just now |
| PROJECT_PATH | Just now |

## 🧪 Тестирование

### Вариант 1: Создать тестовый коммит
```bash
# В вашем проекте
echo "# Test deployment $(date)" >> README.md
git add README.md
git commit -m "test: автоматическое развертывание"
git push origin main
```

### Вариант 2: Запустить workflow вручную
1. Перейдите в **Actions** в вашем репозитории
2. Выберите workflow **"🚀 Production Deployment"**
3. Нажмите **"Run workflow"**
4. Выберите ветку **main**
5. Нажмите **"Run workflow"**

## 📊 Мониторинг

### Просмотр выполнения:
1. Перейдите в **Actions**
2. Выберите последний запуск
3. Нажмите на job **"deploy"**
4. Просмотрите логи выполнения

### Проверка результата:
- **Frontend**: http://87.228.88.77:3002
- **Backend**: http://87.228.88.77:8001/docs

## 🔧 Устранение проблем

### Проблема: "Permission denied"
**Решение**: 
- Убедитесь, что SERVER_SSH_KEY содержит полный приватный ключ
- Проверьте, что ключ начинается с `-----BEGIN OPENSSH PRIVATE KEY-----`

### Проблема: "Connection refused"
**Решение**: 
- Проверьте SERVER_HOST (должен быть `87.228.88.77`)
- Проверьте SERVER_USER (должен быть `root`)

### Проблема: "No such file or directory"
**Решение**: 
- Проверьте PROJECT_PATH (должен быть `/opt/credit-analytics`)

### Проблема: Workflow не запускается
**Решение**: 
- Убедитесь, что все секреты добавлены
- Проверьте, что вы push'ите в ветку `main`
- Убедитесь, что workflow файл находится в `.github/workflows/`

## 🎯 Результат

После успешной настройки:
- ✅ **Автоматическое развертывание** при каждом push в main
- ✅ **Тестирование** перед развертыванием
- ✅ **Сборка Docker образов** и публикация в Registry
- ✅ **Развертывание на сервер** через SSH
- ✅ **Проверка работоспособности** после развертывания

## 🚀 Следующие шаги

1. **Протестируйте развертывание** создав тестовый коммит
2. **Мониторьте выполнение** в GitHub Actions
3. **Проверьте работоспособность** сервисов
4. **Настройте уведомления** (опционально)

---
*Инструкция создана: 17 октября 2025*

# 🐙 Подключение к GitHub - Пошаговая инструкция

## 📋 Что нужно сделать:

### 1. Создать репозиторий на GitHub

#### Вариант A: Через веб-интерфейс GitHub
1. Перейдите на [github.com](https://github.com)
2. Нажмите кнопку **"New repository"** (зеленая кнопка)
3. Заполните форму:
   - **Repository name**: `credanlv2` или `credit-portfolio-analytics`
   - **Description**: `Credit Portfolio Analytics System - FastAPI + React`
   - **Visibility**: Public или Private (на ваш выбор)
   - **НЕ** добавляйте README, .gitignore, license (у нас уже есть)
4. Нажмите **"Create repository"**

#### Вариант B: Через GitHub CLI (если установлен)
```bash
# Установить GitHub CLI (если нужно)
brew install gh

# Авторизоваться
gh auth login

# Создать репозиторий
gh repo create credanlv2 --public --description "Credit Portfolio Analytics System"
```

### 2. Подключить локальный репозиторий к GitHub

После создания репозитория на GitHub, выполните команды:

```bash
# Добавить удаленный репозиторий (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/credanlv2.git

# Проверить подключение
git remote -v

# Отправить все ветки и теги
git push -u origin main
git push origin develop
git push origin feature/new-features
git push origin hotfix/bug-fixes
git push --tags
```

### 3. Настроить ветки на GitHub

```bash
# Установить develop как основную ветку разработки
git checkout develop
git push -u origin develop

# Настроить защиту веток (через веб-интерфейс GitHub)
# Settings → Branches → Add rule
```

## 🔧 Альтернативные способы подключения

### Через SSH (рекомендуется):
```bash
# Генерировать SSH ключ (если нет)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Добавить ключ в GitHub
# Settings → SSH and GPG keys → New SSH key

# Подключить через SSH
git remote add origin git@github.com:YOUR_USERNAME/credanlv2.git
```

### Через Personal Access Token:
```bash
# Создать токен в GitHub
# Settings → Developer settings → Personal access tokens

# Использовать токен вместо пароля
git remote add origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/credanlv2.git
```

## 📝 Рекомендуемые настройки репозитория

### 1. Описание репозитория:
```
Credit Portfolio Analytics System - FastAPI + React/TypeScript
```

### 2. Topics (теги):
```
credit-analytics, portfolio-management, fastapi, react, typescript, quantlib, financial-software
```

### 3. README.md (автоматически подтянется из проекта)

### 4. Настройки веток:
- **main** - защищенная ветка (только через PR)
- **develop** - ветка разработки
- **feature/*** - ветки функций
- **hotfix/*** - ветки исправлений

## 🚀 После подключения

### Проверить статус:
```bash
# Проверить удаленные репозитории
git remote -v

# Проверить статус
git status

# Проверить ветки
git branch -a
```

### Рабочий процесс:
```bash
# Получить изменения
git fetch origin

# Синхронизироваться
git pull origin main

# Отправить изменения
git push origin feature/название-ветки
```

## 📋 Чек-лист готовности

- [ ] Создан репозиторий на GitHub
- [ ] Подключен удаленный репозиторий
- [ ] Отправлены все ветки
- [ ] Отправлены все теги
- [ ] Настроена защита веток
- [ ] Добавлено описание репозитория
- [ ] Настроены теги (topics)

## 🔗 Полезные ссылки

- [GitHub Docs](https://docs.github.com/)
- [Git Workflow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---
*Создано: 13 октября 2025*  
*Версия: 1.0.0*

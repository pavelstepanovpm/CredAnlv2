# 🚀 Настройка нового проекта с Git и GitHub

## 📋 Пошаговая инструкция

### 1. Проверка Git (уже установлен ✅)
```bash
git --version
# Output: git version 2.39.5 (Apple Git-154)
```

### 2. Создание нового проекта
```bash
# Создать папку для нового проекта
mkdir my-awesome-project
cd my-awesome-project

# Инициализировать Git репозиторий
git init
# Output: Initialized empty Git repository in /path/to/my-awesome-project/.git
```

### 3. Настройка Git (если не настроен)
```bash
# Проверить текущие настройки
git config --list

# Настроить имя и email (если нужно)
git config --global user.name "Pavel Stepanov"
git config --global user.email "pavel@example.com"
```

### 4. Создание файлов проекта
```bash
# Создать README
echo "# My Awesome Project" > README.md

# Создать .gitignore
cat > .gitignore << EOF
# Dependencies
node_modules/
*.log

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
EOF

# Создать структуру проекта
mkdir src docs tests
touch src/main.py src/utils.py
```

### 5. Первый коммит
```bash
# Добавить все файлы
git add .

# Проверить что добавлено
git status

# Сделать первый коммит
git commit -m "Initial project setup

- Created project structure
- Added README.md
- Added .gitignore
- Created basic source files"
```

### 6. Создание репозитория на GitHub

#### Вариант A: Через веб-интерфейс
1. Перейти на [github.com](https://github.com)
2. Нажать "New repository"
3. Заполнить:
   - **Repository name**: `my-awesome-project`
   - **Description**: `My awesome project description`
   - **Visibility**: Public или Private
   - **НЕ добавлять** README, .gitignore, license
4. Нажать "Create repository"

#### Вариант B: Через GitHub CLI (если установлен)
```bash
# Установить GitHub CLI (если не установлен)
brew install gh

# Авторизоваться
gh auth login

# Создать репозиторий
gh repo create my-awesome-project --public --description "My awesome project"
```

### 7. Подключение к GitHub
```bash
# Добавить удаленный репозиторий
git remote add origin https://github.com/username/my-awesome-project.git

# Проверить подключение
git remote -v
# Output:
# origin  https://github.com/username/my-awesome-project.git (fetch)
# origin  https://github.com/username/my-awesome-project.git (push)
```

### 8. Отправка кода на GitHub
```bash
# Отправить код на GitHub
git push -u origin main

# Если возникла ошибка с веткой main, попробуйте:
git branch -M main
git push -u origin main
```

## 🔐 Настройка аутентификации

### Personal Access Token (рекомендуется)
1. Перейти на GitHub → Settings → Developer settings → Personal access tokens
2. Нажать "Generate new token"
3. Выбрать scopes: `repo`, `workflow`
4. Скопировать токен
5. Использовать токен вместо пароля при push

### SSH ключи (альтернатива)
```bash
# Генерировать SSH ключ
ssh-keygen -t ed25519 -C "your.email@example.com"

# Добавить ключ в ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Скопировать публичный ключ
cat ~/.ssh/id_ed25519.pub

# Добавить ключ в GitHub:
# Settings → SSH and GPG keys → New SSH key
```

## 🧪 Тестирование настройки

### Проверить локальный репозиторий:
```bash
# Статус репозитория
git status

# История коммитов
git log --oneline

# Ветки
git branch
```

### Проверить подключение к GitHub:
```bash
# Получить информацию с GitHub
git fetch origin

# Проверить удаленные ветки
git branch -r
```

### Проверить на GitHub:
1. Перейти на https://github.com/username/my-awesome-project
2. Убедиться что файлы загружены
3. Проверить историю коммитов

## 🔄 Рабочий процесс

### Ежедневная работа:
```bash
# 1. Получить изменения с GitHub
git pull origin main

# 2. Работать с файлами
# ... вносить изменения ...

# 3. Добавить изменения
git add .

# 4. Сделать коммит
git commit -m "Описание изменений"

# 5. Отправить на GitHub
git push origin main
```

### Создание веток:
```bash
# Создать новую ветку
git checkout -b feature/new-feature

# Работать в ветке
# ... вносить изменения ...

# Коммитить изменения
git add .
git commit -m "Add new feature"

# Отправить ветку на GitHub
git push -u origin feature/new-feature

# Создать Pull Request на GitHub
```

## 🚨 Частые проблемы

### Проблема 1: "Repository not found"
```bash
# Решение: проверить URL
git remote -v
git remote set-url origin https://github.com/username/repo.git
```

### Проблема 2: "Permission denied"
```bash
# Решение: использовать токен или SSH
# Или проверить права доступа к репозиторию
```

### Проблема 3: "Updates were rejected"
```bash
# Решение: получить изменения перед отправкой
git pull origin main
git push origin main
```

### Проблема 4: "Branch 'main' does not exist"
```bash
# Решение: переименовать ветку
git branch -M main
git push -u origin main
```

## 📋 Чек-лист настройки

### Подготовка:
- [ ] Git установлен и настроен
- [ ] Аккаунт GitHub создан
- [ ] Интернет подключение

### Создание проекта:
- [ ] Создана папка проекта
- [ ] Выполнен `git init`
- [ ] Создан `.gitignore`
- [ ] Создан `README.md`
- [ ] Сделан первый коммит

### Подключение к GitHub:
- [ ] Создан репозиторий на GitHub
- [ ] Добавлен remote origin
- [ ] Настроена аутентификация
- [ ] Код отправлен на GitHub
- [ ] Проверен доступ к репозиторию

## 🎯 Итог

### Для работы с удаленными репозиториями нужно:
1. **Git** - установлен на компьютере ✅
2. **Аккаунт GitHub** - для хранения кода
3. **Интернет** - для синхронизации
4. **Аутентификация** - токен или SSH ключи

### Git vs GitHub:
- **Git** - система контроля версий (локально)
- **GitHub** - платформа для хранения кода (в облаке)

**Git обязателен, GitHub опционален, но очень удобен для совместной работы!**

---
*Создано: 13 октября 2025*  
*Версия: 1.0.0*

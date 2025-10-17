# 📚 Git & GitHub Шпаргалка

## 🎯 Основные различия

| | Git | GitHub |
|---|---|---|
| **Что это** | Система контроля версий | Веб-платформа для Git |
| **Где работает** | Локально на компьютере | В интернете |
| **Установка** | ✅ Нужна | ❌ Не нужна |
| **Функции** | Коммиты, ветки, слияния | Хостинг + Pull Requests + Issues |

## 🚀 Быстрая настройка нового проекта

```bash
# 1. Создать проект
mkdir my-project && cd my-project

# 2. Инициализировать Git
git init

# 3. Настроить Git (если не настроен)
git config user.name "Your Name"
git config user.email "your@email.com"

# 4. Создать файлы
echo "# My Project" > README.md
echo "node_modules/" > .gitignore

# 5. Первый коммит
git add .
git commit -m "Initial commit"

# 6. Создать репозиторий на GitHub (вручную или через gh cli)
gh repo create my-project --public

# 7. Подключить к GitHub
git remote add origin https://github.com/username/my-project.git

# 8. Отправить код
git push -u origin main
```

## 🔧 Основные команды

### Локальная работа:
```bash
git status              # Статус репозитория
git add .               # Добавить все изменения
git add filename        # Добавить конкретный файл
git commit -m "msg"     # Сделать коммит
git log --oneline       # История коммитов
git diff                # Показать изменения
```

### Работа с ветками:
```bash
git branch              # Список веток
git checkout -b name    # Создать ветку
git checkout name       # Переключиться на ветку
git merge name          # Слить ветку
git branch -d name      # Удалить ветку
```

### Работа с GitHub:
```bash
git remote -v           # Удаленные репозитории
git push origin main    # Отправить на GitHub
git pull origin main    # Получить с GitHub
git fetch origin        # Получить информацию
git clone url           # Клонировать репозиторий
```

## 🔐 Аутентификация

### Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token
3. Выбрать scopes: `repo`, `workflow`
4. Использовать токен вместо пароля

### SSH ключи:
```bash
ssh-keygen -t ed25519 -C "email@example.com"
cat ~/.ssh/id_ed25519.pub  # Скопировать в GitHub
```

## 🚨 Частые проблемы

| Проблема | Решение |
|----------|---------|
| "Repository not found" | Проверить URL: `git remote -v` |
| "Permission denied" | Использовать токен или SSH |
| "Updates rejected" | `git pull` перед `git push` |
| "Git not found" | Установить Git |

## 📋 Чек-лист нового проекта

- [ ] Git установлен (`git --version`)
- [ ] Git настроен (имя, email)
- [ ] Аккаунт GitHub создан
- [ ] Создан локальный репозиторий (`git init`)
- [ ] Создан `.gitignore`
- [ ] Сделан первый коммит
- [ ] Создан репозиторий на GitHub
- [ ] Подключен remote origin
- [ ] Код отправлен на GitHub

## 🎯 Итог

**Для работы с удаленными репозиториями нужно:**
1. **Git** (обязательно) - система контроля версий
2. **GitHub аккаунт** (для GitHub) - платформа хостинга
3. **Интернет** - для синхронизации
4. **Аутентификация** - токен или SSH

**Git работает локально, GitHub - в облаке!**

---
*Шпаргалка: 13 октября 2025*

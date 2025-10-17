# 🔄 Подробный Git Workflow - Как работать с изменениями

## 🎯 Основные принципы

### Git автоматически отслеживает изменения
Git **НЕ требует** ручного указания файлов для каждого коммита. Он автоматически отслеживает:
- Какие файлы изменены
- Какие файлы добавлены
- Какие файлы удалены
- Содержимое изменений

## 📋 Пошаговый процесс работы с изменениями

### 1. Проверка статуса изменений
```bash
# Посмотреть какие файлы изменены
git status

# Посмотреть детали изменений
git diff

# Посмотреть изменения в конкретном файле
git diff frontend/src/components/MyComponent.tsx
```

### 2. Добавление файлов в staging area
```bash
# Добавить все измененные файлы
git add .

# Добавить конкретный файл
git add frontend/src/components/MyComponent.tsx

# Добавить несколько файлов
git add file1.tsx file2.tsx file3.tsx

# Добавить все файлы определенного типа
git add *.tsx

# Добавить все файлы в папке
git add frontend/src/components/
```

### 3. Создание коммита
```bash
# Коммит с сообщением
git commit -m "feat: добавить новую функцию"

# Коммит с подробным описанием
git commit -m "feat: добавить новую функцию

- Добавлен компонент MyComponent
- Обновлен Dashboard для интеграции
- Добавлены типы в types/index.ts
- Обновлена документация"
```

## 🔍 Как Git определяет изменения

### Автоматическое отслеживание
Git использует несколько механизмов:

1. **Индекс файлов** - отслеживает состояние файлов
2. **Хеши содержимого** - сравнивает содержимое файлов
3. **Временные метки** - отслеживает время изменения
4. **Статус файлов** - отслеживает staged/unstaged состояние

### Команды для анализа изменений
```bash
# Показать все измененные файлы
git status --porcelain

# Показать статистику изменений
git diff --stat

# Показать изменения между коммитами
git diff HEAD~1 HEAD

# Показать изменения в ветке
git diff main..feature/new-feature
```

## 🛠️ Работа с Cursor и другими IDE

### Cursor автоматически отслеживает изменения
Когда вы работаете в Cursor:

1. **Файлы автоматически помечаются** как измененные
2. **Git видит все изменения** в реальном времени
3. **Не нужно вручную указывать** какие файлы изменились

### Проверка изменений в Cursor
```bash
# После работы в Cursor проверьте статус
git status

# Вы увидите что-то вроде:
# Modified:   frontend/src/components/MyComponent.tsx
# Modified:   frontend/src/pages/Dashboard.tsx
# Modified:   frontend/src/types/index.ts
# Untracked:  frontend/src/utils/newUtil.ts
```

### Добавление всех изменений
```bash
# Добавить ВСЕ измененные файлы одной командой
git add .

# Или более селективно
git add frontend/src/components/
git add frontend/src/pages/
git add frontend/src/types/
```

## 📊 Практический пример

### Сценарий: Добавляем новую функцию
Допустим, мы добавляем функцию "Аналитика рисков":

```bash
# 1. Создаем ветку
git checkout -b feature/risk-analytics

# 2. Работаем в Cursor, изменяем файлы:
# - frontend/src/components/RiskChart.tsx (новый)
# - frontend/src/pages/Analytics.tsx (изменен)
# - frontend/src/types/index.ts (изменен)
# - backend/api/risk_calculator.py (новый)

# 3. Проверяем что изменилось
git status
# Output:
# Untracked files:
#   frontend/src/components/RiskChart.tsx
#   backend/api/risk_calculator.py
# Modified files:
#   frontend/src/pages/Analytics.tsx
#   frontend/src/types/index.ts

# 4. Добавляем все изменения
git add .

# 5. Проверяем что добавлено
git status
# Output:
# Changes to be committed:
#   new file:   frontend/src/components/RiskChart.tsx
#   new file:   backend/api/risk_calculator.py
#   modified:   frontend/src/pages/Analytics.tsx
#   modified:   frontend/src/types/index.ts

# 6. Коммитим
git commit -m "feat: добавить аналитику рисков

- Создан компонент RiskChart для визуализации
- Обновлена страница Analytics
- Добавлены типы для рисков
- Реализован backend калькулятор рисков"

# 7. Отправляем на GitHub
git push origin feature/risk-analytics
```

## 🎯 Merge Request включает ВСЕ изменения

### Важно понимать:
- **Merge Request** включает ВСЕ коммиты в ветке
- **Не нужно указывать** конкретные файлы для MR
- **GitHub автоматически** показывает все изменения

### Что видит GitHub в MR:
```
Files changed: 4
+ 156 additions
- 23 deletions

frontend/src/components/RiskChart.tsx     (+89 lines)
frontend/src/pages/Analytics.tsx          (+45 lines, -12 lines)
frontend/src/types/index.ts               (+22 lines, -11 lines)
backend/api/risk_calculator.py            (+67 lines)
```

## 🔧 Полезные команды для работы

### Анализ изменений
```bash
# Показать изменения в последнем коммите
git show

# Показать изменения в конкретном коммите
git show abc1234

# Показать изменения между ветками
git diff main..feature/new-feature

# Показать только имена измененных файлов
git diff --name-only main..feature/new-feature
```

### Работа с staging area
```bash
# Добавить все изменения
git add .

# Добавить только измененные файлы (не новые)
git add -u

# Добавить интерактивно
git add -i

# Убрать файл из staging
git reset HEAD filename

# Убрать все из staging
git reset HEAD
```

### Отмена изменений
```bash
# Отменить изменения в файле (до staging)
git checkout -- filename

# Отменить все изменения
git checkout -- .

# Отменить последний коммит (сохранить изменения)
git reset --soft HEAD~1

# Отменить последний коммит (удалить изменения)
git reset --hard HEAD~1
```

## 🚨 Частые ошибки и решения

### Ошибка 1: "Nothing to commit"
```bash
# Проблема: git add . не сработал
# Решение: проверьте статус
git status

# Если файлы не отслеживаются, добавьте их
git add filename
```

### Ошибка 2: "Changes not staged for commit"
```bash
# Проблема: файлы изменены, но не добавлены
# Решение: добавьте файлы
git add .
git commit -m "your message"
```

### Ошибка 3: "Untracked files"
```bash
# Проблема: новые файлы не отслеживаются
# Решение: добавьте их явно
git add newfile.tsx
# или
git add .
```

## 📋 Best Practices

### 1. Регулярно проверяйте статус
```bash
git status
```

### 2. Делайте атомарные коммиты
```bash
# Хорошо: один коммит = одна функция
git commit -m "feat: добавить компонент RiskChart"

# Плохо: много функций в одном коммите
git commit -m "feat: добавить аналитику, исправить баги, обновить стили"
```

### 3. Используйте .gitignore
```bash
# Добавьте в .gitignore файлы, которые не нужно отслеживать
node_modules/
*.log
.env
```

### 4. Проверяйте изменения перед коммитом
```bash
git diff --cached  # показать staged изменения
git diff           # показать unstaged изменения
```

## 🎯 Итог

**Git автоматически отслеживает все изменения!**

- ✅ **Не нужно** вручную указывать файлы
- ✅ **Cursor** автоматически помечает измененные файлы
- ✅ **git add .** добавляет все изменения
- ✅ **Merge Request** включает все коммиты в ветке
- ✅ **GitHub** автоматически показывает все изменения

**Просто работайте в Cursor, а Git сам отследит что изменилось!**

---
*Создано: 13 октября 2025*  
*Версия: 1.0.0*

#!/bin/bash

# Скрипт для отправки кода на GitHub после создания репозитория

echo "🐙 Отправка кода на GitHub..."
echo "=================================================="

# Проверить подключение к удаленному репозиторию
echo "🔍 Проверка подключения к GitHub..."
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Удаленный репозиторий не настроен"
    echo "   Выполните: git remote add origin https://github.com/pavelstepanovpm/credanlv2.git"
    exit 1
fi

echo "✅ Удаленный репозиторий настроен"
git remote -v

# Проверить статус
echo ""
echo "🔍 Проверка статуса репозитория..."
git status

# Отправить main ветку
echo ""
echo "🚀 Отправка main ветки..."
if git push -u origin main; then
    echo "✅ Main ветка отправлена успешно"
else
    echo "❌ Ошибка при отправке main ветки"
    exit 1
fi

# Отправить остальные ветки
echo ""
echo "🚀 Отправка остальных веток..."

echo "📤 Отправка develop ветки..."
if git push origin develop; then
    echo "✅ Develop ветка отправлена"
else
    echo "⚠️  Develop ветка не отправлена (возможно, уже существует)"
fi

echo "📤 Отправка feature/new-features ветки..."
if git push origin feature/new-features; then
    echo "✅ Feature ветка отправлена"
else
    echo "⚠️  Feature ветка не отправлена (возможно, уже существует)"
fi

echo "📤 Отправка hotfix/bug-fixes ветки..."
if git push origin hotfix/bug-fixes; then
    echo "✅ Hotfix ветка отправлена"
else
    echo "⚠️  Hotfix ветка не отправлена (возможно, уже существует)"
fi

# Отправить теги
echo ""
echo "🏷️  Отправка тегов..."
if git push --tags; then
    echo "✅ Теги отправлены успешно"
else
    echo "❌ Ошибка при отправке тегов"
fi

# Проверить финальный статус
echo ""
echo "🔍 Финальная проверка..."
echo "Ветки на GitHub:"
git branch -r

echo ""
echo "Теги на GitHub:"
git tag -l

echo ""
echo "🎉 Код успешно отправлен на GitHub!"
echo "🔗 Репозиторий: https://github.com/pavelstepanovpm/credanlv2"
echo ""
echo "📋 Что дальше:"
echo "1. Перейдите на https://github.com/pavelstepanovpm/credanlv2"
echo "2. Добавьте описание репозитория"
echo "3. Настройте теги (topics)"
echo "4. Настройте защиту веток (опционально)"

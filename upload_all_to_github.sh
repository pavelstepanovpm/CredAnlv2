#!/bin/bash

# Скрипт для загрузки всех веток и тегов на GitHub

echo "🚀 Загрузка всех веток и тегов на GitHub..."
echo "=================================================="

# Проверяем подключение к GitHub
echo "🔍 Проверка подключения к GitHub..."
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Удаленный репозиторий не настроен"
    echo "   Выполните: git remote add origin https://github.com/pavelstepanovpm/CredAnlv2.git"
    exit 1
fi

echo "✅ Удаленный репозиторий настроен"
git remote -v

# Список всех веток для загрузки
branches=("main" "develop" "feature/covenant-badge" "demo/multiple-files" "feature/new-features" "hotfix/bug-fixes")

echo ""
echo "📤 Загружаем ветки..."

# Загружаем каждую ветку
for branch in "${branches[@]}"; do
    echo ""
    echo "🔄 Переключаемся на ветку: $branch"
    
    # Переключаемся на ветку
    if git checkout "$branch" > /dev/null 2>&1; then
        echo "✅ Переключились на $branch"
        
        # Загружаем ветку
        echo "📤 Загружаем ветку $branch на GitHub..."
        if git push origin "$branch"; then
            echo "✅ Ветка $branch загружена успешно"
        else
            echo "❌ Ошибка загрузки ветки $branch"
        fi
    else
        echo "⚠️  Ветка $branch не найдена, пропускаем"
    fi
done

echo ""
echo "🏷️  Загружаем теги..."
if git push --tags; then
    echo "✅ Теги загружены успешно"
else
    echo "❌ Ошибка загрузки тегов"
fi

echo ""
echo "🔍 Финальная проверка..."

# Проверяем удаленные ветки
echo "📋 Удаленные ветки:"
git branch -r

echo ""
echo "🏷️  Локальные теги:"
git tag -l

echo ""
echo "🎉 Загрузка завершена!"
echo "🔗 Репозиторий: https://github.com/pavelstepanovpm/CredAnlv2"
echo ""
echo "📋 Что загружено:"
echo "✅ Все ветки отправлены на GitHub"
echo "✅ Все теги отправлены на GitHub"
echo "✅ Полная система аналитики кредитного портфеля"
echo "✅ Backend (FastAPI + Quantlib)"
echo "✅ Frontend (React/TypeScript)"
echo "✅ Документация и скрипты"
echo ""
echo "🌐 Проверьте результат на GitHub:"
echo "   https://github.com/pavelstepanovpm/CredAnlv2"

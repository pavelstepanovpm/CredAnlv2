#!/usr/bin/env python3
"""
Скрипт для автоматической отправки кода на GitHub после создания репозитория
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(command, description):
    """Выполнить команду и показать результат"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Успешно")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Ошибка")
            if result.stderr.strip():
                print(f"   {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Исключение: {e}")
        return False

def check_repo_exists():
    """Проверить существование репозитория на GitHub"""
    print("🔍 Проверка существования репозитория на GitHub...")
    
    success = run_command(
        "git ls-remote https://github.com/pavelstepanovpm/credanlv2.git",
        "Проверка репозитория"
    )
    
    if success:
        print("✅ Репозиторий существует на GitHub")
        return True
    else:
        print("❌ Репозиторий НЕ существует на GitHub")
        print("   Сначала создайте репозиторий на https://github.com/new")
        return False

def push_to_github():
    """Отправить код на GitHub"""
    print("🚀 Отправка кода на GitHub...")
    
    # Проверить подключение
    print("🔍 Проверка подключения к GitHub...")
    success = run_command("git remote -v", "Проверка удаленных репозиториев")
    if not success:
        print("❌ Удаленный репозиторий не настроен")
        return False
    
    # Отправить main ветку
    print("\n📤 Отправка main ветки...")
    if not run_command("git push -u origin main", "Отправка main ветки"):
        print("❌ Ошибка отправки main ветки")
        return False
    
    # Отправить остальные ветки
    branches = ["develop", "feature/new-features", "hotfix/bug-fixes"]
    
    for branch in branches:
        print(f"\n📤 Отправка {branch} ветки...")
        success = run_command(f"git push origin {branch}", f"Отправка {branch} ветки")
        if not success:
            print(f"⚠️  {branch} ветка не отправлена (возможно, уже существует)")
    
    # Отправить теги
    print("\n🏷️  Отправка тегов...")
    if not run_command("git push --tags", "Отправка тегов"):
        print("❌ Ошибка отправки тегов")
        return False
    
    return True

def verify_upload():
    """Проверить успешность загрузки"""
    print("\n🔍 Проверка загрузки...")
    
    # Проверить ветки
    success = run_command("git branch -r", "Проверка удаленных веток")
    if success:
        print("✅ Ветки загружены")
    
    # Проверить теги
    success = run_command("git tag -l", "Проверка тегов")
    if success:
        print("✅ Теги загружены")
    
    return True

def main():
    """Основная функция"""
    print("🐙 Отправка кода на GitHub")
    print("=" * 50)
    
    # Проверить существование репозитория
    if not check_repo_exists():
        print("\n❌ Репозиторий не найден на GitHub")
        print("📋 Инструкции:")
        print("1. Перейдите на https://github.com/new")
        print("2. Создайте репозиторий с названием 'credanlv2'")
        print("3. НЕ добавляйте README, .gitignore, license")
        print("4. Запустите этот скрипт снова")
        return
    
    # Отправить код
    if push_to_github():
        print("\n🎉 Код успешно отправлен на GitHub!")
        print("🔗 Репозиторий: https://github.com/pavelstepanovpm/credanlv2")
        
        # Проверить загрузку
        verify_upload()
        
        print("\n📋 Что дальше:")
        print("1. Перейдите на https://github.com/pavelstepanovpm/credanlv2")
        print("2. Добавьте описание репозитория")
        print("3. Настройте теги (topics)")
        print("4. Настройте защиту веток (опционально)")
    else:
        print("\n❌ Ошибка отправки кода на GitHub")
        print("🔧 Проверьте:")
        print("1. Существует ли репозиторий на GitHub")
        print("2. Правильно ли настроен удаленный репозиторий")
        print("3. Есть ли права доступа к репозиторию")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Скрипт для проверки и создания репозитория на GitHub
"""

import subprocess
import sys
import webbrowser
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
            return True, result.stdout.strip()
        else:
            print(f"❌ {description} - Ошибка")
            if result.stderr.strip():
                print(f"   {result.stderr.strip()}")
            return False, result.stderr.strip()
    except Exception as e:
        print(f"❌ {description} - Исключение: {e}")
        return False, str(e)

def check_github_repo():
    """Проверить существование репозитория на GitHub"""
    print("🔍 Проверка репозитория на GitHub...")
    
    # Попробовать получить информацию о репозитории
    success, output = run_command(
        "git ls-remote https://github.com/pavelstepanovpm/credanlv2.git",
        "Проверка существования репозитория"
    )
    
    if success:
        print("✅ Репозиторий существует на GitHub")
        return True
    else:
        print("❌ Репозиторий НЕ существует на GitHub")
        return False

def check_github_cli():
    """Проверить наличие GitHub CLI"""
    print("🔍 Проверка GitHub CLI...")
    
    success, output = run_command("gh --version", "Проверка GitHub CLI")
    
    if success:
        print("✅ GitHub CLI установлен")
        return True
    else:
        print("❌ GitHub CLI не установлен")
        return False

def create_repo_with_cli():
    """Создать репозиторий через GitHub CLI"""
    print("🚀 Создание репозитория через GitHub CLI...")
    
    # Проверить авторизацию
    auth_success, _ = run_command("gh auth status", "Проверка авторизации GitHub CLI")
    if not auth_success:
        print("❌ Не авторизован в GitHub CLI")
        print("   Выполните: gh auth login")
        return False
    
    # Создать репозиторий
    create_success, output = run_command(
        "gh repo create credanlv2 --public --description 'Credit Portfolio Analytics System - FastAPI + React/TypeScript'",
        "Создание репозитория"
    )
    
    if create_success:
        print("✅ Репозиторий создан через GitHub CLI")
        return True
    else:
        print("❌ Ошибка создания репозитория через GitHub CLI")
        return False

def open_github_create_page():
    """Открыть страницу создания репозитория в браузере"""
    print("🌐 Открытие страницы создания репозитория...")
    
    url = "https://github.com/new"
    print(f"🔗 Откройте в браузере: {url}")
    
    try:
        webbrowser.open(url)
        print("✅ Страница открыта в браузере")
        return True
    except Exception as e:
        print(f"❌ Ошибка открытия браузера: {e}")
        return False

def show_manual_instructions():
    """Показать инструкции для ручного создания"""
    print("\n📋 Инструкции для создания репозитория вручную:")
    print("=" * 60)
    print("1. Перейдите на https://github.com/new")
    print("2. Заполните форму:")
    print("   - Repository name: credanlv2")
    print("   - Description: Credit Portfolio Analytics System - FastAPI + React/TypeScript")
    print("   - Visibility: Public")
    print("   - НЕ добавляйте README, .gitignore, license")
    print("3. Нажмите 'Create repository'")
    print("4. После создания выполните команды:")
    print("   git push -u origin main")
    print("   git push origin develop")
    print("   git push origin feature/new-features")
    print("   git push origin hotfix/bug-fixes")
    print("   git push --tags")

def main():
    """Основная функция"""
    print("🐙 Проверка и создание репозитория на GitHub")
    print("=" * 60)
    
    # Проверить существование репозитория
    if check_github_repo():
        print("\n🎉 Репозиторий уже существует!")
        print("🔗 URL: https://github.com/pavelstepanovpm/credanlv2")
        return
    
    print("\n❌ Репозиторий не найден. Создаем...")
    
    # Проверить GitHub CLI
    if check_github_cli():
        print("\n🤖 Попытка создания через GitHub CLI...")
        if create_repo_with_cli():
            print("\n🎉 Репозиторий создан через GitHub CLI!")
            print("🔗 URL: https://github.com/pavelstepanovpm/credanlv2")
            return
    
    print("\n🌐 Создание через веб-интерфейс...")
    open_github_create_page()
    show_manual_instructions()
    
    print("\n⏳ После создания репозитория на GitHub:")
    print("   Выполните: python3 push_to_github.py")

if __name__ == "__main__":
    main()

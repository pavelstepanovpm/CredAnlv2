#!/usr/bin/env python3
"""
Скрипт для подключения локального Git репозитория к GitHub
"""

import subprocess
import sys
import os
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

def check_git_status():
    """Проверить статус Git репозитория"""
    print("🔍 Проверка Git репозитория...")
    
    # Проверить, что мы в Git репозитории
    if not run_command("git rev-parse --git-dir", "Проверка Git репозитория"):
        print("❌ Не найден Git репозиторий. Запустите 'git init' сначала.")
        return False
    
    # Проверить статус
    run_command("git status", "Проверка статуса")
    
    # Проверить ветки
    run_command("git branch -a", "Проверка веток")
    
    # Проверить теги
    run_command("git tag -l", "Проверка тегов")
    
    return True

def get_github_info():
    """Получить информацию о GitHub репозитории"""
    print("\n📝 Информация для подключения к GitHub:")
    print("=" * 50)
    
    username = input("Введите ваш GitHub username: ").strip()
    if not username:
        print("❌ Username не может быть пустым")
        return None
    
    repo_name = input("Введите название репозитория (по умолчанию: credanlv2): ").strip()
    if not repo_name:
        repo_name = "credanlv2"
    
    visibility = input("Репозиторий будет публичным? (y/n, по умолчанию: y): ").strip().lower()
    is_public = visibility != 'n'
    
    return {
        'username': username,
        'repo_name': repo_name,
        'is_public': is_public
    }

def create_github_commands(github_info):
    """Создать команды для подключения к GitHub"""
    username = github_info['username']
    repo_name = github_info['repo_name']
    
    print(f"\n🚀 Команды для подключения к GitHub:")
    print("=" * 50)
    
    print(f"1. Создайте репозиторий на GitHub:")
    print(f"   https://github.com/new")
    print(f"   Название: {repo_name}")
    print(f"   Описание: Credit Portfolio Analytics System - FastAPI + React")
    print(f"   Видимость: {'Public' if github_info['is_public'] else 'Private'}")
    print(f"   НЕ добавляйте README, .gitignore, license")
    
    print(f"\n2. После создания репозитория выполните команды:")
    print(f"   git remote add origin https://github.com/{username}/{repo_name}.git")
    print(f"   git remote -v")
    print(f"   git push -u origin main")
    print(f"   git push origin develop")
    print(f"   git push origin feature/new-features")
    print(f"   git push origin hotfix/bug-fixes")
    print(f"   git push --tags")
    
    return f"https://github.com/{username}/{repo_name}.git"

def main():
    """Основная функция"""
    print("🐙 Подключение к GitHub")
    print("=" * 50)
    
    # Проверить Git репозиторий
    if not check_git_status():
        return
    
    # Получить информацию о GitHub
    github_info = get_github_info()
    if not github_info:
        return
    
    # Создать команды
    repo_url = create_github_commands(github_info)
    
    # Спросить, хочет ли пользователь выполнить команды автоматически
    auto_execute = input("\n🤖 Выполнить команды автоматически? (y/n): ").strip().lower()
    
    if auto_execute == 'y':
        print("\n🚀 Выполнение команд...")
        
        # Добавить удаленный репозиторий
        remote_cmd = f"git remote add origin {repo_url}"
        if run_command(remote_cmd, "Добавление удаленного репозитория"):
            # Проверить подключение
            run_command("git remote -v", "Проверка удаленных репозиториев")
            
            # Отправить ветки
            run_command("git push -u origin main", "Отправка main ветки")
            run_command("git push origin develop", "Отправка develop ветки")
            run_command("git push origin feature/new-features", "Отправка feature ветки")
            run_command("git push origin hotfix/bug-fixes", "Отправка hotfix ветки")
            run_command("git push --tags", "Отправка тегов")
            
            print(f"\n🎉 Репозиторий успешно подключен к GitHub!")
            print(f"🔗 URL: {repo_url}")
        else:
            print("❌ Ошибка при добавлении удаленного репозитория")
    else:
        print(f"\n📋 Выполните команды вручную после создания репозитория на GitHub")
        print(f"🔗 URL репозитория: {repo_url}")

if __name__ == "__main__":
    main()

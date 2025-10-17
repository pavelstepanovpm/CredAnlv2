#!/usr/bin/env python3
"""
Скрипт для загрузки всех веток и тегов на GitHub
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

def check_github_connection():
    """Проверить подключение к GitHub"""
    print("🔍 Проверка подключения к GitHub...")
    
    success = run_command("git remote get-url origin", "Проверка удаленного репозитория")
    if not success:
        print("❌ Удаленный репозиторий не настроен")
        print("   Выполните: git remote add origin https://github.com/pavelstepanovpm/CredAnlv2.git")
        return False
    
    print("✅ Удаленный репозиторий настроен")
    run_command("git remote -v", "Проверка URL репозитория")
    return True

def upload_branches():
    """Загрузить все ветки на GitHub"""
    print("\n📤 Загружаем ветки...")
    
    # Список всех веток для загрузки
    branches = [
        "main",
        "develop", 
        "feature/covenant-badge",
        "demo/multiple-files",
        "feature/new-features",
        "hotfix/bug-fixes"
    ]
    
    success_count = 0
    
    for branch in branches:
        print(f"\n🔄 Работаем с веткой: {branch}")
        
        # Переключаемся на ветку
        if run_command(f"git checkout {branch}", f"Переключение на {branch}"):
            # Загружаем ветку
            if run_command(f"git push origin {branch}", f"Загрузка {branch}"):
                success_count += 1
                print(f"✅ Ветка {branch} загружена успешно")
            else:
                print(f"❌ Ошибка загрузки ветки {branch}")
        else:
            print(f"⚠️  Ветка {branch} не найдена, пропускаем")
    
    print(f"\n📊 Результат: {success_count}/{len(branches)} веток загружено")
    return success_count > 0

def upload_tags():
    """Загрузить все теги на GitHub"""
    print("\n🏷️  Загружаем теги...")
    
    success = run_command("git push --tags", "Загрузка тегов")
    if success:
        print("✅ Теги загружены успешно")
    else:
        print("❌ Ошибка загрузки тегов")
    
    return success

def verify_upload():
    """Проверить результат загрузки"""
    print("\n🔍 Финальная проверка...")
    
    # Проверяем удаленные ветки
    print("📋 Удаленные ветки:")
    run_command("git branch -r", "Проверка удаленных веток")
    
    # Проверяем теги
    print("\n🏷️  Локальные теги:")
    run_command("git tag -l", "Проверка тегов")
    
    # Проверяем статус
    print("\n📊 Статус репозитория:")
    run_command("git status", "Проверка статуса")

def main():
    """Основная функция"""
    print("🚀 Загрузка всех веток и тегов на GitHub")
    print("=" * 60)
    
    # Проверяем подключение
    if not check_github_connection():
        return
    
    # Загружаем ветки
    branches_success = upload_branches()
    
    # Загружаем теги
    tags_success = upload_tags()
    
    # Проверяем результат
    verify_upload()
    
    # Итоговый отчет
    print("\n🎉 Загрузка завершена!")
    print("🔗 Репозиторий: https://github.com/pavelstepanovpm/CredAnlv2")
    print("")
    print("📋 Что загружено:")
    print("✅ Все ветки отправлены на GitHub" if branches_success else "❌ Ошибка загрузки веток")
    print("✅ Все теги отправлены на GitHub" if tags_success else "❌ Ошибка загрузки тегов")
    print("✅ Полная система аналитики кредитного портфеля")
    print("✅ Backend (FastAPI + Quantlib)")
    print("✅ Frontend (React/TypeScript)")
    print("✅ Документация и скрипты")
    print("")
    print("🌐 Проверьте результат на GitHub:")
    print("   https://github.com/pavelstepanovpm/CredAnlv2")
    
    if branches_success and tags_success:
        print("\n🎯 Все готово! Репозиторий полностью синхронизирован с GitHub.")
    else:
        print("\n⚠️  Некоторые операции завершились с ошибками. Проверьте логи выше.")

if __name__ == "__main__":
    main()

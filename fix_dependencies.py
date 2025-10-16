#!/usr/bin/env python3
"""
Скрипт для исправления проблем с зависимостями
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Вывод баннера"""
    print("🔧 Исправление зависимостей системы аналитики кредитного портфеля")
    print("=" * 70)

def clean_frontend():
    """Очистка фронтенда"""
    print("\n🧹 Очистка фронтенда...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Директория frontend не найдена")
        return False
    
    # Удаляем node_modules и package-lock.json
    node_modules = frontend_dir / "node_modules"
    package_lock = frontend_dir / "package-lock.json"
    
    if node_modules.exists():
        print("🗑️ Удаление node_modules...")
        shutil.rmtree(node_modules)
    
    if package_lock.exists():
        print("🗑️ Удаление package-lock.json...")
        package_lock.unlink()
    
    print("✅ Фронтенд очищен")
    return True

def install_frontend_deps():
    """Установка зависимостей фронтенда"""
    print("\n📦 Установка зависимостей фронтенда...")
    
    frontend_dir = Path("frontend")
    os.chdir(frontend_dir)
    
    try:
        # Установка с legacy-peer-deps и исправление ajv
        result = subprocess.run([
            'npm', 'install', 'ajv@^8.0.0', '--legacy-peer-deps', '--force'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Дополнительная установка всех зависимостей
            result = subprocess.run([
                'npm', 'install', '--legacy-peer-deps', '--force'
            ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Зависимости фронтенда установлены")
            return True
        else:
            print(f"❌ Ошибка установки: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    finally:
        os.chdir("..")

def clean_backend():
    """Очистка бэкенда"""
    print("\n🧹 Очистка бэкенда...")
    
    try:
        # Удаляем кэш pip
        subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], 
                      capture_output=True)
        print("✅ Кэш pip очищен")
        return True
    except Exception as e:
        print(f"❌ Ошибка очистки бэкенда: {e}")
        return False

def install_backend_deps():
    """Установка зависимостей бэкенда"""
    print("\n📦 Установка зависимостей бэкенда...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt", "--upgrade"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Зависимости бэкенда установлены")
            return True
        else:
            print(f"❌ Ошибка установки: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция"""
    print_banner()
    
    print("🔍 Проверка проблем с зависимостями...")
    print("💡 Этот скрипт исправит конфликты версий и переустановит зависимости")
    
    # Очистка и переустановка фронтенда
    if not clean_frontend():
        print("❌ Не удалось очистить фронтенд")
        return False
    
    if not install_frontend_deps():
        print("❌ Не удалось установить зависимости фронтенда")
        return False
    
    # Очистка и переустановка бэкенда
    if not clean_backend():
        print("❌ Не удалось очистить бэкенд")
        return False
    
    if not install_backend_deps():
        print("❌ Не удалось установить зависимости бэкенда")
        return False
    
    print("\n" + "=" * 70)
    print("🎉 Зависимости успешно исправлены!")
    print("=" * 70)
    print("💡 Теперь можно запустить систему:")
    print("   python start.py")
    print("   или")
    print("   python start_system.py")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Не удалось исправить зависимости")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)

#!/usr/bin/env python3
"""
Единый скрипт для запуска системы аналитики кредитного портфеля
Запускает бэкенд и фронтенд одновременно
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path
from datetime import datetime

class SystemLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def print_banner(self):
        """Вывод баннера системы"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🏦 СИСТЕМА АНАЛИТИКИ КРЕДИТНОГО ПОРТФЕЛЯ 🏦                    ║
║                                                                              ║
║  🚀 Запуск полной системы в режиме разработки                                ║
║  📊 Backend: FastAPI + Quantlib                                              ║
║  🎨 Frontend: React + TypeScript                                             ║
║  💼 Trading Terminal Style Interface                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"🕐 Время запуска: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print("=" * 80)
    
    def check_requirements(self):
        """Проверка требований системы"""
        print("🔍 Проверка требований системы...")
        
        # Проверка Python
        try:
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
                print("❌ Требуется Python 3.8 или выше")
                return False
            print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        except Exception as e:
            print(f"❌ Ошибка проверки Python: {e}")
            return False
        
        # Проверка Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js {result.stdout.strip()}")
            else:
                print("❌ Node.js не найден. Установите Node.js 16+")
                return False
        except FileNotFoundError:
            print("❌ Node.js не найден. Установите Node.js 16+")
            return False
        
        # Проверка npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm {result.stdout.strip()}")
            else:
                print("❌ npm не найден")
                return False
        except FileNotFoundError:
            print("❌ npm не найден")
            return False
        
        return True
    
    def install_backend_dependencies(self):
        """Установка зависимостей бэкенда"""
        print("\n📦 Установка зависимостей бэкенда...")
        
        backend_requirements = Path("backend/requirements.txt")
        if not backend_requirements.exists():
            print("❌ Файл backend/requirements.txt не найден")
            return False
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Зависимости бэкенда установлены")
                return True
            else:
                print(f"❌ Ошибка установки зависимостей бэкенда: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Ошибка установки зависимостей бэкенда: {e}")
            return False
    
    def install_frontend_dependencies(self):
        """Установка зависимостей фронтенда"""
        print("\n📦 Установка зависимостей фронтенда...")
        
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            print("❌ Директория frontend не найдена")
            return False
        
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            print("❌ Файл frontend/package.json не найден")
            return False
        
        try:
            # Переходим в директорию фронтенда
            os.chdir(frontend_dir)
            
            # Проверяем, есть ли node_modules
            if not Path("node_modules").exists():
                print("📥 Установка npm пакетов...")
                result = subprocess.run(['npm', 'install', '--legacy-peer-deps'], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Зависимости фронтенда установлены")
                else:
                    print(f"❌ Ошибка установки зависимостей фронтенда: {result.stderr}")
                    return False
            else:
                print("✅ Зависимости фронтенда уже установлены")
            
            # Возвращаемся в корневую директорию
            os.chdir("..")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка установки зависимостей фронтенда: {e}")
            return False
    
    def start_backend(self):
        """Запуск бэкенда"""
        print("\n🚀 Запуск бэкенда...")
        
        try:
            # Запускаем бэкенд в отдельном процессе
            self.backend_process = subprocess.Popen([
                sys.executable, "run_backend.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Ждем немного, чтобы бэкенд запустился
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ Бэкенд запущен на http://localhost:8000")
                print("📚 API документация: http://localhost:8000/docs")
                return True
            else:
                print("❌ Ошибка запуска бэкенда")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка запуска бэкенда: {e}")
            return False
    
    def start_frontend(self):
        """Запуск фронтенда"""
        print("\n🎨 Запуск фронтенда...")
        
        try:
            # Переходим в директорию фронтенда
            frontend_dir = Path("frontend")
            os.chdir(frontend_dir)
            
            # Запускаем фронтенд в отдельном процессе
            self.frontend_process = subprocess.Popen([
                'npm', 'start'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Возвращаемся в корневую директорию
            os.chdir("..")
            
            # Ждем немного, чтобы фронтенд запустился
            time.sleep(5)
            
            if self.frontend_process.poll() is None:
                print("✅ Фронтенд запущен на http://localhost:3000")
                return True
            else:
                print("❌ Ошибка запуска фронтенда")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка запуска фронтенда: {e}")
            return False
    
    def monitor_processes(self):
        """Мониторинг процессов"""
        print("\n👀 Мониторинг процессов...")
        print("💡 Нажмите Ctrl+C для остановки системы")
        print("=" * 80)
        
        try:
            while self.running:
                # Проверяем статус бэкенда
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Бэкенд остановлен неожиданно")
                    break
                
                # Проверяем статус фронтенда
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Фронтенд остановлен неожиданно")
                    break
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Получен сигнал остановки...")
            self.stop_system()
    
    def stop_system(self):
        """Остановка системы"""
        print("\n🛑 Остановка системы...")
        self.running = False
        
        if self.backend_process:
            print("🔄 Остановка бэкенда...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
                print("✅ Бэкенд остановлен")
            except subprocess.TimeoutExpired:
                print("⚠️ Принудительная остановка бэкенда...")
                self.backend_process.kill()
        
        if self.frontend_process:
            print("🔄 Остановка фронтенда...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
                print("✅ Фронтенд остановлен")
            except subprocess.TimeoutExpired:
                print("⚠️ Принудительная остановка фронтенда...")
                self.frontend_process.kill()
        
        print("✅ Система остановлена")
    
    def run(self):
        """Основной метод запуска"""
        self.print_banner()
        
        # Проверка требований
        if not self.check_requirements():
            print("\n❌ Требования не выполнены. Установите необходимые компоненты.")
            return False
        
        # Установка зависимостей
        if not self.install_backend_dependencies():
            print("\n❌ Не удалось установить зависимости бэкенда")
            return False
        
        if not self.install_frontend_dependencies():
            print("\n❌ Не удалось установить зависимости фронтенда")
            return False
        
        # Запуск бэкенда
        if not self.start_backend():
            print("\n❌ Не удалось запустить бэкенд")
            return False
        
        # Запуск фронтенда
        if not self.start_frontend():
            print("\n❌ Не удалось запустить фронтенд")
            self.stop_system()
            return False
        
        # Вывод информации о системе
        print("\n" + "=" * 80)
        print("🎉 СИСТЕМА УСПЕШНО ЗАПУЩЕНА!")
        print("=" * 80)
        print("🌐 Фронтенд: http://localhost:3000")
        print("🔧 Бэкенд API: http://localhost:8000")
        print("📚 API документация: http://localhost:8000/docs")
        print("🔍 Health check: http://localhost:8000/health")
        print("=" * 80)
        print("💡 Система готова к работе!")
        print("🛑 Для остановки нажмите Ctrl+C")
        print("=" * 80)
        
        # Мониторинг процессов
        self.monitor_processes()
        
        return True

def signal_handler(signum, frame):
    """Обработчик сигналов"""
    print("\n🛑 Получен сигнал остановки...")
    launcher.stop_system()
    sys.exit(0)

if __name__ == "__main__":
    # Регистрация обработчиков сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Создание и запуск лаунчера
    launcher = SystemLauncher()
    
    try:
        success = launcher.run()
        if not success:
            print("\n❌ Не удалось запустить систему")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        launcher.stop_system()
        sys.exit(1)

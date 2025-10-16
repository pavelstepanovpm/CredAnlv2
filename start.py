#!/usr/bin/env python3
"""
Быстрый запуск системы аналитики кредитного портфеля
"""

import subprocess
import sys
import os

def main():
    print("🚀 Запуск системы аналитики кредитного портфеля...")
    print("📊 Backend: FastAPI + Quantlib")
    print("🎨 Frontend: React + TypeScript")
    print("=" * 60)
    
    # Проверяем, какой скрипт использовать
    if os.path.exists("start_system.py"):
        print("🐍 Используем Python скрипт...")
        subprocess.run([sys.executable, "start_system.py"])
    elif os.path.exists("start_system.sh"):
        print("🐚 Используем Bash скрипт...")
        subprocess.run(["./start_system.sh"])
    else:
        print("❌ Скрипты запуска не найдены")
        print("💡 Используйте: python start_system.py или ./start_system.sh")

if __name__ == "__main__":
    main()


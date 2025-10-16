#!/usr/bin/env python3
"""
Скрипт для исправления импортов в фронтенде
"""

import os
import re
from pathlib import Path

def fix_imports():
    """Исправление импортов во всех файлах"""
    print("🔧 Исправление импортов в фронтенде...")
    
    frontend_dir = Path("frontend/src")
    
    # Список файлов для исправления
    files_to_fix = [
        "components/CashflowChart.tsx",
        "components/MetricCard.tsx", 
        "components/Sidebar.tsx",
        "pages/Portfolio.tsx",
        "pages/Scenarios.tsx",
        "pages/Settings.tsx"
    ]
    
    for file_path in files_to_fix:
        full_path = frontend_dir / file_path
        if full_path.exists():
            print(f"📝 Исправление {file_path}...")
            fix_file_imports(full_path)
        else:
            print(f"⚠️ Файл {file_path} не найден")
    
    print("✅ Импорты исправлены")

def fix_file_imports(file_path: Path):
    """Исправление импортов в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Замена старых импортов Redux на новые
        content = re.sub(
            r"import \{ useDispatch, useSelector \} from 'react-redux';\nimport \{ RootState \} from '\.\./store';",
            "import { useAppDispatch, useAppSelector } from '../store';",
            content
        )
        
        content = re.sub(
            r"import \{ useDispatch, useSelector \} from 'react-redux';\nimport \{ RootState \} from '\.\./\.\./store';",
            "import { useAppDispatch, useAppSelector } from '../../store';",
            content
        )
        
        # Замена useDispatch на useAppDispatch
        content = re.sub(r"const dispatch = useDispatch\(\);", "const dispatch = useAppDispatch();", content)
        
        # Замена useSelector на useAppSelector
        content = re.sub(
            r"useSelector\(\(state: RootState\) => state\.(\w+)\)",
            r"useAppSelector((state) => state.\1)",
            content
        )
        
        # Исправление типов параметров
        content = re.sub(
            r"\(state\) => state\.(\w+)\)",
            r"(state: any) => state.\1)",
            content
        )
        
        # Исправление типов в map функциях
        content = re.sub(
            r"\.map\(([^=]+) =>",
            r".map((\1: any) =>",
            content
        )
        
        # Исправление типов в filter функциях
        content = re.sub(
            r"\.filter\(([^=]+) =>",
            r".filter((\1: any) =>",
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"❌ Ошибка при исправлении {file_path}: {e}")

def main():
    """Основная функция"""
    print("🔧 Исправление импортов в системе аналитики кредитного портфеля")
    print("=" * 70)
    
    # Переходим в директорию проекта
    os.chdir(Path(__file__).parent)
    
    # Исправляем импорты
    fix_imports()
    
    print("\n" + "=" * 70)
    print("🎉 Импорты исправлены!")
    print("=" * 70)
    print("💡 Теперь можно запустить фронтенд:")
    print("   cd frontend && npm start")
    print("=" * 70)

if __name__ == "__main__":
    main()


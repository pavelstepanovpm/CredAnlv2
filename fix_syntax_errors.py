#!/usr/bin/env python3
"""
Скрипт для исправления синтаксических ошибок в фронтенде
"""

import os
import re
from pathlib import Path

def fix_syntax_errors():
    """Исправление синтаксических ошибок во всех файлах"""
    print("🔧 Исправление синтаксических ошибок в фронтенде...")
    
    frontend_dir = Path("frontend/src")
    
    # Список файлов для исправления
    files_to_fix = [
        "components/Sidebar.tsx",
        "pages/Portfolio.tsx", 
        "pages/Scenarios.tsx",
        "store/index.ts"
    ]
    
    for file_path in files_to_fix:
        full_path = frontend_dir / file_path
        if full_path.exists():
            print(f"📝 Исправление {file_path}...")
            fix_file_syntax(full_path)
        else:
            print(f"⚠️ Файл {file_path} не найден")
    
    print("✅ Синтаксические ошибки исправлены")

def fix_file_syntax(file_path: Path):
    """Исправление синтаксических ошибок в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Исправление двойных скобок в map функциях
        content = re.sub(
            r'\.map\(\(\(([^)]+)\): any\) =>',
            r'.map((\1: any) =>',
            content
        )
        
        # Исправление импортов в store/index.ts
        if file_path.name == "index.ts":
            # Перемещаем импорты в начало
            content = re.sub(
                r'export type RootState = ReturnType<typeof store\.getState>;\nexport type AppDispatch = typeof store\.dispatch;\n\n// Типизированные хуки\nimport \{ useDispatch, useSelector, TypedUseSelectorHook \} from \'react-redux\';\n\nexport const useAppDispatch = \(\) => useDispatch<AppDispatch>\(\);\nexport const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;',
                '// Типизированные хуки\nimport { useDispatch, useSelector, TypedUseSelectorHook } from \'react-redux\';\n\nexport type RootState = ReturnType<typeof store.getState>;\nexport type AppDispatch = typeof store.dispatch;\n\nexport const useAppDispatch = () => useDispatch<AppDispatch>();\nexport const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;',
                content
            )
        
        # Добавление недостающих импортов в компоненты
        if "useAppDispatch" in content and "import { useAppDispatch" not in content:
            # Находим место для добавления импорта
            import_match = re.search(r"import.*from.*react.*;", content)
            if import_match:
                insert_pos = import_match.end()
                content = content[:insert_pos] + "\nimport { useAppDispatch, useAppSelector } from '../store';" + content[insert_pos:]
            else:
                # Если нет импортов React, добавляем в начало
                content = "import { useAppDispatch, useAppSelector } from '../store';\n" + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"❌ Ошибка при исправлении {file_path}: {e}")

def main():
    """Основная функция"""
    print("🔧 Исправление синтаксических ошибок в системе аналитики кредитного портфеля")
    print("=" * 70)
    
    # Переходим в директорию проекта
    os.chdir(Path(__file__).parent)
    
    # Исправляем синтаксические ошибки
    fix_syntax_errors()
    
    print("\n" + "=" * 70)
    print("🎉 Синтаксические ошибки исправлены!")
    print("=" * 70)
    print("💡 Теперь можно запустить фронтенд:")
    print("   cd frontend && npm start")
    print("=" * 70)

if __name__ == "__main__":
    main()


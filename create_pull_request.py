#!/usr/bin/env python3
"""
Скрипт для создания Pull Request на GitHub
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

def create_pr_with_cli():
    """Создать Pull Request через GitHub CLI"""
    print("🚀 Создание Pull Request через GitHub CLI...")
    
    # Проверить авторизацию
    auth_success, _ = run_command("gh auth status", "Проверка авторизации GitHub CLI")
    if not auth_success:
        print("❌ Не авторизован в GitHub CLI")
        print("   Выполните: gh auth login")
        return False
    
    # Создать Pull Request
    pr_success, output = run_command(
        "gh pr create --title 'feat: добавить компонент бейджа ковинант' --body '## 🎯 Описание\n\nДобавлен новый компонент CovenantBadge для отображения уровня ковинант на дашборде.\n\n## ✨ Изменения\n\n- Создан компонент CovenantBadge с поддержкой различных уровней\n- Добавлены статические бейджи ковинант на главную страницу\n- Поддержка уровней: excellent, good, fair, poor, critical\n- Визуальные индикаторы трендов и прогресса\n- Адаптивный дизайн с Material-UI\n\n## 🧪 Тестирование\n\n- [x] Компонент отображается корректно\n- [x] Поддерживаются все уровни ковинант\n- [x] Адаптивный дизайн работает\n- [x] Интеграция с дашбордом\n\n## 📸 Скриншоты\n\nКомпонент отображается на главной странице дашборда с тремя бейджами ковинант разных уровней.\n\n## 🔗 Связанные задачи\n\n- Добавление визуализации ковинант\n- Улучшение UX дашборда' --base main --head feature/covenant-badge",
        "Создание Pull Request"
    )
    
    if pr_success:
        print("✅ Pull Request создан через GitHub CLI")
        return True
    else:
        print("❌ Ошибка создания Pull Request через GitHub CLI")
        return False

def open_github_pr_page():
    """Открыть страницу создания Pull Request в браузере"""
    print("🌐 Открытие страницы создания Pull Request...")
    
    url = "https://github.com/pavelstepanovpm/CredAnlv2/compare/main...feature/covenant-badge"
    print(f"🔗 Откройте в браузере: {url}")
    
    try:
        webbrowser.open(url)
        print("✅ Страница открыта в браузере")
        return True
    except Exception as e:
        print(f"❌ Ошибка открытия браузера: {e}")
        return False

def show_manual_instructions():
    """Показать инструкции для ручного создания PR"""
    print("\n📋 Инструкции для создания Pull Request вручную:")
    print("=" * 60)
    print("1. Перейдите на https://github.com/pavelstepanovpm/CredAnlv2")
    print("2. Нажмите 'Compare & pull request' для ветки feature/covenant-badge")
    print("3. Заполните форму:")
    print("   - Title: feat: добавить компонент бейджа ковинант")
    print("   - Description: см. ниже")
    print("4. Нажмите 'Create pull request'")
    print("\n📝 Описание для PR:")
    print("-" * 40)
    print("## 🎯 Описание")
    print("Добавлен новый компонент CovenantBadge для отображения уровня ковинант на дашборде.")
    print("\n## ✨ Изменения")
    print("- Создан компонент CovenantBadge с поддержкой различных уровней")
    print("- Добавлены статические бейджи ковинант на главную страницу")
    print("- Поддержка уровней: excellent, good, fair, poor, critical")
    print("- Визуальные индикаторы трендов и прогресса")
    print("- Адаптивный дизайн с Material-UI")
    print("\n## 🧪 Тестирование")
    print("- [x] Компонент отображается корректно")
    print("- [x] Поддерживаются все уровни ковинант")
    print("- [x] Адаптивный дизайн работает")
    print("- [x] Интеграция с дашбордом")

def main():
    """Основная функция"""
    print("🔀 Создание Pull Request для feature/covenant-badge")
    print("=" * 60)
    
    # Проверить GitHub CLI
    if check_github_cli():
        print("\n🤖 Попытка создания через GitHub CLI...")
        if create_pr_with_cli():
            print("\n🎉 Pull Request создан через GitHub CLI!")
            print("🔗 URL: https://github.com/pavelstepanovpm/CredAnlv2/pulls")
            return
    
    print("\n🌐 Создание через веб-интерфейс...")
    open_github_pr_page()
    show_manual_instructions()
    
    print("\n⏳ После создания Pull Request:")
    print("   Проверьте статус на https://github.com/pavelstepanovpm/CredAnlv2/pulls")

if __name__ == "__main__":
    main()

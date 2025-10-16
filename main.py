"""
Главный модуль приложения плагина аналитики кредитного портфеля
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь для импортов
sys.path.append(str(Path(__file__).parent))

from ui.app import create_app

def main():
    """Запуск приложения"""
    app = create_app()
    app.run_server(debug=True, host='0.0.0.0', port=8050)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Запуск бэкенда системы аналитики кредитного портфеля
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent))

if __name__ == "__main__":
    import uvicorn
    from backend.main import app
    
    print("🚀 Запуск бэкенда системы аналитики кредитного портфеля...")
    print("📊 API будет доступен по адресу: http://localhost:8000")
    print("📚 Документация API: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

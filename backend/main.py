"""
FastAPI бэкенд для системы аналитики кредитного портфеля
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from api import TreasuryAPIClient
from portfolio import PortfolioManager
from versions import VersionManager
from calculations import CalculationEngine

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание приложения FastAPI
app = FastAPI(
    title="Аналитика кредитного портфеля",
    description="API для системы аналитики кредитного портфеля",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация компонентов
api_client = TreasuryAPIClient(
    base_url="http://localhost:8001/api",  # URL казначейской системы
    api_key="your-api-key-here"
)

portfolio_manager = PortfolioManager(api_client)
version_manager = VersionManager(portfolio_manager)
calculation_engine = CalculationEngine()

# Зависимости
def get_portfolio_manager():
    return portfolio_manager

def get_version_manager():
    return version_manager

def get_calculation_engine():
    return calculation_engine

# API Endpoints

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Система аналитики кредитного портфеля",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Проверка состояния системы"""
    try:
        # Проверка подключения к API казначейской системы
        api_connected = api_client.test_connection()
        
        return {
            "status": "healthy" if api_connected else "degraded",
            "api_connected": api_connected,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Portfolio endpoints
@app.get("/api/portfolio/data")
async def get_portfolio_data(portfolio_manager: PortfolioManager = Depends(get_portfolio_manager)):
    """Получение данных портфеля"""
    try:
        data = portfolio_manager.load_portfolio_data()
        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Error loading portfolio data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolio/metrics/{version_id}")
async def get_portfolio_metrics(
    version_id: str,
    portfolio_manager: PortfolioManager = Depends(get_portfolio_manager)
):
    """Получение метрик портфеля для версии"""
    try:
        # Получение версии
        version = version_manager.get_version(version_id)
        if not version:
            raise HTTPException(status_code=404, detail="Version not found")
        
        # Расчет кэш-флоу и метрик
        cashflow = portfolio_manager.calculate_portfolio_cashflow(version)
        contracts = portfolio_manager._contracts_cache or []
        metrics = calculation_engine.calculate_portfolio_metrics(cashflow, contracts)
        
        return JSONResponse(content=metrics)
    except Exception as e:
        logger.error(f"Error getting portfolio metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolio/cashflow/{version_id}")
async def get_portfolio_cashflow(
    version_id: str,
    portfolio_manager: PortfolioManager = Depends(get_portfolio_manager)
):
    """Получение кэш-флоу портфеля для версии"""
    try:
        version = version_manager.get_version(version_id)
        if not version:
            raise HTTPException(status_code=404, detail="Version not found")
        
        cashflow = portfolio_manager.calculate_portfolio_cashflow(version)
        return JSONResponse(content=cashflow.dict())
    except Exception as e:
        logger.error(f"Error getting portfolio cashflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/portfolio/refresh")
async def refresh_portfolio_data(portfolio_manager: PortfolioManager = Depends(get_portfolio_manager)):
    """Обновление данных портфеля"""
    try:
        data = portfolio_manager.load_portfolio_data(force_refresh=True)
        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Error refreshing portfolio data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Versions endpoints
@app.get("/api/versions")
async def get_versions(version_manager: VersionManager = Depends(get_version_manager)):
    """Получение списка версий"""
    try:
        versions = version_manager.get_all_versions()
        return JSONResponse(content=[v.dict() for v in versions])
    except Exception as e:
        logger.error(f"Error getting versions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/versions")
async def create_version(
    version_data: Dict[str, Any],
    version_manager: VersionManager = Depends(get_version_manager)
):
    """Создание новой версии"""
    try:
        if version_data.get('version_type') == 'base':
            version = version_manager.create_base_version(
                name=version_data['name'],
                description=version_data.get('description', ''),
                created_by=version_data.get('created_by', 'system')
            )
        else:
            version = version_manager.create_scenario_version(
                base_version_id=version_data['base_version_id'],
                name=version_data['name'],
                description=version_data.get('description', ''),
                created_by=version_data.get('created_by', 'system'),
                scenario_parameters=version_data.get('scenario_parameters', {})
            )
        
        return JSONResponse(content=version.dict())
    except Exception as e:
        logger.error(f"Error creating version: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/versions/{version_id}")
async def update_version(
    version_id: str,
    version_data: Dict[str, Any],
    version_manager: VersionManager = Depends(get_version_manager)
):
    """Обновление версии"""
    try:
        # TODO: Implement version update
        raise HTTPException(status_code=501, detail="Not implemented")
    except Exception as e:
        logger.error(f"Error updating version: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/versions/{version_id}")
async def delete_version(
    version_id: str,
    version_manager: VersionManager = Depends(get_version_manager)
):
    """Удаление версии"""
    try:
        success = version_manager.delete_version(version_id)
        if not success:
            raise HTTPException(status_code=404, detail="Version not found")
        return JSONResponse(content={"message": "Version deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting version: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/versions/{version_id}/activate")
async def activate_version(
    version_id: str,
    version_manager: VersionManager = Depends(get_version_manager)
):
    """Активация версии"""
    try:
        success = version_manager.set_active_version(version_id)
        if not success:
            raise HTTPException(status_code=404, detail="Version not found")
        return JSONResponse(content={"message": "Version activated successfully"})
    except Exception as e:
        logger.error(f"Error activating version: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/versions/compare/{version1_id}/{version2_id}")
async def compare_versions(
    version1_id: str,
    version2_id: str,
    version_manager: VersionManager = Depends(get_version_manager)
):
    """Сравнение версий"""
    try:
        comparison = version_manager.compare_versions(version1_id, version2_id)
        return JSONResponse(content=comparison)
    except Exception as e:
        logger.error(f"Error comparing versions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Scenarios endpoints
@app.get("/api/scenarios/templates")
async def get_scenario_templates():
    """Получение шаблонов сценариев"""
    templates = [
        {
            "id": "rate_increase",
            "name": "Повышение ставок",
            "description": "Сценарий повышения базовой ставки на 1-3%",
            "parameters": {
                "rate_increase": {"min": 0.01, "max": 0.03, "default": 0.02}
            }
        },
        {
            "id": "rate_decrease",
            "name": "Снижение ставок",
            "description": "Сценарий снижения базовой ставки на 1-3%",
            "parameters": {
                "rate_decrease": {"min": 0.01, "max": 0.03, "default": 0.02}
            }
        },
        {
            "id": "stress_test",
            "name": "Стресс-тест",
            "description": "Сценарий стресс-тестирования портфеля",
            "parameters": {
                "rate_shock": {"min": 0.05, "max": 0.20, "default": 0.10},
                "drawdown_shock": {"min": 0.1, "max": 0.5, "default": 0.2}
            }
        }
    ]
    return JSONResponse(content=templates)

@app.post("/api/scenarios")
async def create_scenario(
    scenario_data: Dict[str, Any],
    version_manager: VersionManager = Depends(get_version_manager)
):
    """Создание сценария"""
    try:
        # Создание сценарной версии
        version = version_manager.create_scenario_version(
            base_version_id=scenario_data['base_version_id'],
            name=scenario_data['name'],
            description=scenario_data.get('description', ''),
            created_by=scenario_data.get('created_by', 'system'),
            scenario_parameters=scenario_data.get('parameters', {})
        )
        
        return JSONResponse(content=version.dict())
    except Exception as e:
        logger.error(f"Error creating scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Reports endpoints
@app.post("/api/reports/{report_type}")
async def generate_report(
    report_type: str,
    parameters: Dict[str, Any]
):
    """Генерация отчета"""
    try:
        # TODO: Implement report generation
        return JSONResponse(content={
            "report_id": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "generated",
            "message": f"Report {report_type} generated successfully"
        })
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/{report_id}/download/{format}")
async def download_report(report_id: str, format: str):
    """Скачивание отчета"""
    try:
        # TODO: Implement report download
        raise HTTPException(status_code=501, detail="Not implemented")
    except Exception as e:
        logger.error(f"Error downloading report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Data endpoints
@app.get("/api/data/export/{format}")
async def export_data(format: str):
    """Экспорт данных"""
    try:
        # TODO: Implement data export
        raise HTTPException(status_code=501, detail="Not implemented")
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/data/import")
async def import_data():
    """Импорт данных"""
    try:
        # TODO: Implement data import
        raise HTTPException(status_code=501, detail="Not implemented")
    except Exception as e:
        logger.error(f"Error importing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

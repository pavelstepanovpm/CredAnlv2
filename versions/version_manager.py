"""
Менеджер версий расчетов
"""

from datetime import datetime, date
from decimal import Decimal
from typing import List, Dict, Any, Optional
import logging
import json

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import CalculationVersion, PortfolioCashflow
from portfolio import PortfolioManager

logger = logging.getLogger(__name__)


class VersionManager:
    """Менеджер версий расчетов"""
    
    def __init__(self, portfolio_manager: PortfolioManager):
        """
        Инициализация менеджера версий
        
        Args:
            portfolio_manager: Менеджер портфеля
        """
        self.portfolio_manager = portfolio_manager
        self._versions: Dict[str, CalculationVersion] = {}
        self._cashflows: Dict[str, PortfolioCashflow] = {}
    
    def create_base_version(self, 
                           name: str,
                           description: str,
                           created_by: str) -> CalculationVersion:
        """
        Создание базовой версии
        
        Args:
            name: Наименование версии
            description: Описание версии
            created_by: Автор версии
            
        Returns:
            Созданная базовая версия
        """
        try:
            version = self.portfolio_manager.create_calculation_version(
                name=name,
                description=description,
                created_by=created_by,
                version_type='base'
            )
            
            # Сохранение версии
            self._versions[version.id] = version
            
            # Расчет кэш-флоу для базовой версии
            cashflow = self.portfolio_manager.calculate_portfolio_cashflow(version)
            self._cashflows[version.id] = cashflow
            
            logger.info(f"Base version created: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating base version: {e}")
            raise
    
    def create_scenario_version(self, 
                               base_version_id: str,
                               name: str,
                               description: str,
                               created_by: str,
                               scenario_parameters: Dict[str, Any]) -> CalculationVersion:
        """
        Создание сценарной версии
        
        Args:
            base_version_id: ID базовой версии
            name: Наименование сценария
            description: Описание сценария
            created_by: Автор версии
            scenario_parameters: Параметры сценария
            
        Returns:
            Созданная сценарная версия
        """
        try:
            # Проверка существования базовой версии
            if base_version_id not in self._versions:
                raise ValueError(f"Base version {base_version_id} not found")
            
            # Создание сценарной версии
            version = self.portfolio_manager.create_calculation_version(
                name=name,
                description=description,
                created_by=created_by,
                version_type='scenario',
                base_version_id=base_version_id,
                scenario_parameters=scenario_parameters
            )
            
            # Сохранение версии
            self._versions[version.id] = version
            
            # Расчет кэш-флоу для сценарной версии
            cashflow = self.portfolio_manager.calculate_portfolio_cashflow(version)
            self._cashflows[version.id] = cashflow
            
            logger.info(f"Scenario version created: {version.id} based on {base_version_id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating scenario version: {e}")
            raise
    
    def get_version(self, version_id: str) -> Optional[CalculationVersion]:
        """
        Получение версии по ID
        
        Args:
            version_id: ID версии
            
        Returns:
            Версия расчета или None
        """
        return self._versions.get(version_id)
    
    def get_all_versions(self) -> List[CalculationVersion]:
        """
        Получение всех версий
        
        Returns:
            Список всех версий
        """
        return list(self._versions.values())
    
    def get_base_versions(self) -> List[CalculationVersion]:
        """
        Получение базовых версий
        
        Returns:
            Список базовых версий
        """
        return [v for v in self._versions.values() if v.is_base_version()]
    
    def get_scenario_versions(self, base_version_id: Optional[str] = None) -> List[CalculationVersion]:
        """
        Получение сценарных версий
        
        Args:
            base_version_id: ID базовой версии (если None, все сценарные)
            
        Returns:
            Список сценарных версий
        """
        if base_version_id:
            return [v for v in self._versions.values() 
                   if v.is_scenario_version() and v.base_version_id == base_version_id]
        else:
            return [v for v in self._versions.values() if v.is_scenario_version()]
    
    def get_version_cashflow(self, version_id: str) -> Optional[PortfolioCashflow]:
        """
        Получение кэш-флоу версии
        
        Args:
            version_id: ID версии
            
        Returns:
            Кэш-флоу версии или None
        """
        return self._cashflows.get(version_id)
    
    def compare_versions(self, 
                         version1_id: str, 
                         version2_id: str) -> Dict[str, Any]:
        """
        Сравнение двух версий
        
        Args:
            version1_id: ID первой версии
            version2_id: ID второй версии
            
        Returns:
            Результаты сравнения
        """
        try:
            version1 = self.get_version(version1_id)
            version2 = self.get_version(version2_id)
            
            if not version1 or not version2:
                raise ValueError("One or both versions not found")
            
            # Сравнение через менеджер портфеля
            comparison = self.portfolio_manager.compare_versions(version1, version2)
            
            logger.info(f"Versions compared: {version1_id} vs {version2_id}")
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing versions: {e}")
            return {}
    
    def delete_version(self, version_id: str) -> bool:
        """
        Удаление версии
        
        Args:
            version_id: ID версии
            
        Returns:
            True если удалено успешно, False иначе
        """
        try:
            if version_id not in self._versions:
                return False
            
            # Проверка, что это не базовая версия с зависимыми сценариями
            if self._versions[version_id].is_base_version():
                dependent_scenarios = self.get_scenario_versions(version_id)
                if dependent_scenarios:
                    logger.warning(f"Cannot delete base version {version_id} with dependent scenarios")
                    return False
            
            # Удаление версии и кэш-флоу
            del self._versions[version_id]
            if version_id in self._cashflows:
                del self._cashflows[version_id]
            
            logger.info(f"Version deleted: {version_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting version: {e}")
            return False
    
    def set_active_version(self, version_id: str) -> bool:
        """
        Установка активной версии
        
        Args:
            version_id: ID версии
            
        Returns:
            True если установлено успешно, False иначе
        """
        try:
            if version_id not in self._versions:
                return False
            
            # Сброс активности всех версий
            for version in self._versions.values():
                version.status = 'draft'
            
            # Установка активности
            self._versions[version_id].status = 'active'
            
            logger.info(f"Active version set: {version_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting active version: {e}")
            return False
    
    def get_active_version(self) -> Optional[CalculationVersion]:
        """
        Получение активной версии
        
        Returns:
            Активная версия или None
        """
        for version in self._versions.values():
            if version.is_active():
                return version
        return None
    
    def export_version(self, version_id: str) -> Dict[str, Any]:
        """
        Экспорт версии в JSON
        
        Args:
            version_id: ID версии
            
        Returns:
            Данные версии в формате JSON
        """
        try:
            version = self.get_version(version_id)
            cashflow = self.get_version_cashflow(version_id)
            
            if not version:
                return {}
            
            export_data = {
                'version': version.dict(),
                'cashflow': cashflow.dict() if cashflow else None,
                'export_date': datetime.now().isoformat()
            }
            
            return export_data
            
        except Exception as e:
            logger.error(f"Error exporting version: {e}")
            return {}
    
    def import_version(self, version_data: Dict[str, Any]) -> Optional[CalculationVersion]:
        """
        Импорт версии из JSON
        
        Args:
            version_data: Данные версии
            
        Returns:
            Импортированная версия или None
        """
        try:
            if 'version' not in version_data:
                return None
            
            version_dict = version_data['version']
            version = CalculationVersion(**version_dict)
            
            # Проверка уникальности ID
            if version.id in self._versions:
                logger.warning(f"Version {version.id} already exists, skipping import")
                return None
            
            # Сохранение версии
            self._versions[version.id] = version
            
            # Импорт кэш-флоу если есть
            if 'cashflow' in version_data and version_data['cashflow']:
                cashflow_dict = version_data['cashflow']
                cashflow = PortfolioCashflow(**cashflow_dict)
                self._cashflows[version.id] = cashflow
            
            logger.info(f"Version imported: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error importing version: {e}")
            return None
    
    def get_version_statistics(self) -> Dict[str, Any]:
        """
        Получение статистики по версиям
        
        Returns:
            Статистика версий
        """
        try:
            all_versions = list(self._versions.values())
            base_versions = [v for v in all_versions if v.is_base_version()]
            scenario_versions = [v for v in all_versions if v.is_scenario_version()]
            active_versions = [v for v in all_versions if v.is_active()]
            
            # Группировка по авторам
            authors = {}
            for version in all_versions:
                author = version.created_by
                if author not in authors:
                    authors[author] = 0
                authors[author] += 1
            
            # Группировка по датам создания
            creation_dates = {}
            for version in all_versions:
                date_key = version.created_at.date().isoformat()
                if date_key not in creation_dates:
                    creation_dates[date_key] = 0
                creation_dates[date_key] += 1
            
            return {
                'total_versions': len(all_versions),
                'base_versions': len(base_versions),
                'scenario_versions': len(scenario_versions),
                'active_versions': len(active_versions),
                'authors': authors,
                'creation_timeline': creation_dates,
                'latest_version': max(all_versions, key=lambda v: v.created_at).id if all_versions else None
            }
            
        except Exception as e:
            logger.error(f"Error getting version statistics: {e}")
            return {}

"""
Построитель сценариев для моделирования
"""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
import logging

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import CalculationVersion, CreditContract, Drawdown, Repayment
from portfolio import PortfolioManager

logger = logging.getLogger(__name__)


class ScenarioBuilder:
    """Построитель сценариев"""
    
    def __init__(self, portfolio_manager: PortfolioManager):
        """
        Инициализация построителя сценариев
        
        Args:
            portfolio_manager: Менеджер портфеля
        """
        self.portfolio_manager = portfolio_manager
    
    def create_rate_scenario(self, 
                           base_version_id: str,
                           scenario_name: str,
                           scenario_description: str,
                           created_by: str,
                           new_base_rate: Decimal,
                           rate_change_date: Optional[date] = None) -> CalculationVersion:
        """
        Создание сценария изменения процентных ставок
        
        Args:
            base_version_id: ID базовой версии
            scenario_name: Наименование сценария
            scenario_description: Описание сценария
            created_by: Автор сценария
            new_base_rate: Новая базовая ставка
            rate_change_date: Дата изменения ставки
            
        Returns:
            Созданная сценарная версия
        """
        try:
            scenario_parameters = {
                'scenario_type': 'rate_change',
                'new_base_rate': float(new_base_rate),
                'rate_change_date': rate_change_date.isoformat() if rate_change_date else None,
                'description': f"Изменение базовой ставки до {new_base_rate}%"
            }
            
            version = self.portfolio_manager.create_calculation_version(
                name=scenario_name,
                description=scenario_description,
                created_by=created_by,
                version_type='scenario',
                base_version_id=base_version_id,
                scenario_parameters=scenario_parameters
            )
            
            logger.info(f"Rate scenario created: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating rate scenario: {e}")
            raise
    
    def create_drawdown_scenario(self, 
                               base_version_id: str,
                               scenario_name: str,
                               scenario_description: str,
                               created_by: str,
                               additional_drawdowns: List[Dict[str, Any]]) -> CalculationVersion:
        """
        Создание сценария дополнительных выборок
        
        Args:
            base_version_id: ID базовой версии
            scenario_name: Наименование сценария
            scenario_description: Описание сценария
            created_by: Автор сценария
            additional_drawdowns: Список дополнительных выборок
            
        Returns:
            Созданная сценарная версия
        """
        try:
            scenario_parameters = {
                'scenario_type': 'additional_drawdowns',
                'additional_drawdowns': additional_drawdowns,
                'description': f"Добавление {len(additional_drawdowns)} дополнительных выборок"
            }
            
            version = self.portfolio_manager.create_calculation_version(
                name=scenario_name,
                description=scenario_description,
                created_by=created_by,
                version_type='scenario',
                base_version_id=base_version_id,
                scenario_parameters=scenario_parameters
            )
            
            logger.info(f"Drawdown scenario created: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating drawdown scenario: {e}")
            raise
    
    def create_repayment_scenario(self, 
                                base_version_id: str,
                                scenario_name: str,
                                scenario_description: str,
                                created_by: str,
                                additional_repayments: List[Dict[str, Any]]) -> CalculationVersion:
        """
        Создание сценария дополнительных погашений
        
        Args:
            base_version_id: ID базовой версии
            scenario_name: Наименование сценария
            scenario_description: Описание сценария
            created_by: Автор сценария
            additional_repayments: Список дополнительных погашений
            
        Returns:
            Созданная сценарная версия
        """
        try:
            scenario_parameters = {
                'scenario_type': 'additional_repayments',
                'additional_repayments': additional_repayments,
                'description': f"Добавление {len(additional_repayments)} дополнительных погашений"
            }
            
            version = self.portfolio_manager.create_calculation_version(
                name=scenario_name,
                description=scenario_description,
                created_by=created_by,
                version_type='scenario',
                base_version_id=base_version_id,
                scenario_parameters=scenario_parameters
            )
            
            logger.info(f"Repayment scenario created: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating repayment scenario: {e}")
            raise
    
    def create_stress_scenario(self, 
                             base_version_id: str,
                             scenario_name: str,
                             scenario_description: str,
                             created_by: str,
                             stress_parameters: Dict[str, Any]) -> CalculationVersion:
        """
        Создание стресс-сценария
        
        Args:
            base_version_id: ID базовой версии
            scenario_name: Наименование сценария
            scenario_description: Описание сценария
            created_by: Автор сценария
            stress_parameters: Параметры стресс-теста
            
        Returns:
            Созданная сценарная версия
        """
        try:
            scenario_parameters = {
                'scenario_type': 'stress_test',
                'stress_parameters': stress_parameters,
                'description': f"Стресс-тест: {stress_parameters.get('description', '')}"
            }
            
            version = self.portfolio_manager.create_calculation_version(
                name=scenario_name,
                description=scenario_description,
                created_by=created_by,
                version_type='scenario',
                base_version_id=base_version_id,
                scenario_parameters=scenario_parameters
            )
            
            logger.info(f"Stress scenario created: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating stress scenario: {e}")
            raise
    
    def create_optimization_scenario(self, 
                                   base_version_id: str,
                                   scenario_name: str,
                                   scenario_description: str,
                                   created_by: str,
                                   optimization_parameters: Dict[str, Any]) -> CalculationVersion:
        """
        Создание сценария оптимизации
        
        Args:
            base_version_id: ID базовой версии
            scenario_name: Наименование сценария
            scenario_description: Описание сценария
            created_by: Автор сценария
            optimization_parameters: Параметры оптимизации
            
        Returns:
            Созданная сценарная версия
        """
        try:
            scenario_parameters = {
                'scenario_type': 'optimization',
                'optimization_parameters': optimization_parameters,
                'description': f"Оптимизация: {optimization_parameters.get('description', '')}"
            }
            
            version = self.portfolio_manager.create_calculation_version(
                name=scenario_name,
                description=scenario_description,
                created_by=created_by,
                version_type='scenario',
                base_version_id=base_version_id,
                scenario_parameters=scenario_parameters
            )
            
            logger.info(f"Optimization scenario created: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating optimization scenario: {e}")
            raise
    
    def create_custom_scenario(self, 
                             base_version_id: str,
                             scenario_name: str,
                             scenario_description: str,
                             created_by: str,
                             custom_parameters: Dict[str, Any]) -> CalculationVersion:
        """
        Создание пользовательского сценария
        
        Args:
            base_version_id: ID базовой версии
            scenario_name: Наименование сценария
            scenario_description: Описание сценария
            created_by: Автор сценария
            custom_parameters: Пользовательские параметры
            
        Returns:
            Созданная сценарная версия
        """
        try:
            scenario_parameters = {
                'scenario_type': 'custom',
                'custom_parameters': custom_parameters,
                'description': f"Пользовательский сценарий: {custom_parameters.get('description', '')}"
            }
            
            version = self.portfolio_manager.create_calculation_version(
                name=scenario_name,
                description=scenario_description,
                created_by=created_by,
                version_type='scenario',
                base_version_id=base_version_id,
                scenario_parameters=scenario_parameters
            )
            
            logger.info(f"Custom scenario created: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating custom scenario: {e}")
            raise
    
    def get_scenario_templates(self) -> List[Dict[str, Any]]:
        """
        Получение шаблонов сценариев
        
        Returns:
            Список шаблонов сценариев
        """
        return [
            {
                'id': 'rate_increase',
                'name': 'Повышение ставок',
                'description': 'Сценарий повышения базовой ставки на 1-3%',
                'parameters': {
                    'rate_increase': {'min': 0.01, 'max': 0.03, 'default': 0.02}
                }
            },
            {
                'id': 'rate_decrease',
                'name': 'Снижение ставок',
                'description': 'Сценарий снижения базовой ставки на 1-3%',
                'parameters': {
                    'rate_decrease': {'min': 0.01, 'max': 0.03, 'default': 0.02}
                }
            },
            {
                'id': 'stress_test',
                'name': 'Стресс-тест',
                'description': 'Сценарий стресс-тестирования портфеля',
                'parameters': {
                    'rate_shock': {'min': 0.05, 'max': 0.20, 'default': 0.10},
                    'drawdown_shock': {'min': 0.1, 'max': 0.5, 'default': 0.2}
                }
            },
            {
                'id': 'optimization',
                'name': 'Оптимизация',
                'description': 'Сценарий оптимизации структуры портфеля',
                'parameters': {
                    'target_utilization': {'min': 0.3, 'max': 0.8, 'default': 0.6},
                    'max_concentration': {'min': 0.1, 'max': 0.3, 'default': 0.2}
                }
            }
        ]
    
    def validate_scenario_parameters(self, 
                                   scenario_type: str,
                                   parameters: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Валидация параметров сценария
        
        Args:
            scenario_type: Тип сценария
            parameters: Параметры сценария
            
        Returns:
            Кортеж (валидность, список ошибок)
        """
        errors = []
        
        try:
            if scenario_type == 'rate_change':
                if 'new_base_rate' not in parameters:
                    errors.append("new_base_rate is required for rate_change scenario")
                elif not isinstance(parameters['new_base_rate'], (int, float, Decimal)):
                    errors.append("new_base_rate must be a number")
                elif parameters['new_base_rate'] < 0:
                    errors.append("new_base_rate must be non-negative")
            
            elif scenario_type == 'additional_drawdowns':
                if 'additional_drawdowns' not in parameters:
                    errors.append("additional_drawdowns is required")
                elif not isinstance(parameters['additional_drawdowns'], list):
                    errors.append("additional_drawdowns must be a list")
                else:
                    for i, drawdown in enumerate(parameters['additional_drawdowns']):
                        if not isinstance(drawdown, dict):
                            errors.append(f"Drawdown {i} must be a dictionary")
                            continue
                        
                        required_fields = ['contract_id', 'amount', 'date']
                        for field in required_fields:
                            if field not in drawdown:
                                errors.append(f"Drawdown {i} missing required field: {field}")
            
            elif scenario_type == 'additional_repayments':
                if 'additional_repayments' not in parameters:
                    errors.append("additional_repayments is required")
                elif not isinstance(parameters['additional_repayments'], list):
                    errors.append("additional_repayments must be a list")
                else:
                    for i, repayment in enumerate(parameters['additional_repayments']):
                        if not isinstance(repayment, dict):
                            errors.append(f"Repayment {i} must be a dictionary")
                            continue
                        
                        required_fields = ['contract_id', 'principal_amount', 'interest_amount', 'date']
                        for field in required_fields:
                            if field not in repayment:
                                errors.append(f"Repayment {i} missing required field: {field}")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            errors.append(f"Validation error: {e}")
            return False, errors

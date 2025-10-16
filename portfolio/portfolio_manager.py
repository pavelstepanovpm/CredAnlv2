"""
Менеджер портфеля для управления данными и расчетами
"""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
import logging

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import (
    CreditContract, Drawdown, Repayment, CalculationVersion,
    PaymentSchedule, PortfolioCashflow
)
from api import TreasuryAPIClient
from calculations import CalculationEngine
from .data_aggregator import DataAggregator

logger = logging.getLogger(__name__)


class PortfolioManager:
    """Менеджер портфеля"""
    
    def __init__(self, api_client: TreasuryAPIClient):
        """
        Инициализация менеджера портфеля
        
        Args:
            api_client: Клиент для работы с API
        """
        self.api_client = api_client
        self.calculation_engine = CalculationEngine()
        self.data_aggregator = DataAggregator()
        
        # Кэш данных
        self._contracts_cache: Optional[List[CreditContract]] = None
        self._drawdowns_cache: Optional[List[Drawdown]] = None
        self._repayments_cache: Optional[List[Repayment]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl_minutes = 30  # Время жизни кэша в минутах
    
    def load_portfolio_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Загрузка данных портфеля
        
        Args:
            force_refresh: Принудительное обновление кэша
            
        Returns:
            Данные портфеля
        """
        try:
            # Проверка кэша
            if not force_refresh and self._is_cache_valid():
                logger.info("Using cached portfolio data")
                return self._get_cached_data()
            
            logger.info("Loading fresh portfolio data from API")
            
            # Загрузка данных из API
            contracts = self.api_client.get_active_contracts()
            
            all_drawdowns = []
            all_repayments = []
            
            for contract in contracts:
                try:
                    contract_drawdowns = self.api_client.get_contract_drawdowns(contract.id)
                    contract_repayments = self.api_client.get_contract_repayments(contract.id)
                    
                    all_drawdowns.extend(contract_drawdowns)
                    all_repayments.extend(contract_repayments)
                    
                except Exception as e:
                    logger.error(f"Failed to load data for contract {contract.id}: {e}")
                    continue
            
            # Обновление кэша
            self._update_cache(contracts, all_drawdowns, all_repayments)
            
            # Агрегация данных
            aggregated_data = self.data_aggregator.aggregate_portfolio_data(
                contracts, all_drawdowns, all_repayments
            )
            
            logger.info(f"Portfolio data loaded: {len(contracts)} contracts")
            return aggregated_data
            
        except Exception as e:
            logger.error(f"Error loading portfolio data: {e}")
            return {}
    
    def create_calculation_version(self, 
                                 name: str,
                                 description: str,
                                 created_by: str,
                                 version_type: str = 'base',
                                 base_version_id: Optional[str] = None,
                                 scenario_parameters: Optional[Dict[str, Any]] = None) -> CalculationVersion:
        """
        Создание новой версии расчета
        
        Args:
            name: Наименование версии
            description: Описание версии
            created_by: Автор версии
            version_type: Тип версии (base/scenario)
            base_version_id: ID базовой версии (для сценарных)
            scenario_parameters: Параметры сценария
            
        Returns:
            Созданная версия расчета
        """
        try:
            version = CalculationVersion(
                id=f"version_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                name=name,
                description=description,
                created_by=created_by,
                version_type=version_type,
                base_version_id=base_version_id,
                scenario_parameters=scenario_parameters or {}
            )
            
            logger.info(f"Created calculation version: {version.id}")
            return version
            
        except Exception as e:
            logger.error(f"Error creating calculation version: {e}")
            raise
    
    def calculate_portfolio_cashflow(self, 
                                   version: CalculationVersion,
                                   force_refresh: bool = False) -> PortfolioCashflow:
        """
        Расчет кэш-флоу портфеля для версии
        
        Args:
            version: Версия расчета
            force_refresh: Принудительное обновление данных
            
        Returns:
            Кэш-флоу портфеля
        """
        try:
            # Загрузка данных портфеля
            portfolio_data = self.load_portfolio_data(force_refresh)
            if not portfolio_data:
                raise ValueError("Failed to load portfolio data")
            
            # Получение данных из кэша
            contracts = self._contracts_cache or []
            all_drawdowns = self._drawdowns_cache or []
            all_repayments = self._repayments_cache or []
            
            # Получение текущей базовой ставки
            current_base_rate = self.api_client.get_current_base_rate()
            
            # Расчет кэш-флоу
            cashflow = self.calculation_engine.calculate_portfolio_cashflow(
                contracts=contracts,
                all_drawdowns=all_drawdowns,
                all_repayments=all_repayments,
                version=version,
                current_base_rate=current_base_rate
            )
            
            logger.info(f"Portfolio cashflow calculated for version {version.id}")
            return cashflow
            
        except Exception as e:
            logger.error(f"Error calculating portfolio cashflow: {e}")
            raise
    
    def compare_versions(self, 
                        base_version: CalculationVersion,
                        scenario_version: CalculationVersion) -> Dict[str, Any]:
        """
        Сравнение версий расчета
        
        Args:
            base_version: Базовая версия
            scenario_version: Сценарная версия
            
        Returns:
            Результаты сравнения
        """
        try:
            # Расчет кэш-флоу для обеих версий
            base_cashflow = self.calculate_portfolio_cashflow(base_version)
            scenario_cashflow = self.calculate_portfolio_cashflow(scenario_version)
            
            # Расчет влияния сценария
            scenario_impact = self.calculation_engine.calculate_scenario_impact(
                base_cashflow, scenario_cashflow
            )
            
            # Расчет метрик для обеих версий
            contracts = self._contracts_cache or []
            base_metrics = self.calculation_engine.calculate_portfolio_metrics(base_cashflow, contracts)
            scenario_metrics = self.calculation_engine.calculate_portfolio_metrics(scenario_cashflow, contracts)
            
            comparison = {
                'base_version': {
                    'id': base_version.id,
                    'name': base_version.name,
                    'metrics': base_metrics
                },
                'scenario_version': {
                    'id': scenario_version.id,
                    'name': scenario_version.name,
                    'metrics': scenario_metrics
                },
                'scenario_impact': scenario_impact,
                'comparison_date': datetime.now().isoformat()
            }
            
            logger.info(f"Versions compared: {base_version.id} vs {scenario_version.id}")
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing versions: {e}")
            return {}
    
    def get_portfolio_report(self, 
                           version: Optional[CalculationVersion] = None,
                           report_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Получение отчета по портфелю
        
        Args:
            version: Версия расчета (если None, используется текущее состояние)
            report_date: Дата отчета
            
        Returns:
            Отчет по портфелю
        """
        try:
            # Загрузка данных портфеля
            portfolio_data = self.load_portfolio_data()
            
            # Если указана версия, добавляем расчеты
            if version:
                cashflow = self.calculate_portfolio_cashflow(version)
                contracts = self._contracts_cache or []
                metrics = self.calculation_engine.calculate_portfolio_metrics(cashflow, contracts)
                portfolio_data['cashflow_metrics'] = metrics
            
            # Создание отчета
            report = self.data_aggregator.create_portfolio_report(portfolio_data, report_date)
            
            logger.info("Portfolio report generated")
            return report
            
        except Exception as e:
            logger.error(f"Error generating portfolio report: {e}")
            return {}
    
    def get_contract_details(self, contract_id: str) -> Dict[str, Any]:
        """
        Получение детальной информации по договору
        
        Args:
            contract_id: ID договора
            
        Returns:
            Детальная информация по договору
        """
        try:
            # Поиск договора
            contracts = self._contracts_cache or []
            contract = next((c for c in contracts if c.id == contract_id), None)
            
            if not contract:
                return {}
            
            # Получение данных по договору
            drawdowns = [d for d in (self._drawdowns_cache or []) if d.contract_id == contract_id]
            repayments = [r for r in (self._repayments_cache or []) if r.contract_id == contract_id]
            
            # Расчет дополнительных метрик
            total_drawdowns = sum(d.amount for d in drawdowns)
            total_principal_repayments = sum(r.principal_amount for r in repayments)
            total_interest_repayments = sum(r.interest_amount for r in repayments)
            
            return {
                'contract': contract.dict(),
                'drawdowns': [d.dict() for d in drawdowns],
                'repayments': [r.dict() for r in repayments],
                'summary': {
                    'total_drawdowns': float(total_drawdowns),
                    'total_principal_repayments': float(total_principal_repayments),
                    'total_interest_repayments': float(total_interest_repayments),
                    'current_balance': float(total_drawdowns - total_principal_repayments),
                    'utilization_ratio': float(contract.get_utilization_ratio())
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting contract details: {e}")
            return {}
    
    def _is_cache_valid(self) -> bool:
        """Проверка валидности кэша"""
        if not self._cache_timestamp:
            return False
        
        cache_age = datetime.now() - self._cache_timestamp
        return cache_age.total_seconds() < (self._cache_ttl_minutes * 60)
    
    def _get_cached_data(self) -> Dict[str, Any]:
        """Получение данных из кэша"""
        contracts = self._contracts_cache or []
        all_drawdowns = self._drawdowns_cache or []
        all_repayments = self._repayments_cache or []
        
        return self.data_aggregator.aggregate_portfolio_data(
            contracts, all_drawdowns, all_repayments
        )
    
    def _update_cache(self, 
                     contracts: List[CreditContract],
                     all_drawdowns: List[Drawdown],
                     all_repayments: List[Repayment]) -> None:
        """Обновление кэша"""
        self._contracts_cache = contracts
        self._drawdowns_cache = all_drawdowns
        self._repayments_cache = all_repayments
        self._cache_timestamp = datetime.now()
        
        logger.info(f"Cache updated: {len(contracts)} contracts, {len(all_drawdowns)} drawdowns, {len(all_repayments)} repayments")
    
    def clear_cache(self) -> None:
        """Очистка кэша"""
        self._contracts_cache = None
        self._drawdowns_cache = None
        self._repayments_cache = None
        self._cache_timestamp = None
        
        logger.info("Cache cleared")

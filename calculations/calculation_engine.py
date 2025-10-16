"""
Основной движок расчетов для системы аналитики кредитного портфеля
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
    PaymentSchedule, PortfolioCashflow, PortfolioCashflowItem
)
from .payment_scheduler import PaymentScheduler
from .interest_calculator import InterestCalculator

logger = logging.getLogger(__name__)


class CalculationEngine:
    """Основной движок расчетов"""
    
    def __init__(self, day_count_basis: str = 'Actual/360'):
        """
        Инициализация движка расчетов
        
        Args:
            day_count_basis: База для расчета дней
        """
        self.payment_scheduler = PaymentScheduler(day_count_basis)
        self.interest_calculator = InterestCalculator(day_count_basis)
        self.day_count_basis = day_count_basis
    
    def calculate_portfolio_cashflow(self, 
                                   contracts: List[CreditContract],
                                   all_drawdowns: List[Drawdown],
                                   all_repayments: List[Repayment],
                                   version: CalculationVersion,
                                   current_base_rate: Optional[Decimal] = None) -> PortfolioCashflow:
        """
        Расчет консолидированного кэш-флоу портфеля
        
        Args:
            contracts: Список кредитных договоров
            all_drawdowns: Все выборки по портфелю
            all_repayments: Все погашения по портфелю
            version: Версия расчета
            current_base_rate: Текущая базовая ставка
            
        Returns:
            Консолидированный кэш-флоу портфеля
        """
        try:
            logger.info(f"Calculating portfolio cashflow for version {version.id}")
            
            # Получение параметров сценария
            scenario_base_rate = version.get_base_rate() or current_base_rate
            
            # Создание консолидированного кэш-флоу
            portfolio_cashflow = PortfolioCashflow(
                version_id=version.id
            )
            
            # Получение всех дат из графиков платежей
            all_dates = set()
            payment_schedules = {}
            
            for contract in contracts:
                # Получение данных по договору
                contract_drawdowns = [d for d in all_drawdowns if d.contract_id == contract.id]
                contract_repayments = [r for r in all_repayments if r.contract_id == contract.id]
                
                # Создание графика платежей
                schedule = self.payment_scheduler.create_payment_schedule(
                    contract=contract,
                    drawdowns=contract_drawdowns,
                    repayments=contract_repayments,
                    version_id=version.id,
                    current_base_rate=scenario_base_rate
                )
                
                payment_schedules[contract.id] = schedule
                
                # Сбор всех дат
                for item in schedule.schedule_items:
                    all_dates.add(item.payment_date)
            
            # Консолидация по датам
            for event_date in sorted(all_dates):
                cashflow_item = self._create_consolidated_cashflow_item(
                    event_date, payment_schedules, contracts
                )
                portfolio_cashflow.add_item(cashflow_item)
            
            # Установка периода отчета
            if all_dates:
                portfolio_cashflow.report_start_date = min(all_dates)
                portfolio_cashflow.report_end_date = max(all_dates)
            
            logger.info(f"Portfolio cashflow calculated with {len(portfolio_cashflow.cashflow_items)} items")
            return portfolio_cashflow
            
        except Exception as e:
            logger.error(f"Error calculating portfolio cashflow: {e}")
            raise
    
    def _create_consolidated_cashflow_item(self, 
                                         event_date: date,
                                         payment_schedules: Dict[str, PaymentSchedule],
                                         contracts: List[CreditContract]) -> PortfolioCashflowItem:
        """Создание консолидированного элемента кэш-флоу"""
        
        total_drawdowns = Decimal('0')
        total_principal_payments = Decimal('0')
        total_interest_payments = Decimal('0')
        total_debt_balance = Decimal('0')
        total_available_limit = Decimal('0')
        
        # Агрегация данных по всем договорам
        for contract in contracts:
            schedule = payment_schedules.get(contract.id)
            if not schedule:
                continue
            
            # Получение элемента графика на дату
            cashflow_item = schedule.get_cashflow_by_date(event_date)
            if cashflow_item:
                total_drawdowns += cashflow_item.drawdown_amount
                total_principal_payments += cashflow_item.principal_payment
                total_interest_payments += cashflow_item.interest_payment
                total_debt_balance += cashflow_item.debt_balance_end
                total_available_limit += contract.available_limit
        
        return PortfolioCashflowItem(
            cashflow_date=event_date,
            total_drawdowns=total_drawdowns,
            total_principal_payments=total_principal_payments,
            total_interest_payments=total_interest_payments,
            total_debt_balance=total_debt_balance,
            total_available_limit=total_available_limit
        )
    
    def calculate_scenario_impact(self, 
                                base_cashflow: PortfolioCashflow,
                                scenario_cashflow: PortfolioCashflow) -> Dict[str, Any]:
        """
        Расчет влияния сценария на портфель
        
        Args:
            base_cashflow: Базовый кэш-флоу
            scenario_cashflow: Сценарный кэш-флоу
            
        Returns:
            Метрики влияния сценария
        """
        try:
            # Получение дат для сравнения
            base_dates = {item.cashflow_date for item in base_cashflow.cashflow_items}
            scenario_dates = {item.cashflow_date for item in scenario_cashflow.cashflow_items}
            common_dates = base_dates.intersection(scenario_dates)
            
            if not common_dates:
                return {
                    'net_cashflow_impact': Decimal('0'),
                    'debt_balance_impact': Decimal('0'),
                    'utilization_impact': Decimal('0'),
                    'max_positive_impact': Decimal('0'),
                    'max_negative_impact': Decimal('0')
                }
            
            # Расчет влияния
            net_cashflow_impact = Decimal('0')
            debt_balance_impact = Decimal('0')
            utilization_impact = Decimal('0')
            max_positive_impact = Decimal('0')
            max_negative_impact = Decimal('0')
            
            for event_date in common_dates:
                base_item = base_cashflow.get_cashflow_on_date(event_date)
                scenario_item = scenario_cashflow.get_cashflow_on_date(event_date)
                
                if base_item and scenario_item:
                    # Влияние на чистый денежный поток
                    net_impact = scenario_item.net_cashflow - base_item.net_cashflow
                    net_cashflow_impact += net_impact
                    
                    # Влияние на остаток долга
                    debt_impact = scenario_item.total_debt_balance - base_item.total_debt_balance
                    debt_balance_impact += debt_impact
                    
                    # Влияние на коэффициент использования
                    base_utilization = base_item.utilization_ratio
                    scenario_utilization = scenario_item.utilization_ratio
                    utilization_impact += scenario_utilization - base_utilization
                    
                    # Максимальные влияния
                    if net_impact > max_positive_impact:
                        max_positive_impact = net_impact
                    if net_impact < max_negative_impact:
                        max_negative_impact = net_impact
            
            return {
                'net_cashflow_impact': net_cashflow_impact,
                'debt_balance_impact': debt_balance_impact,
                'utilization_impact': utilization_impact,
                'max_positive_impact': max_positive_impact,
                'max_negative_impact': max_negative_impact,
                'common_dates_count': len(common_dates)
            }
            
        except Exception as e:
            logger.error(f"Error calculating scenario impact: {e}")
            return {}
    
    def calculate_portfolio_metrics(self, 
                                  cashflow: PortfolioCashflow,
                                  contracts: List[CreditContract]) -> Dict[str, Any]:
        """
        Расчет ключевых метрик портфеля
        
        Args:
            cashflow: Кэш-флоу портфеля
            contracts: Список договоров
            
        Returns:
            Метрики портфеля
        """
        try:
            if not cashflow.cashflow_items:
                return {}
            
            # Базовые метрики
            total_contracts = len(contracts)
            total_limit = sum(contract.total_limit for contract in contracts)
            total_utilized = sum(contract.get_utilized_amount() for contract in contracts)
            total_available = sum(contract.available_limit for contract in contracts)
            
            # Метрики кэш-флоу
            net_cashflow_summary = cashflow.get_net_cashflow_summary()
            
            # Средневзвешенная ставка
            weighted_rate = self._calculate_weighted_average_rate(contracts, cashflow)
            
            # Концентрация портфеля
            concentration_metrics = self._calculate_concentration_metrics(contracts)
            
            return {
                'total_contracts': total_contracts,
                'total_limit': float(total_limit),
                'total_utilized': float(total_utilized),
                'total_available': float(total_available),
                'utilization_ratio': float(total_utilized / total_limit) if total_limit > 0 else 0,
                'weighted_average_rate': float(weighted_rate),
                'net_cashflow_summary': {
                    k: float(v) if isinstance(v, Decimal) else v 
                    for k, v in net_cashflow_summary.items()
                },
                'concentration_metrics': concentration_metrics,
                'debt_balance_start': float(cashflow.debt_balance_start_period),
                'debt_balance_end': float(cashflow.debt_balance_end_period),
                'limit_balance_start': float(cashflow.limit_balance_start_period),
                'limit_balance_end': float(cashflow.limit_balance_end_period)
            }
            
        except Exception as e:
            logger.error(f"Error calculating portfolio metrics: {e}")
            return {}
    
    def _calculate_weighted_average_rate(self, 
                                      contracts: List[CreditContract],
                                      cashflow: PortfolioCashflow) -> Decimal:
        """Расчет средневзвешенной ставки портфеля"""
        try:
            total_weighted_rate = Decimal('0')
            total_weight = Decimal('0')
            
            for contract in contracts:
                # Использование остатка долга как веса
                contract_balance = cashflow.get_balance_on_date(date.today())[0]
                if contract_balance > 0:
                    # Упрощенный расчет ставки (можно улучшить)
                    rate = Decimal('0.075')  # Примерная ставка
                    total_weighted_rate += rate * contract_balance
                    total_weight += contract_balance
            
            return total_weighted_rate / total_weight if total_weight > 0 else Decimal('0')
            
        except Exception as e:
            logger.error(f"Error calculating weighted average rate: {e}")
            return Decimal('0')
    
    def _calculate_concentration_metrics(self, contracts: List[CreditContract]) -> Dict[str, float]:
        """Расчет метрик концентрации портфеля"""
        try:
            if not contracts:
                return {}
            
            total_limit = sum(contract.total_limit for contract in contracts)
            if total_limit == 0:
                return {}
            
            # Расчет доли каждого договора
            contract_shares = [float(contract.total_limit / total_limit) for contract in contracts]
            
            # Индекс Херфиндаля-Хиршмана
            hhi = sum(share ** 2 for share in contract_shares)
            
            # Максимальная доля
            max_share = max(contract_shares)
            
            # Количество договоров с долей > 5%
            large_contracts = sum(1 for share in contract_shares if share > 0.05)
            
            return {
                'hhi': hhi,
                'max_share': max_share,
                'large_contracts_count': large_contracts,
                'concentration_risk': 'high' if hhi > 0.25 else 'medium' if hhi > 0.15 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error calculating concentration metrics: {e}")
            return {}

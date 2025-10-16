"""
Планировщик платежей для построения графиков погашения
"""

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional
import logging

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import CreditContract, Drawdown, Repayment, PaymentSchedule, PaymentScheduleItem
from .interest_calculator import InterestCalculator

logger = logging.getLogger(__name__)


class PaymentScheduler:
    """Планировщик платежей"""
    
    def __init__(self, day_count_basis: str = 'Actual/360'):
        """
        Инициализация планировщика
        
        Args:
            day_count_basis: База для расчета дней
        """
        self.interest_calculator = InterestCalculator(day_count_basis)
        self.day_count_basis = day_count_basis
    
    def create_payment_schedule(self, 
                               contract: CreditContract,
                               drawdowns: List[Drawdown],
                               repayments: List[Repayment],
                               version_id: str,
                               current_base_rate: Optional[Decimal] = None) -> PaymentSchedule:
        """
        Создать график платежей по кредиту
        
        Args:
            contract: Кредитный договор
            drawdowns: Список выборок
            repayments: Список погашений
            version_id: ID версии расчета
            current_base_rate: Текущая базовая ставка для плавающих ставок
            
        Returns:
            График платежей
        """
        try:
            logger.info(f"Creating payment schedule for contract {contract.id}")
            
            # Создание временной сетки
            timeline = self._create_timeline(contract, drawdowns, repayments)
            
            # Создание графика платежей
            schedule = PaymentSchedule(
                contract_id=contract.id,
                version_id=version_id,
                calculation_date=date.today()
            )
            
            # Расчет по каждой дате
            debt_balance = Decimal('0')
            available_limit = contract.available_limit
            
            for event_date in sorted(timeline.keys()):
                events = timeline[event_date]
                
                # Остаток долга на начало дня
                debt_balance_start = debt_balance
                
                # Обработка выборок
                drawdown_amount = sum(event['amount'] for event in events if event['type'] == 'drawdown')
                if drawdown_amount > 0:
                    debt_balance += drawdown_amount
                    available_limit -= drawdown_amount
                
                # Обработка погашений
                principal_payment = sum(event['principal'] for event in events if event['type'] == 'repayment')
                interest_payment = sum(event['interest'] for event in events if event['type'] == 'repayment')
                
                if principal_payment > 0 or interest_payment > 0:
                    debt_balance -= principal_payment
                    available_limit += principal_payment  # Для возобновляемых кредитов
                
                # Расчет процентов за период (если это дата начисления)
                if self._is_interest_payment_date(contract, event_date):
                    interest_for_period = self._calculate_interest_for_period(
                        contract, drawdowns, debt_balance_start, event_date, current_base_rate
                    )
                    interest_payment += interest_for_period
                
                # Остаток долга на конец дня
                debt_balance_end = debt_balance
                
                # Создание элемента графика
                schedule_item = PaymentScheduleItem(
                    payment_date=event_date,
                    debt_balance_start=debt_balance_start,
                    debt_balance_end=debt_balance_end,
                    drawdown_amount=drawdown_amount,
                    principal_payment=principal_payment,
                    interest_payment=interest_payment,
                    effective_rate=self._get_effective_rate(contract, drawdowns, event_date, current_base_rate),
                    days_in_period=self._get_days_in_period(event_date, timeline)
                )
                
                schedule.add_item(schedule_item)
            
            logger.info(f"Payment schedule created with {len(schedule.schedule_items)} items")
            return schedule
            
        except Exception as e:
            logger.error(f"Error creating payment schedule: {e}")
            raise
    
    def _create_timeline(self, 
                        contract: CreditContract, 
                        drawdowns: List[Drawdown], 
                        repayments: List[Repayment]) -> Dict[date, List[Dict[str, Any]]]:
        """Создание временной сетки событий"""
        timeline = {}
        
        # Добавление граничных дат
        timeline[contract.start_date] = []
        timeline[contract.end_date] = []
        
        # Добавление выборок
        for drawdown in drawdowns:
            if drawdown.drawdown_date not in timeline:
                timeline[drawdown.drawdown_date] = []
            timeline[drawdown.drawdown_date].append({
                'type': 'drawdown',
                'amount': drawdown.amount,
                'drawdown_id': drawdown.id
            })
        
        # Добавление погашений
        for repayment in repayments:
            if repayment.repayment_date not in timeline:
                timeline[repayment.repayment_date] = []
            timeline[repayment.repayment_date].append({
                'type': 'repayment',
                'principal': repayment.principal_amount,
                'interest': repayment.interest_amount,
                'repayment_id': repayment.id
            })
        
        # Добавление дат начисления процентов
        interest_dates = self._generate_interest_dates(contract)
        for interest_date in interest_dates:
            if interest_date not in timeline:
                timeline[interest_date] = []
            timeline[interest_date].append({
                'type': 'interest_calculation',
                'amount': Decimal('0')
            })
        
        return timeline
    
    def _generate_interest_dates(self, contract: CreditContract) -> List[date]:
        """Генерация дат начисления процентов"""
        dates = []
        current_date = contract.start_date
        
        while current_date <= contract.end_date:
            dates.append(current_date)
            current_date = self._add_period(current_date, contract.interest_payment_frequency)
        
        return dates
    
    def _add_period(self, start_date: date, frequency: str) -> date:
        """Добавить период к дате"""
        if frequency == 'daily':
            return start_date + timedelta(days=1)
        elif frequency == 'weekly':
            return start_date + timedelta(weeks=1)
        elif frequency == 'monthly':
            # Простое добавление месяца
            if start_date.month == 12:
                return start_date.replace(year=start_date.year + 1, month=1)
            else:
                return start_date.replace(month=start_date.month + 1)
        elif frequency == 'quarterly':
            return start_date + timedelta(days=90)  # Приблизительно
        elif frequency == 'semi_annually':
            return start_date + timedelta(days=180)  # Приблизительно
        elif frequency == 'annually':
            return start_date.replace(year=start_date.year + 1)
        else:
            return start_date + timedelta(days=30)  # По умолчанию
    
    def _is_interest_payment_date(self, contract: CreditContract, event_date: date) -> bool:
        """Проверка, является ли дата датой начисления процентов"""
        # Упрощенная логика - можно расширить
        return True  # Для простоты считаем, что проценты начисляются каждый день
    
    def _calculate_interest_for_period(self, 
                                     contract: CreditContract,
                                     drawdowns: List[Drawdown],
                                     debt_balance: Decimal,
                                     event_date: date,
                                     current_base_rate: Optional[Decimal]) -> Decimal:
        """Расчет процентов за период"""
        if debt_balance == 0:
            return Decimal('0')
        
        # Определение эффективной ставки
        effective_rate = self._get_effective_rate(contract, drawdowns, event_date, current_base_rate)
        
        # Расчет процентов за один день (упрощенно)
        daily_rate = effective_rate / Decimal('365')
        return debt_balance * daily_rate
    
    def _get_effective_rate(self, 
                           contract: CreditContract,
                           drawdowns: List[Drawdown],
                           event_date: date,
                           current_base_rate: Optional[Decimal]) -> Decimal:
        """Получение эффективной ставки на дату"""
        # Поиск активной выборки на дату
        active_drawdown = None
        for drawdown in sorted(drawdowns, key=lambda x: x.drawdown_date, reverse=True):
            if drawdown.drawdown_date <= event_date:
                active_drawdown = drawdown
                break
        
        if not active_drawdown:
            return Decimal('0')
        
        # Получение эффективной ставки
        if active_drawdown.is_floating_rate():
            if current_base_rate is not None:
                return active_drawdown.get_effective_rate(current_base_rate)
            else:
                return active_drawdown.interest_rate
        else:
            return active_drawdown.interest_rate
    
    def _get_days_in_period(self, event_date: date, timeline: Dict[date, List[Dict[str, Any]]]) -> int:
        """Получение количества дней в периоде"""
        # Упрощенная реализация - возвращаем 1 день
        return 1
    
    def create_annuity_schedule(self, 
                               contract: CreditContract,
                               principal: Decimal,
                               rate: Decimal,
                               periods: int,
                               version_id: str) -> PaymentSchedule:
        """
        Создание аннуитетного графика платежей
        
        Args:
            contract: Кредитный договор
            principal: Основная сумма
            rate: Месячная процентная ставка
            periods: Количество периодов
            version_id: ID версии расчета
            
        Returns:
            Аннуитетный график платежей
        """
        try:
            # Расчет аннуитетного платежа
            annuity_payment = self.interest_calculator.calculate_annuity_payment(principal, rate, periods)
            
            schedule = PaymentSchedule(
                contract_id=contract.id,
                version_id=version_id,
                calculation_date=date.today()
            )
            
            remaining_principal = principal
            current_date = contract.start_date
            
            for period in range(periods):
                # Расчет процентов за период
                interest_payment = remaining_principal * rate
                
                # Расчет погашения основного долга
                principal_payment = annuity_payment - interest_payment
                
                # Корректировка последнего платежа
                if period == periods - 1:
                    principal_payment = remaining_principal
                    annuity_payment = principal_payment + interest_payment
                
                # Создание элемента графика
                schedule_item = PaymentScheduleItem(
                    payment_date=current_date,
                    debt_balance_start=remaining_principal,
                    debt_balance_end=remaining_principal - principal_payment,
                    drawdown_amount=Decimal('0'),
                    principal_payment=principal_payment,
                    interest_payment=interest_payment,
                    effective_rate=rate,
                    days_in_period=30  # Приблизительно
                )
                
                schedule.add_item(schedule_item)
                
                # Обновление остатка
                remaining_principal -= principal_payment
                current_date = self._add_period(current_date, 'monthly')
            
            return schedule
            
        except Exception as e:
            logger.error(f"Error creating annuity schedule: {e}")
            raise

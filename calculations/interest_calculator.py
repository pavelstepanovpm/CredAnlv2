"""
Калькулятор процентных ставок с использованием Quantlib
"""

import QuantLib as ql
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class InterestCalculator:
    """Калькулятор процентных ставок"""
    
    def __init__(self, day_count_basis: str = 'Actual/360'):
        """
        Инициализация калькулятора
        
        Args:
            day_count_basis: База для расчета дней (Actual/360, Actual/365, 30/360)
        """
        self.day_count_basis = day_count_basis
        self._setup_quantlib()
    
    def _setup_quantlib(self):
        """Настройка Quantlib"""
        # Установка календаря (рабочие дни)
        self.calendar = ql.NullCalendar()  # Можно заменить на конкретный календарь
        
        # Установка базы для расчета дней
        if self.day_count_basis == 'Actual/360':
            self.day_count = ql.Actual360()
        elif self.day_count_basis == 'Actual/365':
            self.day_count = ql.Actual365Fixed()
        elif self.day_count_basis == '30/360':
            self.day_count = ql.Thirty360()
        else:
            self.day_count = ql.Actual360()  # По умолчанию
    
    def calculate_interest(self, 
                          principal: Decimal, 
                          rate: Decimal, 
                          start_date: date, 
                          end_date: date) -> Decimal:
        """
        Расчет процентов за период
        
        Args:
            principal: Основная сумма
            rate: Процентная ставка (в десятичном виде, например 0.075 для 7.5%)
            start_date: Дата начала периода
            end_date: Дата окончания периода
            
        Returns:
            Сумма процентов
        """
        try:
            # Конвертация в Quantlib типы
            ql_start_date = ql.Date(start_date.day, start_date.month, start_date.year)
            ql_end_date = ql.Date(end_date.day, end_date.month, end_date.year)
            
            # Расчет количества дней
            days = self.day_count.dayCount(ql_start_date, ql_end_date)
            
            # Расчет процентов
            interest = float(principal) * float(rate) * days / self.day_count.yearFraction(ql_start_date, ql_end_date)
            
            return Decimal(str(round(interest, 2)))
            
        except Exception as e:
            logger.error(f"Interest calculation error: {e}")
            return Decimal('0')
    
    def calculate_compound_interest(self, 
                                   principal: Decimal, 
                                   rate: Decimal, 
                                   periods: int, 
                                   compounding_frequency: int = 12) -> Decimal:
        """
        Расчет сложных процентов
        
        Args:
            principal: Основная сумма
            rate: Годовая процентная ставка
            periods: Количество периодов
            compounding_frequency: Частота начисления (12 для ежемесячного)
            
        Returns:
            Итоговая сумма с процентами
        """
        try:
            # Формула сложных процентов: A = P(1 + r/n)^(nt)
            # где P - основная сумма, r - ставка, n - частота начисления, t - время
            amount = float(principal) * (1 + float(rate) / compounding_frequency) ** (compounding_frequency * periods / 12)
            return Decimal(str(round(amount, 2)))
            
        except Exception as e:
            logger.error(f"Compound interest calculation error: {e}")
            return principal
    
    def calculate_annuity_payment(self, 
                                 principal: Decimal, 
                                 rate: Decimal, 
                                 periods: int) -> Decimal:
        """
        Расчет аннуитетного платежа
        
        Args:
            principal: Основная сумма
            rate: Месячная процентная ставка
            periods: Количество периодов
            
        Returns:
            Размер аннуитетного платежа
        """
        try:
            if rate == 0:
                return principal / periods
            
            # Формула аннуитета: PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
            rate_float = float(rate)
            periods_float = float(periods)
            
            if rate_float == 0:
                payment = float(principal) / periods_float
            else:
                payment = float(principal) * (rate_float * (1 + rate_float) ** periods_float) / ((1 + rate_float) ** periods_float - 1)
            
            return Decimal(str(round(payment, 2)))
            
        except Exception as e:
            logger.error(f"Annuity payment calculation error: {e}")
            return Decimal('0')
    
    def calculate_effective_rate(self, 
                                nominal_rate: Decimal, 
                                compounding_frequency: int) -> Decimal:
        """
        Расчет эффективной процентной ставки
        
        Args:
            nominal_rate: Номинальная ставка
            compounding_frequency: Частота начисления
            
        Returns:
            Эффективная ставка
        """
        try:
            # Формула: EAR = (1 + r/n)^n - 1
            rate_float = float(nominal_rate)
            freq_float = float(compounding_frequency)
            
            effective_rate = (1 + rate_float / freq_float) ** freq_float - 1
            
            return Decimal(str(round(effective_rate, 6)))
            
        except Exception as e:
            logger.error(f"Effective rate calculation error: {e}")
            return nominal_rate
    
    def calculate_present_value(self, 
                               future_value: Decimal, 
                               rate: Decimal, 
                               periods: int) -> Decimal:
        """
        Расчет приведенной стоимости
        
        Args:
            future_value: Будущая стоимость
            rate: Ставка дисконтирования
            periods: Количество периодов
            
        Returns:
            Приведенная стоимость
        """
        try:
            if rate == 0:
                return future_value
            
            # Формула: PV = FV / (1 + r)^n
            rate_float = float(rate)
            periods_float = float(periods)
            
            present_value = float(future_value) / (1 + rate_float) ** periods_float
            
            return Decimal(str(round(present_value, 2)))
            
        except Exception as e:
            logger.error(f"Present value calculation error: {e}")
            return future_value
    
    def calculate_net_present_value(self, 
                                   cashflows: list, 
                                   discount_rate: Decimal) -> Decimal:
        """
        Расчет чистой приведенной стоимости
        
        Args:
            cashflows: Список денежных потоков (словари с 'amount' и 'date')
            discount_rate: Ставка дисконтирования
            
        Returns:
            Чистая приведенная стоимость
        """
        try:
            npv = Decimal('0')
            base_date = cashflows[0]['date'] if cashflows else date.today()
            
            for cf in cashflows:
                periods = (cf['date'] - base_date).days / 365.25  # В годах
                pv = self.calculate_present_value(cf['amount'], discount_rate, periods)
                npv += pv
            
            return npv
            
        except Exception as e:
            logger.error(f"NPV calculation error: {e}")
            return Decimal('0')
    
    def calculate_internal_rate_of_return(self, 
                                        cashflows: list, 
                                        initial_guess: Decimal = Decimal('0.1')) -> Optional[Decimal]:
        """
        Расчет внутренней нормы доходности
        
        Args:
            cashflows: Список денежных потоков
            initial_guess: Начальное приближение для IRR
            
        Returns:
            Внутренняя норма доходности или None если не найдена
        """
        try:
            # Простая реализация методом Ньютона-Рафсона
            guess = float(initial_guess)
            tolerance = 1e-6
            max_iterations = 100
            
            for _ in range(max_iterations):
                npv = 0
                npv_derivative = 0
                
                for i, cf in enumerate(cashflows):
                    periods = i / 12.0  # Предполагаем ежемесячные платежи
                    amount = float(cf['amount'])
                    
                    npv += amount / (1 + guess) ** periods
                    npv_derivative -= periods * amount / (1 + guess) ** (periods + 1)
                
                if abs(npv) < tolerance:
                    return Decimal(str(round(guess, 6)))
                
                if abs(npv_derivative) < tolerance:
                    break
                
                guess = guess - npv / npv_derivative
            
            return None
            
        except Exception as e:
            logger.error(f"IRR calculation error: {e}")
            return None


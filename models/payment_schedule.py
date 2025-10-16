"""
Модель графика платежей
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class PaymentScheduleItem(BaseModel):
    """Элемент графика платежей"""
    
    # Дата и остатки
    payment_date: date = Field(..., description="Дата платежа")
    debt_balance_start: Decimal = Field(..., ge=0, description="Остаток долга на начало периода")
    debt_balance_end: Decimal = Field(..., ge=0, description="Остаток долга на конец периода")
    
    # Движения
    drawdown_amount: Decimal = Field(default=Decimal('0'), ge=0, description="Сумма выборки")
    principal_payment: Decimal = Field(default=Decimal('0'), ge=0, description="Сумма погашения основного долга")
    interest_payment: Decimal = Field(default=Decimal('0'), ge=0, description="Сумма процентов к уплате")
    
    # Расчетные поля
    effective_rate: Decimal = Field(..., ge=0, description="Эффективная ставка на период")
    days_in_period: int = Field(..., gt=0, description="Количество дней в периоде")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    
    @property
    def total_payment(self) -> Decimal:
        """Общая сумма платежа"""
        return self.principal_payment + self.interest_payment
    
    @property
    def net_cashflow(self) -> Decimal:
        """Чистый денежный поток (выборки - погашения)"""
        return self.drawdown_amount - self.total_payment
    
    def validate_balance_consistency(self) -> bool:
        """Проверка консистентности остатков"""
        expected_end_balance = (
            self.debt_balance_start + 
            self.drawdown_amount - 
            self.principal_payment
        )
        return abs(self.debt_balance_end - expected_end_balance) < Decimal('0.01')


class PaymentSchedule(BaseModel):
    """График платежей по кредиту"""
    
    # Основные атрибуты
    contract_id: str = Field(..., description="ID кредитного договора")
    version_id: str = Field(..., description="ID версии расчета")
    
    # График
    schedule_items: List[PaymentScheduleItem] = Field(default_factory=list, description="Элементы графика")
    
    # Метаданные
    calculation_date: date = Field(..., description="Дата расчета")
    total_drawdowns: Decimal = Field(default=Decimal('0'), description="Общая сумма выборок")
    total_principal_payments: Decimal = Field(default=Decimal('0'), description="Общая сумма погашений основного долга")
    total_interest_payments: Decimal = Field(default=Decimal('0'), description="Общая сумма процентных платежей")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    
    def add_item(self, item: PaymentScheduleItem) -> None:
        """Добавить элемент в график"""
        self.schedule_items.append(item)
        self._update_totals()
    
    def _update_totals(self) -> None:
        """Обновить итоговые суммы"""
        self.total_drawdowns = sum(item.drawdown_amount for item in self.schedule_items)
        self.total_principal_payments = sum(item.principal_payment for item in self.schedule_items)
        self.total_interest_payments = sum(item.interest_payment for item in self.schedule_items)
    
    def get_items_by_date_range(self, start_date: date, end_date: date) -> List[PaymentScheduleItem]:
        """Получить элементы за период"""
        return [
            item for item in self.schedule_items
            if start_date <= item.payment_date <= end_date
        ]
    
    def get_balance_on_date(self, target_date: date) -> Decimal:
        """Получить остаток долга на дату"""
        for item in reversed(self.schedule_items):
            if item.payment_date <= target_date:
                return item.debt_balance_end
        return Decimal('0')
    
    def get_cashflow_by_date(self, target_date: date) -> Optional[PaymentScheduleItem]:
        """Получить денежный поток на дату"""
        for item in self.schedule_items:
            if item.payment_date == target_date:
                return item
        return None
    
    def validate_schedule(self) -> bool:
        """Валидация графика платежей"""
        if not self.schedule_items:
            return True
        
        # Проверка хронологического порядка
        dates = [item.payment_date for item in self.schedule_items]
        if dates != sorted(dates):
            return False
        
        # Проверка консистентности остатков
        for item in self.schedule_items:
            if not item.validate_balance_consistency():
                return False
        
        return True


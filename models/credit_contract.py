"""
Модель кредитного договора
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class CreditType(str, Enum):
    """Типы кредитов"""
    CREDIT_LINE = "credit_line"  # Кредитная линия
    ONE_TIME_LOAN = "one_time_loan"  # Разовый кредит
    OVERDRAFT = "overdraft"  # Овердрафт
    REVOLVING = "revolving"  # Возобновляемый кредит


class Currency(str, Enum):
    """Валюты"""
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class PaymentScheduleType(str, Enum):
    """Типы графиков погашения"""
    ANNUITY = "annuity"  # Аннуитетный
    DIFFERENTIATED = "differentiated"  # Дифференцированный
    BULLET = "bullet"  # Единовременный
    CUSTOM = "custom"  # Индивидуальный


class PaymentFrequency(str, Enum):
    """Периодичность платежей"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semi_annually"
    ANNUALLY = "annually"


class CreditContract(BaseModel):
    """Кредитный договор"""
    
    # Основные атрибуты
    id: str = Field(..., description="Уникальный идентификатор договора")
    credit_type: CreditType = Field(..., description="Тип кредита")
    currency: Currency = Field(..., description="Валюта договора")
    
    # Лимиты
    total_limit: Decimal = Field(..., gt=0, description="Общий лимит кредитования")
    available_limit: Decimal = Field(..., ge=0, description="Доступный остаток лимита")
    
    # Даты
    start_date: date = Field(..., description="Дата начала действия договора")
    end_date: date = Field(..., description="Дата окончания / срок погашения")
    
    # График погашения
    payment_schedule_type: PaymentScheduleType = Field(..., description="Тип графика погашения")
    interest_payment_frequency: PaymentFrequency = Field(..., description="Периодичность уплаты процентов")
    principal_payment_frequency: PaymentFrequency = Field(..., description="Периодичность погашения основного долга")
    
    # Дополнительные параметры
    interest_rate_base: Optional[Decimal] = Field(None, description="Базовая ставка для плавающих ставок")
    margin: Optional[Decimal] = Field(None, description="Маржа к базовой ставке")
    
    # Метаданные
    created_at: datetime = Field(default_factory=datetime.now, description="Дата создания записи")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата последнего обновления")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    
    def validate_dates(self) -> bool:
        """Валидация дат договора"""
        return self.start_date < self.end_date
    
    def validate_limits(self) -> bool:
        """Валидация лимитов"""
        return self.available_limit <= self.total_limit
    
    def get_utilized_amount(self) -> Decimal:
        """Получить сумму использованного лимита"""
        return self.total_limit - self.available_limit
    
    def get_utilization_ratio(self) -> Decimal:
        """Получить коэффициент использования лимита"""
        if self.total_limit == 0:
            return Decimal('0')
        return self.get_utilized_amount() / self.total_limit


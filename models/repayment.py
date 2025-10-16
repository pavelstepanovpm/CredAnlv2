"""
Модель погашения
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class RepaymentStatus(str, Enum):
    """Статусы погашения"""
    PLANNED = "planned"  # Планируемое
    ACTUAL = "actual"  # Фактическое


class RepaymentType(str, Enum):
    """Типы погашения"""
    PRINCIPAL = "principal"  # Погашение основного долга
    INTEREST = "interest"  # Погашение процентов
    FULL = "full"  # Полное погашение (основной долг + проценты)


class Repayment(BaseModel):
    """Погашение"""
    
    # Основные атрибуты
    id: str = Field(..., description="Уникальный идентификатор погашения")
    contract_id: str = Field(..., description="Ссылка на кредитный договор")
    
    # Параметры погашения
    repayment_date: date = Field(..., description="Дата погашения")
    principal_amount: Decimal = Field(..., ge=0, description="Сумма погашения основного долга")
    interest_amount: Decimal = Field(..., ge=0, description="Сумма погашения процентов")
    
    # Статус и тип
    status: RepaymentStatus = Field(..., description="Статус погашения")
    repayment_type: RepaymentType = Field(..., description="Тип погашения")
    
    # Метаданные
    created_at: datetime = Field(default_factory=datetime.now, description="Дата создания записи")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата последнего обновления")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    
    @property
    def total_amount(self) -> Decimal:
        """Общая сумма погашения"""
        return self.principal_amount + self.interest_amount
    
    def is_principal_repayment(self) -> bool:
        """Проверка, является ли погашение основного долга"""
        return self.principal_amount > 0
    
    def is_interest_repayment(self) -> bool:
        """Проверка, является ли погашение процентов"""
        return self.interest_amount > 0
    
    def is_full_repayment(self) -> bool:
        """Проверка, является ли полным погашением"""
        return self.repayment_type == RepaymentType.FULL
    
    def validate_amounts(self) -> bool:
        """Валидация сумм погашения"""
        return self.principal_amount >= 0 and self.interest_amount >= 0


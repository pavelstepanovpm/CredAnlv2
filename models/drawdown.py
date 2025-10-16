"""
Модель выборки (транша)
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class InterestRateType(str, Enum):
    """Типы процентных ставок"""
    FIXED = "fixed"  # Фиксированная
    FLOATING = "floating"  # Плавающая


class DrawdownStatus(str, Enum):
    """Статусы выборки"""
    PLANNED = "planned"  # Планируемая
    ACTUAL = "actual"  # Фактическая


class Drawdown(BaseModel):
    """Выборка (транш)"""
    
    # Основные атрибуты
    id: str = Field(..., description="Уникальный идентификатор выборки")
    contract_id: str = Field(..., description="Ссылка на кредитный договор")
    
    # Параметры выборки
    drawdown_date: date = Field(..., description="Дата выборки")
    amount: Decimal = Field(..., gt=0, description="Сумма выборки")
    
    # Процентная ставка
    interest_rate_type: InterestRateType = Field(..., description="Тип процентной ставки")
    interest_rate: Decimal = Field(..., ge=0, description="Значение процентной ставки")
    base_rate: Optional[Decimal] = Field(None, description="Базовая ставка для плавающей ставки")
    margin: Optional[Decimal] = Field(None, description="Маржа к базовой ставке")
    
    # Статус
    status: DrawdownStatus = Field(..., description="Статус выборки")
    
    # Метаданные
    created_at: datetime = Field(default_factory=datetime.now, description="Дата создания записи")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата последнего обновления")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    
    def get_effective_rate(self, current_base_rate: Optional[Decimal] = None) -> Decimal:
        """Получить эффективную ставку на дату"""
        if self.interest_rate_type == InterestRateType.FIXED:
            return self.interest_rate
        
        if self.interest_rate_type == InterestRateType.FLOATING:
            if current_base_rate is None:
                current_base_rate = self.base_rate or Decimal('0')
            return current_base_rate + (self.margin or Decimal('0'))
        
        return self.interest_rate
    
    def validate_amount(self, available_limit: Decimal) -> bool:
        """Валидация суммы выборки относительно доступного лимита"""
        return self.amount <= available_limit
    
    def is_floating_rate(self) -> bool:
        """Проверка, является ли ставка плавающей"""
        return self.interest_rate_type == InterestRateType.FLOATING


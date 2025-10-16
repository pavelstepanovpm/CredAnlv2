"""
Модель версии расчета
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class VersionType(str, Enum):
    """Типы версий"""
    BASE = "base"  # Базовая версия
    SCENARIO = "scenario"  # Сценарная версия


class VersionStatus(str, Enum):
    """Статусы версий"""
    DRAFT = "draft"  # Черновик
    ACTIVE = "active"  # Активная
    ARCHIVED = "archived"  # Архивная


class CalculationVersion(BaseModel):
    """Версия расчета"""
    
    # Основные атрибуты
    id: str = Field(..., description="Уникальный идентификатор версии")
    name: str = Field(..., description="Наименование версии")
    description: Optional[str] = Field(None, description="Описание сценария")
    
    # Тип и статус
    version_type: VersionType = Field(..., description="Тип версии")
    status: VersionStatus = Field(default=VersionStatus.DRAFT, description="Статус версии")
    
    # Связи
    base_version_id: Optional[str] = Field(None, description="ID базовой версии (для сценарных)")
    
    # Параметры сценария
    scenario_parameters: Dict[str, Any] = Field(default_factory=dict, description="Параметры сценария")
    
    # Метаданные
    created_at: datetime = Field(default_factory=datetime.now, description="Дата создания")
    created_by: str = Field(..., description="Автор версии")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата последнего обновления")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    
    def is_base_version(self) -> bool:
        """Проверка, является ли версия базовой"""
        return self.version_type == VersionType.BASE
    
    def is_scenario_version(self) -> bool:
        """Проверка, является ли версия сценарной"""
        return self.version_type == VersionType.SCENARIO
    
    def is_active(self) -> bool:
        """Проверка, является ли версия активной"""
        return self.status == VersionStatus.ACTIVE
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Получить параметр сценария"""
        return self.scenario_parameters.get(key, default)
    
    def set_parameter(self, key: str, value: Any) -> None:
        """Установить параметр сценария"""
        self.scenario_parameters[key] = value
        self.updated_at = datetime.now()
    
    def get_base_rate(self) -> Optional[Decimal]:
        """Получить базовую ставку из параметров"""
        rate = self.get_parameter('base_rate')
        if rate is not None:
            return Decimal(str(rate))
        return None
    
    def set_base_rate(self, rate: Decimal) -> None:
        """Установить базовую ставку"""
        self.set_parameter('base_rate', float(rate))
    
    def get_scenario_date(self) -> Optional[date]:
        """Получить дату сценария"""
        scenario_date = self.get_parameter('scenario_date')
        if scenario_date:
            if isinstance(scenario_date, str):
                return date.fromisoformat(scenario_date)
            elif isinstance(scenario_date, date):
                return scenario_date
        return None
    
    def set_scenario_date(self, scenario_date: date) -> None:
        """Установить дату сценария"""
        self.set_parameter('scenario_date', scenario_date.isoformat())


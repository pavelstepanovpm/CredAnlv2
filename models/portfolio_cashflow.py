"""
Модель консолидированного кэш-флоу портфеля
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class PortfolioCashflowItem(BaseModel):
    """Элемент консолидированного кэш-флоу"""
    
    # Дата
    cashflow_date: date = Field(..., description="Дата")
    
    # Движения по портфелю
    total_drawdowns: Decimal = Field(default=Decimal('0'), ge=0, description="Общая сумма выборок")
    total_principal_payments: Decimal = Field(default=Decimal('0'), ge=0, description="Общая сумма погашений основного долга")
    total_interest_payments: Decimal = Field(default=Decimal('0'), ge=0, description="Общая сумма процентных платежей")
    
    # Остатки
    total_debt_balance: Decimal = Field(default=Decimal('0'), ge=0, description="Совокупный остаток долга")
    total_available_limit: Decimal = Field(default=Decimal('0'), ge=0, description="Совокупный остаток доступного лимита")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    
    @property
    def total_payments(self) -> Decimal:
        """Общая сумма платежей"""
        return self.total_principal_payments + self.total_interest_payments
    
    @property
    def net_cashflow(self) -> Decimal:
        """Чистый денежный поток (выборки - платежи)"""
        return self.total_drawdowns - self.total_payments
    
    @property
    def utilization_ratio(self) -> Decimal:
        """Коэффициент использования лимита"""
        total_limit = self.total_debt_balance + self.total_available_limit
        if total_limit == 0:
            return Decimal('0')
        return self.total_debt_balance / total_limit


class PortfolioCashflow(BaseModel):
    """Консолидированный кэш-флоу портфеля"""
    
    # Основные атрибуты
    version_id: str = Field(..., description="ID версии расчета")
    
    # Кэш-флоу
    cashflow_items: List[PortfolioCashflowItem] = Field(default_factory=list, description="Элементы кэш-флоу")
    
    # Период отчета
    report_start_date: Optional[date] = Field(None, description="Начало периода отчета")
    report_end_date: Optional[date] = Field(None, description="Конец периода отчета")
    
    # Итоговые показатели
    total_drawdowns: Decimal = Field(default=Decimal('0'), description="Общая сумма выборок за период")
    total_principal_payments: Decimal = Field(default=Decimal('0'), description="Общая сумма погашений основного долга за период")
    total_interest_payments: Decimal = Field(default=Decimal('0'), description="Общая сумма процентных платежей за период")
    
    # Остатки на даты
    debt_balance_start_period: Decimal = Field(default=Decimal('0'), description="Остаток долга на начало периода")
    debt_balance_end_period: Decimal = Field(default=Decimal('0'), description="Остаток долга на конец периода")
    limit_balance_start_period: Decimal = Field(default=Decimal('0'), description="Остаток лимита на начало периода")
    limit_balance_end_period: Decimal = Field(default=Decimal('0'), description="Остаток лимита на конец периода")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    
    def add_item(self, item: PortfolioCashflowItem) -> None:
        """Добавить элемент в кэш-флоу"""
        self.cashflow_items.append(item)
        self._update_totals()
    
    def _update_totals(self) -> None:
        """Обновить итоговые суммы"""
        if not self.cashflow_items:
            return
        
        # Сортировка по дате
        self.cashflow_items.sort(key=lambda x: x.cashflow_date)
        
        # Расчет итогов
        self.total_drawdowns = sum(item.total_drawdowns for item in self.cashflow_items)
        self.total_principal_payments = sum(item.total_principal_payments for item in self.cashflow_items)
        self.total_interest_payments = sum(item.total_interest_payments for item in self.cashflow_items)
        
        # Остатки на начало и конец периода
        if self.cashflow_items:
            self.debt_balance_start_period = self.cashflow_items[0].total_debt_balance
            self.debt_balance_end_period = self.cashflow_items[-1].total_debt_balance
            self.limit_balance_start_period = self.cashflow_items[0].total_available_limit
            self.limit_balance_end_period = self.cashflow_items[-1].total_available_limit
    
    def get_items_by_date_range(self, start_date: date, end_date: date) -> List[PortfolioCashflowItem]:
        """Получить элементы за период"""
        return [
            item for item in self.cashflow_items
            if start_date <= item.cashflow_date <= end_date
        ]
    
    def get_balance_on_date(self, target_date: date) -> tuple[Decimal, Decimal]:
        """Получить остатки на дату (долг, лимит)"""
        for item in reversed(self.cashflow_items):
            if item.cashflow_date <= target_date:
                return item.total_debt_balance, item.total_available_limit
        return Decimal('0'), Decimal('0')
    
    def get_cashflow_on_date(self, target_date: date) -> Optional[PortfolioCashflowItem]:
        """Получить денежный поток на дату"""
        for item in self.cashflow_items:
            if item.cashflow_date == target_date:
                return item
        return None
    
    def get_net_cashflow_summary(self) -> dict:
        """Получить сводку по чистому денежному потоку"""
        if not self.cashflow_items:
            return {
                'total_net_cashflow': Decimal('0'),
                'positive_days': 0,
                'negative_days': 0,
                'max_positive': Decimal('0'),
                'max_negative': Decimal('0')
            }
        
        net_flows = [item.net_cashflow for item in self.cashflow_items]
        positive_flows = [flow for flow in net_flows if flow > 0]
        negative_flows = [flow for flow in net_flows if flow < 0]
        
        return {
            'total_net_cashflow': sum(net_flows),
            'positive_days': len(positive_flows),
            'negative_days': len(negative_flows),
            'max_positive': max(positive_flows) if positive_flows else Decimal('0'),
            'max_negative': min(negative_flows) if negative_flows else Decimal('0')
        }


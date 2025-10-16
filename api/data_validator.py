"""
Валидатор данных для проверки корректности полученных из API данных
"""

from typing import List
from datetime import date
from decimal import Decimal
import logging

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import CreditContract, Drawdown, Repayment

logger = logging.getLogger(__name__)


class DataValidator:
    """Валидатор данных для API"""
    
    def validate_contract(self, contract: CreditContract) -> bool:
        """
        Валидация кредитного договора
        
        Args:
            contract: Кредитный договор для валидации
            
        Returns:
            True если данные корректны, False иначе
        """
        try:
            # Проверка обязательных полей
            if not contract.id:
                logger.error("Contract ID is required")
                return False
            
            # Проверка дат
            if not contract.validate_dates():
                logger.error(f"Invalid contract dates: {contract.id}")
                return False
            
            # Проверка лимитов
            if not contract.validate_limits():
                logger.error(f"Invalid contract limits: {contract.id}")
                return False
            
            # Проверка положительности лимитов
            if contract.total_limit <= 0:
                logger.error(f"Total limit must be positive: {contract.id}")
                return False
            
            if contract.available_limit < 0:
                logger.error(f"Available limit cannot be negative: {contract.id}")
                return False
            
            # Проверка превышения доступного лимита над общим
            if contract.available_limit > contract.total_limit:
                logger.error(f"Available limit exceeds total limit: {contract.id}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Contract validation error: {e}")
            return False
    
    def validate_drawdown(self, drawdown: Drawdown) -> bool:
        """
        Валидация выборки
        
        Args:
            drawdown: Выборка для валидации
            
        Returns:
            True если данные корректны, False иначе
        """
        try:
            # Проверка обязательных полей
            if not drawdown.id:
                logger.error("Drawdown ID is required")
                return False
            
            if not drawdown.contract_id:
                logger.error("Contract ID is required for drawdown")
                return False
            
            # Проверка суммы
            if drawdown.amount <= 0:
                logger.error(f"Drawdown amount must be positive: {drawdown.id}")
                return False
            
            # Проверка ставки
            if drawdown.interest_rate < 0:
                logger.error(f"Interest rate cannot be negative: {drawdown.id}")
                return False
            
            # Проверка плавающей ставки
            if drawdown.is_floating_rate():
                if drawdown.base_rate is None:
                    logger.error(f"Base rate is required for floating rate: {drawdown.id}")
                    return False
                
                if drawdown.margin is None:
                    logger.error(f"Margin is required for floating rate: {drawdown.id}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Drawdown validation error: {e}")
            return False
    
    def validate_repayment(self, repayment: Repayment) -> bool:
        """
        Валидация погашения
        
        Args:
            repayment: Погашение для валидации
            
        Returns:
            True если данные корректны, False иначе
        """
        try:
            # Проверка обязательных полей
            if not repayment.id:
                logger.error("Repayment ID is required")
                return False
            
            if not repayment.contract_id:
                logger.error("Contract ID is required for repayment")
                return False
            
            # Проверка сумм
            if not repayment.validate_amounts():
                logger.error(f"Invalid repayment amounts: {repayment.id}")
                return False
            
            # Проверка, что хотя бы одна сумма больше нуля
            if repayment.principal_amount == 0 and repayment.interest_amount == 0:
                logger.error(f"At least one repayment amount must be positive: {repayment.id}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Repayment validation error: {e}")
            return False
    
    def validate_contract_data_consistency(self, contract: CreditContract, 
                                         drawdowns: List[Drawdown], 
                                         repayments: List[Repayment]) -> bool:
        """
        Валидация консистентности данных по договору
        
        Args:
            contract: Кредитный договор
            drawdowns: Список выборок
            repayments: Список погашений
            
        Returns:
            True если данные консистентны, False иначе
        """
        try:
            # Проверка, что все выборки и погашения относятся к данному договору
            for drawdown in drawdowns:
                if drawdown.contract_id != contract.id:
                    logger.error(f"Drawdown {drawdown.id} belongs to different contract")
                    return False
            
            for repayment in repayments:
                if repayment.contract_id != contract.id:
                    logger.error(f"Repayment {repayment.id} belongs to different contract")
                    return False
            
            # Проверка превышения выборок над лимитом
            total_drawdowns = sum(drawdown.amount for drawdown in drawdowns)
            if total_drawdowns > contract.total_limit:
                logger.error(f"Total drawdowns exceed contract limit: {contract.id}")
                return False
            
            # Проверка логики погашений
            total_principal_repayments = sum(repayment.principal_amount for repayment in repayments)
            if total_principal_repayments > total_drawdowns:
                logger.error(f"Total principal repayments exceed total drawdowns: {contract.id}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Data consistency validation error: {e}")
            return False
    
    def validate_portfolio_data(self, contracts: List[CreditContract], 
                              all_drawdowns: List[Drawdown], 
                              all_repayments: List[Repayment]) -> bool:
        """
        Валидация данных портфеля
        
        Args:
            contracts: Список договоров
            all_drawdowns: Все выборки
            all_repayments: Все погашения
            
        Returns:
            True если данные портфеля корректны, False иначе
        """
        try:
            # Проверка уникальности ID договоров
            contract_ids = [contract.id for contract in contracts]
            if len(contract_ids) != len(set(contract_ids)):
                logger.error("Duplicate contract IDs found")
                return False
            
            # Проверка каждого договора отдельно
            for contract in contracts:
                contract_drawdowns = [d for d in all_drawdowns if d.contract_id == contract.id]
                contract_repayments = [r for r in all_repayments if r.contract_id == contract.id]
                
                if not self.validate_contract_data_consistency(contract, contract_drawdowns, contract_repayments):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Portfolio data validation error: {e}")
            return False

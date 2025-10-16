"""
Клиент для работы с API казначейской системы
"""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from decimal import Decimal
import logging

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import CreditContract, Drawdown, Repayment
from .data_validator import DataValidator

logger = logging.getLogger(__name__)


class TreasuryAPIClient:
    """Клиент для работы с API казначейской системы"""
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        """
        Инициализация клиента
        
        Args:
            base_url: Базовый URL API
            api_key: API ключ для аутентификации
            timeout: Таймаут запросов в секундах
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self.validator = DataValidator()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Выполнить HTTP запрос к API
        
        Args:
            method: HTTP метод
            endpoint: Эндпоинт API
            **kwargs: Дополнительные параметры запроса
            
        Returns:
            Ответ API в виде словаря
            
        Raises:
            requests.RequestException: Ошибка HTTP запроса
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {method} {url} - {e}")
            raise
    
    def get_active_contracts(self) -> List[CreditContract]:
        """
        Получить список активных кредитных договоров
        
        Returns:
            Список активных кредитных договоров
        """
        try:
            response = self._make_request('GET', '/api/v1/contracts/active')
            contracts = []
            
            for contract_data in response.get('data', []):
                try:
                    contract = self._parse_contract(contract_data)
                    if self.validator.validate_contract(contract):
                        contracts.append(contract)
                    else:
                        logger.warning(f"Invalid contract data: {contract.id}")
                except Exception as e:
                    logger.error(f"Failed to parse contract: {e}")
                    continue
            
            logger.info(f"Retrieved {len(contracts)} active contracts")
            return contracts
            
        except Exception as e:
            logger.error(f"Failed to get active contracts: {e}")
            raise
    
    def get_contract_drawdowns(self, contract_id: str) -> List[Drawdown]:
        """
        Получить историю выборок по договору
        
        Args:
            contract_id: ID кредитного договора
            
        Returns:
            Список выборок по договору
        """
        try:
            response = self._make_request('GET', f'/api/v1/contracts/{contract_id}/drawdowns')
            drawdowns = []
            
            for drawdown_data in response.get('data', []):
                try:
                    drawdown = self._parse_drawdown(drawdown_data)
                    if self.validator.validate_drawdown(drawdown):
                        drawdowns.append(drawdown)
                    else:
                        logger.warning(f"Invalid drawdown data: {drawdown.id}")
                except Exception as e:
                    logger.error(f"Failed to parse drawdown: {e}")
                    continue
            
            logger.info(f"Retrieved {len(drawdowns)} drawdowns for contract {contract_id}")
            return drawdowns
            
        except Exception as e:
            logger.error(f"Failed to get drawdowns for contract {contract_id}: {e}")
            raise
    
    def get_contract_repayments(self, contract_id: str) -> List[Repayment]:
        """
        Получить историю погашений по договору
        
        Args:
            contract_id: ID кредитного договора
            
        Returns:
            Список погашений по договору
        """
        try:
            response = self._make_request('GET', f'/api/v1/contracts/{contract_id}/repayments')
            repayments = []
            
            for repayment_data in response.get('data', []):
                try:
                    repayment = self._parse_repayment(repayment_data)
                    if self.validator.validate_repayment(repayment):
                        repayments.append(repayment)
                    else:
                        logger.warning(f"Invalid repayment data: {repayment.id}")
                except Exception as e:
                    logger.error(f"Failed to parse repayment: {e}")
                    continue
            
            logger.info(f"Retrieved {len(repayments)} repayments for contract {contract_id}")
            return repayments
            
        except Exception as e:
            logger.error(f"Failed to get repayments for contract {contract_id}: {e}")
            raise
    
    def get_current_base_rate(self) -> Decimal:
        """
        Получить текущую базовую ставку (ключевую ставку ЦБ)
        
        Returns:
            Текущая базовая ставка
        """
        try:
            response = self._make_request('GET', '/api/v1/rates/current')
            rate = Decimal(str(response.get('base_rate', 0)))
            logger.info(f"Retrieved current base rate: {rate}")
            return rate
            
        except Exception as e:
            logger.error(f"Failed to get current base rate: {e}")
            # Возвращаем значение по умолчанию
            return Decimal('7.5')  # Примерная ключевая ставка ЦБ
    
    def _parse_contract(self, data: Dict[str, Any]) -> CreditContract:
        """Парсинг данных кредитного договора"""
        return CreditContract(
            id=data['id'],
            credit_type=data['credit_type'],
            currency=data['currency'],
            total_limit=Decimal(str(data['total_limit'])),
            available_limit=Decimal(str(data['available_limit'])),
            start_date=date.fromisoformat(data['start_date']),
            end_date=date.fromisoformat(data['end_date']),
            payment_schedule_type=data['payment_schedule_type'],
            interest_payment_frequency=data['interest_payment_frequency'],
            principal_payment_frequency=data['principal_payment_frequency'],
            interest_rate_base=Decimal(str(data['interest_rate_base'])) if data.get('interest_rate_base') else None,
            margin=Decimal(str(data['margin'])) if data.get('margin') else None
        )
    
    def _parse_drawdown(self, data: Dict[str, Any]) -> Drawdown:
        """Парсинг данных выборки"""
        return Drawdown(
            id=data['id'],
            contract_id=data['contract_id'],
            drawdown_date=date.fromisoformat(data['drawdown_date']),
            amount=Decimal(str(data['amount'])),
            interest_rate_type=data['interest_rate_type'],
            interest_rate=Decimal(str(data['interest_rate'])),
            base_rate=Decimal(str(data['base_rate'])) if data.get('base_rate') else None,
            margin=Decimal(str(data['margin'])) if data.get('margin') else None,
            status=data['status']
        )
    
    def _parse_repayment(self, data: Dict[str, Any]) -> Repayment:
        """Парсинг данных погашения"""
        return Repayment(
            id=data['id'],
            contract_id=data['contract_id'],
            repayment_date=date.fromisoformat(data['repayment_date']),
            principal_amount=Decimal(str(data['principal_amount'])),
            interest_amount=Decimal(str(data['interest_amount'])),
            status=data['status'],
            repayment_type=data['repayment_type']
        )
    
    def test_connection(self) -> bool:
        """
        Проверить соединение с API
        
        Returns:
            True если соединение успешно, False иначе
        """
        try:
            self._make_request('GET', '/api/v1/health')
            logger.info("API connection test successful")
            return True
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False

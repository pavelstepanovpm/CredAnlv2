"""
Агрегатор данных для консолидации портфеля
"""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
import logging

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import (
    CreditContract, Drawdown, Repayment, 
    PaymentSchedule, PortfolioCashflow, PortfolioCashflowItem
)

logger = logging.getLogger(__name__)


class DataAggregator:
    """Агрегатор данных портфеля"""
    
    def __init__(self):
        """Инициализация агрегатора"""
        pass
    
    def aggregate_portfolio_data(self, 
                               contracts: List[CreditContract],
                               all_drawdowns: List[Drawdown],
                               all_repayments: List[Repayment]) -> Dict[str, Any]:
        """
        Агрегация данных портфеля
        
        Args:
            contracts: Список кредитных договоров
            all_drawdowns: Все выборки
            all_repayments: Все погашения
            
        Returns:
            Агрегированные данные портфеля
        """
        try:
            logger.info(f"Aggregating data for {len(contracts)} contracts")
            
            # Базовые метрики портфеля
            portfolio_summary = self._calculate_portfolio_summary(contracts)
            
            # Агрегация по валютам
            currency_breakdown = self._aggregate_by_currency(contracts, all_drawdowns, all_repayments)
            
            # Агрегация по типам кредитов
            credit_type_breakdown = self._aggregate_by_credit_type(contracts, all_drawdowns, all_repayments)
            
            # Временной анализ
            temporal_analysis = self._analyze_temporal_patterns(all_drawdowns, all_repayments)
            
            # Анализ рисков
            risk_analysis = self._analyze_risk_metrics(contracts, all_drawdowns, all_repayments)
            
            return {
                'portfolio_summary': portfolio_summary,
                'currency_breakdown': currency_breakdown,
                'credit_type_breakdown': credit_type_breakdown,
                'temporal_analysis': temporal_analysis,
                'risk_analysis': risk_analysis,
                'aggregation_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error aggregating portfolio data: {e}")
            return {}
    
    def _calculate_portfolio_summary(self, contracts: List[CreditContract]) -> Dict[str, Any]:
        """Расчет сводных показателей портфеля"""
        try:
            if not contracts:
                return {}
            
            total_contracts = len(contracts)
            total_limit = sum(contract.total_limit for contract in contracts)
            total_available = sum(contract.available_limit for contract in contracts)
            total_utilized = total_limit - total_available
            
            # Расчет средних показателей
            avg_limit = total_limit / total_contracts if total_contracts > 0 else Decimal('0')
            avg_utilization = total_utilized / total_limit if total_limit > 0 else Decimal('0')
            
            # Анализ сроков
            active_contracts = [c for c in contracts if c.end_date >= date.today()]
            expired_contracts = [c for c in contracts if c.end_date < date.today()]
            
            return {
                'total_contracts': total_contracts,
                'active_contracts': len(active_contracts),
                'expired_contracts': len(expired_contracts),
                'total_limit': float(total_limit),
                'total_utilized': float(total_utilized),
                'total_available': float(total_available),
                'average_limit': float(avg_limit),
                'utilization_ratio': float(avg_utilization),
                'portfolio_size': self._categorize_portfolio_size(total_limit)
            }
            
        except Exception as e:
            logger.error(f"Error calculating portfolio summary: {e}")
            return {}
    
    def _aggregate_by_currency(self, 
                              contracts: List[CreditContract],
                              all_drawdowns: List[Drawdown],
                              all_repayments: List[Repayment]) -> Dict[str, Any]:
        """Агрегация по валютам"""
        try:
            currency_data = {}
            
            for contract in contracts:
                currency = contract.currency
                if currency not in currency_data:
                    currency_data[currency] = {
                        'contracts': [],
                        'total_limit': Decimal('0'),
                        'total_utilized': Decimal('0'),
                        'total_available': Decimal('0'),
                        'drawdowns_count': 0,
                        'repayments_count': 0
                    }
                
                currency_data[currency]['contracts'].append(contract.id)
                currency_data[currency]['total_limit'] += contract.total_limit
                currency_data[currency]['total_utilized'] += contract.get_utilized_amount()
                currency_data[currency]['total_available'] += contract.available_limit
            
            # Добавление данных по выборкам и погашениям
            for drawdown in all_drawdowns:
                contract = next((c for c in contracts if c.id == drawdown.contract_id), None)
                if contract:
                    currency = contract.currency
                    if currency in currency_data:
                        currency_data[currency]['drawdowns_count'] += 1
            
            for repayment in all_repayments:
                contract = next((c for c in contracts if c.id == repayment.contract_id), None)
                if contract:
                    currency = contract.currency
                    if currency in currency_data:
                        currency_data[currency]['repayments_count'] += 1
            
            # Конвертация в float для JSON сериализации
            for currency in currency_data:
                for key in ['total_limit', 'total_utilized', 'total_available']:
                    currency_data[currency][key] = float(currency_data[currency][key])
            
            return currency_data
            
        except Exception as e:
            logger.error(f"Error aggregating by currency: {e}")
            return {}
    
    def _aggregate_by_credit_type(self, 
                                 contracts: List[CreditContract],
                                 all_drawdowns: List[Drawdown],
                                 all_repayments: List[Repayment]) -> Dict[str, Any]:
        """Агрегация по типам кредитов"""
        try:
            credit_type_data = {}
            
            for contract in contracts:
                credit_type = contract.credit_type
                if credit_type not in credit_type_data:
                    credit_type_data[credit_type] = {
                        'contracts': [],
                        'total_limit': Decimal('0'),
                        'total_utilized': Decimal('0'),
                        'total_available': Decimal('0'),
                        'average_utilization': Decimal('0')
                    }
                
                credit_type_data[credit_type]['contracts'].append(contract.id)
                credit_type_data[credit_type]['total_limit'] += contract.total_limit
                credit_type_data[credit_type]['total_utilized'] += contract.get_utilized_amount()
                credit_type_data[credit_type]['total_available'] += contract.available_limit
            
            # Расчет средних показателей
            for credit_type in credit_type_data:
                data = credit_type_data[credit_type]
                if data['total_limit'] > 0:
                    data['average_utilization'] = data['total_utilized'] / data['total_limit']
                else:
                    data['average_utilization'] = Decimal('0')
                
                # Конвертация в float
                for key in ['total_limit', 'total_utilized', 'total_available', 'average_utilization']:
                    data[key] = float(data[key])
            
            return credit_type_data
            
        except Exception as e:
            logger.error(f"Error aggregating by credit type: {e}")
            return {}
    
    def _analyze_temporal_patterns(self, 
                                  all_drawdowns: List[Drawdown],
                                  all_repayments: List[Repayment]) -> Dict[str, Any]:
        """Анализ временных паттернов"""
        try:
            # Анализ выборок по месяцам
            drawdowns_by_month = {}
            for drawdown in all_drawdowns:
                month_key = drawdown.drawdown_date.strftime('%Y-%m')
                if month_key not in drawdowns_by_month:
                    drawdowns_by_month[month_key] = {'count': 0, 'amount': Decimal('0')}
                drawdowns_by_month[month_key]['count'] += 1
                drawdowns_by_month[month_key]['amount'] += drawdown.amount
            
            # Анализ погашений по месяцам
            repayments_by_month = {}
            for repayment in all_repayments:
                month_key = repayment.repayment_date.strftime('%Y-%m')
                if month_key not in repayments_by_month:
                    repayments_by_month[month_key] = {
                        'count': 0, 
                        'principal': Decimal('0'), 
                        'interest': Decimal('0')
                    }
                repayments_by_month[month_key]['count'] += 1
                repayments_by_month[month_key]['principal'] += repayment.principal_amount
                repayments_by_month[month_key]['interest'] += repayment.interest_amount
            
            # Конвертация в float
            for month in drawdowns_by_month:
                drawdowns_by_month[month]['amount'] = float(drawdowns_by_month[month]['amount'])
            
            for month in repayments_by_month:
                repayments_by_month[month]['principal'] = float(repayments_by_month[month]['principal'])
                repayments_by_month[month]['interest'] = float(repayments_by_month[month]['interest'])
            
            return {
                'drawdowns_by_month': drawdowns_by_month,
                'repayments_by_month': repayments_by_month,
                'analysis_period': {
                    'start': min([d.drawdown_date for d in all_drawdowns] + [r.repayment_date for r in all_repayments]) if all_drawdowns or all_repayments else None,
                    'end': max([d.drawdown_date for d in all_drawdowns] + [r.repayment_date for r in all_repayments]) if all_drawdowns or all_repayments else None
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing temporal patterns: {e}")
            return {}
    
    def _analyze_risk_metrics(self, 
                             contracts: List[CreditContract],
                             all_drawdowns: List[Drawdown],
                             all_repayments: List[Repayment]) -> Dict[str, Any]:
        """Анализ метрик риска"""
        try:
            if not contracts:
                return {}
            
            # Концентрация портфеля
            total_limit = sum(contract.total_limit for contract in contracts)
            if total_limit == 0:
                return {}
            
            # Расчет индекса Херфиндаля-Хиршмана
            contract_shares = [float(contract.total_limit / total_limit) for contract in contracts]
            hhi = sum(share ** 2 for share in contract_shares)
            
            # Максимальная доля
            max_share = max(contract_shares)
            
            # Анализ сроков
            current_date = date.today()
            contracts_by_maturity = {
                'short_term': len([c for c in contracts if (c.end_date - current_date).days <= 30]),
                'medium_term': len([c for c in contracts if 30 < (c.end_date - current_date).days <= 365]),
                'long_term': len([c for c in contracts if (c.end_date - current_date).days > 365])
            }
            
            # Анализ использования лимитов
            utilization_levels = {
                'low': len([c for c in contracts if c.get_utilization_ratio() < 0.3]),
                'medium': len([c for c in contracts if 0.3 <= c.get_utilization_ratio() < 0.7]),
                'high': len([c for c in contracts if c.get_utilization_ratio() >= 0.7])
            }
            
            return {
                'concentration_risk': {
                    'hhi': hhi,
                    'max_share': max_share,
                    'risk_level': 'high' if hhi > 0.25 else 'medium' if hhi > 0.15 else 'low'
                },
                'maturity_distribution': contracts_by_maturity,
                'utilization_distribution': utilization_levels,
                'total_exposure': float(total_limit),
                'average_exposure': float(total_limit / len(contracts))
            }
            
        except Exception as e:
            logger.error(f"Error analyzing risk metrics: {e}")
            return {}
    
    def _categorize_portfolio_size(self, total_limit: Decimal) -> str:
        """Категоризация размера портфеля"""
        limit_float = float(total_limit)
        
        if limit_float < 1_000_000:  # Менее 1 млн
            return 'small'
        elif limit_float < 10_000_000:  # Менее 10 млн
            return 'medium'
        elif limit_float < 100_000_000:  # Менее 100 млн
            return 'large'
        else:
            return 'very_large'
    
    def create_portfolio_report(self, 
                              aggregated_data: Dict[str, Any],
                              report_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Создание отчета по портфелю
        
        Args:
            aggregated_data: Агрегированные данные
            report_date: Дата отчета
            
        Returns:
            Отчет по портфелю
        """
        try:
            if report_date is None:
                report_date = date.today()
            
            report = {
                'report_date': report_date.isoformat(),
                'portfolio_summary': aggregated_data.get('portfolio_summary', {}),
                'currency_breakdown': aggregated_data.get('currency_breakdown', {}),
                'credit_type_breakdown': aggregated_data.get('credit_type_breakdown', {}),
                'temporal_analysis': aggregated_data.get('temporal_analysis', {}),
                'risk_analysis': aggregated_data.get('risk_analysis', {}),
                'key_insights': self._generate_key_insights(aggregated_data)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error creating portfolio report: {e}")
            return {}
    
    def _generate_key_insights(self, aggregated_data: Dict[str, Any]) -> List[str]:
        """Генерация ключевых инсайтов"""
        insights = []
        
        try:
            # Анализ концентрации
            risk_analysis = aggregated_data.get('risk_analysis', {})
            concentration_risk = risk_analysis.get('concentration_risk', {})
            risk_level = concentration_risk.get('risk_level', 'unknown')
            
            if risk_level == 'high':
                insights.append("Высокая концентрация риска в портфеле")
            elif risk_level == 'medium':
                insights.append("Умеренная концентрация риска в портфеле")
            else:
                insights.append("Низкая концентрация риска в портфеле")
            
            # Анализ использования
            portfolio_summary = aggregated_data.get('portfolio_summary', {})
            utilization_ratio = portfolio_summary.get('utilization_ratio', 0)
            
            if utilization_ratio > 0.8:
                insights.append("Высокий уровень использования лимитов")
            elif utilization_ratio > 0.5:
                insights.append("Умеренный уровень использования лимитов")
            else:
                insights.append("Низкий уровень использования лимитов")
            
            # Анализ валютной структуры
            currency_breakdown = aggregated_data.get('currency_breakdown', {})
            if len(currency_breakdown) > 1:
                insights.append("Мультивалютный портфель")
            else:
                insights.append("Моновалютный портфель")
            
        except Exception as e:
            logger.error(f"Error generating key insights: {e}")
        
        return insights

"""
Создатель дашбордов для визуализации данных портфеля
"""

from datetime import datetime, date
from typing import List, Dict, Any, Optional
import logging

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import PortfolioCashflow, CreditContract, CalculationVersion
from .chart_builder import ChartBuilder

logger = logging.getLogger(__name__)


class DashboardCreator:
    """Создатель дашбордов"""
    
    def __init__(self, theme: str = 'dark'):
        """
        Инициализация создателя дашбордов
        
        Args:
            theme: Тема оформления
        """
        self.chart_builder = ChartBuilder(theme)
        self.theme = theme
    
    def create_portfolio_dashboard(self, 
                                 cashflow: PortfolioCashflow,
                                 contracts: List[CreditContract],
                                 metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создание дашборда портфеля
        
        Args:
            cashflow: Кэш-флоу портфеля
            contracts: Список договоров
            metrics: Метрики портфеля
            
        Returns:
            Данные дашборда
        """
        try:
            logger.info("Creating portfolio dashboard")
            
            # Создание графиков
            cashflow_chart = self.chart_builder.create_cashflow_chart(
                cashflow, "Консолидированный кэш-флоу портфеля"
            )
            
            utilization_chart = self.chart_builder.create_utilization_chart(
                contracts, "Использование лимитов по договорам"
            )
            
            metrics_chart = self.chart_builder.create_portfolio_metrics_chart(
                metrics, "Ключевые метрики портфеля"
            )
            
            # Создание дашборда
            dashboard = {
                'title': 'Дашборд портфеля',
                'created_at': datetime.now().isoformat(),
                'charts': {
                    'cashflow': cashflow_chart,
                    'utilization': utilization_chart,
                    'metrics': metrics_chart
                },
                'summary': self._create_portfolio_summary(metrics),
                'alerts': self._create_alerts(metrics)
            }
            
            logger.info("Portfolio dashboard created successfully")
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating portfolio dashboard: {e}")
            return {}
    
    def create_scenario_dashboard(self, 
                                base_cashflow: PortfolioCashflow,
                                scenario_cashflow: PortfolioCashflow,
                                base_version: CalculationVersion,
                                scenario_version: CalculationVersion) -> Dict[str, Any]:
        """
        Создание дашборда сравнения сценариев
        
        Args:
            base_cashflow: Базовый кэш-флоу
            scenario_cashflow: Сценарный кэш-флоу
            base_version: Базовая версия
            scenario_version: Сценарная версия
            
        Returns:
            Данные дашборда
        """
        try:
            logger.info("Creating scenario comparison dashboard")
            
            # Создание графиков
            comparison_chart = self.chart_builder.create_scenario_comparison_chart(
                base_cashflow, scenario_cashflow, 
                f"Сравнение: {base_version.name} vs {scenario_version.name}"
            )
            
            # Расчет влияния сценария
            impact_analysis = self._calculate_scenario_impact(base_cashflow, scenario_cashflow)
            
            # Создание дашборда
            dashboard = {
                'title': 'Сравнение сценариев',
                'created_at': datetime.now().isoformat(),
                'base_version': {
                    'id': base_version.id,
                    'name': base_version.name,
                    'description': base_version.description
                },
                'scenario_version': {
                    'id': scenario_version.id,
                    'name': scenario_version.name,
                    'description': scenario_version.description
                },
                'charts': {
                    'comparison': comparison_chart
                },
                'impact_analysis': impact_analysis,
                'recommendations': self._generate_recommendations(impact_analysis)
            }
            
            logger.info("Scenario dashboard created successfully")
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating scenario dashboard: {e}")
            return {}
    
    def create_risk_dashboard(self, 
                            risk_metrics: Dict[str, Any],
                            contracts: List[CreditContract]) -> Dict[str, Any]:
        """
        Создание дашборда анализа рисков
        
        Args:
            risk_metrics: Метрики рисков
            contracts: Список договоров
            
        Returns:
            Данные дашборда
        """
        try:
            logger.info("Creating risk analysis dashboard")
            
            # Создание графиков
            risk_chart = self.chart_builder.create_risk_analysis_chart(
                risk_metrics, "Анализ рисков портфеля"
            )
            
            # Создание дашборда
            dashboard = {
                'title': 'Анализ рисков',
                'created_at': datetime.now().isoformat(),
                'charts': {
                    'risk_analysis': risk_chart
                },
                'risk_summary': self._create_risk_summary(risk_metrics),
                'recommendations': self._generate_risk_recommendations(risk_metrics)
            }
            
            logger.info("Risk dashboard created successfully")
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating risk dashboard: {e}")
            return {}
    
    def create_executive_dashboard(self, 
                                 portfolio_data: Dict[str, Any],
                                 key_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создание исполнительного дашборда
        
        Args:
            portfolio_data: Данные портфеля
            key_metrics: Ключевые метрики
            
        Returns:
            Данные дашборда
        """
        try:
            logger.info("Creating executive dashboard")
            
            # Создание дашборда
            dashboard = {
                'title': 'Исполнительный дашборд',
                'created_at': datetime.now().isoformat(),
                'executive_summary': self._create_executive_summary(portfolio_data, key_metrics),
                'kpi_cards': self._create_kpi_cards(key_metrics),
                'trend_analysis': self._create_trend_analysis(portfolio_data),
                'alerts': self._create_executive_alerts(key_metrics)
            }
            
            logger.info("Executive dashboard created successfully")
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating executive dashboard: {e}")
            return {}
    
    def _create_portfolio_summary(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Создание сводки портфеля"""
        return {
            'total_contracts': metrics.get('total_contracts', 0),
            'total_limit': metrics.get('total_limit', 0),
            'total_utilized': metrics.get('total_utilized', 0),
            'utilization_ratio': metrics.get('utilization_ratio', 0),
            'weighted_rate': metrics.get('weighted_average_rate', 0)
        }
    
    def _create_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Создание предупреждений"""
        alerts = []
        
        # Проверка использования лимитов
        utilization = metrics.get('utilization_ratio', 0)
        if utilization > 0.8:
            alerts.append({
                'type': 'warning',
                'message': 'Высокий уровень использования лимитов',
                'severity': 'high'
            })
        elif utilization > 0.6:
            alerts.append({
                'type': 'info',
                'message': 'Умеренный уровень использования лимитов',
                'severity': 'medium'
            })
        
        # Проверка концентрации риска
        concentration = metrics.get('concentration_metrics', {})
        hhi = concentration.get('hhi', 0)
        if hhi > 0.25:
            alerts.append({
                'type': 'danger',
                'message': 'Высокая концентрация риска в портфеле',
                'severity': 'high'
            })
        
        return alerts
    
    def _calculate_scenario_impact(self, 
                                 base_cashflow: PortfolioCashflow,
                                 scenario_cashflow: PortfolioCashflow) -> Dict[str, Any]:
        """Расчет влияния сценария"""
        try:
            # Простой расчет влияния
            base_total = sum(item.net_cashflow for item in base_cashflow.cashflow_items)
            scenario_total = sum(item.net_cashflow for item in scenario_cashflow.cashflow_items)
            
            impact = scenario_total - base_total
            impact_percentage = (impact / base_total * 100) if base_total != 0 else 0
            
            return {
                'net_cashflow_impact': float(impact),
                'impact_percentage': float(impact_percentage),
                'scenario_effectiveness': 'positive' if impact > 0 else 'negative'
            }
            
        except Exception as e:
            logger.error(f"Error calculating scenario impact: {e}")
            return {}
    
    def _generate_recommendations(self, impact_analysis: Dict[str, Any]) -> List[str]:
        """Генерация рекомендаций"""
        recommendations = []
        
        impact = impact_analysis.get('net_cashflow_impact', 0)
        if impact > 0:
            recommendations.append("Сценарий показывает положительное влияние на денежные потоки")
        else:
            recommendations.append("Сценарий может негативно повлиять на денежные потоки")
        
        return recommendations
    
    def _create_risk_summary(self, risk_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Создание сводки рисков"""
        return {
            'concentration_risk': risk_metrics.get('concentration_risk', {}),
            'maturity_distribution': risk_metrics.get('maturity_distribution', {}),
            'utilization_distribution': risk_metrics.get('utilization_distribution', {}),
            'overall_risk_level': self._assess_overall_risk(risk_metrics)
        }
    
    def _assess_overall_risk(self, risk_metrics: Dict[str, Any]) -> str:
        """Оценка общего уровня риска"""
        concentration = risk_metrics.get('concentration_risk', {})
        hhi = concentration.get('hhi', 0)
        
        if hhi > 0.25:
            return 'high'
        elif hhi > 0.15:
            return 'medium'
        else:
            return 'low'
    
    def _generate_risk_recommendations(self, risk_metrics: Dict[str, Any]) -> List[str]:
        """Генерация рекомендаций по рискам"""
        recommendations = []
        
        concentration = risk_metrics.get('concentration_risk', {})
        hhi = concentration.get('hhi', 0)
        
        if hhi > 0.25:
            recommendations.append("Рекомендуется диверсификация портфеля для снижения концентрации риска")
        
        utilization = risk_metrics.get('utilization_distribution', {})
        high_utilization = utilization.get('high', 0)
        if high_utilization > 5:
            recommendations.append("Высокое количество договоров с полным использованием лимитов")
        
        return recommendations
    
    def _create_executive_summary(self, 
                                portfolio_data: Dict[str, Any],
                                key_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Создание исполнительной сводки"""
        return {
            'portfolio_size': portfolio_data.get('portfolio_summary', {}).get('total_limit', 0),
            'utilization_rate': key_metrics.get('utilization_ratio', 0),
            'risk_level': self._assess_overall_risk(portfolio_data.get('risk_analysis', {})),
            'key_insights': portfolio_data.get('key_insights', [])
        }
    
    def _create_kpi_cards(self, key_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Создание карточек KPI"""
        return [
            {
                'title': 'Общий лимит',
                'value': key_metrics.get('total_limit', 0),
                'format': 'currency',
                'trend': 'stable'
            },
            {
                'title': 'Использование',
                'value': key_metrics.get('utilization_ratio', 0),
                'format': 'percentage',
                'trend': 'increasing'
            },
            {
                'title': 'Средневзвешенная ставка',
                'value': key_metrics.get('weighted_average_rate', 0),
                'format': 'percentage',
                'trend': 'stable'
            }
        ]
    
    def _create_trend_analysis(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание анализа трендов"""
        return {
            'utilization_trend': 'increasing',
            'risk_trend': 'stable',
            'performance_trend': 'positive'
        }
    
    def _create_executive_alerts(self, key_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Создание исполнительных предупреждений"""
        alerts = []
        
        utilization = key_metrics.get('utilization_ratio', 0)
        if utilization > 0.8:
            alerts.append({
                'type': 'critical',
                'message': 'Критический уровень использования лимитов',
                'action_required': True
            })
        
        return alerts

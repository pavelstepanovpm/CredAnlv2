"""
Построитель графиков для визуализации данных портфеля
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
import logging

import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from models import PortfolioCashflow, PaymentSchedule, CreditContract

logger = logging.getLogger(__name__)


class ChartBuilder:
    """Построитель графиков"""
    
    def __init__(self, theme: str = 'dark'):
        """
        Инициализация построителя
        
        Args:
            theme: Тема оформления (dark/light)
        """
        self.theme = theme
        self.colors = {
            'primary': '#0066cc',
            'success': '#00ff00',
            'warning': '#ffaa00',
            'danger': '#ff0000',
            'info': '#00ffff',
            'secondary': '#666666'
        }
    
    def create_cashflow_chart(self, 
                             cashflow: PortfolioCashflow,
                             title: str = "Консолидированный кэш-флоу портфеля") -> go.Figure:
        """
        Создание графика кэш-флоу
        
        Args:
            cashflow: Кэш-флоу портфеля
            title: Заголовок графика
            
        Returns:
            График кэш-флоу
        """
        try:
            if not cashflow.cashflow_items:
                return self._create_empty_chart("Нет данных для отображения")
            
            # Подготовка данных
            dates = [item.cashflow_date for item in cashflow.cashflow_items]
            drawdowns = [float(item.total_drawdowns) for item in cashflow.cashflow_items]
            principal_payments = [float(item.total_principal_payments) for item in cashflow.cashflow_items]
            interest_payments = [float(item.total_interest_payments) for item in cashflow.cashflow_items]
            net_cashflow = [float(item.net_cashflow) for item in cashflow.cashflow_items]
            
            # Создание графика
            fig = go.Figure()
            
            # Добавление линий
            fig.add_trace(go.Scatter(
                x=dates,
                y=drawdowns,
                mode='lines+markers',
                name='Выборки',
                line=dict(color=self.colors['success'], width=3),
                marker=dict(size=6)
            ))
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=principal_payments,
                mode='lines+markers',
                name='Погашения основного долга',
                line=dict(color=self.colors['danger'], width=3),
                marker=dict(size=6)
            ))
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=interest_payments,
                mode='lines+markers',
                name='Процентные платежи',
                line=dict(color=self.colors['warning'], width=3),
                marker=dict(size=6)
            ))
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=net_cashflow,
                mode='lines+markers',
                name='Чистый денежный поток',
                line=dict(color=self.colors['primary'], width=4),
                marker=dict(size=8)
            ))
            
            # Настройка макета
            fig.update_layout(
                title=title,
                xaxis_title='Дата',
                yaxis_title='Сумма (руб.)',
                hovermode='x unified',
                template=self._get_template(),
                plot_bgcolor=self._get_bg_color(),
                paper_bgcolor=self._get_bg_color(),
                font=dict(color=self._get_text_color()),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            # Форматирование оси Y
            fig.update_yaxis(tickformat=',.0f')
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating cashflow chart: {e}")
            return self._create_empty_chart("Ошибка создания графика")
    
    def create_utilization_chart(self, 
                                contracts: List[CreditContract],
                                title: str = "Использование лимитов по договорам") -> go.Figure:
        """
        Создание графика использования лимитов
        
        Args:
            contracts: Список договоров
            title: Заголовок графика
            
        Returns:
            График использования лимитов
        """
        try:
            if not contracts:
                return self._create_empty_chart("Нет данных о договорах")
            
            # Подготовка данных
            contract_ids = [contract.id for contract in contracts]
            limits = [float(contract.total_limit) for contract in contracts]
            utilized = [float(contract.get_utilized_amount()) for contract in contracts]
            available = [float(contract.available_limit) for contract in contracts]
            
            # Создание графика
            fig = go.Figure()
            
            # Добавление столбцов
            fig.add_trace(go.Bar(
                name='Общий лимит',
                x=contract_ids,
                y=limits,
                marker_color=self.colors['secondary'],
                opacity=0.7
            ))
            
            fig.add_trace(go.Bar(
                name='Использовано',
                x=contract_ids,
                y=utilized,
                marker_color=self.colors['success']
            ))
            
            fig.add_trace(go.Bar(
                name='Доступно',
                x=contract_ids,
                y=available,
                marker_color=self.colors['info']
            ))
            
            # Настройка макета
            fig.update_layout(
                title=title,
                xaxis_title='Договоры',
                yaxis_title='Сумма (руб.)',
                template=self._get_template(),
                plot_bgcolor=self._get_bg_color(),
                paper_bgcolor=self._get_bg_color(),
                font=dict(color=self._get_text_color()),
                barmode='group'
            )
            
            # Форматирование оси Y
            fig.update_yaxis(tickformat=',.0f')
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating utilization chart: {e}")
            return self._create_empty_chart("Ошибка создания графика")
    
    def create_portfolio_metrics_chart(self, 
                                     metrics: Dict[str, Any],
                                     title: str = "Ключевые метрики портфеля") -> go.Figure:
        """
        Создание графика ключевых метрик
        
        Args:
            metrics: Метрики портфеля
            title: Заголовок графика
            
        Returns:
            График метрик
        """
        try:
            # Подготовка данных для радиальной диаграммы
            categories = ['Использование лимитов', 'Концентрация риска', 'Средневзвешенная ставка']
            values = [
                metrics.get('utilization_ratio', 0) * 100,
                metrics.get('concentration_metrics', {}).get('hhi', 0) * 100,
                metrics.get('weighted_average_rate', 0) * 100
            ]
            
            # Создание радиальной диаграммы
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Метрики',
                line_color=self.colors['primary']
            ))
            
            # Настройка макета
            fig.update_layout(
                title=title,
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                template=self._get_template(),
                plot_bgcolor=self._get_bg_color(),
                paper_bgcolor=self._get_bg_color(),
                font=dict(color=self._get_text_color())
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating metrics chart: {e}")
            return self._create_empty_chart("Ошибка создания графика")
    
    def create_scenario_comparison_chart(self, 
                                       base_cashflow: PortfolioCashflow,
                                       scenario_cashflow: PortfolioCashflow,
                                       title: str = "Сравнение сценариев") -> go.Figure:
        """
        Создание графика сравнения сценариев
        
        Args:
            base_cashflow: Базовый кэш-флоу
            scenario_cashflow: Сценарный кэш-флоу
            title: Заголовок графика
            
        Returns:
            График сравнения
        """
        try:
            # Подготовка данных
            base_dates = [item.cashflow_date for item in base_cashflow.cashflow_items]
            base_net = [float(item.net_cashflow) for item in base_cashflow.cashflow_items]
            
            scenario_dates = [item.cashflow_date for item in scenario_cashflow.cashflow_items]
            scenario_net = [float(item.net_cashflow) for item in scenario_cashflow.cashflow_items]
            
            # Создание графика
            fig = go.Figure()
            
            # Базовый сценарий
            fig.add_trace(go.Scatter(
                x=base_dates,
                y=base_net,
                mode='lines+markers',
                name='Базовый сценарий',
                line=dict(color=self.colors['secondary'], width=3),
                marker=dict(size=6)
            ))
            
            # Сценарный сценарий
            fig.add_trace(go.Scatter(
                x=scenario_dates,
                y=scenario_net,
                mode='lines+markers',
                name='Сценарный сценарий',
                line=dict(color=self.colors['primary'], width=3),
                marker=dict(size=6)
            ))
            
            # Настройка макета
            fig.update_layout(
                title=title,
                xaxis_title='Дата',
                yaxis_title='Чистый денежный поток (руб.)',
                hovermode='x unified',
                template=self._get_template(),
                plot_bgcolor=self._get_bg_color(),
                paper_bgcolor=self._get_bg_color(),
                font=dict(color=self._get_text_color())
            )
            
            # Форматирование оси Y
            fig.update_yaxis(tickformat=',.0f')
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating comparison chart: {e}")
            return self._create_empty_chart("Ошибка создания графика")
    
    def create_risk_analysis_chart(self, 
                                  risk_metrics: Dict[str, Any],
                                  title: str = "Анализ рисков портфеля") -> go.Figure:
        """
        Создание графика анализа рисков
        
        Args:
            risk_metrics: Метрики рисков
            title: Заголовок графика
            
        Returns:
            График анализа рисков
        """
        try:
            # Подготовка данных
            categories = ['Концентрация', 'Сроки погашения', 'Использование лимитов', 'Валютный риск']
            values = [
                risk_metrics.get('concentration_risk', {}).get('hhi', 0) * 100,
                75,  # Примерное значение для сроков
                risk_metrics.get('utilization_distribution', {}).get('high', 0) * 10,
                30   # Примерное значение для валютного риска
            ]
            
            # Создание столбчатой диаграммы
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=categories,
                y=values,
                marker_color=[self.colors['danger'] if v > 70 else 
                             self.colors['warning'] if v > 40 else 
                             self.colors['success'] for v in values]
            ))
            
            # Настройка макета
            fig.update_layout(
                title=title,
                xaxis_title='Типы рисков',
                yaxis_title='Уровень риска (%)',
                template=self._get_template(),
                plot_bgcolor=self._get_bg_color(),
                paper_bgcolor=self._get_bg_color(),
                font=dict(color=self._get_text_color())
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating risk analysis chart: {e}")
            return self._create_empty_chart("Ошибка создания графика")
    
    def create_heatmap_chart(self, 
                           data: pd.DataFrame,
                           title: str = "Тепловая карта портфеля") -> go.Figure:
        """
        Создание тепловой карты
        
        Args:
            data: Данные для тепловой карты
            title: Заголовок графика
            
        Returns:
            Тепловая карта
        """
        try:
            fig = go.Figure(data=go.Heatmap(
                z=data.values,
                x=data.columns,
                y=data.index,
                colorscale='RdYlBu_r',
                showscale=True
            ))
            
            fig.update_layout(
                title=title,
                template=self._get_template(),
                plot_bgcolor=self._get_bg_color(),
                paper_bgcolor=self._get_bg_color(),
                font=dict(color=self._get_text_color())
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating heatmap chart: {e}")
            return self._create_empty_chart("Ошибка создания графика")
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Создание пустого графика с сообщением"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=self._get_text_color())
        )
        fig.update_layout(
            template=self._get_template(),
            plot_bgcolor=self._get_bg_color(),
            paper_bgcolor=self._get_bg_color(),
            font=dict(color=self._get_text_color())
        )
        return fig
    
    def _get_template(self) -> str:
        """Получение шаблона оформления"""
        return 'plotly_dark' if self.theme == 'dark' else 'plotly_white'
    
    def _get_bg_color(self) -> str:
        """Получение цвета фона"""
        return '#1e1e1e' if self.theme == 'dark' else '#ffffff'
    
    def _get_text_color(self) -> str:
        """Получение цвета текста"""
        return '#ffffff' if self.theme == 'dark' else '#000000'

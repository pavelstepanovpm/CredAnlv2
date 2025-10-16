import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchPortfolioCashflow } from '../store/slices/portfolioSlice';

export const CashflowChart: React.FC = () => {
  const dispatch = useAppDispatch();
  const { cashflow, loading, error } = useAppSelector((state: any) => state.portfolio);
  const { activeVersion } = useAppSelector((state: any) => state.versions);
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    if (activeVersion) {
      dispatch(fetchPortfolioCashflow(activeVersion));
    }
  }, [dispatch, activeVersion]);

  useEffect(() => {
    if (cashflow?.cashflow_items) {
      const data = cashflow.cashflow_items.map((item: any) => ({
        date: new Date(item.cashflow_date).toLocaleDateString('ru-RU'),
        drawdowns: item.total_drawdowns,
        principalPayments: item.total_principal_payments,
        interestPayments: item.total_interest_payments,
        netCashflow: item.total_drawdowns - item.total_principal_payments - item.total_interest_payments,
      }));
      setChartData(data);
    }
  }, [cashflow]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={400}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        {error}
      </Alert>
    );
  }

  if (!chartData.length) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={400}>
        <Typography color="text.secondary">
          Нет данных для отображения
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', height: 400 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
          <XAxis 
            dataKey="date" 
            stroke="#cccccc"
            fontSize={12}
          />
          <YAxis 
            stroke="#cccccc"
            fontSize={12}
            tickFormatter={(value) => new Intl.NumberFormat('ru-RU', {
              notation: 'compact',
              compactDisplay: 'short'
            }).format(value)}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#2d2d2d',
              border: '1px solid #555',
              borderRadius: '8px',
              color: '#ffffff',
            }}
            formatter={(value: any, name: string) => [
              new Intl.NumberFormat('ru-RU', {
                style: 'currency',
                currency: 'RUB',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0,
              }).format(value),
              name
            ]}
            labelFormatter={(label) => `Дата: ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="drawdowns"
            stroke="#00ff00"
            strokeWidth={3}
            name="Выборки"
            dot={{ fill: '#00ff00', strokeWidth: 2, r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="principalPayments"
            stroke="#ff0000"
            strokeWidth={3}
            name="Погашения основного долга"
            dot={{ fill: '#ff0000', strokeWidth: 2, r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="interestPayments"
            stroke="#ffaa00"
            strokeWidth={3}
            name="Процентные платежи"
            dot={{ fill: '#ffaa00', strokeWidth: 2, r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="netCashflow"
            stroke="#0066cc"
            strokeWidth={4}
            name="Чистый денежный поток"
            dot={{ fill: '#0066cc', strokeWidth: 2, r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

import React from 'react';
import {
  Box,
  Typography,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { CreditContract } from '../types';

interface UtilizationChartProps {
  contracts: CreditContract[];
}

export const UtilizationChart: React.FC<UtilizationChartProps> = ({ contracts }) => {
  const chartData = contracts.map(contract => ({
    contractId: contract.id,
    totalLimit: contract.total_limit,
    utilized: contract.total_limit - contract.available_limit,
    available: contract.available_limit,
    utilizationRate: ((contract.total_limit - contract.available_limit) / contract.total_limit) * 100,
  }));

  if (!chartData.length) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={400}>
        <Typography color="text.secondary">
          Нет данных о договорах
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', height: 400 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
          <XAxis 
            dataKey="contractId" 
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
            labelFormatter={(label) => `Договор: ${label}`}
          />
          <Legend />
          <Bar
            dataKey="totalLimit"
            stackId="a"
            fill="#666666"
            name="Общий лимит"
            radius={[0, 0, 0, 0]}
          />
          <Bar
            dataKey="utilized"
            stackId="a"
            fill="#00ff00"
            name="Использовано"
            radius={[0, 0, 0, 0]}
          />
          <Bar
            dataKey="available"
            stackId="a"
            fill="#00ffff"
            name="Доступно"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
};


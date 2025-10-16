import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  useTheme,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  TrendingFlat as TrendingFlatIcon,
} from '@mui/icons-material';
import { MetricCard as MetricCardType } from '../types';

interface MetricCardProps extends MetricCardType {
  loading?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  format,
  trend,
  color = 'primary',
  loading = false,
}) => {
  const theme = useTheme();

  const formatValue = (val: number | string, formatType: string) => {
    if (typeof val === 'string') return val;
    
    switch (formatType) {
      case 'currency':
        return new Intl.NumberFormat('ru-RU', {
          style: 'currency',
          currency: 'RUB',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        }).format(val);
      case 'percentage':
        return `${(val * 100).toFixed(1)}%`;
      case 'number':
        return new Intl.NumberFormat('ru-RU').format(val);
      default:
        return val.toString();
    }
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'increasing':
        return <TrendingUpIcon sx={{ fontSize: 16, color: '#00ff00' }} />;
      case 'decreasing':
        return <TrendingDownIcon sx={{ fontSize: 16, color: '#ff0000' }} />;
      case 'stable':
        return <TrendingFlatIcon sx={{ fontSize: 16, color: '#cccccc' }} />;
      default:
        return null;
    }
  };

  const getColorValue = () => {
    switch (color) {
      case 'primary':
        return '#0066cc';
      case 'success':
        return '#00ff00';
      case 'warning':
        return '#ffaa00';
      case 'error':
        return '#ff0000';
      case 'info':
        return '#00ffff';
      default:
        return '#0066cc';
    }
  };

  return (
    <Card
      sx={{
        backgroundColor: '#2d2d2d',
        border: '1px solid #555',
        borderRadius: 2,
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4)',
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography
            variant="body2"
            sx={{
              color: '#cccccc',
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
              fontWeight: 600,
            }}
          >
            {title}
          </Typography>
          {trend && (
            <Chip
              icon={getTrendIcon() as React.ReactElement}
              label={trend === 'increasing' ? 'Рост' : trend === 'decreasing' ? 'Спад' : 'Стабильно'}
              size="small"
              sx={{
                backgroundColor: trend === 'increasing' ? '#00ff0020' : 
                               trend === 'decreasing' ? '#ff000020' : '#cccccc20',
                color: trend === 'increasing' ? '#00ff00' : 
                       trend === 'decreasing' ? '#ff0000' : '#cccccc',
                border: '1px solid',
                borderColor: trend === 'increasing' ? '#00ff00' : 
                             trend === 'decreasing' ? '#ff0000' : '#cccccc',
              }}
            />
          )}
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography
            variant="h4"
            sx={{
              color: getColorValue(),
              fontWeight: 700,
              fontSize: '2rem',
            }}
          >
            {loading ? '...' : formatValue(value, format)}
          </Typography>
          
          {loading && (
            <Box
              sx={{
                width: 20,
                height: 20,
                border: '2px solid #404040',
                borderTop: '2px solid #0066cc',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
              }}
            />
          )}
        </Box>
      </CardContent>
    </Card>
  );
};


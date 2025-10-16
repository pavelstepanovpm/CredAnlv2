import React from 'react';
import {
  Box,
  Chip,
  Typography,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  TrendingFlat as TrendingFlatIcon,
} from '@mui/icons-material';

interface CovenantBadgeProps {
  level: 'excellent' | 'good' | 'fair' | 'poor' | 'critical';
  value: number;
  target?: number;
  trend?: 'up' | 'down' | 'stable';
}

export const CovenantBadge: React.FC<CovenantBadgeProps> = ({
  level,
  value,
  target,
  trend = 'stable',
}) => {
  const getLevelConfig = () => {
    switch (level) {
      case 'excellent':
        return {
          color: '#4caf50',
          label: 'Отличный',
          bgColor: '#e8f5e8',
          icon: <TrendingUpIcon />,
        };
      case 'good':
        return {
          color: '#8bc34a',
          label: 'Хороший',
          bgColor: '#f1f8e9',
          icon: <TrendingUpIcon />,
        };
      case 'fair':
        return {
          color: '#ff9800',
          label: 'Удовлетворительный',
          bgColor: '#fff3e0',
          icon: <TrendingFlatIcon />,
        };
      case 'poor':
        return {
          color: '#f44336',
          label: 'Плохой',
          bgColor: '#ffebee',
          icon: <TrendingDownIcon />,
        };
      case 'critical':
        return {
          color: '#d32f2f',
          label: 'Критический',
          bgColor: '#ffcdd2',
          icon: <TrendingDownIcon />,
        };
      default:
        return {
          color: '#757575',
          label: 'Неизвестно',
          bgColor: '#f5f5f5',
          icon: <TrendingFlatIcon />,
        };
    }
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUpIcon sx={{ fontSize: 16, color: '#4caf50' }} />;
      case 'down':
        return <TrendingDownIcon sx={{ fontSize: 16, color: '#f44336' }} />;
      default:
        return <TrendingFlatIcon sx={{ fontSize: 16, color: '#757575' }} />;
    }
  };

  const config = getLevelConfig();
  const progressValue = Math.min((value / (target || 100)) * 100, 100);

  return (
    <Card
      sx={{
        background: `linear-gradient(135deg, ${config.bgColor} 0%, #ffffff 100%)`,
        border: `2px solid ${config.color}`,
        borderRadius: 2,
        boxShadow: `0 4px 12px ${config.color}20`,
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: `0 8px 24px ${config.color}30`,
        },
      }}
    >
      <CardContent sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Box sx={{ mr: 1, color: config.color }}>
            {config.icon}
          </Box>
          <Typography
            variant="h6"
            sx={{
              color: config.color,
              fontWeight: 'bold',
              fontSize: '1.1rem',
            }}
          >
            Уровень ковинант
          </Typography>
        </Box>

        <Box sx={{ mb: 2 }}>
          <Chip
            label={config.label}
            sx={{
              backgroundColor: config.color,
              color: 'white',
              fontWeight: 'bold',
              fontSize: '0.9rem',
            }}
          />
        </Box>

        <Box sx={{ mb: 2 }}>
          <Typography variant="h4" sx={{ color: config.color, fontWeight: 'bold' }}>
            {value.toFixed(1)}%
          </Typography>
          {target && (
            <Typography variant="body2" color="text.secondary">
              Целевое значение: {target}%
            </Typography>
          )}
        </Box>

        <Box sx={{ mb: 1 }}>
          <LinearProgress
            variant="determinate"
            value={progressValue}
            sx={{
              height: 8,
              borderRadius: 4,
              backgroundColor: `${config.color}20`,
              '& .MuiLinearProgress-bar': {
                backgroundColor: config.color,
                borderRadius: 4,
              },
            }}
          />
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography variant="body2" color="text.secondary">
            Прогресс: {progressValue.toFixed(1)}%
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {getTrendIcon()}
            <Typography
              variant="body2"
              sx={{
                ml: 0.5,
                color: trend === 'up' ? '#4caf50' : trend === 'down' ? '#f44336' : '#757575',
                fontWeight: 'bold',
              }}
            >
              {trend === 'up' ? '↗' : trend === 'down' ? '↘' : '→'}
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

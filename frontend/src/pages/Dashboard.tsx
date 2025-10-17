import React, { useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Chip,
  Paper,
} from '@mui/material';
import { CheckCircle, Update, Rocket } from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchPortfolioData, fetchPortfolioMetrics } from '../store/slices/portfolioSlice';
import { fetchVersions } from '../store/slices/versionsSlice';
import { MetricCard } from '../components/MetricCard';
import { CashflowChart } from '../components/CashflowChart';
import { UtilizationChart } from '../components/UtilizationChart';
import { VersionsPanel } from '../components/VersionsPanel';
import { CovenantBadge } from '../components/CovenantBadge';

export const Dashboard: React.FC = () => {
  const dispatch = useAppDispatch();
  const { contracts, metrics, loading, error, lastUpdated } = useAppSelector(
    (state) => state.portfolio
  );
  const { versions, activeVersion } = useAppSelector((state) => state.versions);

  useEffect(() => {
    dispatch(fetchPortfolioData());
    dispatch(fetchVersions());
  }, [dispatch]);

  useEffect(() => {
    if (activeVersion) {
      dispatch(fetchPortfolioMetrics(activeVersion));
    }
  }, [dispatch, activeVersion]);

  if (loading && !lastUpdated) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  const metricCards = [
    {
      title: 'Договоров',
      value: contracts.length,
      format: 'number' as const,
      color: 'primary' as const,
    },
    {
      title: 'Общий лимит',
      value: contracts.reduce((sum, contract) => sum + contract.total_limit, 0),
      format: 'currency' as const,
      color: 'info' as const,
    },
    {
      title: 'Использовано',
      value: contracts.reduce((sum, contract) => sum + (contract.total_limit - contract.available_limit), 0),
      format: 'currency' as const,
      color: 'warning' as const,
    },
    {
      title: 'Использование',
      value: metrics?.utilization_ratio || 0,
      format: 'percentage' as const,
      color: 'success' as const,
    },
  ];

  return (
    <Box>
      {/* Page Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, color: '#ffffff', mb: 1 }}>
          Дашборд портфеля
        </Typography>
        <Typography variant="body1" sx={{ color: '#cccccc' }}>
          Обзор ключевых метрик и показателей кредитного портфеля
        </Typography>
      </Box>

      {/* System Status Banner */}
      <Paper 
        elevation={3} 
        sx={{ 
          mb: 4, 
          p: 3, 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          border: '1px solid #555',
          borderRadius: 2
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Rocket sx={{ color: '#ffffff', fontSize: 28 }} />
            <Box>
              <Typography variant="h6" sx={{ color: '#ffffff', fontWeight: 600 }}>
                🚀 Система обновлена через CI/CD
              </Typography>
              <Typography variant="body2" sx={{ color: '#e0e0e0' }}>
                Автоматическое развертывание работает отлично!
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip 
              icon={<CheckCircle />} 
              label="v1.0.0" 
              sx={{ 
                backgroundColor: '#4caf50', 
                color: '#ffffff',
                '& .MuiChip-icon': { color: '#ffffff' }
              }} 
            />
            <Chip 
              icon={<Update />} 
              label={`Обновлено: ${new Date().toLocaleString('ru-RU')}`}
              sx={{ 
                backgroundColor: '#2196f3', 
                color: '#ffffff',
                '& .MuiChip-icon': { color: '#ffffff' }
              }} 
            />
            <Chip 
              label="Production Ready" 
              sx={{ 
                backgroundColor: '#ff9800', 
                color: '#ffffff'
              }} 
            />
          </Box>
        </Box>
      </Paper>

      {/* Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metricCards.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <MetricCard {...metric} />
          </Grid>
        ))}
      </Grid>

      {/* Covenant Badge */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <CovenantBadge
            level="good"
            value={78.5}
            target={80}
            trend="up"
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <CovenantBadge
            level="excellent"
            value={92.3}
            target={90}
            trend="stable"
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <CovenantBadge
            level="fair"
            value={65.2}
            target={70}
            trend="down"
          />
        </Grid>
      </Grid>

      {/* Charts Row */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Cashflow Chart */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#ffffff', mb: 2 }}>
                Консолидированный кэш-флоу
              </Typography>
              <CashflowChart />
            </CardContent>
          </Card>
        </Grid>

        {/* Versions Panel */}
        <Grid item xs={12} lg={4}>
          <VersionsPanel />
        </Grid>
      </Grid>

      {/* Utilization Chart */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#ffffff', mb: 2 }}>
                Использование лимитов по договорам
              </Typography>
              <UtilizationChart contracts={contracts} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

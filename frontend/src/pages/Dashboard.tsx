import React, { useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchPortfolioData, fetchPortfolioMetrics } from '../store/slices/portfolioSlice';
import { fetchVersions } from '../store/slices/versionsSlice';
import { MetricCard } from '../components/MetricCard';
import { CashflowChart } from '../components/CashflowChart';
import { UtilizationChart } from '../components/UtilizationChart';
import { VersionsPanel } from '../components/VersionsPanel';

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

      {/* Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metricCards.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <MetricCard {...metric} />
          </Grid>
        ))}
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

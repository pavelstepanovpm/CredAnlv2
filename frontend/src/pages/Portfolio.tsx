import React, { useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  TextField,
  InputAdornment,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Search as SearchIcon,
  Visibility as VisibilityIcon,
  Edit as EditIcon,
  MoreVert as MoreVertIcon,
} from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchPortfolioData } from '../store/slices/portfolioSlice';
import { CreditContract } from '../types';

export const Portfolio: React.FC = () => {
  const dispatch = useAppDispatch();
  const { contracts, loading, error } = useAppSelector((state: any) => state.portfolio);
  const [searchTerm, setSearchTerm] = React.useState('');
  const [typeFilter, setTypeFilter] = React.useState('all');
  const [currencyFilter, setCurrencyFilter] = React.useState('all');

  useEffect(() => {
    dispatch(fetchPortfolioData());
  }, [dispatch]);

  const filteredContracts = contracts.filter((contract: any) => {
    const matchesSearch = contract.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         contract.credit_type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === 'all' || contract.credit_type === typeFilter;
    const matchesCurrency = currencyFilter === 'all' || contract.currency === currencyFilter;
    
    return matchesSearch && matchesType && matchesCurrency;
  });

  const getCreditTypeLabel = (type: string) => {
    switch (type) {
      case 'credit_line':
        return 'Кредитная линия';
      case 'one_time_loan':
        return 'Разовый кредит';
      case 'overdraft':
        return 'Овердрафт';
      case 'revolving':
        return 'Возобновляемый';
      default:
        return type;
    }
  };

  const getCreditTypeColor = (type: string) => {
    switch (type) {
      case 'credit_line':
        return 'primary';
      case 'one_time_loan':
        return 'success';
      case 'overdraft':
        return 'warning';
      case 'revolving':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusColor = (contract: CreditContract) => {
    const utilizationRate = (contract.total_limit - contract.available_limit) / contract.total_limit;
    if (utilizationRate >= 0.9) return 'error';
    if (utilizationRate >= 0.7) return 'warning';
    return 'success';
  };

  const getStatusLabel = (contract: CreditContract) => {
    const utilizationRate = (contract.total_limit - contract.available_limit) / contract.total_limit;
    if (utilizationRate >= 0.9) return 'Критическое использование';
    if (utilizationRate >= 0.7) return 'Высокое использование';
    return 'Нормальное использование';
  };

  if (loading) {
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

  return (
    <Box>
      {/* Page Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, color: '#ffffff', mb: 1 }}>
          Управление портфелем
        </Typography>
        <Typography variant="body1" sx={{ color: '#cccccc' }}>
          Детальная информация по кредитным договорам
        </Typography>
      </Box>

      {/* Filters */}
      <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555', mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                placeholder="Поиск по договорам..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon sx={{ color: '#cccccc' }} />
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: '#404040',
                    '& fieldset': {
                      borderColor: '#555',
                    },
                    '&:hover fieldset': {
                      borderColor: '#777',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#0066cc',
                    },
                  },
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel sx={{ color: '#cccccc' }}>Тип кредита</InputLabel>
                <Select
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                  sx={{
                    backgroundColor: '#404040',
                    color: '#ffffff',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#555',
                    },
                    '&:hover .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#777',
                    },
                    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#0066cc',
                    },
                  }}
                >
                  <MenuItem value="all">Все типы</MenuItem>
                  <MenuItem value="credit_line">Кредитные линии</MenuItem>
                  <MenuItem value="one_time_loan">Разовые кредиты</MenuItem>
                  <MenuItem value="overdraft">Овердрафты</MenuItem>
                  <MenuItem value="revolving">Возобновляемые</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel sx={{ color: '#cccccc' }}>Валюта</InputLabel>
                <Select
                  value={currencyFilter}
                  onChange={(e) => setCurrencyFilter(e.target.value)}
                  sx={{
                    backgroundColor: '#404040',
                    color: '#ffffff',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#555',
                    },
                    '&:hover .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#777',
                    },
                    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#0066cc',
                    },
                  }}
                >
                  <MenuItem value="all">Все валюты</MenuItem>
                  <MenuItem value="RUB">RUB</MenuItem>
                  <MenuItem value="USD">USD</MenuItem>
                  <MenuItem value="EUR">EUR</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <Typography variant="body2" sx={{ color: '#cccccc' }}>
                Найдено: {filteredContracts.length} из {contracts.length}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Contracts Table */}
      <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
        <CardContent sx={{ p: 0 }}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#404040' }}>
                  <TableCell sx={{ color: '#ffffff', fontWeight: 600 }}>Договор</TableCell>
                  <TableCell sx={{ color: '#ffffff', fontWeight: 600 }}>Тип</TableCell>
                  <TableCell sx={{ color: '#ffffff', fontWeight: 600 }}>Лимит</TableCell>
                  <TableCell sx={{ color: '#ffffff', fontWeight: 600 }}>Использовано</TableCell>
                  <TableCell sx={{ color: '#ffffff', fontWeight: 600 }}>Статус</TableCell>
                  <TableCell sx={{ color: '#ffffff', fontWeight: 600 }}>Действия</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredContracts.map((contract: any) => {
                  const utilized = contract.total_limit - contract.available_limit;
                  const utilizationRate = utilized / contract.total_limit;
                  
                  return (
                    <TableRow
                      key={contract.id}
                      sx={{
                        '&:hover': {
                          backgroundColor: '#404040',
                        },
                      }}
                    >
                      <TableCell sx={{ color: '#ffffff' }}>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          {contract.id}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#cccccc' }}>
                          {contract.currency}
                        </Typography>
                      </TableCell>
                      <TableCell sx={{ color: '#ffffff' }}>
                        <Chip
                          label={getCreditTypeLabel(contract.credit_type)}
                          color={getCreditTypeColor(contract.credit_type) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell sx={{ color: '#ffffff' }}>
                        {new Intl.NumberFormat('ru-RU', {
                          style: 'currency',
                          currency: 'RUB',
                          minimumFractionDigits: 0,
                          maximumFractionDigits: 0,
                        }).format(contract.total_limit)}
                      </TableCell>
                      <TableCell sx={{ color: '#ffffff' }}>
                        <Box>
                          <Typography variant="body2">
                            {new Intl.NumberFormat('ru-RU', {
                              style: 'currency',
                              currency: 'RUB',
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            }).format(utilized)}
                          </Typography>
                          <Typography variant="caption" sx={{ color: '#cccccc' }}>
                            {(utilizationRate * 100).toFixed(1)}%
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell sx={{ color: '#ffffff' }}>
                        <Chip
                          label={getStatusLabel(contract)}
                          color={getStatusColor(contract) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell sx={{ color: '#ffffff' }}>
                        <Box sx={{ display: 'flex', gap: 0.5 }}>
                          <IconButton
                            size="small"
                            sx={{ color: '#0066cc' }}
                          >
                            <VisibilityIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            sx={{ color: '#ffaa00' }}
                          >
                            <EditIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            sx={{ color: '#cccccc' }}
                          >
                            <MoreVertIcon />
                          </IconButton>
                        </Box>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

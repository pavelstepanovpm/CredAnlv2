import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
} from '@mui/material';
import {
  Download as DownloadIcon,
  PictureAsPdf as PdfIcon,
  TableChart as ExcelIcon,
  Assessment as ReportIcon,
  Refresh as RefreshIcon,
  Share as ShareIcon,
} from '@mui/icons-material';

export const Reports: React.FC = () => {
  const [generateDialogOpen, setGenerateDialogOpen] = useState(false);
  const [selectedReportType, setSelectedReportType] = useState('');
  const [reportParameters, setReportParameters] = useState({});

  const reportTypes = [
    {
      id: 'portfolio',
      name: 'Отчет по портфелю',
      description: 'Детальный анализ текущего состояния портфеля',
      icon: <ReportIcon />,
      formats: ['pdf', 'excel'],
    },
    {
      id: 'scenario_comparison',
      name: 'Сравнение сценариев',
      description: 'Анализ влияния различных сценариев на портфель',
      icon: <ReportIcon />,
      formats: ['pdf', 'excel'],
    },
    {
      id: 'stress_test',
      name: 'Стресс-тестирование',
      description: 'Анализ устойчивости портфеля к стрессам',
      icon: <ReportIcon />,
      formats: ['pdf', 'excel'],
    },
    {
      id: 'risk_analysis',
      name: 'Анализ рисков',
      description: 'Оценка рисков и концентрации портфеля',
      icon: <ReportIcon />,
      formats: ['pdf', 'excel'],
    },
  ];

  const recentReports = [
    {
      id: '1',
      name: 'Отчет по портфелю - Январь 2024',
      type: 'portfolio',
      created: '2024-01-15',
      status: 'completed',
      size: '2.3 MB',
    },
    {
      id: '2',
      name: 'Сравнение сценариев - Повышение ставок',
      type: 'scenario_comparison',
      created: '2024-01-14',
      status: 'completed',
      size: '1.8 MB',
    },
    {
      id: '3',
      name: 'Стресс-тест - Кризисный сценарий',
      type: 'stress_test',
      created: '2024-01-13',
      status: 'processing',
      size: '-',
    },
  ];

  const handleGenerateReport = (reportType: string) => {
    setSelectedReportType(reportType);
    setGenerateDialogOpen(true);
  };

  const handleDownloadReport = (reportId: string, format: string) => {
    // TODO: Implement download functionality
    console.log(`Downloading report ${reportId} in ${format} format`);
  };

  const handleShareReport = (reportId: string) => {
    // TODO: Implement share functionality
    console.log(`Sharing report ${reportId}`);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Готов';
      case 'processing':
        return 'Обработка';
      case 'failed':
        return 'Ошибка';
      default:
        return status;
    }
  };

  const getFormatIcon = (format: string) => {
    switch (format) {
      case 'pdf':
        return <PdfIcon />;
      case 'excel':
        return <ExcelIcon />;
      default:
        return <DownloadIcon />;
    }
  };

  return (
    <Box>
      {/* Page Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, color: '#ffffff', mb: 1 }}>
          Отчеты и аналитика
        </Typography>
        <Typography variant="body1" sx={{ color: '#cccccc' }}>
          Генерация и управление отчетами по портфелю
        </Typography>
      </Box>

      {/* Report Generation Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {reportTypes.map((reportType) => (
          <Grid item xs={12} sm={6} md={3} key={reportType.id}>
            <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555', height: '100%' }}>
              <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ color: '#0066cc', mr: 1 }}>
                    {reportType.icon}
                  </Box>
                  <Typography variant="h6" sx={{ color: '#ffffff', fontWeight: 600 }}>
                    {reportType.name}
                  </Typography>
                </Box>
                <Typography variant="body2" sx={{ color: '#cccccc', mb: 2, flexGrow: 1 }}>
                  {reportType.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                  {reportType.formats.map((format) => (
                    <Chip
                      key={format}
                      label={format.toUpperCase()}
                      size="small"
                      sx={{
                        backgroundColor: format === 'pdf' ? '#ff000020' : '#00ff0020',
                        color: format === 'pdf' ? '#ff0000' : '#00ff00',
                        border: '1px solid',
                        borderColor: format === 'pdf' ? '#ff0000' : '#00ff00',
                        fontSize: '10px',
                        height: 20,
                      }}
                    />
                  ))}
                </Box>
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => handleGenerateReport(reportType.id)}
                  sx={{
                    background: 'linear-gradient(135deg, #0066cc 0%, #004499 100%)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #0088ff 0%, #0066cc 100%)',
                    },
                  }}
                >
                  Сгенерировать
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Recent Reports */}
      <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" sx={{ color: '#ffffff' }}>
              Последние отчеты
            </Typography>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              sx={{
                borderColor: '#555',
                color: '#cccccc',
                '&:hover': {
                  borderColor: '#777',
                  backgroundColor: '#404040',
                },
              }}
            >
              Обновить
            </Button>
          </Box>
          <List>
            {recentReports.map((report, index) => (
              <React.Fragment key={report.id}>
                <ListItem
                  sx={{
                    backgroundColor: 'transparent',
                    borderRadius: 1,
                    '&:hover': {
                      backgroundColor: '#404040',
                    },
                  }}
                >
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="subtitle2" sx={{ color: '#ffffff', fontWeight: 600 }}>
                          {report.name}
                        </Typography>
                        <Chip
                          label={getStatusLabel(report.status)}
                          size="small"
                          color={getStatusColor(report.status) as any}
                          sx={{ fontSize: '10px', height: 20 }}
                        />
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" sx={{ color: '#cccccc' }}>
                          Создан: {new Date(report.created).toLocaleDateString('ru-RU')}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#999999' }}>
                          Размер: {report.size}
                        </Typography>
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <Box sx={{ display: 'flex', gap: 0.5 }}>
                      {report.status === 'completed' && (
                        <>
                          <IconButton
                            size="small"
                            onClick={() => handleDownloadReport(report.id, 'pdf')}
                            sx={{ color: '#ff0000' }}
                          >
                            <PdfIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDownloadReport(report.id, 'excel')}
                            sx={{ color: '#00ff00' }}
                          >
                            <ExcelIcon />
                          </IconButton>
                        </>
                      )}
                      <IconButton
                        size="small"
                        onClick={() => handleShareReport(report.id)}
                        sx={{ color: '#0066cc' }}
                      >
                        <ShareIcon />
                      </IconButton>
                    </Box>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < recentReports.length - 1 && <Divider sx={{ borderColor: '#555' }} />}
              </React.Fragment>
            ))}
          </List>
        </CardContent>
      </Card>

      {/* Generate Report Dialog */}
      <Dialog
        open={generateDialogOpen}
        onClose={() => setGenerateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
        PaperProps={{
          sx: {
            backgroundColor: '#2d2d2d',
            border: '1px solid #555',
          },
        }}
      >
        <DialogTitle sx={{ color: '#ffffff' }}>
          Генерация отчета
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <Typography variant="body1" sx={{ color: '#cccccc', mb: 2 }}>
              Выберите параметры для генерации отчета
            </Typography>
            <TextField
              fullWidth
              label="Название отчета"
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Период</InputLabel>
              <Select>
                <MenuItem value="current">Текущий период</MenuItem>
                <MenuItem value="last_month">Прошлый месяц</MenuItem>
                <MenuItem value="last_quarter">Прошлый квартал</MenuItem>
                <MenuItem value="last_year">Прошлый год</MenuItem>
                <MenuItem value="custom">Пользовательский</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Формат</InputLabel>
              <Select>
                <MenuItem value="pdf">PDF</MenuItem>
                <MenuItem value="excel">Excel</MenuItem>
                <MenuItem value="both">PDF + Excel</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => setGenerateDialogOpen(false)}
            sx={{ color: '#cccccc' }}
          >
            Отмена
          </Button>
          <Button
            variant="contained"
            sx={{
              background: 'linear-gradient(135deg, #0066cc 0%, #004499 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #0088ff 0%, #0066cc 100%)',
              },
            }}
          >
            Сгенерировать
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};


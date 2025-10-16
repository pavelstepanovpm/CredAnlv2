import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  IconButton,
  Divider,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  PlayArrow as PlayArrowIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Compare as CompareIcon,
} from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchVersions, createVersion, deleteVersion, setActiveVersion } from '../store/slices/versionsSlice';

export const Scenarios: React.FC = () => {
  const dispatch = useAppDispatch();
  const { versions, loading, error } = useAppSelector((state: any) => state.versions);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [scenarioForm, setScenarioForm] = useState({
    name: '',
    description: '',
    type: 'rate_change',
    base_version_id: '',
  });

  useEffect(() => {
    dispatch(fetchVersions());
  }, [dispatch]);

  const handleCreateScenario = () => {
    if (scenarioForm.name && scenarioForm.base_version_id) {
      const versionData = {
        name: scenarioForm.name,
        description: scenarioForm.description,
        version_type: 'scenario' as const,
        base_version_id: scenarioForm.base_version_id,
        scenario_parameters: {
          scenario_type: scenarioForm.type,
        },
        created_by: 'current_user', // TODO: Get from auth context
      };
      
      dispatch(createVersion(versionData));
      setCreateDialogOpen(false);
      setScenarioForm({
        name: '',
        description: '',
        type: 'rate_change',
        base_version_id: '',
      });
    }
  };

  const handleDeleteVersion = (versionId: string) => {
    if (window.confirm('Вы уверены, что хотите удалить эту версию?')) {
      dispatch(deleteVersion(versionId));
    }
  };

  const handleSetActive = (versionId: string) => {
    dispatch(setActiveVersion(versionId));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'draft':
        return 'secondary';
      case 'archived':
        return 'default';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active':
        return 'Активная';
      case 'draft':
        return 'Черновик';
      case 'archived':
        return 'Архивная';
      default:
        return status;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'base':
        return 'Базовая';
      case 'scenario':
        return 'Сценарная';
      default:
        return type;
    }
  };

  const getScenarioTypeLabel = (type: string) => {
    switch (type) {
      case 'rate_change':
        return 'Изменение ставок';
      case 'additional_drawdowns':
        return 'Дополнительные выборки';
      case 'early_repayments':
        return 'Досрочные погашения';
      case 'stress_test':
        return 'Стресс-тест';
      default:
        return type;
    }
  };

  const baseVersions = versions.filter((v: any) => v.version_type === 'base');
  const scenarioVersions = versions.filter((v: any) => v.version_type === 'scenario');

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
          Сценарное моделирование
        </Typography>
        <Typography variant="body1" sx={{ color: '#cccccc' }}>
          Создание и управление сценариями для анализа портфеля
        </Typography>
      </Box>

      {/* Create Scenario Button */}
      <Box sx={{ mb: 3 }}>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setCreateDialogOpen(true)}
          sx={{
            background: 'linear-gradient(135deg, #0066cc 0%, #004499 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #0088ff 0%, #0066cc 100%)',
            },
          }}
        >
          Создать сценарий
        </Button>
      </Box>

      {/* Versions List */}
      <Grid container spacing={3}>
        {/* Base Versions */}
        <Grid item xs={12} md={6}>
          <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#ffffff', mb: 2 }}>
                Базовые версии
              </Typography>
              <List>
                {baseVersions.map((version: any) => (
                  <ListItem
                    key={version.id}
                    sx={{
                      backgroundColor: version.status === 'active' ? '#0066cc20' : 'transparent',
                      borderRadius: 1,
                      mb: 1,
                      border: version.status === 'active' ? '1px solid #0066cc' : '1px solid transparent',
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="subtitle2" sx={{ color: '#ffffff', fontWeight: 600 }}>
                            {version.name}
                          </Typography>
                          <Chip
                            label={getStatusLabel(version.status)}
                            size="small"
                            color={getStatusColor(version.status) as any}
                            sx={{ fontSize: '10px', height: 20 }}
                          />
                        </Box>
                      }
                      secondary={
                        <Typography variant="body2" sx={{ color: '#cccccc' }}>
                          {version.description || 'Без описания'}
                        </Typography>
                      }
                    />
                    <ListItemSecondaryAction>
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        {version.status !== 'active' && (
                          <IconButton
                            size="small"
                            onClick={() => handleSetActive(version.id)}
                            sx={{ color: '#00ff00' }}
                          >
                            <PlayArrowIcon />
                          </IconButton>
                        )}
                        <IconButton size="small" sx={{ color: '#ffaa00' }}>
                          <EditIcon />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDeleteVersion(version.id)}
                          sx={{ color: '#ff0000' }}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Scenario Versions */}
        <Grid item xs={12} md={6}>
          <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#ffffff', mb: 2 }}>
                Сценарные версии
              </Typography>
              <List>
                {scenarioVersions.map((version: any) => (
                  <ListItem
                    key={version.id}
                    sx={{
                      backgroundColor: version.status === 'active' ? '#0066cc20' : 'transparent',
                      borderRadius: 1,
                      mb: 1,
                      border: version.status === 'active' ? '1px solid #0066cc' : '1px solid transparent',
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="subtitle2" sx={{ color: '#ffffff', fontWeight: 600 }}>
                            {version.name}
                          </Typography>
                          <Chip
                            label={getStatusLabel(version.status)}
                            size="small"
                            color={getStatusColor(version.status) as any}
                            sx={{ fontSize: '10px', height: 20 }}
                          />
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" sx={{ color: '#cccccc', mb: 0.5 }}>
                            {version.description || 'Без описания'}
                          </Typography>
                          <Chip
                            label={getScenarioTypeLabel(version.scenario_parameters?.scenario_type || '')}
                            size="small"
                            sx={{
                              backgroundColor: '#ffaa0020',
                              color: '#ffaa00',
                              border: '1px solid #ffaa00',
                              fontSize: '10px',
                              height: 20,
                            }}
                          />
                        </Box>
                      }
                    />
                    <ListItemSecondaryAction>
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        {version.status !== 'active' && (
                          <IconButton
                            size="small"
                            onClick={() => handleSetActive(version.id)}
                            sx={{ color: '#00ff00' }}
                          >
                            <PlayArrowIcon />
                          </IconButton>
                        )}
                        <IconButton size="small" sx={{ color: '#0066cc' }}>
                          <CompareIcon />
                        </IconButton>
                        <IconButton size="small" sx={{ color: '#ffaa00' }}>
                          <EditIcon />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDeleteVersion(version.id)}
                          sx={{ color: '#ff0000' }}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Create Scenario Dialog */}
      <Dialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
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
          Создать новый сценарий
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Название сценария"
              value={scenarioForm.name}
              onChange={(e) => setScenarioForm({ ...scenarioForm, name: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Описание"
              multiline
              rows={3}
              value={scenarioForm.description}
              onChange={(e) => setScenarioForm({ ...scenarioForm, description: e.target.value })}
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Тип сценария</InputLabel>
              <Select
                value={scenarioForm.type}
                onChange={(e) => setScenarioForm({ ...scenarioForm, type: e.target.value })}
              >
                <MenuItem value="rate_change">Изменение ставок</MenuItem>
                <MenuItem value="additional_drawdowns">Дополнительные выборки</MenuItem>
                <MenuItem value="early_repayments">Досрочные погашения</MenuItem>
                <MenuItem value="stress_test">Стресс-тест</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Базовая версия</InputLabel>
              <Select
                value={scenarioForm.base_version_id}
                onChange={(e) => setScenarioForm({ ...scenarioForm, base_version_id: e.target.value })}
              >
                {baseVersions.map((version: any) => (
                  <MenuItem key={version.id} value={version.id}>
                    {version.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => setCreateDialogOpen(false)}
            sx={{ color: '#cccccc' }}
          >
            Отмена
          </Button>
          <Button
            onClick={handleCreateScenario}
            variant="contained"
            sx={{
              background: 'linear-gradient(135deg, #0066cc 0%, #004499 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #0088ff 0%, #0066cc 100%)',
              },
            }}
          >
            Создать
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

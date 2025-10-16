import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Switch,
  FormControlLabel,
  TextField,
  Button,
  Grid,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  Upload as UploadIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../store';
import { setTheme, setSidebarOpen } from '../store/slices/uiSlice';

export const Settings: React.FC = () => {
  const dispatch = useAppDispatch();
  const { theme, sidebarOpen } = useAppSelector((state: any) => state.ui);
  const [settings, setSettings] = useState({
    theme: theme,
    sidebarOpen: sidebarOpen,
    autoRefresh: true,
    refreshInterval: 30,
    notifications: true,
    emailNotifications: false,
    apiEndpoint: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
    cacheTimeout: 30,
  });
  const [backupDialogOpen, setBackupDialogOpen] = useState(false);
  const [restoreDialogOpen, setRestoreDialogOpen] = useState(false);

  const handleSettingChange = (key: string, value: any) => {
    setSettings({ ...settings, [key]: value });
  };

  const handleSaveSettings = () => {
    dispatch(setTheme(settings.theme));
    dispatch(setSidebarOpen(settings.sidebarOpen));
    // TODO: Save other settings to backend
    console.log('Settings saved:', settings);
  };

  const handleExportSettings = () => {
    const dataStr = JSON.stringify(settings, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'settings.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleImportSettings = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedSettings = JSON.parse(e.target?.result as string);
          setSettings({ ...settings, ...importedSettings });
        } catch (error) {
          console.error('Error parsing settings file:', error);
        }
      };
      reader.readAsText(file);
    }
  };

  const handleResetSettings = () => {
    setSettings({
      theme: 'dark',
      sidebarOpen: true,
      autoRefresh: true,
      refreshInterval: 30,
      notifications: true,
      emailNotifications: false,
      apiEndpoint: 'http://localhost:8000/api',
      cacheTimeout: 30,
    });
  };

  return (
    <Box>
      {/* Page Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, color: '#ffffff', mb: 1 }}>
          Настройки системы
        </Typography>
        <Typography variant="body1" sx={{ color: '#cccccc' }}>
          Конфигурация параметров приложения
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Appearance Settings */}
        <Grid item xs={12} md={6}>
          <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#ffffff', mb: 2 }}>
                Внешний вид
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.theme === 'dark'}
                    onChange={(e) => handleSettingChange('theme', e.target.checked ? 'dark' : 'light')}
                    sx={{
                      '& .MuiSwitch-switchBase.Mui-checked': {
                        color: '#0066cc',
                      },
                      '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                        backgroundColor: '#0066cc',
                      },
                    }}
                  />
                }
                label="Темная тема"
                sx={{ color: '#ffffff' }}
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.sidebarOpen}
                    onChange={(e) => handleSettingChange('sidebarOpen', e.target.checked)}
                    sx={{
                      '& .MuiSwitch-switchBase.Mui-checked': {
                        color: '#0066cc',
                      },
                      '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                        backgroundColor: '#0066cc',
                      },
                    }}
                  />
                }
                label="Боковая панель открыта"
                sx={{ color: '#ffffff' }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* System Settings */}
        <Grid item xs={12} md={6}>
          <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#ffffff', mb: 2 }}>
                Система
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.autoRefresh}
                    onChange={(e) => handleSettingChange('autoRefresh', e.target.checked)}
                    sx={{
                      '& .MuiSwitch-switchBase.Mui-checked': {
                        color: '#0066cc',
                      },
                      '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                        backgroundColor: '#0066cc',
                      },
                    }}
                  />
                }
                label="Автообновление данных"
                sx={{ color: '#ffffff' }}
              />
              <TextField
                fullWidth
                label="Интервал обновления (сек)"
                type="number"
                value={settings.refreshInterval}
                onChange={(e) => handleSettingChange('refreshInterval', parseInt(e.target.value))}
                sx={{ mt: 2 }}
                disabled={!settings.autoRefresh}
              />
              <TextField
                fullWidth
                label="API Endpoint"
                value={settings.apiEndpoint}
                onChange={(e) => handleSettingChange('apiEndpoint', e.target.value)}
                sx={{ mt: 2 }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Notification Settings */}
        <Grid item xs={12} md={6}>
          <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#ffffff', mb: 2 }}>
                Уведомления
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications}
                    onChange={(e) => handleSettingChange('notifications', e.target.checked)}
                    sx={{
                      '& .MuiSwitch-switchBase.Mui-checked': {
                        color: '#0066cc',
                      },
                      '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                        backgroundColor: '#0066cc',
                      },
                    }}
                  />
                }
                label="Включить уведомления"
                sx={{ color: '#ffffff' }}
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.emailNotifications}
                    onChange={(e) => handleSettingChange('emailNotifications', e.target.checked)}
                    sx={{
                      '& .MuiSwitch-switchBase.Mui-checked': {
                        color: '#0066cc',
                      },
                      '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                        backgroundColor: '#0066cc',
                      },
                    }}
                  />
                }
                label="Email уведомления"
                sx={{ color: '#ffffff' }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Data Management */}
        <Grid item xs={12} md={6}>
          <Card sx={{ backgroundColor: '#2d2d2d', border: '1px solid #555' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#ffffff', mb: 2 }}>
                Управление данными
              </Typography>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Экспорт настроек"
                    secondary="Скачать файл конфигурации"
                  />
                  <ListItemSecondaryAction>
                    <IconButton onClick={handleExportSettings} sx={{ color: '#0066cc' }}>
                      <DownloadIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Импорт настроек"
                    secondary="Загрузить файл конфигурации"
                  />
                  <ListItemSecondaryAction>
                    <input
                      type="file"
                      accept=".json"
                      onChange={handleImportSettings}
                      style={{ display: 'none' }}
                      id="import-settings"
                    />
                    <label htmlFor="import-settings">
                      <IconButton component="span" sx={{ color: '#00ff00' }}>
                        <UploadIcon />
                      </IconButton>
                    </label>
                  </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Сброс настроек"
                    secondary="Вернуть настройки по умолчанию"
                  />
                  <ListItemSecondaryAction>
                    <IconButton onClick={handleResetSettings} sx={{ color: '#ff0000' }}>
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Save Button */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button
              variant="outlined"
              onClick={handleResetSettings}
              sx={{
                borderColor: '#555',
                color: '#cccccc',
                '&:hover': {
                  borderColor: '#777',
                  backgroundColor: '#404040',
                },
              }}
            >
              Сбросить
            </Button>
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={handleSaveSettings}
              sx={{
                background: 'linear-gradient(135deg, #0066cc 0%, #004499 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #0088ff 0%, #0066cc 100%)',
                },
              }}
            >
              Сохранить настройки
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

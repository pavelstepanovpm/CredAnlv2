import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
  Button,
  useTheme,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Business as BusinessIcon,
  Timeline as TimelineIcon,
  Assessment as AssessmentIcon,
  Settings as SettingsIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchPortfolioData } from '../store/slices/portfolioSlice';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const menuItems = [
  { id: 'dashboard', label: 'Дашборд', icon: DashboardIcon, path: '/dashboard' },
  { id: 'portfolio', label: 'Портфель', icon: BusinessIcon, path: '/portfolio' },
  { id: 'scenarios', label: 'Сценарии', icon: TimelineIcon, path: '/scenarios' },
  { id: 'reports', label: 'Отчеты', icon: AssessmentIcon, path: '/reports' },
  { id: 'settings', label: 'Настройки', icon: SettingsIcon, path: '/settings' },
];

export const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useAppDispatch();
  const { loading } = useAppSelector((state: any) => state.portfolio);

  const handleNavigation = (path: string) => {
    navigate(path);
    onClose();
  };

  const handleRefresh = () => {
    dispatch(fetchPortfolioData());
  };

  const handleExport = () => {
    // TODO: Implement export functionality
    console.log('Export data');
  };

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: 280,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 280,
          boxSizing: 'border-box',
          backgroundColor: '#2d2d2d',
          borderRight: '1px solid #404040',
          color: '#ffffff',
        },
      }}
    >
      <Box sx={{ p: 3 }}>
        {/* Logo */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <TimelineIcon sx={{ color: '#0066cc', mr: 1, fontSize: 32 }} />
          <Typography variant="h5" sx={{ fontWeight: 700, color: '#ffffff' }}>
            CredAnalytics
          </Typography>
        </Box>

        {/* Quick Actions */}
        <Box sx={{ mb: 3 }}>
          <Button
            variant="contained"
            startIcon={<RefreshIcon />}
            onClick={handleRefresh}
            disabled={loading}
            sx={{
              mb: 1,
              width: '100%',
              background: 'linear-gradient(135deg, #0066cc 0%, #004499 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #0088ff 0%, #0066cc 100%)',
              },
            }}
          >
            Обновить данные
          </Button>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={handleExport}
            sx={{
              width: '100%',
              borderColor: '#555',
              color: '#ffffff',
              '&:hover': {
                borderColor: '#777',
                backgroundColor: '#404040',
              },
            }}
          >
            Экспорт
          </Button>
        </Box>

        <Divider sx={{ borderColor: '#555', mb: 2 }} />

        {/* Navigation Menu */}
        <List>
          {menuItems.map((item: any) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <ListItem key={item.id} disablePadding>
                <ListItemButton
                  onClick={() => handleNavigation(item.path)}
                  sx={{
                    borderRadius: 1,
                    mb: 0.5,
                    backgroundColor: isActive ? '#0066cc' : 'transparent',
                    '&:hover': {
                      backgroundColor: isActive ? '#0088ff' : '#404040',
                    },
                  }}
                >
                  <ListItemIcon>
                    <Icon sx={{ color: isActive ? '#ffffff' : '#cccccc' }} />
                  </ListItemIcon>
                  <ListItemText
                    primary={item.label}
                    sx={{
                      '& .MuiListItemText-primary': {
                        color: isActive ? '#ffffff' : '#cccccc',
                        fontWeight: isActive ? 600 : 400,
                      },
                    }}
                  />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </Box>
    </Drawer>
  );
};

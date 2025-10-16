import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Chip,
  Avatar,
  Menu,
  MenuItem,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  AccountCircle as AccountCircleIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
} from '@mui/icons-material';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

interface HeaderProps {
  onToggleSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleSidebar }) => {
  const theme = useTheme();
  const { lastUpdated, loading } = useSelector((state: RootState) => state.portfolio);
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const formatLastUpdated = () => {
    if (!lastUpdated) return 'Никогда';
    return format(new Date(lastUpdated), 'dd.MM.yyyy HH:mm', { locale: ru });
  };

  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: '#2d2d2d',
        borderBottom: '1px solid #404040',
        boxShadow: 'none',
      }}
    >
      <Toolbar>
        {/* Menu Button */}
        <IconButton
          edge="start"
          color="inherit"
          onClick={onToggleSidebar}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        {/* Title */}
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
          Аналитика кредитного портфеля
        </Typography>

        {/* Status Info */}
        <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
          <Chip
            label={loading ? 'Обновление...' : `Обновлено: ${formatLastUpdated()}`}
            size="small"
            color={loading ? 'warning' : 'success'}
            sx={{
              backgroundColor: loading ? '#ffaa00' : '#00ff00',
              color: '#000000',
              fontWeight: 600,
            }}
          />
        </Box>

        {/* Notifications */}
        <IconButton color="inherit" sx={{ mr: 1 }}>
          <NotificationsIcon />
        </IconButton>

        {/* User Menu */}
        <IconButton
          color="inherit"
          onClick={handleMenuOpen}
          sx={{ p: 0 }}
        >
          <Avatar sx={{ width: 32, height: 32, backgroundColor: '#0066cc' }}>
            <AccountCircleIcon />
          </Avatar>
        </IconButton>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          PaperProps={{
            sx: {
              backgroundColor: '#2d2d2d',
              border: '1px solid #555',
              mt: 1,
            },
          }}
        >
          <MenuItem onClick={handleMenuClose}>
            <SettingsIcon sx={{ mr: 1 }} />
            Настройки
          </MenuItem>
          <MenuItem onClick={handleMenuClose}>
            <LogoutIcon sx={{ mr: 1 }} />
            Выйти
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};


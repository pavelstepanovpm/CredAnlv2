import React from 'react';
import { Box, useMediaQuery, useTheme } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { toggleSidebar } from '../store/slices/uiSlice';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const dispatch = useDispatch();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { sidebarOpen } = useSelector((state: RootState) => state.ui);

  const handleToggleSidebar = () => {
    dispatch(toggleSidebar());
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <Sidebar 
        open={sidebarOpen && !isMobile}
        onClose={() => dispatch(toggleSidebar())}
      />
      
      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          marginLeft: { xs: 0, md: sidebarOpen ? '280px' : 0 },
          transition: theme.transitions.create(['margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
          minHeight: '100vh',
          backgroundColor: '#1e1e1e',
        }}
      >
        {/* Header */}
        <Header onToggleSidebar={handleToggleSidebar} />
        
        {/* Page Content */}
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      </Box>
    </Box>
  );
};


import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#0066cc',
      light: '#0088ff',
      dark: '#004499',
    },
    secondary: {
      main: '#00ff00',
      light: '#33ff33',
      dark: '#00cc00',
    },
    background: {
      default: '#1e1e1e',
      paper: '#2d2d2d',
    },
    text: {
      primary: '#ffffff',
      secondary: '#cccccc',
    },
    error: {
      main: '#ff0000',
    },
    warning: {
      main: '#ffaa00',
    },
    info: {
      main: '#00ffff',
    },
    success: {
      main: '#00ff00',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      color: '#ffffff',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    h4: {
      fontSize: '1.25rem',
      fontWeight: 500,
      color: '#ffffff',
    },
    h5: {
      fontSize: '1.125rem',
      fontWeight: 500,
      color: '#ffffff',
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
      color: '#ffffff',
    },
    body1: {
      fontSize: '1rem',
      color: '#cccccc',
    },
    body2: {
      fontSize: '0.875rem',
      color: '#cccccc',
    },
    button: {
      textTransform: 'uppercase',
      fontWeight: 600,
      letterSpacing: '0.5px',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
          padding: '8px 16px',
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: '0.5px',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-1px)',
            boxShadow: '0 4px 12px rgba(0, 102, 204, 0.3)',
          },
        },
        contained: {
          background: 'linear-gradient(135deg, #0066cc 0%, #004499 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #0088ff 0%, #0066cc 100%)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#2d2d2d',
          border: '1px solid #555',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#2d2d2d',
          border: '1px solid #555',
        },
      },
    },
    MuiTable: {
      styleOverrides: {
        root: {
          backgroundColor: '#2d2d2d',
          borderRadius: '8px',
          overflow: 'hidden',
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: '#404040',
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderColor: '#555',
          color: '#ffffff',
        },
        head: {
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: '0.5px',
          fontSize: '12px',
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: '#404040',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: '0.5px',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
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
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          backgroundColor: '#404040',
          '&:hover': {
            backgroundColor: '#555',
          },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: '#404040',
          },
        },
      },
    },
  },
});


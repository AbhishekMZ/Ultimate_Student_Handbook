import { createTheme } from '@mui/material/styles';

export const authTheme = createTheme({
  palette: {
    primary: {
      main: '#6e8efb',
      light: '#a777e3',
    },
    background: {
      default: '#f4f4f9',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 8px 15px rgba(0, 0, 0, 0.3)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: 'rgba(255, 255, 255, 0.8)',
            '&:hover': {
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
            },
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          background: 'linear-gradient(90deg, #6e8efb, #a777e3)',
          '&:hover': {
            background: 'linear-gradient(90deg, #a777e3, #6e8efb)',
            transform: 'scale(1.05)',
          },
        },
      },
    },
  },
});

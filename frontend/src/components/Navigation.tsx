import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/dashboard')}
        >
          Student Tracking System
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button 
            color="inherit" 
            onClick={() => navigate('/dashboard')}
            sx={{ 
              backgroundColor: isActive('/dashboard') ? 'rgba(255, 255, 255, 0.1)' : 'transparent'
            }}
          >
            Dashboard
          </Button>
          <Button 
            color="inherit" 
            onClick={() => navigate('/students')}
            sx={{ 
              backgroundColor: isActive('/students') ? 'rgba(255, 255, 255, 0.1)' : 'transparent'
            }}
          >
            Students
          </Button>
          <Button 
            color="inherit" 
            onClick={() => navigate('/progress')}
            sx={{ 
              backgroundColor: isActive('/progress') ? 'rgba(255, 255, 255, 0.1)' : 'transparent'
            }}
          >
            Progress
          </Button>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;

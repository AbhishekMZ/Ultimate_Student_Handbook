import React from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  AppBar,
  Toolbar,
  Button,
  Grid,
  Card,
  CardContent,
  IconButton,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import PeopleIcon from '@mui/icons-material/People';
import TimelineIcon from '@mui/icons-material/Timeline';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Student Tracking System
          </Typography>
          <Button color="inherit" onClick={() => navigate('/students')}>
            Students
          </Button>
          <Button color="inherit" onClick={() => navigate('/progress')}>
            Progress
          </Button>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Welcome, {user?.name}!
              </Typography>
              <Typography variant="body1">
                Student ID: {user?.student_id}
              </Typography>
            </Paper>
          </Grid>
          
          {/* Quick Access Cards */}
          <Grid item xs={12} md={6}>
            <Card 
              sx={{ 
                cursor: 'pointer',
                '&:hover': { backgroundColor: 'action.hover' }
              }}
              onClick={() => navigate('/students')}
            >
              <CardContent sx={{ textAlign: 'center' }}>
                <IconButton color="primary" sx={{ mb: 1 }}>
                  <PeopleIcon fontSize="large" />
                </IconButton>
                <Typography variant="h6" gutterBottom>
                  Students Directory
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  View and manage student information
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card 
              sx={{ 
                cursor: 'pointer',
                '&:hover': { backgroundColor: 'action.hover' }
              }}
              onClick={() => navigate('/progress')}
            >
              <CardContent sx={{ textAlign: 'center' }}>
                <IconButton color="primary" sx={{ mb: 1 }}>
                  <TimelineIcon fontSize="large" />
                </IconButton>
                <Typography variant="h6" gutterBottom>
                  Progress Tracking
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Monitor performance and activities
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Dashboard;

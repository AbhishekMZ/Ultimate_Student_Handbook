import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Divider,
} from '@mui/material';
import PerformanceCard from './PerformanceCard';
import NotificationsPanel from './NotificationsPanel';
import CourseProgressList from './CourseProgressList';
import { useAuth } from '../../contexts/AuthContext';
import { useApi } from '../../hooks/useApi';

const Dashboard = () => {
  const { currentUser } = useAuth();
  const { getDashboardData } = useApi();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await getDashboardData(currentUser.student_id);
        setDashboardData(data);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [currentUser.student_id, getDashboardData]);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="80vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container>
        <Typography color="error" align="center" variant="h6">
          {error}
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Welcome Message */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, mb: 2 }}>
            <Typography variant="h4" gutterBottom>
              Welcome, {currentUser.name}!
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Student ID: {currentUser.student_id}
            </Typography>
          </Paper>
        </Grid>

        {/* Performance Overview */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Performance Overview
            </Typography>
            <Divider sx={{ mb: 2 }} />
            {dashboardData?.performance && (
              <PerformanceCard performance={dashboardData.performance} />
            )}
          </Paper>
        </Grid>

        {/* Notifications */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Recent Notifications
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <NotificationsPanel 
              notifications={dashboardData?.notifications || []}
            />
          </Paper>
        </Grid>

        {/* Course Progress */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Course Progress
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <CourseProgressList 
              courses={dashboardData?.courses || []}
            />
          </Paper>
        </Grid>

        {/* Achievement Badges */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Achievements
            </Typography>
            <Divider sx={{ mb: 2 }} />
            {/* Achievement component will be added */}
          </Paper>
        </Grid>

        {/* Device Sync Status */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Device Sync Status
            </Typography>
            <Divider sx={{ mb: 2 }} />
            {dashboardData?.sync_status && (
              <Box>
                <Typography variant="body1">
                  Last Sync: {new Date(dashboardData.sync_status.last_sync_time).toLocaleString()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Status: {dashboardData.sync_status.status}
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;

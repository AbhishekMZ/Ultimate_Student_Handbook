import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import Navigation from './Navigation';
import { useAuth } from '../contexts/AuthContext';
import { getStudentProgress } from '../services/api';

interface ProgressData {
  overall_progress: number;
  recent_activities: Activity[];
  performance_metrics: {
    attendance: number;
    assignments_completed: number;
    average_score: number;
  };
}

interface Activity {
  id: string;
  timestamp: string;
  description: string;
  type: string;
}

const Progress: React.FC = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progressData, setProgressData] = useState<ProgressData>({
    overall_progress: 0,
    recent_activities: [],
    performance_metrics: {
      attendance: 0,
      assignments_completed: 0,
      average_score: 0,
    },
  });

  useEffect(() => {
    const fetchProgress = async () => {
      if (!user?.student_id) {
        setError('User ID not found');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await getStudentProgress(user.student_id);
        setProgressData(response.data);
        setError(null);
      } catch (error) {
        console.error('Error fetching progress:', error);
        setError('Failed to load progress data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
  }, [user]);

  if (loading) {
    return (
      <Box sx={{ flexGrow: 1 }}>
        <Navigation />
        <Container>
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Navigation />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {/* Overall Progress */}
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Overall Progress
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={progressData.overall_progress} 
                sx={{ height: 10, borderRadius: 5 }}
              />
              <Typography variant="body2" sx={{ mt: 1 }}>
                {progressData.overall_progress}% Complete
              </Typography>
            </Paper>
          </Grid>

          {/* Performance Metrics */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Performance Metrics
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Typography variant="body2">Attendance</Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={progressData.performance_metrics.attendance} 
                    />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {progressData.performance_metrics.attendance}%
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="body2">Assignments Completed</Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={progressData.performance_metrics.assignments_completed} 
                    />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {progressData.performance_metrics.assignments_completed}%
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="body2">Average Score</Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={progressData.performance_metrics.average_score} 
                    />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {progressData.performance_metrics.average_score}%
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Recent Activities */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Activities
                </Typography>
                <List>
                  {progressData.recent_activities.map((activity, index) => (
                    <React.Fragment key={activity.id}>
                      <ListItem>
                        <ListItemText
                          primary={activity.description}
                          secondary={new Date(activity.timestamp).toLocaleString()}
                        />
                      </ListItem>
                      {index < progressData.recent_activities.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Progress;

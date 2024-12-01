import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import axios from 'axios';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Analytics() {
  const [selectedStudent, setSelectedStudent] = useState('');
  const [students, setStudents] = useState([]);
  const [analyticsData, setAnalyticsData] = useState(null);

  useEffect(() => {
    // Fetch students list
    const fetchStudents = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/students');
        setStudents(response.data);
      } catch (error) {
        console.error('Error fetching students:', error);
      }
    };

    fetchStudents();
  }, []);

  useEffect(() => {
    // Fetch analytics data when student is selected
    const fetchAnalytics = async () => {
      if (selectedStudent) {
        try {
          const response = await axios.get(`http://localhost:5000/api/analytics/${selectedStudent}`);
          setAnalyticsData(response.data);
        } catch (error) {
          console.error('Error fetching analytics:', error);
        }
      }
    };

    fetchAnalytics();
  }, [selectedStudent]);

  const performanceData = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
      {
        label: 'Performance Score',
        data: analyticsData?.weekly_performance || [75, 82, 88, 85],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const strengthsData = {
    labels: analyticsData?.strengths?.map(s => s.area) || ['Area 1', 'Area 2', 'Area 3'],
    datasets: [
      {
        label: 'Strength Score',
        data: analyticsData?.strengths?.map(s => s.score) || [85, 75, 90],
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Analytics Dashboard
      </Typography>

      <Box sx={{ mb: 4 }}>
        <FormControl fullWidth>
          <InputLabel>Select Student</InputLabel>
          <Select
            value={selectedStudent}
            onChange={(e) => setSelectedStudent(e.target.value)}
            label="Select Student"
          >
            {students.map((student) => (
              <MenuItem key={student.student_id} value={student.student_id}>
                {student.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {selectedStudent && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Performance Trend
                </Typography>
                <Box sx={{ height: 300 }}>
                  <Line 
                    data={performanceData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                    }}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Strengths Analysis
                </Typography>
                <Box sx={{ height: 300 }}>
                  <Bar
                    data={strengthsData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                    }}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {analyticsData?.improvement_areas && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Areas for Improvement
                  </Typography>
                  {analyticsData.improvement_areas.map((area, index) => (
                    <Typography key={index} variant="body1" gutterBottom>
                      • {area}
                    </Typography>
                  ))}
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}
    </Container>
  );
}

export default Analytics;

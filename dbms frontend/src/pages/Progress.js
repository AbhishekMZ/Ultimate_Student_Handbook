import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  LinearProgress,
  Box,
  Card,
  CardContent,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import axios from 'axios';

function Progress() {
  const [selectedStudent, setSelectedStudent] = useState('');
  const [students, setStudents] = useState([]);
  const [progress, setProgress] = useState([]);

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
    // Fetch progress data when student is selected
    const fetchProgress = async () => {
      if (selectedStudent) {
        try {
          const response = await axios.get(`http://localhost:5000/api/progress/${selectedStudent}`);
          setProgress(response.data);
        } catch (error) {
          console.error('Error fetching progress:', error);
        }
      }
    };

    fetchProgress();
  }, [selectedStudent]);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Student Progress
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
          {progress.map((item) => (
            <Grid item xs={12} key={item.topic_id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {item.topic_name}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Box sx={{ width: '100%', mr: 1 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={(item.understanding_level / 5) * 100} 
                      />
                    </Box>
                    <Box sx={{ minWidth: 35 }}>
                      <Typography variant="body2" color="text.secondary">
                        {item.understanding_level}/5
                      </Typography>
                    </Box>
                  </Box>
                  <Typography color="text.secondary" variant="body2">
                    Status: {item.completion_status}
                  </Typography>
                  <Typography color="text.secondary" variant="body2">
                    Time Spent: {item.time_spent_hours} hours
                  </Typography>
                  {item.notes && (
                    <Typography color="text.secondary" variant="body2">
                      Notes: {item.notes}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
}

export default Progress;

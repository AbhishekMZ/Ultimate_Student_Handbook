import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  IconButton,
  LinearProgress,
  CircularProgress,
} from '@mui/material';
import {
  Visibility,
  Edit,
  School,
  Email,
  Assessment,
  TrendingUp,
} from '@mui/icons-material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Students() {
  const [students, setStudents] = useState([]);
  const [studentDetails, setStudentDetails] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStudentData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://localhost:5000/api/students');
        const studentsData = response.data || [];
        setStudents(studentsData);

        // Fetch additional details for each student
        for (const student of studentsData) {
          try {
            const [academic, learning, progress] = await Promise.all([
              axios.get(`http://localhost:5000/api/academic/${student.id}`),
              axios.get(`http://localhost:5000/api/learning/${student.id}`),
              axios.get(`http://localhost:5000/api/progress/${student.id}`)
            ]);

            setStudentDetails(prev => ({
              ...prev,
              [student.id]: {
                academic: academic.data,
                learning: learning.data,
                progress: progress.data
              }
            }));
          } catch (error) {
            console.error(`Error fetching details for student ${student.id}:`, error);
          }
        }
      } catch (error) {
        console.error('Error fetching students:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStudentData();
  }, []);

  const calculateProgress = (studentId) => {
    const details = studentDetails[studentId];
    if (!details?.progress) return 0;
    
    const progress = details.progress;
    const totalTopics = progress.length;
    if (totalTopics === 0) return 0;
    
    const completed = progress.filter(p => p.status === 'completed').length;
    return (completed / totalTopics) * 100;
  };

  const getLatestAcademicRecord = (studentId) => {
    const details = studentDetails[studentId];
    if (!details?.academic || details.academic.length === 0) return null;
    
    return details.academic[0]; // Records are already sorted by year_of_completion DESC
  };

  const getLearningStyle = (studentId) => {
    const details = studentDetails[studentId];
    return details?.learning?.learning_style || 'Not specified';
  };

  const viewStudent = (studentId) => {
    navigate(`/progress?student=${studentId}`);
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Students
        </Typography>
        <Button variant="contained" color="primary" startIcon={<School />}>
          Add Student
        </Button>
      </Box>

      <Grid container spacing={3}>
        {students.map((student) => {
          const latestAcademic = getLatestAcademicRecord(student.id);
          
          return (
            <Grid item xs={12} md={6} key={student.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Box>
                      <Typography variant="h6">
                        {student.name}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                        <Email fontSize="small" color="action" />
                        <Typography variant="body2" color="text.secondary">
                          {student.email}
                        </Typography>
                      </Box>
                    </Box>
                    <Box>
                      <IconButton onClick={() => viewStudent(student.id)} color="primary">
                        <Visibility />
                      </IconButton>
                      <IconButton color="secondary">
                        <Edit />
                      </IconButton>
                    </Box>
                  </Box>

                  {/* Academic Info */}
                  {latestAcademic && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Latest Education
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1 }}>
                        <Chip
                          size="small"
                          label={latestAcademic.education_level}
                          color="primary"
                          variant="outlined"
                        />
                        <Chip
                          size="small"
                          label={`${latestAcademic.percentage}%`}
                          color={latestAcademic.percentage >= 75 ? "success" : "warning"}
                        />
                      </Box>
                    </Box>
                  )}

                  {/* Learning Style */}
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Learning Style
                    </Typography>
                    <Chip
                      size="small"
                      label={getLearningStyle(student.id)}
                      color="secondary"
                      variant="outlined"
                      sx={{ mt: 1 }}
                    />
                  </Box>

                  {/* Progress */}
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Overall Progress
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Box sx={{ width: '100%', mr: 1 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={calculateProgress(student.id)} 
                        />
                      </Box>
                      <Box sx={{ minWidth: 35 }}>
                        <Typography variant="body2" color="text.secondary">
                          {`${Math.round(calculateProgress(student.id))}%`}
                        </Typography>
                      </Box>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>
    </Container>
  );
}

export default Students;

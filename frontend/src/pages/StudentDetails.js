import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Box,
  Chip,
  Avatar,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Card,
  CardContent
} from '@mui/material';
import {
  School as SchoolIcon,
  Email as EmailIcon,
  Grade as GradeIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Book as BookIcon
} from '@mui/icons-material';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const StudentDetails = () => {
  const { studentId } = useParams();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStudentDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/students/${studentId}`);
        setStudent(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching student details:', err);
        setError(err.message || 'Failed to fetch student details');
        setLoading(false);
      }
    };

    fetchStudentDetails();
  }, [studentId]);

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase();
  };

  const getRandomColor = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = hash % 360;
    return `hsl(${hue}, 70%, 50%)`;
  };

  if (loading) {
    return (
      <Container sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!student) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="info">Student not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Student Profile Card */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
              <Avatar
                sx={{
                  width: 80,
                  height: 80,
                  bgcolor: getRandomColor(student.name),
                  mr: 2
                }}
              >
                {getInitials(student.name)}
              </Avatar>
              <Box>
                <Typography variant="h5">{student.name}</Typography>
                <Typography color="text.secondary">{student.studentId}</Typography>
              </Box>
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <EmailIcon />
                </ListItemIcon>
                <ListItemText primary={student.email} />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <SchoolIcon />
                </ListItemIcon>
                <ListItemText primary={`Semester ${student.semester}`} />
              </ListItem>
            </List>
          </Paper>
        </Grid>

        {/* Academic Performance */}
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Academic Performance
            </Typography>
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={6}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      10th Grade
                    </Typography>
                    <Typography variant="h4">
                      {student.tenthMarks}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={6}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      12th Grade
                    </Typography>
                    <Typography variant="h4">
                      {student.twelfthMarks}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Divider sx={{ my: 3 }} />

            {/* Strengths and Weaknesses */}
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom color="primary">
                  Strengths
                </Typography>
                <List dense>
                  {student.strengths.map((strength, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <TrendingUpIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={strength} />
                    </ListItem>
                  ))}
                </List>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom color="error">
                  Areas for Improvement
                </Typography>
                <List dense>
                  {student.weaknesses.map((weakness, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <TrendingDownIcon color="error" />
                      </ListItemIcon>
                      <ListItemText primary={weakness} />
                    </ListItem>
                  ))}
                </List>
              </Grid>
            </Grid>

            <Divider sx={{ my: 3 }} />

            {/* Current Courses */}
            <Typography variant="h6" gutterBottom>
              Current Courses
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {student.courses.map((course, index) => (
                <Chip
                  key={index}
                  icon={<BookIcon />}
                  label={course}
                  variant="outlined"
                  color="primary"
                />
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default StudentDetails;

import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Container,
  Typography,
  CircularProgress,
  Alert
} from '@mui/material';
import axios from 'axios';

const Courses = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/courses');
        setCourses(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error details:', err);
        setError(err.message || 'Failed to fetch courses data');
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

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

  return (
    <Container sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 2 }}>
        <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
          Courses
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Code</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Category</TableCell>
                <TableCell>Credits</TableCell>
                <TableCell>Hours</TableCell>
                <TableCell>CIE</TableCell>
                <TableCell>SEE</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {courses.map((course) => (
                <TableRow key={course.CourseCode}>
                  <TableCell>{course.CourseCode}</TableCell>
                  <TableCell>{course.CourseName}</TableCell>
                  <TableCell>{course.Category}</TableCell>
                  <TableCell>{course.Credits}</TableCell>
                  <TableCell>{course.TotalHours}</TableCell>
                  <TableCell>{course.CIE}</TableCell>
                  <TableCell>{course.SEE}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Container>
  );
};

export default Courses;

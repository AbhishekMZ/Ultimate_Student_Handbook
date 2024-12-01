import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
} from '@mui/material';
import axios from 'axios';

function Courses() {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    // Fetch courses data
    const fetchCourses = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/textbooks');
        setCourses(response.data);
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    };

    fetchCourses();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Courses
        </Typography>
        <Button variant="contained" color="primary">
          Add Course
        </Button>
      </Box>

      <Grid container spacing={3}>
        {courses.map((course) => (
          <Grid item xs={12} sm={6} md={4} key={course.textbook_id}>
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2">
                  {course.title}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  {course.course_code}
                </Typography>
                <Typography variant="body2" component="p">
                  {course.description}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary">View Details</Button>
                <Button size="small" color="secondary">Edit</Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default Courses;

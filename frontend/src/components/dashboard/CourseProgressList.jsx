import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  Button,
  Tooltip,
} from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from '@mui/lab';
import {
  School,
  Assignment,
  Grade,
  Flag,
} from '@mui/icons-material';

const getGradeColor = (grade) => {
  if (grade >= 75) return 'success';
  if (grade >= 60) return 'warning';
  return 'error';
};

const CourseCard = ({ course }) => {
  const {
    course_code,
    course_name,
    syllabus_covered,
    current_grade,
    tests_completed,
    next_milestone,
    recommendations,
  } = course;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box mb={2}>
          <Typography variant="h6" gutterBottom>
            {course_code}
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {course_name}
          </Typography>
        </Box>

        <Box mb={2}>
          <Typography variant="subtitle2" gutterBottom>
            Progress
          </Typography>
          <Box display="flex" alignItems="center">
            <Box width="100%" mr={1}>
              <LinearProgress
                variant="determinate"
                value={syllabus_covered * 100}
                sx={{
                  height: 8,
                  borderRadius: 4,
                }}
              />
            </Box>
            <Box minWidth={35}>
              <Typography variant="body2" color="text.secondary">
                {`${Math.round(syllabus_covered * 100)}%`}
              </Typography>
            </Box>
          </Box>
        </Box>

        <Box mb={2} display="flex" gap={1}>
          <Tooltip title="Current Grade">
            <Chip
              icon={<Grade />}
              label={`${Math.round(current_grade)}%`}
              color={getGradeColor(current_grade)}
              size="small"
            />
          </Tooltip>
          <Tooltip title="Tests Completed">
            <Chip
              icon={<Assignment />}
              label={`${tests_completed} Tests`}
              variant="outlined"
              size="small"
            />
          </Tooltip>
        </Box>

        <Timeline position="right" sx={{ mb: 0, p: 0 }}>
          <TimelineItem>
            <TimelineSeparator>
              <TimelineDot color="primary">
                <Flag fontSize="small" />
              </TimelineDot>
              <TimelineConnector />
            </TimelineSeparator>
            <TimelineContent>
              <Typography variant="body2">
                Next: {next_milestone}
              </Typography>
            </TimelineContent>
          </TimelineItem>
        </Timeline>

        <Box mt={2}>
          <Button
            variant="outlined"
            size="small"
            startIcon={<School />}
            fullWidth
          >
            View Details
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

const CourseProgressList = ({ courses }) => {
  if (!courses.length) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight={200}
      >
        <Typography variant="body2" color="text.secondary">
          No courses available
        </Typography>
      </Box>
    );
  }

  return (
    <Grid container spacing={3}>
      {courses.map((course, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <CourseCard course={course} />
        </Grid>
      ))}
    </Grid>
  );
};

export default CourseProgressList;

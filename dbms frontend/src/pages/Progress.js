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
  Divider,
  Chip,
  List,
  ListItem,
  ListItemText,
  Tab,
  Tabs,
  Tooltip,
  IconButton,
} from '@mui/material';
import {
  School,
  Psychology,
  TrendingUp,
  Timer,
  StickyNote2,
} from '@mui/icons-material';
import axios from 'axios';

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function Progress() {
  const [selectedStudent, setSelectedStudent] = useState('');
  const [students, setStudents] = useState([]);
  const [studentData, setStudentData] = useState(null);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
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
    const fetchStudentData = async () => {
      if (selectedStudent) {
        try {
          const [academic, learning, progress] = await Promise.all([
            axios.get(`http://localhost:5000/api/academic/${selectedStudent}`),
            axios.get(`http://localhost:5000/api/learning/${selectedStudent}`),
            axios.get(`http://localhost:5000/api/progress/${selectedStudent}`)
          ]);
          
          setStudentData({
            academic: academic.data,
            learning: learning.data,
            progress: progress.data
          });
        } catch (error) {
          console.error('Error fetching student data:', error);
        }
      }
    };

    fetchStudentData();
  }, [selectedStudent]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const renderAcademicHistory = () => (
    <Grid container spacing={3}>
      {studentData?.academic.map((record) => (
        <Grid item xs={12} md={6} key={record.education_level}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {record.education_level}
              </Typography>
              <Typography color="textSecondary">
                {record.institution} ({record.board})
              </Typography>
              <Typography variant="h5" sx={{ color: 'primary.main', my: 2 }}>
                {record.percentage}%
              </Typography>
              <Typography variant="body2">
                Year: {record.year_of_completion}
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Subjects:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {record.subjects.split(',').map((subject, index) => (
                    <Chip 
                      key={index}
                      label={subject.trim()}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Box>
              {record.achievements && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Achievements:
                  </Typography>
                  <Chip 
                    label={record.achievements}
                    color="success"
                    size="small"
                  />
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  const renderLearningProfile = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Learning Preferences
            </Typography>
            <List>
              <ListItem>
                <ListItemText 
                  primary="Learning Style"
                  secondary={studentData?.learning.learning_style}
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="Preferred Study Time"
                  secondary={studentData?.learning.preferred_study_time}
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="Concentration Span"
                  secondary={`${studentData?.learning.concentration_span} minutes`}
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="Learning Pace"
                  secondary={studentData?.learning.learning_pace}
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="Study Group Preference"
                  secondary={studentData?.learning.study_group_preference}
                />
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Academic Focus
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Subjects of Interest
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {studentData?.learning.subjects_of_interest.split(',').map((subject, index) => (
                  <Chip 
                    key={index}
                    label={subject.trim()}
                    color="success"
                    size="small"
                  />
                ))}
              </Box>
            </Box>
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Areas for Improvement
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {studentData?.learning.weak_areas.split(',').map((area, index) => (
                  <Chip 
                    key={index}
                    label={area.trim()}
                    color="error"
                    size="small"
                  />
                ))}
              </Box>
            </Box>
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Attendance Rate
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ width: '100%', mr: 1 }}>
                  <LinearProgress
                    variant="determinate"
                    value={studentData?.learning.attendance_percentage || 0}
                  />
                </Box>
                <Box sx={{ minWidth: 35 }}>
                  <Typography variant="body2" color="text.secondary">
                    {studentData?.learning.attendance_percentage}%
                  </Typography>
                </Box>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const renderProgress = () => (
    <Grid container spacing={3}>
      {studentData?.progress.map((item) => (
        <Grid item xs={12} key={item.topic_id}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  {item.topic_name}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Tooltip title={`Time spent: ${item.time_spent_hours} hours`}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Timer />
                      <Typography variant="body2" sx={{ ml: 0.5 }}>
                        {item.time_spent_hours}h
                      </Typography>
                    </Box>
                  </Tooltip>
                  {item.notes && (
                    <Tooltip title={item.notes}>
                      <IconButton size="small">
                        <StickyNote2 />
                      </IconButton>
                    </Tooltip>
                  )}
                </Box>
              </Box>
              
              <Typography variant="subtitle2" gutterBottom>
                Understanding Level
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
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

              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Chip 
                  label={item.completion_status}
                  color={item.completion_status === 'Completed' ? 'success' : 'warning'}
                  size="small"
                />
                {item.last_assessment_score !== null && (
                  <Typography variant="body2" color="text.secondary">
                    Last Assessment: {item.last_assessment_score}%
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Student Performance Tracking
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
                {student.name} ({student.username})
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {studentData && (
        <>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
            <Tabs value={tabValue} onChange={handleTabChange} centered>
              <Tab icon={<School />} label="Academic History" />
              <Tab icon={<Psychology />} label="Learning Profile" />
              <Tab icon={<TrendingUp />} label="Current Progress" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            {renderAcademicHistory()}
          </TabPanel>
          <TabPanel value={tabValue} index={1}>
            {renderLearningProfile()}
          </TabPanel>
          <TabPanel value={tabValue} index={2}>
            {renderProgress()}
          </TabPanel>
        </>
      )}
    </Container>
  );
}

export default Progress;

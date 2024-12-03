import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Container,
  CircularProgress,
  Alert,
  Box,
  Avatar,
  TextField,
  InputAdornment,
  IconButton
} from '@mui/material';
import {
  Email as EmailIcon,
  Search as SearchIcon,
  Clear as ClearIcon
} from '@mui/icons-material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Students = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/students');
        const sortedStudents = [...response.data].sort((a, b) => {
          const numA = a.studentId ? parseInt(a.studentId.replace(/\D/g, '')) : 0;
          const numB = b.studentId ? parseInt(b.studentId.replace(/\D/g, '')) : 0;
          return numA - numB;
        });
        setStudents(sortedStudents);
        setLoading(false);
      } catch (err) {
        console.error('Error details:', err);
        setError(err.message || 'Failed to fetch students data');
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  const filteredStudents = students.filter(student => {
    const searchLower = searchTerm.toLowerCase().trim();
    const nameMatch = student.name?.toLowerCase().includes(searchLower);
    const idMatch = student.studentId?.toLowerCase().includes(searchLower);
    return nameMatch || idMatch;
  });

  const getInitials = (name) => {
    if (!name) return '';
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase();
  };

  const getRandomColor = (str) => {
    if (!str) return '#000000';
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = hash % 360;
    return `hsl(${hue}, 70%, 50%)`;
  };

  const handleClearSearch = () => {
    setSearchTerm('');
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

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Students Directory
        </Typography>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search by name or USN..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color="action" />
              </InputAdornment>
            ),
            endAdornment: searchTerm && (
              <InputAdornment position="end">
                <IconButton onClick={handleClearSearch} size="small">
                  <ClearIcon />
                </IconButton>
              </InputAdornment>
            ),
          }}
          sx={{
            mb: 3,
            '& .MuiOutlinedInput-root': {
              '& fieldset': {
                borderRadius: '8px',
              },
              '&:hover fieldset': {
                borderColor: 'primary.main',
              },
            },
          }}
        />
      </Box>

      <Grid container spacing={3}>
        {filteredStudents.map((student) => (
          <Grid item xs={12} sm={6} md={4} key={student.studentId || 'unknown'}>
            <Card 
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                transition: 'transform 0.2s, box-shadow 0.2s',
                borderRadius: '12px',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 6,
                  cursor: 'pointer'
                }
              }}
              onClick={() => navigate(`/student/${student.studentId}`)}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar 
                    sx={{ 
                      width: 56, 
                      height: 56, 
                      bgcolor: getRandomColor(student.name),
                      mr: 2,
                      fontWeight: 'bold'
                    }}
                  >
                    {getInitials(student.name)}
                  </Avatar>
                  <Box>
                    <Typography 
                      variant="h6" 
                      component="div"
                      sx={{ 
                        fontWeight: 500,
                        color: 'text.primary',
                        mb: 1
                      }}
                    >
                      {student.name}
                    </Typography>
                    <Typography 
                      variant="subtitle1" 
                      sx={{ 
                        color: 'text.secondary',
                        fontWeight: 400,
                        mb: 1
                      }}
                    >
                      {student.studentId}
                    </Typography>
                    <Box sx={{ 
                      display: 'flex', 
                      alignItems: 'center',
                      color: 'text.secondary'
                    }}>
                      <EmailIcon sx={{ mr: 1, fontSize: '1.1rem' }} />
                      <Typography 
                        variant="body2" 
                        sx={{ 
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap'
                        }}
                      >
                        {student.email}
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Students;

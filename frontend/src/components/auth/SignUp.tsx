import React, { useState } from 'react';
import {
  TextField,
  Button,
  Typography,
  MenuItem,
  Alert,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { api } from '../../services/api';
import { AuthContainer, AuthPaper, FormContainer, LinkText } from './styles';

const SignUp: React.FC = () => {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    fullName: '',
    usn: '',
    year: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const yearOptions = [
    { value: '1', label: '1st Year' },
    { value: '2', label: '2nd Year' },
    { value: '3', label: '3rd Year' },
    { value: '4', label: '4th Year' }
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      await api.post('/auth/register', {
        name: formData.fullName,
        email: formData.email,
        password: formData.password,
        student_id: formData.usn,
        role: 'student'
      });
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to create account');
    }
  };

  return (
    <AuthContainer>
      <AuthPaper>
        <Typography variant="h4" align="center" gutterBottom>
          Create Your Account
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <FormContainer component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            required
            name="fullName"
            label="Full Name"
            value={formData.fullName}
            onChange={handleChange}
          />
          <TextField
            fullWidth
            required
            name="usn"
            label="USN"
            value={formData.usn}
            onChange={handleChange}
          />
          <TextField
            fullWidth
            required
            select
            name="year"
            label="Year of Study"
            value={formData.year}
            onChange={handleChange}
          >
            {yearOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            fullWidth
            required
            name="email"
            label="Email Address"
            type="email"
            value={formData.email}
            onChange={handleChange}
          />
          <TextField
            fullWidth
            required
            name="password"
            label="Password"
            type="password"
            value={formData.password}
            onChange={handleChange}
          />
          <TextField
            fullWidth
            required
            name="confirmPassword"
            label="Confirm Password"
            type="password"
            value={formData.confirmPassword}
            onChange={handleChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
          >
            Sign Up
          </Button>
          <Typography align="center" sx={{ mt: 2 }}>
            Already have an account?{' '}
            <LinkText component="span" onClick={() => navigate('/login')}>
              Login
            </LinkText>
          </Typography>
        </FormContainer>
      </AuthPaper>
    </AuthContainer>
  );
};

export default SignUp;

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  TextField,
  Button,
  Typography,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { FormContainer, FormPaper } from './styles';
import { FormError, FormSuccess, LoadingOverlay } from '../Common/FormHelpers';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Forgot Password Dialog
  const [resetEmail, setResetEmail] = useState('');
  const [openResetDialog, setOpenResetDialog] = useState(false);
  const [resetSuccess, setResetSuccess] = useState('');
  const [resetError, setResetError] = useState('');
  const [resetLoading, setResetLoading] = useState(false);

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setApiError('');
    setSuccess('');

    try {
      // Your existing login logic here
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();
      localStorage.setItem('token', data.token);
      setSuccess('Login successful!');
      setTimeout(() => navigate('/dashboard'), 1000);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async () => {
    if (!resetEmail || !/\S+@\S+\.\S+/.test(resetEmail)) {
      setResetError('Please enter a valid email');
      return;
    }

    setResetLoading(true);
    setResetError('');
    setResetSuccess('');

    try {
      // Implement your password reset logic here
      await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: resetEmail }),
      });

      setResetSuccess('Password reset instructions sent to your email');
      setTimeout(() => setOpenResetDialog(false), 2000);
    } catch (error) {
      setResetError('Failed to send reset instructions');
    } finally {
      setResetLoading(false);
    }
  };

  return (
    <FormContainer>
      <FormPaper elevation={3}>
        <LoadingOverlay loading={loading} />
        
        <Typography variant="h4" component="h1" gutterBottom>
          Login
        </Typography>

        {apiError && <FormError error={apiError} />}
        {success && <FormSuccess message={success} />}

        <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
          <TextField
            fullWidth
            margin="normal"
            label="Email"
            type="email"
            value={formData.email}
            onChange={(e) => {
              setFormData({ ...formData, email: e.target.value });
              if (errors.email) {
                const { email, ...rest } = errors;
                setErrors(rest);
              }
            }}
            error={!!errors.email}
            helperText={errors.email}
            disabled={loading}
          />

          <TextField
            fullWidth
            margin="normal"
            label="Password"
            type="password"
            value={formData.password}
            onChange={(e) => {
              setFormData({ ...formData, password: e.target.value });
              if (errors.password) {
                const { password, ...rest } = errors;
                setErrors(rest);
              }
            }}
            error={!!errors.password}
            helperText={errors.password}
            disabled={loading}
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </Button>

          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
            <Button
              component={Link}
              to="/signup"
              color="primary"
              disabled={loading}
            >
              Create Account
            </Button>
            <Button
              onClick={() => setOpenResetDialog(true)}
              color="primary"
              disabled={loading}
            >
              Forgot Password?
            </Button>
          </Box>
        </Box>
      </FormPaper>

      {/* Forgot Password Dialog */}
      <Dialog open={openResetDialog} onClose={() => setOpenResetDialog(false)}>
        <DialogTitle>Reset Password</DialogTitle>
        <DialogContent>
          {resetError && <FormError error={resetError} />}
          {resetSuccess && <FormSuccess message={resetSuccess} />}
          
          <TextField
            autoFocus
            margin="dense"
            label="Email Address"
            type="email"
            fullWidth
            value={resetEmail}
            onChange={(e) => setResetEmail(e.target.value)}
            disabled={resetLoading}
          />
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setOpenResetDialog(false)} 
            disabled={resetLoading}
          >
            Cancel
          </Button>
          <Button 
            onClick={handleForgotPassword}
            disabled={resetLoading}
            variant="contained"
          >
            {resetLoading ? 'Sending...' : 'Send Reset Link'}
          </Button>
        </DialogActions>
      </Dialog>
    </FormContainer>
  );
};

export default Login;

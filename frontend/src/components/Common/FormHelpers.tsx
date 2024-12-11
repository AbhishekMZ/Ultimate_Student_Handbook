import React from 'react';
import { Alert, CircularProgress, Box } from '@mui/material';
import { styled } from '@mui/material/styles';

export const LoadingSpinner = styled(CircularProgress)({
  position: 'absolute',
  top: '50%',
  left: '50%',
  marginTop: -12,
  marginLeft: -12,
});

export const FormError: React.FC<{ error?: string }> = ({ error }) => {
  if (!error) return null;
  return (
    <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
      {error}
    </Alert>
  );
};

export const FormSuccess: React.FC<{ message?: string }> = ({ message }) => {
  if (!message) return null;
  return (
    <Alert severity="success" sx={{ mb: 2, width: '100%' }}>
      {message}
    </Alert>
  );
};

export const LoadingOverlay: React.FC<{ loading: boolean }> = ({ loading }) => {
  if (!loading) return null;
  return (
    <Box
      sx={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
    >
      <CircularProgress />
    </Box>
  );
};

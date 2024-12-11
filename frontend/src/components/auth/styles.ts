import { styled } from '@mui/material/styles';
import { Box, Container, Paper } from '@mui/material';

export const AuthContainer = styled(Container)(({ theme }) => ({
  height: '100vh',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.primary.light})`,
}));

export const AuthPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  width: '100%',
  maxWidth: '400px',
  borderRadius: '15px',
  animation: 'fadeIn 0.5s ease-in-out',
  '@keyframes fadeIn': {
    from: {
      opacity: 0,
      transform: 'translateY(20px)',
    },
    to: {
      opacity: 1,
      transform: 'translateY(0)',
    },
  },
}));

export const FormContainer = styled(Box)(({ theme }) => ({
  width: '100%',
  '& .MuiTextField-root': {
    marginBottom: theme.spacing(2),
  },
  '& .MuiButton-root': {
    margin: theme.spacing(2, 0),
  },
}));

export const LinkText = styled(Box)(({ theme }) => ({
  color: theme.palette.primary.main,
  cursor: 'pointer',
  textDecoration: 'underline',
  '&:hover': {
    color: theme.palette.primary.light,
  },
}));

import React from 'react';
import { Outlet } from 'react-router-dom';
import { Box, Container, CssBaseline } from '@mui/material';
import Breadcrumbs from '../Common/Breadcrumbs';
import PageTransition from '../Common/PageTransition';

const Layout: React.FC = () => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <CssBaseline />
      
      <Container component="main" sx={{ flexGrow: 1, py: 4 }}>
        <Breadcrumbs />
        <PageTransition>
          <Outlet />
        </PageTransition>
      </Container>
    </Box>
  );
};

export default Layout;

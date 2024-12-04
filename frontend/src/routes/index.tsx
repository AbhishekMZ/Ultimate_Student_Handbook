import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Students from '../components/Students';
import Login from '../components/Auth/Login';
import Layout from '../components/Layout';

const AppRoutes: React.FC = () => {
  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
        
        {/* Protected Routes */}
        <Route element={<Layout />}>
          <Route path="/" element={isAuthenticated ? <Navigate to="/students" /> : <Navigate to="/login" />} />
          <Route 
            path="/students" 
            element={isAuthenticated ? <Students /> : <Navigate to="/login" />} 
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;

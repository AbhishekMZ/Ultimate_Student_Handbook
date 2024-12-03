import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';

/**
 * AuthContext is a React context that provides authentication functionality.
 */
const AuthContext = createContext(null);

/**
 * useAuth hook provides access to the AuthContext.
 * @throws {Error} if used outside of an AuthProvider.
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

/**
 * AuthProvider component provides the AuthContext to its children.
 * @param {ReactNode} children - The children components that will have access to the AuthContext.
 */
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check for stored auth token and user data
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');
    
    if (token && userData) {
      setCurrentUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  /**
   * login function logs in a user with the provided credentials.
   * @param {string} email - The user's email.
   * @param {string} password - The user's password.
   * @param {string} deviceId - The user's device ID.
   * @returns {Promise<{success: boolean, message: string, token: string, user_data: object}>} - The login result.
   */
  const login = async (email, password, deviceId) => {
    try {
      const data = await authAPI.login(email, password, deviceId);
      if (data.success) {
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('userData', JSON.stringify(data.user_data));
        setCurrentUser(data.user_data);
      }
      return data;
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        message: error.message || 'An error occurred during login',
      };
    }
  };

  /**
   * register function registers a new user with the provided data.
   * @param {object} userData - The user's data.
   * @param {string} password - The user's password.
   * @param {string} deviceId - The user's device ID.
   * @returns {Promise<{success: boolean, message: string, token: string, user_data: object}>} - The registration result.
   */
  const register = async (userData, password, deviceId) => {
    try {
      const data = await authAPI.register(userData, password, deviceId);
      if (data.success) {
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('userData', JSON.stringify(data.user_data));
        setCurrentUser(data.user_data);
      }
      return data;
    } catch (error) {
      console.error('Registration error:', error);
      return {
        success: false,
        message: error.message || 'An error occurred during registration',
      };
    }
  };

  /**
   * logout function logs out the current user.
   */
  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    setCurrentUser(null);
    navigate('/login');
  };

  const value = {
    currentUser,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

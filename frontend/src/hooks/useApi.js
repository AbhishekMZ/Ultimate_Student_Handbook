import { useState, useCallback } from 'react';

const API_BASE_URL = '/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getAuthHeaders = useCallback(() => {
    const token = localStorage.getItem('authToken');
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    };
  }, []);

  const handleResponse = useCallback(async (response) => {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'An error occurred');
    }
    return data;
  }, []);

  const getDashboardData = useCallback(async (studentId) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE_URL}/dashboard/${studentId}`, {
        headers: getAuthHeaders(),
      });

      return await handleResponse(response);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [getAuthHeaders, handleResponse]);

  const getCourseProgress = useCallback(async (studentId, courseCode) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${API_BASE_URL}/courses/${courseCode}/progress/${studentId}`,
        {
          headers: getAuthHeaders(),
        }
      );

      return await handleResponse(response);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [getAuthHeaders, handleResponse]);

  const getNotifications = useCallback(async (studentId, unreadOnly = false) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${API_BASE_URL}/notifications/${studentId}?unread_only=${unreadOnly}`,
        {
          headers: getAuthHeaders(),
        }
      );

      return await handleResponse(response);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [getAuthHeaders, handleResponse]);

  const markNotificationAsRead = useCallback(async (notificationId) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${API_BASE_URL}/notifications/${notificationId}/read`,
        {
          method: 'POST',
          headers: getAuthHeaders(),
        }
      );

      return await handleResponse(response);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [getAuthHeaders, handleResponse]);

  const updateDeviceSync = useCallback(async (studentId, deviceId, syncData) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${API_BASE_URL}/sync/${studentId}/device/${deviceId}`,
        {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify(syncData),
        }
      );

      return await handleResponse(response);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [getAuthHeaders, handleResponse]);

  const trackAchievement = useCallback(async (studentId, achievementData) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${API_BASE_URL}/achievements/${studentId}`,
        {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify(achievementData),
        }
      );

      return await handleResponse(response);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [getAuthHeaders, handleResponse]);

  return {
    loading,
    error,
    getDashboardData,
    getCourseProgress,
    getNotifications,
    markNotificationAsRead,
    updateDeviceSync,
    trackAchievement,
  };
};

export default useApi;

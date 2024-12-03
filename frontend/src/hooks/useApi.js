import { useState, useCallback } from 'react';
import {
  dashboardAPI,
  notificationAPI,
  courseAPI,
  achievementAPI,
  syncAPI
} from '../services/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleApiCall = useCallback(async (apiCall) => {
    try {
      setLoading(true);
      setError(null);
      return await apiCall();
    } catch (err) {
      setError(err.message || 'An error occurred');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getDashboardData = useCallback((studentId) => 
    handleApiCall(() => dashboardAPI.getDashboardData(studentId)),
  [handleApiCall]);

  const getCourseProgress = useCallback((studentId, courseCode) =>
    handleApiCall(() => courseAPI.getCourseProgress(studentId, courseCode)),
  [handleApiCall]);

  const getNotifications = useCallback((studentId, unreadOnly = false) =>
    handleApiCall(() => notificationAPI.getNotifications(studentId, unreadOnly)),
  [handleApiCall]);

  const markNotificationAsRead = useCallback((notificationId) =>
    handleApiCall(() => notificationAPI.markAsRead(notificationId)),
  [handleApiCall]);

  const updateDeviceSync = useCallback((studentId, deviceId, syncData) =>
    handleApiCall(() => syncAPI.syncDevice(studentId, deviceId, syncData)),
  [handleApiCall]);

  const trackAchievement = useCallback((studentId, achievementData) =>
    handleApiCall(() => achievementAPI.trackAchievement(studentId, achievementData)),
  [handleApiCall]);

  const getStudentCourses = useCallback((studentId) =>
    handleApiCall(() => courseAPI.getStudentCourses(studentId)),
  [handleApiCall]);

  const updateCourseProgress = useCallback((studentId, courseCode, progressData) =>
    handleApiCall(() => courseAPI.updateCourseProgress(studentId, courseCode, progressData)),
  [handleApiCall]);

  const getPerformanceAnalytics = useCallback((studentId) =>
    handleApiCall(() => dashboardAPI.getPerformanceAnalytics(studentId)),
  [handleApiCall]);

  return {
    loading,
    error,
    getDashboardData,
    getCourseProgress,
    getNotifications,
    markNotificationAsRead,
    updateDeviceSync,
    trackAchievement,
    getStudentCourses,
    updateCourseProgress,
    getPerformanceAnalytics,
  };
};

export default useApi;

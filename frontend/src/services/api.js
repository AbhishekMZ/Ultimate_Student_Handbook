import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      // Handle token expiration
      if (error.response.status === 401) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        window.location.href = '/login';
      }
      return Promise.reject(error.response.data);
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const authAPI = {
  login: (email, password, deviceId) =>
    api.post('/auth/login', { email, password, device_id: deviceId }),

  register: (userData, password, deviceId) =>
    api.post('/auth/register', { ...userData, password, device_id: deviceId }),
};

// Dashboard endpoints
export const dashboardAPI = {
  getDashboardData: (studentId) =>
    api.get(`/dashboard/${studentId}`),

  getCourseProgress: (studentId, courseCode) =>
    api.get(`/courses/${courseCode}/progress/${studentId}`),

  getPerformanceAnalytics: (studentId) =>
    api.get(`/performance/${studentId}/analytics`),
};

// Notification endpoints
export const notificationAPI = {
  getNotifications: (studentId, unreadOnly = false) =>
    api.get(`/notifications/${studentId}`, {
      params: { unread_only: unreadOnly }
    }),

  markAsRead: (notificationId) =>
    api.post(`/notifications/${notificationId}/read`),

  markAllAsRead: (studentId) =>
    api.post(`/notifications/${studentId}/read-all`),
};

// Device sync endpoints
export const syncAPI = {
  syncDevice: (studentId, deviceId, syncData) =>
    api.post(`/sync/${studentId}/device/${deviceId}`, syncData),

  getDeviceInfo: (studentId, deviceId) =>
    api.get(`/sync/${studentId}/device/${deviceId}`),
};

// Achievement endpoints
export const achievementAPI = {
  trackAchievement: (studentId, achievementData) =>
    api.post(`/achievements/${studentId}`, achievementData),

  getAchievements: (studentId) =>
    api.get(`/achievements/${studentId}`),
};

// Course endpoints
export const courseAPI = {
  getStudentCourses: (studentId) =>
    api.get(`/courses/${studentId}`),

  updateCourseProgress: (studentId, courseCode, progressData) =>
    api.post(`/courses/${courseCode}/progress/${studentId}`, progressData),
};

export default api;

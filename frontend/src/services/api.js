import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_URL = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add Authorization header if token exists
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('session_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Handle 401 errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear session and redirect to login
      localStorage.removeItem('session_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  processSession: (sessionId) => 
    apiClient.post('/auth/session', { session_id: sessionId }),
  
  getCurrentUser: () => 
    apiClient.get('/auth/me'),
  
  logout: () => 
    apiClient.post('/auth/logout')
};

// Dashboard & Stats API
export const statsApi = {
  getStats: () => 
    apiClient.get('/stats'),
  
  getDailyActivity: () => 
    apiClient.get('/activity/daily'),
  
  getWeeklyActivity: () => 
    apiClient.get('/activity/weekly'),
  
  getAlerts: () => 
    apiClient.get('/alerts')
};

// Cabins API
export const cabinsApi = {
  getAll: () => 
    apiClient.get('/cabins'),
  
  getOne: (cabinNo) => 
    apiClient.get(`/cabins/${cabinNo}`),
  
  assign: (cabinNo, data) => 
    apiClient.post(`/cabins/${cabinNo}/assign`, data),
  
  unassign: (cabinNo) => 
    apiClient.delete(`/cabins/${cabinNo}/unassign`)
};

// Students API
export const studentsApi = {
  getAll: () => 
    apiClient.get('/students')
};

// Reports API
export const reportsApi = {
  getAll: () => 
    apiClient.get('/reports'),
  
  generate: (data) => 
    apiClient.post('/reports/generate', data),
  
  download: (reportId) => 
    apiClient.get(`/reports/${reportId}/download`, { responseType: 'blob' }),
  
  send: (reportId) => 
    apiClient.post(`/reports/${reportId}/send`)
};

// Settings API
export const settingsApi = {
  getTelegramConfig: () => 
    apiClient.get('/settings/telegram'),
  
  updateTelegramConfig: (data) => 
    apiClient.put('/settings/telegram', data),
  
  getCameraConfigs: () => 
    apiClient.get('/settings/cameras'),
  
  addCamera: (data) => 
    apiClient.post('/settings/cameras', data),
  
  removeCamera: (cabinNo) => 
    apiClient.delete(`/settings/cameras/${cabinNo}`)
};

// Export all APIs
const api = {
  auth: authApi,
  stats: statsApi,
  cabins: cabinsApi,
  students: studentsApi,
  reports: reportsApi,
  settings: settingsApi
};

export default api;

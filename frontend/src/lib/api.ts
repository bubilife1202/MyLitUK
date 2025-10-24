import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: (data: { email: string; username: string; full_name: string; password: string; preferred_language: string }) =>
    api.post('/auth/register', data),
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  getMe: () => api.get('/auth/me'),
};

// Authors API
export const authorsApi = {
  list: (params?: { page?: number; size?: number; search?: string }) =>
    api.get('/authors', { params }),
  get: (id: number) => api.get(`/authors/${id}`),
  follow: (id: number) => api.post(`/authors/${id}/follow`),
  unfollow: (id: number) => api.delete(`/authors/${id}/follow`),
};

// Books API
export const booksApi = {
  list: (params?: { page?: number; size?: number; author_id?: number; genre?: string }) =>
    api.get('/books', { params }),
  get: (id: number) => api.get(`/books/${id}`),
  new: (params?: { page?: number; size?: number }) =>
    api.get('/books/new', { params }),
};

// Events API
export const eventsApi = {
  list: (params?: { page?: number; size?: number; search?: string; region?: string; event_type?: string; upcoming?: boolean }) =>
    api.get('/events', { params }),
  get: (id: number) => api.get(`/events/${id}`),
  follow: (id: number) => api.post(`/events/${id}/follow`),
  unfollow: (id: number) => api.delete(`/events/${id}/follow`),
};

// Awards API
export const awardsApi = {
  list: (params?: { page?: number; size?: number; search?: string; category?: string }) =>
    api.get('/awards', { params }),
  get: (id: number) => api.get(`/awards/${id}`),
  follow: (id: number) => api.post(`/awards/${id}/follow`),
  unfollow: (id: number) => api.delete(`/awards/${id}/follow`),
};

// Notifications API
export const notificationsApi = {
  list: (params?: { page?: number; size?: number; unread_only?: boolean }) =>
    api.get('/notifications', { params }),
  stats: () => api.get('/notifications/stats'),
  count: () => api.get('/notifications/count'),
  markAsRead: (id: number) => api.put(`/notifications/${id}/read`),
  markAllAsRead: () => api.post('/notifications/mark-all-read'),
  delete: (id: number) => api.delete(`/notifications/${id}`),
};

// Dashboard API
export const dashboardApi = {
  get: () => api.get('/dashboard'),
  today: () => api.get('/dashboard/today'),
  following: () => api.get('/dashboard/following'),
};

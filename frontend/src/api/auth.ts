import { apiClient, fetchCsrfToken } from './client';
import { User } from '../types/api';

export const authApi = {
  bootstrapCsrf: async (): Promise<string> => {
    return fetchCsrfToken();
  },

  getCurrentUser: async (): Promise<User> => {
    return apiClient<User>('/api/auth/me/');
  },

  login: async (credentials: { username: string; password: string }): Promise<User> => {
    return apiClient<User>('/api/auth/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  register: async (payload: { username: string; email?: string; password: string; password_confirm: string }): Promise<User> => {
    return apiClient<User>('/api/auth/register/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  logout: async (): Promise<{ detail: string }> => {
    return apiClient<{ detail: string }>('/api/auth/logout/', {
      method: 'POST',
    });
  },
};

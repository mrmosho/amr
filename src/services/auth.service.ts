import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export const authService = {
  async login(email: string, password: string) {
    const response = await axios.post(`${API_URL}/auth/login`, {
      email,
      password
    });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    return response.data;
  },

  async register(userData: {
    email: string;
    password: string;
    name: string;
  }) {
    return axios.post(`${API_URL}/auth/register`, userData);
  },

  logout() {
    localStorage.removeItem('token');
  }
};
import instanceOriginal from './api';
import type { AxiosInstance } from 'axios';

interface CustomAxiosInstance extends AxiosInstance {
  setToken: (token: string | null) => void;
  getToken: () => string | null;
  clearToken: () => void;
}

// Cast the runtime JS axios instance to our typed interface
const instance = instanceOriginal as unknown as CustomAxiosInstance;

export default instance;
export const setToken = (token: string | null) => instance.setToken(token);
export const getToken = () => instance.getToken();
export const clearToken = () => instance.clearToken();

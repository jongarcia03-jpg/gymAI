import { AxiosInstance } from 'axios';

interface CustomAxiosInstance extends AxiosInstance {
  setToken: (token: string | null) => void;
  getToken: () => string | null;
  clearToken: () => void;
}

declare const instance: CustomAxiosInstance;

export default instance;
export function setToken(token: string | null): void;
export function getToken(): string | null;
export function clearToken(): void;
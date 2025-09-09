import { LoginResponse, Transaction } from '../types';

const API_BASE = '/api';

class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'ApiError';
  }
}

const api = async (endpoint: string, options: RequestInit = {}) => {
  const token = localStorage.getItem('access_token');

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new ApiError(error.detail, response.status);
  }

  return response.json();
};

const authApi = {
  login: (username: string, password: string): Promise<LoginResponse> =>
    api('/login', { method: 'POST', body: JSON.stringify({ username, password }) })
};

const transactionsApi = {
  getTransactions: (): Promise<Transaction[]> => api('/transactions'),
  createTransaction: (data: Omit<Transaction, 'id'>): Promise<Transaction> =>
    api('/transactions', { method: 'POST', body: JSON.stringify(data) }),
  deleteTransaction: (id: string): Promise<void> =>
    api(`/transactions/${id}`, { method: 'DELETE' })
};

export { authApi, transactionsApi };

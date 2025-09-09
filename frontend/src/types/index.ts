import { FormEvent } from 'react';

export interface LoginResponse {
  username: string;
  access_token: string;
  message?: string;
}

export interface ErrorResponse {
  detail: string;
}

export interface Transaction {
  id: string;
  date: string;
  amount: number;
  type?: string;
}

export interface AlertProps {
  message: string;
  type: 'success' | 'danger';
  onClose: () => void;
}

export interface HeaderProps {
  username: string;
  onLogout: () => void;
  transactions: Transaction[];
}

export interface TransactionFormProps {
  onSubmit: (transaction: Omit<Transaction, 'id'>) => Promise<void>;
  isLoading?: boolean;
}

export interface TransactionListProps {
  transactions: Transaction[];
  onDelete: (id: string) => void;
}

export interface LoginFormProps {
  onSubmit: (e: FormEvent<HTMLFormElement>) => Promise<void>;
  isLoading: boolean;
}

import { useState, useEffect, useCallback } from 'react';
import { Transaction } from '../types';
import { transactionsApi } from '../services/api';

export function useTransactions(loggedIn: boolean) {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isAdding, setIsAdding] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');

  // Load transactions when user is logged in
  useEffect(() => {
    if (loggedIn) {
      loadTransactions();
    } else {
      setTransactions([]);
    }
  }, [loggedIn]);

  const loadTransactions = useCallback(async () => {
    setIsLoading(true);
    setError('');

    try {
      const transactionsData = await transactionsApi.getTransactions();
      setTransactions(transactionsData);
    } catch (error) {
      console.error('Load transactions error:', error);
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError('Failed to load transactions. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const addTransaction = useCallback(
    async (transactionData: Omit<Transaction, 'id'>): Promise<void> => {
      setIsAdding(true);
      setError('');

      try {
        const newTransaction =
          await transactionsApi.createTransaction(transactionData);
        setTransactions((prev) => [newTransaction, ...prev]);
        setSuccessMessage('Transaction added successfully!');
      } catch (error) {
        console.error('Add transaction error:', error);
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError('Failed to add transaction. Please try again.');
        }
        throw error;
      } finally {
        setIsAdding(false);
      }
    },
    []
  );

  const deleteTransaction = useCallback(async (id: string) => {
    try {
      await transactionsApi.deleteTransaction(id);
      setTransactions((prev) =>
        prev.filter((transaction) => transaction.id !== id)
      );
      setSuccessMessage('Transaction deleted successfully!');
    } catch (error) {
      console.error('Delete transaction error:', error);
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError('Failed to delete transaction. Please try again.');
      }
    }
  }, []);

  const clearError = useCallback(() => setError(''), []);
  const clearSuccessMessage = useCallback(() => setSuccessMessage(''), []);

  return {
    transactions,
    isLoading,
    isAdding,
    error,
    successMessage,
    addTransaction,
    deleteTransaction,
    clearError,
    clearSuccessMessage,
    refreshTransactions: loadTransactions,
  };
}

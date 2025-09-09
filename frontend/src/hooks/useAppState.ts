import { useAuth } from './useAuth';
import { useTransactions } from './useTransactions';

export const useAppState = () => {
  const auth = useAuth();
  const transactions = useTransactions(auth.loggedIn);

  return {
    auth,
    transactions,
    error: auth.error || transactions.error,
    successMessage: auth.successMessage || transactions.successMessage,
    clearError: () => {
      auth.clearError();
      transactions.clearError();
    },
    clearSuccessMessage: () => {
      auth.clearSuccessMessage();
      transactions.clearSuccessMessage();
    },
  };
};

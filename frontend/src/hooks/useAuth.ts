import { useState, useEffect, useCallback, FormEvent } from 'react';
import { useLocalStorage } from './useLocalStorage';
import { authApi } from '../services/api';

export function useAuth() {
  const [loggedIn, setLoggedIn] = useLocalStorage('loggedIn', false);
  const [username, setUsername] = useLocalStorage('username', '');
  const [accessToken, setAccessToken] = useLocalStorage('access_token', '');
  const [error, setError] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Clear messages after timeout
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(''), 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(''), 6000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  const handleLogin = useCallback(
    async (e: FormEvent<HTMLFormElement>): Promise<void> => {
      e.preventDefault();
      setIsLoading(true);
      setError('');

      const formData = new FormData(e.currentTarget);
      const usernameValue = formData.get('username') as string;
      const password = formData.get('password') as string;

      // Basic validation
      if (!usernameValue?.trim() || !password?.trim()) {
        setError('Username and password are required');
        setIsLoading(false);
        return;
      }

      try {
        const data = await authApi.login(usernameValue.trim(), password);

        setLoggedIn(true);
        setUsername(data.username);
        setAccessToken(data.access_token);

        if (data.message) {
          setSuccessMessage(data.message);
        }
      } catch (error) {
        console.error('Login error:', error);

        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError('Login failed. Please try again.');
        }
      } finally {
        setIsLoading(false);
      }
    },
    [setLoggedIn, setUsername, setAccessToken]
  );

  const handleLogout = useCallback((): void => {
    setLoggedIn(false);
    setUsername('');
    setAccessToken('');
    setSuccessMessage('Logged out successfully');
    setError('');
  }, [setLoggedIn, setUsername, setAccessToken]);

  const isAuthenticated = useCallback((): boolean => {
    return loggedIn && !!accessToken;
  }, [loggedIn, accessToken]);

  const clearSuccessMessage = useCallback(() => setSuccessMessage(''), []);
  const clearError = useCallback(() => setError(''), []);

  return {
    loggedIn,
    username,
    accessToken,
    error,
    successMessage,
    isLoading,
    handleLogin,
    handleLogout,
    isAuthenticated,
    clearSuccessMessage,
    clearError,
  };
}

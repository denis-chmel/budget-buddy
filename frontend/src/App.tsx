import React from 'react';
import './App.scss';
import { Alert } from './components/common/Alert';
import { Header } from './components/auth/Header';
import { LoginForm } from './components/auth/LoginForm';
import { TransactionForm } from './components/transactions/TransactionForm';
import { TransactionList } from './components/transactions/TransactionList';
import { useAppState } from './hooks/useAppState';

const App: React.FC = () => {
  const {
    auth,
    transactions,
    error,
    successMessage,
    clearError,
    clearSuccessMessage,
  } = useAppState();

  if (auth.loggedIn) {
    return (
      <div className="main-container">
        <Header
          username={auth.username}
          onLogout={auth.handleLogout}
          transactions={transactions.transactions}
        />

        {successMessage && (
          <Alert
            message={successMessage}
            type="success"
            onClose={clearSuccessMessage}
          />
        )}

        {error && <Alert message={error} type="danger" onClose={clearError} />}

        <TransactionForm
          onSubmit={transactions.addTransaction}
          isLoading={transactions.isAdding}
        />

        {transactions.isLoading ? (
          <div className="card">
            <div className="card-body text-center">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              <p className="mt-2 mb-0">Loading transactions...</p>
            </div>
          </div>
        ) : (
          <TransactionList
            transactions={transactions.transactions}
            onDelete={transactions.deleteTransaction}
          />
        )}
      </div>
    );
  }

  return (
    <div className="login-container">
      <div className="card">
        <div className="card-body">
          <h1 className="card-title text-center mb-4">Budget Buddy</h1>

          {error && (
            <Alert message={error} type="danger" onClose={clearError} />
          )}

          <LoginForm onSubmit={auth.handleLogin} isLoading={auth.isLoading} />
        </div>
      </div>
    </div>
  );
};

export default App;

import React from 'react';
import { LoginFormProps } from '../../types';
import { Alert } from '../common/Alert';

export const LoginForm: React.FC<LoginFormProps> = ({ onSubmit, error, isLoading }) => (
  <form onSubmit={onSubmit}>
    <div className="mb-3">
      <input
        type="text"
        name="username"
        className="form-control"
        placeholder="Username"
        required
        disabled={isLoading}
      />
    </div>
    <div className="mb-3">
      <input
        type="password"
        name="password"
        className="form-control"
        placeholder="Password"
        required
        disabled={isLoading}
      />
    </div>
    <button type="submit" className="btn btn-primary w-100" disabled={isLoading}>
      {isLoading ? 'Logging in...' : 'Log In'}
    </button>
    {error && <Alert message={error} type="danger" onClose={() => {}} />}
  </form>
);

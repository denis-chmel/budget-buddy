import React from 'react';
import { AlertProps } from '../../types';

export const Alert: React.FC<AlertProps> = ({ message, type, onClose }) => (
  <div
    className={`alert alert-${type} alert-dismissible fade show mt-3`}
    role="alert"
  >
    <strong>{message}</strong>
    <button
      type="button"
      className="btn-close"
      aria-label="Close"
      onClick={onClose}
    />
  </div>
);

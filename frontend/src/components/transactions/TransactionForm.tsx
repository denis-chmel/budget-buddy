import React, { useState, FormEvent } from 'react';
import { TransactionFormProps } from '../../types';

export const TransactionForm: React.FC<TransactionFormProps> = ({ onSubmit, isLoading = false }) => {
  const [date, setDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [amount, setAmount] = useState<string>('');
  const [type, setType] = useState<string>('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!date || !amount) {
      return;
    }

    const numAmount = parseFloat(amount);
    if (isNaN(numAmount)) {
      return;
    }

    try {
      await onSubmit({
        date,
        amount: numAmount,
        type: type.trim() || undefined
      });

      // Reset form only on success
      setAmount('');
      setType('');
    } catch (error) {
      // Error handling is done in parent component
      console.error('Failed to add transaction:', error);
    }
  };

  return (
    <div className="card mb-4">
      <div className="card-body">
        <h5 className="card-title mb-3">Add Transaction</h5>
        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col-md-3">
              <label htmlFor="date" className="form-label">Date</label>
              <input
                type="date"
                id="date"
                className="form-control"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            <div className="col-md-3">
              <label htmlFor="amount" className="form-label">Amount (USD)</label>
              <input
                type="number"
                id="amount"
                className="form-control"
                placeholder="Enter amount (+ or -)"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            <div className="col-md-4">
              <label htmlFor="type" className="form-label">Type (Optional)</label>
              <input
                type="text"
                id="type"
                className="form-control"
                placeholder="e.g., Food, Commute, Salary"
                value={type}
                onChange={(e) => setType(e.target.value)}
                disabled={isLoading}
              />
            </div>
            <div className="col-md-2">
              <br />
              <button type="submit" className="btn btn-primary mt-2 w-100" disabled={isLoading}>
                {isLoading ? 'Adding...' : 'Add'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

import React from 'react';
import { HeaderProps } from '../../types';
import { formatCurrency } from '../../utils/formatters';

export const Header: React.FC<HeaderProps> = ({
  username,
  onLogout,
  transactions,
}) => {
  const totalBalance = transactions.reduce(
    (sum, transaction) => sum + transaction.amount,
    0
  );

  const getTopSpending = () => {
    const spendingByType = transactions
      .filter((t) => t.amount < 0)
      .reduce(
        (acc, transaction) => {
          const type = transaction.type || 'other';
          acc[type] = (acc[type] || 0) + Math.abs(transaction.amount);
          return acc;
        },
        {} as Record<string, number>
      );

    return Object.entries(spendingByType)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5);
  };

  const topSpending = getTopSpending();

  return (
    <div className="card mb-4">
      <div className="card-body">
        {/* Header Section */}
        <div className="row">
          <div className="col-md-6">
            <h1 className="h4 mb-0 text-primary">Budget Buddy</h1>
          </div>

          <div className="col-md-6 text-end">
            <span className="text-muted me-3">👤 {username}</span>
            <button
              className="btn btn-outline-danger btn-sm"
              onClick={onLogout}
            >
              Log Out
            </button>
          </div>
        </div>

        {/* Stats Section */}
        <div className="row mt-3">
          <div className="col-md-12">
            <span className="text-muted">Balance:</span>
            <span className="h5 mb-0 fw-bold ms-2">
              {totalBalance >= 0 ? (
                <span className="text-success">
                  {formatCurrency(totalBalance)}
                </span>
              ) : (
                <span className="text-danger">
                  -{formatCurrency(-totalBalance)}
                </span>
              )}
            </span>
          </div>

          {topSpending.length > 0 && (
            <div className="col-md-12 mt-2">
              <span className="text-muted me-2">Top spendings:</span>

              {topSpending.map(([type, amount]) => (
                <span key={type} className="badge bg-light text-dark">
                  {formatCurrency(amount)} on {type}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

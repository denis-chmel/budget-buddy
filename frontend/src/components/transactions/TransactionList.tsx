import React from 'react';
import { TransactionListProps } from '../../types';
import { formatCurrency, formatDate } from '../../utils/formatters';

export const TransactionList: React.FC<TransactionListProps> = ({ transactions, onDelete }) => {

  const handleDelete = (id: string, amount: number, type?: string) => {
    const confirmMessage = `Are you sure you want to delete this transaction?\n\nAmount: ${formatCurrency(amount)}${type ? `\nType: ${type}` : ''}`;
    if (window.confirm(confirmMessage)) {
      onDelete(id);
    }
  };

  if (transactions.length === 0) {
    return (
      <div className="card">
        <div className="card-body text-center">
          <h5 className="card-title">No Transactions</h5>
          <p className="text-muted">Add your first transaction above to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title mb-3">Transactions</h5>
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Date</th>
                <th>Amount</th>
                <th>Type</th>
                <th style={{width: '20px'}}></th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((transaction) => (
                <tr key={transaction.id}>
                  <td>{formatDate(transaction.date)}</td>
                  <td>
                    <span className={`fw-bold`}>
                        {transaction.amount >= 0
                        ? <span className="text-success">{formatCurrency(transaction.amount)}</span>
                        : <span className="text-danger">({formatCurrency(-transaction.amount)})</span>
                    }
                    </span>
                  </td>
                  <td>{transaction.type || <span className="text-muted">—</span>}</td>
                  <td>
                    <button
                      className="btn btn--danger btn-sm"
                      onClick={() => handleDelete(transaction.id, transaction.amount, transaction.type)}
                      title="Delete transaction"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export const formatCurrency = (amount: number): string => {
  const formatted = amount.toFixed(2);
  return '$' + formatted;
};

export const formatDate = (dateString: string): string => {
  const [year, month, day] = dateString.split('-').map(Number);
  const date = new Date(year, month - 1, day);
  return date.toLocaleDateString();
};

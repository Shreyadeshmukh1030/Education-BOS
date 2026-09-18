import React from 'react';

export const Badge = ({ children, status = 'neutral', className = '' }) => {
  const colors = {
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
    primary: 'bg-indigo-100 text-indigo-800',
    neutral: 'bg-gray-100 text-gray-800'
  };

  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${colors[status]} ${className}`}>
      {children}
    </span>
  );
};

import React from 'react';

export const Card = ({ children, className = '' }) => {
  return (
    <div className={`bg-surface-card overflow-hidden rounded-lg shadow ring-1 ring-black ring-opacity-5 ${className}`}>
      {children}
    </div>
  );
};

export const CardHeader = ({ children, className = '' }) => (
  <div className={`px-4 py-5 sm:px-6 border-b border-gray-200 ${className}`}>
    {children}
  </div>
);

export const CardContent = ({ children, className = '' }) => (
  <div className={`px-4 py-5 sm:p-6 ${className}`}>
    {children}
  </div>
);

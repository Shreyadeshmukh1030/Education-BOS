import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useModules } from '../contexts/ModuleContext';
import { ShieldAlert } from 'lucide-react';

const RequireModule = ({ moduleKey, children }) => {
  const { hasModule, loading } = useModules();
  const location = useLocation();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!hasModule(moduleKey)) {
    return (
      <div className="flex flex-col items-center justify-center h-[70vh]">
        <ShieldAlert className="w-16 h-16 text-red-500 mb-4" />
        <h2 className="text-2xl font-bold text-gray-800">Module Disabled</h2>
        <p className="text-gray-600 mt-2 text-center max-w-md">
          The <strong>{moduleKey}</strong> module is either not installed or disabled for your organization.
        </p>
      </div>
    );
  }

  return children;
};

export default RequireModule;

import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from './AuthContext';

const ModuleContext = createContext(null);

export const ModuleProvider = ({ children }) => {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const fetchModules = async () => {
      if (!isAuthenticated) {
        setModules([]);
        setLoading(false);
        return;
      }
      
      try {
        const response = await api.get('/core/modules/');
        // For now we assume all returned modules are enabled globally.
        // In the future this will fetch from /core/organization-modules/ 
        // to filter by current organization.
        // Filter for only actively enabled modules to drive UI visibility
        const allModules = response.data.results || response.data;
        setModules(allModules.filter(m => m.is_active));
      } catch (error) {
        console.error('Failed to fetch modules', error);
      } finally {
        setLoading(false);
      }
    };

    fetchModules();
  }, [isAuthenticated]);

  const hasModule = (moduleKey) => {
    return modules.some(m => m.key === moduleKey);
  };

  const value = {
    modules,
    loading,
    hasModule
  };

  return <ModuleContext.Provider value={value}>{children}</ModuleContext.Provider>;
};

export const useModules = () => {
  const context = useContext(ModuleContext);
  if (!context) {
    throw new Error('useModules must be used within a ModuleProvider');
  }
  return context;
};

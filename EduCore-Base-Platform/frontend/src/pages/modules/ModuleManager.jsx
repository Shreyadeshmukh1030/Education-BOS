import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AlertCircle } from 'lucide-react';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const ModuleManager = () => {
  const queryClient = useQueryClient();

  const { data: modulesData, isLoading, isError } = useQuery({
    queryKey: queryKeys.core_modules.all,
    queryFn: async () => {
      const response = await api.get('core/modules/');
      return response.data.results || response.data;
    }
  });

  const toggleMutation = useMutation({
    mutationFn: async ({ id, is_active }) => {
      // Patch the is_active state of the ModuleDefinition
      const response = await api.patch(`core/modules/${id}/`, {
        is_active: is_active
      });
      return response.data;
    },
    onSuccess: () => {
      // Invalidate the local cache
      queryClient.invalidateQueries({ queryKey: queryKeys.core_modules.all });
      // We must reload the page so the ModuleProvider re-fetches its global state
      // ensuring the Sidebar and Route Guards update instantly.
      window.location.reload();
    },
    onError: (err) => {
      console.error('Failed to toggle module', err);
      alert('Failed to toggle module state.');
    }
  });

  const toggleModule = (module) => {
    if (module.is_core) return;
    toggleMutation.mutate({
      id: module.id,
      is_active: !module.is_active
    });
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center p-24">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-red-500 bg-red-50 rounded-lg border border-red-100">
        <AlertCircle className="h-8 w-8 mb-2" />
        <p>Failed to load core modules. Please check your connection.</p>
      </div>
    );
  }

  const modules = modulesData || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Module Manager</h1>
        <p className="mt-2 text-sm text-gray-700">Enable or disable features across the platform.</p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {modules.map((module) => (
          <Card key={module.key} className={module.is_active ? 'border-primary-500 ring-1 ring-primary-500' : ''}>
            <CardContent className="h-full flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-medium text-gray-900">{module.name}</h3>
                  {module.is_core && <Badge status="neutral">Required</Badge>}
                </div>
                <p className="text-sm text-gray-500 mb-6">
                  {module.description}
                  <br />
                  <br />
                  <span className="font-semibold">{module.is_active ? 'Currently Active.' : 'Currently Disabled.'}</span>
                </p>
              </div>
              <div className="flex justify-between items-center">
                <button
                  onClick={() => toggleModule(module)}
                  disabled={module.is_core || toggleMutation.isPending}
                  className={`
                    relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
                    ${module.is_active ? 'bg-primary-600' : 'bg-gray-200'}
                    ${(module.is_core || toggleMutation.isPending) ? 'opacity-50 cursor-not-allowed' : ''}
                  `}
                >
                  <span className="sr-only">Use setting</span>
                  <span
                    className={`
                      pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out
                      ${module.is_active ? 'translate-x-5' : 'translate-x-0'}
                    `}
                  />
                </button>
                {toggleMutation.variables?.id === module.id && toggleMutation.isPending && (
                  <span className="text-xs text-gray-400">Saving...</span>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

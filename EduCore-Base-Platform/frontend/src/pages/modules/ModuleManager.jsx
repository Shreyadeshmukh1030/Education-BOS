import React, { useState } from 'react';
import { Card, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { MODULES } from '../../configuration/modules';

export const ModuleManager = () => {
  const [modules, setModules] = useState(MODULES);

  const toggleModule = (key) => {
    if (modules[key].required) return;
    setModules({
      ...modules,
      [key]: {
        ...modules[key],
        enabled: !modules[key].enabled
      }
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Module Manager</h1>
        <p className="mt-2 text-sm text-gray-700">Enable or disable features across the platform.</p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {Object.entries(modules).map(([key, module]) => (
          <Card key={key} className={module.enabled ? 'border-primary-500 ring-1 ring-primary-500' : ''}>
            <CardContent className="h-full flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-medium text-gray-900">{module.name}</h3>
                  {module.required && <Badge status="neutral">Required</Badge>}
                </div>
                <p className="text-sm text-gray-500 mb-6">
                  {module.enabled ? 'This module is currently active and available to users.' : 'This module is disabled.'}
                </p>
              </div>
              <div>
                <button
                  onClick={() => toggleModule(key)}
                  disabled={module.required}
                  className={`
                    relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
                    ${module.enabled ? 'bg-primary-600' : 'bg-gray-200'}
                    ${module.required ? 'opacity-50 cursor-not-allowed' : ''}
                  `}
                >
                  <span className="sr-only">Use setting</span>
                  <span
                    className={`
                      pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out
                      ${module.enabled ? 'translate-x-5' : 'translate-x-0'}
                    `}
                  />
                </button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

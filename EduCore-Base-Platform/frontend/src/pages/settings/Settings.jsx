import React from 'react';
import { Card, CardContent } from '../../components/ui/Card';

export const Settings = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Platform Settings</h1>
        <p className="mt-2 text-sm text-gray-700">Configure global platform settings, branding, and defaults.</p>
      </div>

      <Card>
        <CardContent>
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900 border-b pb-2">Branding</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">Institution Name</label>
                <input type="text" defaultValue="EduCore Foundation" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Primary Color</label>
                <input type="color" defaultValue="#4f46e5" className="mt-1 block h-10 w-full rounded-md border-gray-300 shadow-sm" />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

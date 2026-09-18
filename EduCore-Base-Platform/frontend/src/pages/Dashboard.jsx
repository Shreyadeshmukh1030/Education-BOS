import React from 'react';
import { Card, CardContent } from '../components/ui/Card';
import { Users, GraduationCap, Building, CalendarCheck } from 'lucide-react';

export const Dashboard = () => {
  const stats = [
    { name: 'Total Learners', stat: '12,450', icon: Users, change: '12%', changeType: 'increase' },
    { name: 'Active Instructors', stat: '428', icon: GraduationCap, change: '2.5%', changeType: 'increase' },
    { name: 'Active Programs', stat: '36', icon: Building, change: '0%', changeType: 'neutral' },
    { name: 'Attendance Rate', stat: '87.4%', icon: CalendarCheck, change: '1.2%', changeType: 'decrease' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Good Morning, Admin 👋</h1>
        <p className="mt-1 text-sm text-gray-500">Here's what's happening across your institution today.</p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => (
          <Card key={item.name}>
            <CardContent>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <item.icon className="h-6 w-6 text-gray-400" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{item.name}</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{item.stat}</div>
                      <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                        item.changeType === 'increase' ? 'text-green-600' : item.changeType === 'decrease' ? 'text-red-600' : 'text-gray-500'
                      }`}>
                        {item.changeType === 'increase' ? '↑' : item.changeType === 'decrease' ? '↓' : ''}
                        <span className="ml-1">{item.change}</span>
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Card className="h-96">
          <CardContent className="h-full flex flex-col">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Enrollment Overview</h3>
            <div className="flex-1 bg-gray-50 rounded border border-dashed border-gray-300 flex items-center justify-center">
              <span className="text-gray-400">[ Chart Placeholder ]</span>
            </div>
          </CardContent>
        </Card>
        <Card className="h-96">
          <CardContent className="h-full flex flex-col">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Upcoming Activities</h3>
            <div className="flex-1 bg-gray-50 rounded border border-dashed border-gray-300 flex items-center justify-center">
              <span className="text-gray-400">[ Timeline Placeholder ]</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

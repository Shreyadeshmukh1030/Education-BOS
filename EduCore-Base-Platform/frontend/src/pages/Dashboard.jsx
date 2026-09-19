import React from 'react';
import { useQueries } from '@tanstack/react-query';
import { Card, CardContent } from '../components/ui/Card';
import { Users, GraduationCap, Building, CalendarCheck, AlertCircle } from 'lucide-react';
import api from '../services/api';
import { queryKeys } from '../services/queries';

export const Dashboard = () => {
  const fetchStats = async (endpoint) => {
    const response = await api.get(`${endpoint}stats/`);
    return response.data;
  };

  const results = useQueries({
    queries: [
      {
        queryKey: queryKeys.stats.model('learners'),
        queryFn: () => fetchStats('people/studentprofiles/')
      },
      {
        queryKey: queryKeys.stats.model('instructors'),
        queryFn: () => fetchStats('people/instructorprofiles/')
      },
      {
        queryKey: queryKeys.stats.model('programs'),
        queryFn: () => fetchStats('academics/programs/')
      }
    ]
  });

  const isLoading = results.some(result => result.isLoading);
  const isError = results.some(result => result.isError);

  const [learnersData, instructorsData, programsData] = results.map(r => r.data || { total: 0, active: 0 });

  const stats = [
    { name: 'Total Learners', stat: learnersData.total, icon: Users, change: 'Active: ' + learnersData.active, changeType: 'increase' },
    { name: 'Active Instructors', stat: instructorsData.total, icon: GraduationCap, change: 'Active: ' + instructorsData.active, changeType: 'increase' },
    { name: 'Active Programs', stat: programsData.total, icon: Building, change: 'Active: ' + programsData.active, changeType: 'neutral' },
    { name: 'Attendance Rate', stat: '87.4%', icon: CalendarCheck, change: '↓ 1.2%', changeType: 'decrease' },
  ];

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
        <p>Failed to load dashboard metrics. Please check your connection.</p>
      </div>
    );
  }

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
                    <dd className="flex items-baseline mt-1">
                      <div className="text-2xl font-semibold text-gray-900">{item.stat}</div>
                      <div className={`ml-3 flex items-baseline text-xs font-medium ${
                        item.changeType === 'increase' ? 'text-green-600' : item.changeType === 'decrease' ? 'text-red-600' : 'text-gray-500'
                      }`}>
                        <span className="ml-1 bg-gray-100 px-2 py-0.5 rounded-full">{item.change}</span>
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

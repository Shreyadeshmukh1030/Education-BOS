import React from 'react';
import { DataTable } from '../../components/data-display/DataTable';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Plus } from 'lucide-react';

const mockPrograms = [
  { id: 'PRG001', name: 'B.Tech Computer Science', duration: '4 Years', type: 'Degree', status: 'active' },
  { id: 'PRG002', name: 'Data Science Bootcamp', duration: '6 Months', type: 'Certificate', status: 'active' },
  { id: 'PRG003', name: 'Class 10 CBSE', duration: '1 Year', type: 'Schooling', status: 'active' },
];

export const ProgramList = () => {
  const columns = [
    { header: 'Program Name', accessor: 'name', primary: true },
    { header: 'Program ID', accessor: 'id' },
    { header: 'Duration', accessor: 'duration' },
    { header: 'Type', accessor: 'type' },
    { 
      header: 'Status', 
      accessor: 'status',
      render: (row) => (
        <Badge status={row.status === 'active' ? 'success' : 'neutral'}>
          {row.status.charAt(0).toUpperCase() + row.status.slice(1)}
        </Badge>
      )
    },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Academic Programs</h1>
          <p className="mt-2 text-sm text-gray-700">Design and manage courses, degrees, and academic structures.</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Button variant="primary">
            <Plus className="h-4 w-4 mr-2" />
            Create Program
          </Button>
        </div>
      </div>

      <DataTable 
        columns={columns} 
        data={mockPrograms} 
        searchPlaceholder="Search programs..."
      />
    </div>
  );
};

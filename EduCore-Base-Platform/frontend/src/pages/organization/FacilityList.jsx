import React from 'react';
import { DataTable } from '../../components/data-display/DataTable';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Plus } from 'lucide-react';

const mockFacilities = [
  { id: 'FAC01', name: 'Main Campus', type: 'Campus', capacity: 5000, status: 'active' },
  { id: 'FAC02', name: 'Science Block', type: 'Building', capacity: 800, status: 'active' },
  { id: 'FAC03', name: 'Library', type: 'Building', capacity: 300, status: 'maintenance' },
  { id: 'FAC04', name: 'Room 101', type: 'Room', capacity: 40, status: 'active' },
];

export const FacilityList = () => {
  const columns = [
    { header: 'Name', accessor: 'name', primary: true },
    { header: 'ID', accessor: 'id' },
    { header: 'Type', accessor: 'type' },
    { header: 'Capacity', accessor: 'capacity' },
    { 
      header: 'Status', 
      accessor: 'status',
      render: (row) => (
        <Badge status={row.status === 'active' ? 'success' : 'warning'}>
          {row.status.charAt(0).toUpperCase() + row.status.slice(1)}
        </Badge>
      )
    },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Organization & Facilities</h1>
          <p className="mt-2 text-sm text-gray-700">Manage campuses, buildings, and rooms.</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Button variant="primary">
            <Plus className="h-4 w-4 mr-2" />
            Add Facility
          </Button>
        </div>
      </div>

      <DataTable 
        columns={columns} 
        data={mockFacilities} 
        searchPlaceholder="Search facilities..."
      />
    </div>
  );
};

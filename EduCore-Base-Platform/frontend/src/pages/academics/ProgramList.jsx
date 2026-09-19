import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { DataTable } from '../../components/data-display/DataTable';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Plus, AlertCircle } from 'lucide-react';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const ProgramList = () => {
  const navigate = useNavigate();

  const { data, isLoading, isError } = useQuery({
    queryKey: queryKeys.programs.all,
    queryFn: async () => {
      const response = await api.get('academics/programs/');
      return response.data.results || response.data;
    }
  });

  const columns = [
    { header: 'Program Name', accessor: 'name', primary: true },
    { header: 'Program Code', accessor: 'code' },
    { header: 'Duration', accessor: 'duration' },
    { 
      header: 'Level', 
      accessor: 'level',
      render: (row) => row.level || 'Not Specified'
    },
    { 
      header: 'Status', 
      accessor: 'status',
      render: (row) => (
        <Badge status={row.status === 'active' ? 'success' : 'neutral'}>
          {row.status ? (row.status.charAt(0).toUpperCase() + row.status.slice(1)) : 'Unknown'}
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
          <Button variant="primary" onClick={() => navigate('/academics/add')}>
            <Plus className="h-4 w-4 mr-2" />
            Create Program
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center p-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      ) : isError ? (
        <div className="flex flex-col items-center justify-center p-12 text-red-500 bg-red-50 rounded-lg border border-red-100">
          <AlertCircle className="h-8 w-8 mb-2" />
          <p>Failed to load programs. Please check your connection.</p>
        </div>
      ) : (
        <DataTable 
          columns={columns} 
          data={data || []} 
          searchPlaceholder="Search programs..."
        />
      )}
    </div>
  );
};

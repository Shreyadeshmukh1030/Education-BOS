import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { DataTable } from '../../components/data-display/DataTable';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Plus, AlertCircle } from 'lucide-react';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const FacilityList = () => {
  const navigate = useNavigate();

  const { data, isLoading, isError } = useQuery({
    queryKey: queryKeys.campuses.all,
    queryFn: async () => {
      const response = await api.get('organizations/campuses/');
      return response.data.results || response.data;
    }
  });

  const columns = [
    { header: 'Campus Name', accessor: 'name', primary: true },
    { header: 'ID', accessor: 'id' },
    { 
      header: 'Address', 
      accessor: 'address',
      render: (row) => row.address || 'N/A'
    },
    { 
      header: 'Status', 
      accessor: 'is_active',
      render: (row) => (
        <Badge status={row.is_active ? 'success' : 'neutral'}>
          {row.is_active ? 'Active' : 'Archived'}
        </Badge>
      )
    },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Organization & Campuses</h1>
          <p className="mt-2 text-sm text-gray-700">Manage your institution's physical campuses and branches.</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Button variant="primary" onClick={() => navigate('/organization/add-campus')}>
            <Plus className="h-4 w-4 mr-2" />
            Add Campus
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
          <p>Failed to load campuses. Please check your connection.</p>
        </div>
      ) : (
        <DataTable 
          columns={columns} 
          data={data || []} 
          searchPlaceholder="Search campuses..."
        />
      )}
    </div>
  );
};

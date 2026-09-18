import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { DataTable } from '../../components/data-display/DataTable';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Plus } from 'lucide-react';
import api from '../../services/api';

export const LearnerList = () => {
  const navigate = useNavigate();
  const [learners, setLearners] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('people/learners/')
      .then(res => {
        setLearners(res.data.results || res.data); // Handle pagination if enabled
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch learners", err);
        setLoading(false);
      });
  }, []);

  const columns = [
    { header: 'Name', accessor: 'name', primary: true },
    { header: 'ID', accessor: 'id' },
    { header: 'Program', accessor: 'program' },
    { header: 'Group', accessor: 'group' },
    { 
      header: 'Status', 
      accessor: 'status',
      render: (row) => (
        <Badge status={
          row.status === 'active' ? 'success' : 
          row.status === 'inactive' ? 'neutral' : 'warning'
        }>
          {row.status.charAt(0).toUpperCase() + row.status.slice(1)}
        </Badge>
      )
    },
    { header: 'Joined', accessor: 'joined' },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Learners</h1>
          <p className="mt-2 text-sm text-gray-700">Manage all enrolled learners across your institution.</p>
        </div>
        <div className="mt-4 sm:mt-0 flex gap-3">
          <Button variant="secondary">Import</Button>
          <Button variant="primary" onClick={() => navigate('/people/learners/add')}>
            <Plus className="h-4 w-4 mr-2" />
            Add Learner
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center p-8"><p>Loading learners from database...</p></div>
      ) : (
        <DataTable 
          columns={columns} 
          data={learners} 
          onRowClick={(row) => navigate(`/people/learners/${row.id}`)}
          searchPlaceholder="Search learners..."
        />
      )}
    </div>
  );
};

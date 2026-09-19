import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const AddCampus = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    name: '',
    address: ''
  });

  const [error, setError] = useState(null);

  const createCampusMutation = useMutation({
    mutationFn: async (data) => {
      // Create Campus
      const response = await api.post('organizations/campuses/', {
        name: data.name,
        address: data.address,
        organization: 1 // Default organization ID for now
      });
      
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.campuses.all });
      navigate('/organization');
    },
    onError: (err) => {
      setError(err.response?.data?.detail || "An error occurred while saving the campus.");
      console.error(err);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);
    createCampusMutation.mutate(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <button 
        onClick={() => navigate('/organization')}
        className="flex items-center text-sm font-medium text-gray-500 hover:text-gray-900"
      >
        <ArrowLeft className="h-4 w-4 mr-1" />
        Back to Campuses
      </button>

      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Add New Campus</h1>
        <p className="mt-2 text-sm text-gray-700">Register a new physical branch or campus for the institution.</p>
      </div>

      <div className="bg-white shadow sm:rounded-lg">
        <form onSubmit={handleSubmit}>
          <div className="px-4 py-5 sm:p-6 border-b border-gray-200">
            {error && (
              <div className="mb-6 p-4 rounded-md bg-red-50 border border-red-200 flex text-red-700 items-center">
                <AlertCircle className="h-5 w-5 mr-2" />
                <span className="text-sm">{error}</span>
              </div>
            )}

            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
              <div className="sm:col-span-6">
                <label className="block text-sm font-medium text-gray-700">Campus Name *</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="e.g. North Campus"
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-6">
                <label className="block text-sm font-medium text-gray-700">Address</label>
                <div className="mt-1">
                  <textarea 
                    name="address"
                    rows={3}
                    value={formData.address}
                    onChange={handleChange}
                    placeholder="Physical address of the campus"
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
            <Button 
              type="button" 
              variant="secondary" 
              className="mr-3" 
              onClick={() => navigate('/organization')}
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              variant="primary"
              disabled={createCampusMutation.isPending}
            >
              {createCampusMutation.isPending ? 'Saving...' : 'Save Campus'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

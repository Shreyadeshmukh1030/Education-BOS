import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const AddProgram = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    level: 'Undergraduate',
    duration: '4 Years',
    status: 'active'
  });

  const [error, setError] = useState(null);

  const createProgramMutation = useMutation({
    mutationFn: async (data) => {
      // Create Program
      const response = await api.post('academics/programs/', {
        name: data.name,
        code: data.code,
        description: data.description,
        level: data.level,
        duration: data.duration,
        status: data.status,
        organization: 1 // Default organization ID for now
      });
      
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.programs.all });
      navigate('/academics');
    },
    onError: (err) => {
      setError(err.response?.data?.detail || "An error occurred while saving the program.");
      console.error(err);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);
    createProgramMutation.mutate(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <button 
        onClick={() => navigate('/academics')}
        className="flex items-center text-sm font-medium text-gray-500 hover:text-gray-900"
      >
        <ArrowLeft className="h-4 w-4 mr-1" />
        Back to Programs
      </button>

      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Add New Program</h1>
        <p className="mt-2 text-sm text-gray-700">Design a new academic structure or course.</p>
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
              <div className="sm:col-span-4">
                <label className="block text-sm font-medium text-gray-700">Program Name *</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="e.g. B.Tech Computer Science"
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-2">
                <label className="block text-sm font-medium text-gray-700">Program Code *</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="code"
                    required
                    value={formData.code}
                    onChange={handleChange}
                    placeholder="e.g. CS101"
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Level</label>
                <div className="mt-1">
                  <select 
                    name="level"
                    value={formData.level}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border bg-white" 
                  >
                    <option value="Undergraduate">Undergraduate</option>
                    <option value="Postgraduate">Postgraduate</option>
                    <option value="Certificate">Certificate</option>
                    <option value="Diploma">Diploma</option>
                    <option value="Schooling">Schooling</option>
                  </select>
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Duration</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="duration"
                    value={formData.duration}
                    onChange={handleChange}
                    placeholder="e.g. 4 Years"
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>
              
              <div className="sm:col-span-6">
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <div className="mt-1">
                  <textarea 
                    name="description"
                    rows={3}
                    value={formData.description}
                    onChange={handleChange}
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
              onClick={() => navigate('/academics')}
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              variant="primary"
              disabled={createProgramMutation.isPending}
            >
              {createProgramMutation.isPending ? 'Saving...' : 'Save Program'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const AddLearner = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    studentId: `STU-${Math.floor(1000 + Math.random() * 9000)}`
  });

  const [error, setError] = useState(null);

  const createLearnerMutation = useMutation({
    mutationFn: async (data) => {
      // 1. Create Person
      const personRes = await api.post('people/persons/', {
        first_name: data.firstName,
        last_name: data.lastName,
        email: data.email,
        phone: data.phone,
      });
      
      const personId = personRes.data.id;

      // 2. Create StudentProfile
      // We assume organization ID 1 exists because we seeded the DB with "Default EduCore Institute"
      const profileRes = await api.post('people/studentprofiles/', {
        person: personId,
        student_id: data.studentId,
        organization: 1,
        status: 'active'
      });

      return profileRes.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.learners.all });
      navigate('/people/learners');
    },
    onError: (err) => {
      setError(err.response?.data?.detail || "An error occurred while saving the learner.");
      console.error(err);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);
    createLearnerMutation.mutate(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <button 
        onClick={() => navigate('/people/learners')}
        className="flex items-center text-sm font-medium text-gray-500 hover:text-gray-900"
      >
        <ArrowLeft className="h-4 w-4 mr-1" />
        Back to Learners
      </button>

      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Add New Learner</h1>
        <p className="mt-2 text-sm text-gray-700">Enter the details to onboard a new learner to the platform.</p>
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
              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">First name *</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="firstName"
                    required
                    value={formData.firstName}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Last name *</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="lastName"
                    required
                    value={formData.lastName}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Email address</label>
                <div className="mt-1">
                  <input 
                    type="email" 
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Phone</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>
              
              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Student ID (Auto-generated)</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="studentId"
                    readOnly
                    value={formData.studentId}
                    className="block w-full rounded-md border-gray-200 bg-gray-50 shadow-sm text-gray-500 sm:text-sm px-3 py-2 border cursor-not-allowed" 
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
              onClick={() => navigate('/people/learners')}
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              variant="primary"
              disabled={createLearnerMutation.isPending}
            >
              {createLearnerMutation.isPending ? 'Saving...' : 'Save Learner'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const AddExam = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    name: '',
    date: '',
    max_marks: 100,
    passing_marks: 40
  });

  const [error, setError] = useState(null);

  const createAssessmentMutation = useMutation({
    mutationFn: async (data) => {
      // Create Assessment
      const response = await api.post('assessment/assessments/', {
        name: data.name,
        date: data.date || null,
        max_marks: parseFloat(data.max_marks),
        passing_marks: parseFloat(data.passing_marks),
        subject_offering: 1 // Hardcoded to the dummy SubjectOffering for Phase 6
      });
      
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.assessments.all });
      navigate('/assessments');
    },
    onError: (err) => {
      setError(err.response?.data?.detail || "An error occurred while scheduling the assessment.");
      console.error(err);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);
    createAssessmentMutation.mutate(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <button 
        onClick={() => navigate('/assessments')}
        className="flex items-center text-sm font-medium text-gray-500 hover:text-gray-900"
      >
        <ArrowLeft className="h-4 w-4 mr-1" />
        Back to Assessments
      </button>

      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Schedule Assessment</h1>
        <p className="mt-2 text-sm text-gray-700">Create a new exam, quiz, or assignment for a subject.</p>
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
                <label className="block text-sm font-medium text-gray-700">Assessment Name *</label>
                <div className="mt-1">
                  <input 
                    type="text" 
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="e.g. Midterm Physics"
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-2">
                <label className="block text-sm font-medium text-gray-700">Date</label>
                <div className="mt-1">
                  <input 
                    type="date" 
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border text-gray-700" 
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Max Marks *</label>
                <div className="mt-1">
                  <input 
                    type="number" 
                    name="max_marks"
                    required
                    step="0.01"
                    min="0"
                    value={formData.max_marks}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Passing Marks</label>
                <div className="mt-1">
                  <input 
                    type="number" 
                    name="passing_marks"
                    step="0.01"
                    min="0"
                    value={formData.passing_marks}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-6 bg-blue-50 p-4 rounded-md text-sm text-blue-700 border border-blue-100">
                <p><strong>Note:</strong> For Phase 6 testing, this assessment will automatically be assigned to the dummy Subject Offering (ID: 1).</p>
              </div>
            </div>
          </div>
          <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
            <Button 
              type="button" 
              variant="secondary" 
              className="mr-3" 
              onClick={() => navigate('/assessments')}
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              variant="primary"
              disabled={createAssessmentMutation.isPending}
            >
              {createAssessmentMutation.isPending ? 'Scheduling...' : 'Schedule Exam'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

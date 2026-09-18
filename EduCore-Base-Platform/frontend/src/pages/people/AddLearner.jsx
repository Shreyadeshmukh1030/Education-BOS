import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const AddLearner = () => {
  const navigate = useNavigate();

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
        <div className="px-4 py-5 sm:p-6 border-b border-gray-200">
          <div className="flex justify-between items-center mb-8">
            <div className="flex space-x-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-600 text-white font-semibold">1</span>
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-200 text-gray-600 font-semibold">2</span>
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-200 text-gray-600 font-semibold">3</span>
            </div>
            <span className="text-sm font-medium text-gray-500">Step 1: Basic Information</span>
          </div>

          <form className="space-y-6">
            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">First name</label>
                <div className="mt-1">
                  <input type="text" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Last name</label>
                <div className="mt-1">
                  <input type="text" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" />
                </div>
              </div>

              <div className="sm:col-span-4">
                <label className="block text-sm font-medium text-gray-700">Email address</label>
                <div className="mt-1">
                  <input type="email" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border" />
                </div>
              </div>
            </div>
          </form>
        </div>
        <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
          <Button variant="secondary" className="mr-3" onClick={() => navigate('/people/learners')}>Cancel</Button>
          <Button variant="primary">Next Step</Button>
        </div>
      </div>
    </div>
  );
};

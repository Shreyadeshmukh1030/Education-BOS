import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Tabs } from '../../components/ui/Tabs';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { ArrowLeft, Edit } from 'lucide-react';

export const LearnerProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'academic', label: 'Academic' },
    { id: 'attendance', label: 'Attendance' },
    { id: 'assessments', label: 'Assessments' },
    { id: 'payments', label: 'Payments' },
    { id: 'activity', label: 'Activity' },
  ];

  return (
    <div className="space-y-6">
      <button 
        onClick={() => navigate('/people/learners')}
        className="flex items-center text-sm font-medium text-gray-500 hover:text-gray-900"
      >
        <ArrowLeft className="h-4 w-4 mr-1" />
        Back to Learners
      </button>

      <div className="bg-white shadow sm:rounded-lg overflow-hidden">
        <div className="px-4 py-5 sm:px-6 flex justify-between items-start">
          <div className="flex items-center space-x-5">
            <div className="h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center text-2xl font-bold text-primary-700">
              A
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900 flex items-center gap-3">
                Aarav Sharma
                <Badge status="success">Active</Badge>
              </h2>
              <p className="text-sm font-medium text-gray-500">{id || 'LRN001'}</p>
            </div>
          </div>
          <div className="flex space-x-3">
            <Button variant="secondary">More Actions</Button>
            <Button variant="primary">
              <Edit className="h-4 w-4 mr-2" />
              Edit Profile
            </Button>
          </div>
        </div>
        
        <div className="px-4 sm:px-6">
          <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />
        </div>
        
        <div className="px-4 py-5 sm:p-6 bg-gray-50 min-h-[400px]">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-5 rounded-lg border border-gray-200">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Basic Information</h3>
                <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Email</dt>
                    <dd className="mt-1 text-sm text-gray-900">aarav.sharma@example.com</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Phone</dt>
                    <dd className="mt-1 text-sm text-gray-900">+1 (555) 123-4567</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Date of Birth</dt>
                    <dd className="mt-1 text-sm text-gray-900">15 May 2004</dd>
                  </div>
                </dl>
              </div>
              <div className="bg-white p-5 rounded-lg border border-gray-200">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Enrollment Summary</h3>
                <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                  <div className="sm:col-span-2">
                    <dt className="text-sm font-medium text-gray-500">Program</dt>
                    <dd className="mt-1 text-sm text-gray-900 font-medium">B.Tech Computer Science</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Group/Batch</dt>
                    <dd className="mt-1 text-sm text-gray-900">Batch DS-01</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Enrollment Date</dt>
                    <dd className="mt-1 text-sm text-gray-900">12 Jan 2026</dd>
                  </div>
                </dl>
              </div>
            </div>
          )}
          
          {activeTab !== 'overview' && (
            <div className="flex items-center justify-center h-64 border-2 border-dashed border-gray-300 rounded-lg">
              <span className="text-gray-500">Content for {activeTab} will load here.</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

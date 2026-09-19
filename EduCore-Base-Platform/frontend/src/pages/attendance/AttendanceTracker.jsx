import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '../../components/ui/Button';
import { Card, CardContent } from '../../components/ui/Card';
import { Check, X, Clock, AlertCircle } from 'lucide-react';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const AttendanceTracker = () => {
  const queryClient = useQueryClient();
  const today = new Date().toISOString().split('T')[0];

  // Fetch the students we want to mark attendance for. 
  // In a real app, this would filter by class_schedule/enrollment.
  const { data: studentsData, isLoading, isError } = useQuery({
    queryKey: queryKeys.learners.all,
    queryFn: async () => {
      // For phase 8, we just fetch all person records (or student profiles)
      const response = await api.get('people/persons/');
      return response.data.results || response.data;
    }
  });

  const [attendanceState, setAttendanceState] = useState({});
  const [saveStatus, setSaveStatus] = useState(null);

  // Initialize all students to "Present" once data loads
  useEffect(() => {
    if (studentsData && studentsData.length > 0 && Object.keys(attendanceState).length === 0) {
      const initialState = {};
      studentsData.forEach(student => {
        initialState[student.id] = 'Present';
      });
      setAttendanceState(initialState);
    }
  }, [studentsData]);

  const handleStatusChange = (studentId, status) => {
    setAttendanceState(prev => ({
      ...prev,
      [studentId]: status
    }));
  };

  const saveAttendanceMutation = useMutation({
    mutationFn: async () => {
      // Fire parallel requests for each student to save their attendance record
      const promises = Object.entries(attendanceState).map(([personId, status]) => {
        return api.post('operations/attendancerecords/', {
          class_schedule: 1, // Hardcoded to Dummy ClassSchedule for Phase 8
          date: today,
          person: parseInt(personId),
          status: status
        });
      });
      
      await Promise.all(promises);
    },
    onSuccess: () => {
      setSaveStatus('success');
      setTimeout(() => setSaveStatus(null), 3000);
    },
    onError: (err) => {
      setSaveStatus('error');
      console.error(err);
      setTimeout(() => setSaveStatus(null), 5000);
    }
  });

  const handleSave = () => {
    saveAttendanceMutation.mutate();
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center p-24">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-red-500 bg-red-50 rounded-lg border border-red-100">
        <AlertCircle className="h-8 w-8 mb-2" />
        <p>Failed to load student roster. Please check your connection.</p>
      </div>
    );
  }

  const students = studentsData || [];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Attendance Tracker</h1>
          <p className="mt-2 text-sm text-gray-700">Mark daily attendance for Class Schedule ID: 1 on {today}.</p>
        </div>
        <div className="mt-4 sm:mt-0 flex items-center">
          {saveStatus === 'success' && (
            <span className="text-green-600 text-sm mr-4 font-medium flex items-center">
              <Check className="h-4 w-4 mr-1" /> Saved Successfully!
            </span>
          )}
          {saveStatus === 'error' && (
            <span className="text-red-600 text-sm mr-4 font-medium flex items-center">
              <AlertCircle className="h-4 w-4 mr-1" /> Save Failed
            </span>
          )}
          <Button 
            variant="primary" 
            onClick={handleSave}
            disabled={saveAttendanceMutation.isPending || students.length === 0}
          >
            {saveAttendanceMutation.isPending ? 'Saving...' : 'Save Attendance'}
          </Button>
        </div>
      </div>

      <Card>
        <div className="px-4 py-5 sm:p-6">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-300">
              <thead>
                <tr>
                  <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">Student</th>
                  <th className="px-3 py-3.5 text-center text-sm font-semibold text-gray-900 flex justify-center items-center gap-1"><Check className="h-4 w-4 text-green-600"/> Present</th>
                  <th className="px-3 py-3.5 text-center text-sm font-semibold text-gray-900 flex justify-center items-center gap-1"><X className="h-4 w-4 text-red-600"/> Absent</th>
                  <th className="px-3 py-3.5 text-center text-sm font-semibold text-gray-900 flex justify-center items-center gap-1"><Clock className="h-4 w-4 text-yellow-600"/> Late</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {students.map((student) => (
                  <tr key={student.id}>
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0">
                      {student.first_name} {student.last_name} <span className="text-gray-500 font-normal">({student.email})</span>
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-center">
                      <input 
                        type="radio" 
                        name={`attendance-${student.id}`} 
                        checked={attendanceState[student.id] === 'Present'} 
                        onChange={() => handleStatusChange(student.id, 'Present')}
                        className="h-4 w-4 text-green-600 border-gray-300 focus:ring-green-500" 
                      />
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-center">
                      <input 
                        type="radio" 
                        name={`attendance-${student.id}`} 
                        checked={attendanceState[student.id] === 'Absent'} 
                        onChange={() => handleStatusChange(student.id, 'Absent')}
                        className="h-4 w-4 text-red-600 border-gray-300 focus:ring-red-500" 
                      />
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-center">
                      <input 
                        type="radio" 
                        name={`attendance-${student.id}`} 
                        checked={attendanceState[student.id] === 'Late'} 
                        onChange={() => handleStatusChange(student.id, 'Late')}
                        className="h-4 w-4 text-yellow-600 border-gray-300 focus:ring-yellow-500" 
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            {students.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No students found in the database to mark attendance for.
              </div>
            )}
          </div>
        </div>
      </Card>
    </div>
  );
};

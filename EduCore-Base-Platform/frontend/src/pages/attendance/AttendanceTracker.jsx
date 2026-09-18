import React from 'react';
import { Button } from '../../components/ui/Button';
import { Card, CardContent } from '../../components/ui/Card';
import { Check, X, Clock } from 'lucide-react';

const mockStudents = [
  { id: 'LRN001', name: 'Aarav Sharma', status: 'present' },
  { id: 'LRN002', name: 'Priya Patel', status: 'present' },
  { id: 'LRN003', name: 'Rahul Desai', status: 'absent' },
  { id: 'LRN004', name: 'Neha Gupta', status: 'late' },
];

export const AttendanceTracker = () => {
  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Attendance Tracker</h1>
          <p className="mt-2 text-sm text-gray-700">Mark daily attendance for Batch DS-01 (Data Structures).</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Button variant="primary">Save Attendance</Button>
        </div>
      </div>

      <Card>
        <div className="px-4 py-5 sm:p-6">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-300">
              <thead>
                <tr>
                  <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">Student</th>
                  <th className="px-3 py-3.5 text-center text-sm font-semibold text-gray-900">Present</th>
                  <th className="px-3 py-3.5 text-center text-sm font-semibold text-gray-900">Absent</th>
                  <th className="px-3 py-3.5 text-center text-sm font-semibold text-gray-900">Late</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {mockStudents.map((student) => (
                  <tr key={student.id}>
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0">
                      {student.name} <span className="text-gray-500 font-normal">({student.id})</span>
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-center">
                      <input type="radio" name={`attendance-${student.id}`} defaultChecked={student.status === 'present'} className="h-4 w-4 text-green-600 border-gray-300 focus:ring-green-500" />
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-center">
                      <input type="radio" name={`attendance-${student.id}`} defaultChecked={student.status === 'absent'} className="h-4 w-4 text-red-600 border-gray-300 focus:ring-red-500" />
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-center">
                      <input type="radio" name={`attendance-${student.id}`} defaultChecked={student.status === 'late'} className="h-4 w-4 text-yellow-600 border-gray-300 focus:ring-yellow-500" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </Card>
    </div>
  );
};

import React from 'react';
import { DataTable } from '../../components/data-display/DataTable';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Plus } from 'lucide-react';

const mockExams = [
  { id: 'EX001', name: 'Midterm Physics', date: '2026-10-15', maxMarks: 100, status: 'upcoming' },
  { id: 'EX002', name: 'Final Data Structures', date: '2026-12-01', maxMarks: 100, status: 'scheduled' },
  { id: 'EX003', name: 'Quiz 1 Algebra', date: '2026-09-10', maxMarks: 20, status: 'completed' },
];

export const ExamList = () => {
  const columns = [
    { header: 'Exam Name', accessor: 'name', primary: true },
    { header: 'Date', accessor: 'date' },
    { header: 'Max Marks', accessor: 'maxMarks' },
    { 
      header: 'Status', 
      accessor: 'status',
      render: (row) => (
        <Badge status={row.status === 'completed' ? 'success' : row.status === 'upcoming' ? 'warning' : 'neutral'}>
          {row.status.charAt(0).toUpperCase() + row.status.slice(1)}
        </Badge>
      )
    },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Assessments</h1>
          <p className="mt-2 text-sm text-gray-700">Manage exams, quizzes, and gradebooks.</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Button variant="primary">
            <Plus className="h-4 w-4 mr-2" />
            Create Exam
          </Button>
        </div>
      </div>

      <DataTable 
        columns={columns} 
        data={mockExams} 
        searchPlaceholder="Search exams..."
      />
    </div>
  );
};

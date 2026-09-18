import React from 'react';
import { DataTable } from '../../components/data-display/DataTable';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Plus } from 'lucide-react';

const mockInvoices = [
  { id: 'INV-2026-001', student: 'Aarav Sharma', amount: '$5,000', dueDate: '2026-09-30', status: 'pending' },
  { id: 'INV-2026-002', student: 'Priya Patel', amount: '$1,200', dueDate: '2026-09-15', status: 'paid' },
  { id: 'INV-2026-003', student: 'Rahul Desai', amount: '$4,500', dueDate: '2026-08-30', status: 'overdue' },
];

export const InvoiceList = () => {
  const columns = [
    { header: 'Invoice ID', accessor: 'id', primary: true },
    { header: 'Student', accessor: 'student' },
    { header: 'Amount', accessor: 'amount' },
    { header: 'Due Date', accessor: 'dueDate' },
    { 
      header: 'Status', 
      accessor: 'status',
      render: (row) => (
        <Badge status={row.status === 'paid' ? 'success' : row.status === 'overdue' ? 'danger' : 'warning'}>
          {row.status.charAt(0).toUpperCase() + row.status.slice(1)}
        </Badge>
      )
    },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">Finance & Invoices</h1>
          <p className="mt-2 text-sm text-gray-700">Manage fee structures, invoices, and payments.</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Button variant="primary">
            <Plus className="h-4 w-4 mr-2" />
            Generate Invoice
          </Button>
        </div>
      </div>

      <DataTable 
        columns={columns} 
        data={mockInvoices} 
        searchPlaceholder="Search invoices..."
      />
    </div>
  );
};

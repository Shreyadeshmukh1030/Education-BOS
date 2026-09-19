import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import api from '../../services/api';
import { queryKeys } from '../../services/queries';

export const AddInvoice = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    amount_due: 1000.00,
    due_date: '',
    status: 'Pending',
    notes: ''
  });

  const [error, setError] = useState(null);

  const createInvoiceMutation = useMutation({
    mutationFn: async (data) => {
      // Create Invoice
      const response = await api.post('finance/invoices/', {
        amount_due: parseFloat(data.amount_due),
        due_date: data.due_date,
        status: data.status,
        notes: data.notes,
        person: 1 // Hardcoded to Dummy Person (ID: 1) for Phase 7
      });
      
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.invoices.all });
      navigate('/finance');
    },
    onError: (err) => {
      setError(err.response?.data?.detail || "An error occurred while generating the invoice.");
      console.error(err);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);
    createInvoiceMutation.mutate(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <button 
        onClick={() => navigate('/finance')}
        className="flex items-center text-sm font-medium text-gray-500 hover:text-gray-900"
      >
        <ArrowLeft className="h-4 w-4 mr-1" />
        Back to Invoices
      </button>

      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Generate Invoice</h1>
        <p className="mt-2 text-sm text-gray-700">Create a new bill for a student.</p>
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
                <label className="block text-sm font-medium text-gray-700">Amount Due ($) *</label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span className="text-gray-500 sm:text-sm">$</span>
                  </div>
                  <input 
                    type="number" 
                    name="amount_due"
                    required
                    step="0.01"
                    min="0"
                    value={formData.amount_due}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm pl-7 py-2 border" 
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Due Date *</label>
                <div className="mt-1">
                  <input 
                    type="date" 
                    name="due_date"
                    required
                    value={formData.due_date}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border text-gray-700" 
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Status</label>
                <div className="mt-1">
                  <select 
                    name="status"
                    value={formData.status}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border bg-white" 
                  >
                    <option value="Pending">Pending</option>
                    <option value="Partial">Partially Paid</option>
                    <option value="Paid">Paid</option>
                    <option value="Overdue">Overdue</option>
                  </select>
                </div>
              </div>

              <div className="sm:col-span-6 text-sm text-gray-500 border border-dashed border-gray-300 p-4 rounded bg-gray-50">
                <p><strong>Note:</strong> For this testing phase, the invoice will automatically be assigned to the dummy Student (ID: 1).</p>
              </div>

              <div className="sm:col-span-6">
                <label className="block text-sm font-medium text-gray-700">Internal Notes</label>
                <div className="mt-1">
                  <textarea 
                    name="notes"
                    rows={3}
                    value={formData.notes}
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
              onClick={() => navigate('/finance')}
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              variant="primary"
              disabled={createInvoiceMutation.isPending}
            >
              {createInvoiceMutation.isPending ? 'Generating...' : 'Generate Invoice'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

import React from 'react';
import { MoreVertical, Search, Filter, Download } from 'lucide-react';
import { Button } from '../ui/Button';

export const DataTable = ({ 
  columns, 
  data, 
  onRowClick,
  searchPlaceholder = "Search..."
}) => {
  return (
    <div className="bg-surface-card shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg overflow-hidden">
      <div className="p-4 border-b border-gray-200 sm:flex sm:items-center sm:justify-between">
        <div className="flex flex-1 items-center space-x-2 max-w-md relative">
          <div className="pointer-events-none absolute inset-y-0 left-0 pl-3 flex items-center">
            <Search className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="text"
            className="block w-full pl-9 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder={searchPlaceholder}
          />
        </div>
        <div className="mt-3 sm:mt-0 sm:ml-4 flex items-center space-x-3">
          <Button variant="secondary" className="px-3">
            <Filter className="h-4 w-4 mr-2" />
            Filter
          </Button>
          <Button variant="secondary" className="px-3">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-300">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="relative px-4 sm:px-6 w-12 text-center">
                <input type="checkbox" className="absolute left-4 top-1/2 -mt-2 h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-600" />
              </th>
              {columns.map((col, idx) => (
                <th key={idx} scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  {col.header}
                </th>
              ))}
              <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6 w-16">
                <span className="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {data.length > 0 ? (
              data.map((row, rowIndex) => (
                <tr 
                  key={rowIndex} 
                  className={onRowClick ? "cursor-pointer hover:bg-gray-50 transition-colors" : ""}
                  onClick={() => onRowClick && onRowClick(row)}
                >
                  <td className="relative px-4 sm:px-6 w-12 text-center" onClick={(e) => e.stopPropagation()}>
                    <input type="checkbox" className="absolute left-4 top-1/2 -mt-2 h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-600" />
                  </td>
                  {columns.map((col, colIndex) => (
                    <td key={colIndex} className={`whitespace-nowrap px-3 py-4 text-sm ${col.primary ? 'font-medium text-gray-900' : 'text-gray-500'}`}>
                      {col.render ? col.render(row) : row[col.accessor]}
                    </td>
                  ))}
                  <td className="whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6" onClick={(e) => e.stopPropagation()}>
                    <button className="text-gray-400 hover:text-gray-900">
                      <span className="sr-only">Options</span>
                      <MoreVertical className="h-5 w-5" />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={columns.length + 2} className="px-3 py-8 text-sm text-gray-500 text-center">
                  No data found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="bg-white px-4 py-3 border-t border-gray-200 sm:px-6 flex items-center justify-between">
        <div className="hidden sm:block">
          <p className="text-sm text-gray-700">
            Showing <span className="font-medium">1</span> to <span className="font-medium">{Math.min(10, data.length)}</span> of <span className="font-medium">{data.length}</span> results
          </p>
        </div>
        <div className="flex-1 flex justify-between sm:justify-end">
          <Button variant="secondary" className="mr-2">Previous</Button>
          <Button variant="secondary">Next</Button>
        </div>
      </div>
    </div>
  );
};

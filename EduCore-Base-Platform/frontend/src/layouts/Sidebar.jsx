import React from 'react';
import { NavLink } from 'react-router-dom';
import { getEnabledNavigation } from '../configuration/navigation';
import { useModules } from '../contexts/ModuleContext';
import { GraduationCap } from 'lucide-react';

export const Sidebar = () => {
  const { modules, loading } = useModules();
  const navItems = getEnabledNavigation(modules);

  return (
    <div className="flex flex-col w-64 bg-gray-900 text-white min-h-screen">
      <div className="flex items-center justify-center h-16 bg-gray-900 border-b border-gray-800 px-4">
        <GraduationCap className="w-8 h-8 text-primary-500 mr-2" />
        <span className="text-xl font-bold uppercase tracking-wider">EduCore Base</span>
      </div>
      <div className="overflow-y-auto flex-1">
        <nav className="mt-5 px-2 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.label}
                to={item.route}
                className={({ isActive }) =>
                  `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                    isActive
                      ? 'bg-gray-800 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`
                }
              >
                <Icon className="mr-3 flex-shrink-0 h-5 w-5 text-gray-400 group-hover:text-gray-300" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './contexts/AuthContext';
import { ModuleProvider } from './contexts/ModuleContext';
import RequireAuth from './components/RequireAuth';
import RequireModule from './components/RequireModule';
import LoginPage from './pages/auth/LoginPage';

import { DashboardLayout } from './layouts/DashboardLayout';
import { Dashboard } from './pages/Dashboard';
import { LearnerList } from './pages/people/LearnerList';
import { LearnerProfile } from './pages/people/LearnerProfile';
import { AddLearner } from './pages/people/AddLearner';
import { FacilityList } from './pages/organization/FacilityList';
import { AddCampus } from './pages/organization/AddCampus';
import { ProgramList } from './pages/academics/ProgramList';
import { AddProgram } from './pages/academics/AddProgram';
import { AttendanceTracker } from './pages/attendance/AttendanceTracker';
import { ExamList } from './pages/assessments/ExamList';
import { AddExam } from './pages/assessments/AddExam';
import { InvoiceList } from './pages/finance/InvoiceList';
import { AddInvoice } from './pages/finance/AddInvoice';
import { ModuleManager } from './pages/modules/ModuleManager';
import { Settings } from './pages/settings/Settings';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ModuleProvider>
          <Router>
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<LoginPage />} />

              {/* Protected Routes */}
              <Route
                path="/"
                element={
                  <RequireAuth>
                    <DashboardLayout />
                  </RequireAuth>
                }
              >
                <Route index element={<Dashboard />} />
                
                {/* People Module */}
                <Route path="people" element={<RequireModule moduleKey="people"><Outlet /></RequireModule>}>
                  <Route index element={<Navigate to="learners" replace />} />
                  <Route path="learners" element={<LearnerList />} />
                  <Route path="learners/add" element={<AddLearner />} />
                  <Route path="learners/:id" element={<LearnerProfile />} />
                </Route>

                {/* Application Modules */}
                <Route path="organization" element={<RequireModule moduleKey="organization"><Outlet /></RequireModule>}>
                  <Route index element={<FacilityList />} />
                  <Route path="add-campus" element={<AddCampus />} />
                </Route>
                <Route path="academics" element={<RequireModule moduleKey="academics"><Outlet /></RequireModule>}>
                  <Route index element={<ProgramList />} />
                  <Route path="add" element={<AddProgram />} />
                </Route>
                <Route path="attendance" element={<RequireModule moduleKey="attendance"><AttendanceTracker /></RequireModule>} />
                <Route path="assessments" element={<RequireModule moduleKey="assessments"><Outlet /></RequireModule>}>
                  <Route index element={<ExamList />} />
                  <Route path="add" element={<AddExam />} />
                </Route>
                <Route path="lms" element={<RequireModule moduleKey="lms"><div className="p-4">LMS Dashboard (Coming Soon)</div></RequireModule>} />
                <Route path="finance" element={<RequireModule moduleKey="finance"><Outlet /></RequireModule>}>
                  <Route index element={<InvoiceList />} />
                  <Route path="add" element={<AddInvoice />} />
                </Route>
                
                {/* System Modules */}
                <Route path="modules" element={<ModuleManager />} />
                <Route path="settings" element={<Settings />} />
              </Route>
            </Routes>
          </Router>
        </ModuleProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from './layouts/DashboardLayout';
import { Dashboard } from './pages/Dashboard';
import { LearnerList } from './pages/people/LearnerList';
import { LearnerProfile } from './pages/people/LearnerProfile';
import { AddLearner } from './pages/people/AddLearner';
import { FacilityList } from './pages/organization/FacilityList';
import { ProgramList } from './pages/academics/ProgramList';
import { AttendanceTracker } from './pages/attendance/AttendanceTracker';
import { ExamList } from './pages/assessments/ExamList';
import { InvoiceList } from './pages/finance/InvoiceList';
import { ModuleManager } from './pages/modules/ModuleManager';
import { Settings } from './pages/settings/Settings';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
          
          {/* People Module */}
          <Route path="people">
            <Route index element={<Navigate to="learners" replace />} />
            <Route path="learners" element={<LearnerList />} />
            <Route path="learners/add" element={<AddLearner />} />
            <Route path="learners/:id" element={<LearnerProfile />} />
          </Route>

          {/* Application Modules */}
          <Route path="organization" element={<FacilityList />} />
          <Route path="academics" element={<ProgramList />} />
          <Route path="attendance" element={<AttendanceTracker />} />
          <Route path="assessments" element={<ExamList />} />
          <Route path="lms" element={<div className="p-4">LMS Dashboard (Coming Soon)</div>} />
          <Route path="finance" element={<InvoiceList />} />
          <Route path="modules" element={<ModuleManager />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

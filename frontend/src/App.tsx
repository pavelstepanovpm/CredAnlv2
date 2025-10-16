import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';

import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Portfolio } from './pages/Portfolio';
import { Scenarios } from './pages/Scenarios';
import { Reports } from './pages/Reports';
import { Settings } from './pages/Settings';

function App() {
  return (
    <Box className="trading-terminal">
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/scenarios" element={<Scenarios />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Box>
  );
}

export default App;


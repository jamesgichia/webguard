import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import ScanHistory from './pages/ScanHistory';
import ScanDetail from './pages/ScanDetail';
import ApiKeys from './pages/ApiKeys';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* Public route */}
          <Route path="login" element={<Login />} />

          {/* Protected routes */}
          <Route
            index
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="scans"
            element={
              <ProtectedRoute>
                <ScanHistory />
              </ProtectedRoute>
            }
          />
          <Route
            path="scans/:scanId"
            element={
              <ProtectedRoute>
                <ScanDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="keys"
            element={
              <ProtectedRoute>
                <ApiKeys />
              </ProtectedRoute>
            }
          />

          {/* Catch-all → dashboard */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;

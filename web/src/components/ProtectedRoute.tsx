import { Navigate, useLocation } from 'react-router-dom';

interface Props {
  children: React.ReactNode;
}

/**
 * Wraps routes that require authentication.
 * Redirects to /login if no token is found, preserving the intended destination.
 */
export default function ProtectedRoute({ children }: Props) {
  const location = useLocation();
  const token = localStorage.getItem('token');

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}

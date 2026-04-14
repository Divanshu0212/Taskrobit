import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children, adminOnly = false, userOnly = false }) {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && user?.role !== "admin") {
    return <Navigate to="/dashboard" replace />;
  }

  if (userOnly && user?.role !== "user") {
    return <Navigate to="/admin" replace />;
  }

  return children;
}

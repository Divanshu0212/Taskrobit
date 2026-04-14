import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import AdminPanel from "./pages/AdminPanel";
import ProtectedRoute from "./routes/ProtectedRoute";

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute userOnly>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute adminOnly>
              <AdminPanel />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </div>
  );
}

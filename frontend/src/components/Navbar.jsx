import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="nav-shell">
      <div className="brand">Task Orbit</div>
      <nav className="nav-links">
        {user && <Link to="/dashboard">Dashboard</Link>}
        {user?.role === "admin" && <Link to="/admin">Admin Panel</Link>}
      </nav>
      <div className="nav-user">
        {user && <span>{user.username} ({user.role})</span>}
        {user ? (
          <button
            className="btn btn-outline"
            onClick={() => {
              logout();
              navigate("/login");
            }}
          >
            Logout
          </button>
        ) : (
          <Link className="btn btn-outline" to="/login">Login</Link>
        )}
      </div>
    </header>
  );
}

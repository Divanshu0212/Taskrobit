import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register, loading } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "", confirmPassword: "" });
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    const username = form.username.trim();
    const email = form.email.trim();

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (!/^[a-zA-Z0-9_]{3,50}$/.test(username)) {
      setError("Username must be 3-50 chars, alphanumeric/underscore only");
      return;
    }

    if (form.password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    if (!/[A-Za-z]/.test(form.password) || !/\d/.test(form.password)) {
      setError("Password must contain at least one letter and one number");
      return;
    }

    const result = await register({ username, email, password: form.password });
    if (!result.ok) {
      setError(result.message);
      return;
    }

    navigate("/login");
  };

  return (
    <section className="auth-page">
      <div className="auth-card">
        <h1>Create account</h1>
        <p>Launch your task command center.</p>
        <form onSubmit={submit} className="auth-form">
          <input placeholder="Username" required onChange={(e) => setForm((prev) => ({ ...prev, username: e.target.value }))} />
          <input type="email" placeholder="Email" required onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))} />
          <input type="password" placeholder="Password" required onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))} />
          <input type="password" placeholder="Confirm Password" required onChange={(e) => setForm((prev) => ({ ...prev, confirmPassword: e.target.value }))} />
          <p>Use 3-50 char username and password with letters + numbers.</p>
          {error && <p className="error-text">{error}</p>}
          <button disabled={loading} className="btn btn-primary" type="submit">{loading ? "Creating..." : "Register"}</button>
        </form>
        <p>Already registered? <Link to="/login">Login</Link></p>
      </div>
    </section>
  );
}

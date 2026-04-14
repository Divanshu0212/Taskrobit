import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login, loading } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    const result = await login(form.email, form.password);
    if (!result.ok) {
      setError(result.message);
      return;
    }
    navigate("/dashboard");
  };

  return (
    <section className="auth-page">
      <div className="auth-card">
        <h1>Welcome back</h1>
        <p>Sign in to manage your missions.</p>
        <form onSubmit={submit} className="auth-form">
          <input type="email" placeholder="Email" required onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))} />
          <input type="password" placeholder="Password" required onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))} />
          {error && <p className="error-text">{error}</p>}
          <button disabled={loading} className="btn btn-primary" type="submit">{loading ? "Signing in..." : "Login"}</button>
        </form>
        <p>New here? <Link to="/register">Create account</Link></p>
      </div>
    </section>
  );
}

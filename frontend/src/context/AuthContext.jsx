import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api from "../api/axios";

const AuthContext = createContext(null);

function extractApiError(error, fallbackMessage) {
  const data = error?.response?.data;
  if (!data) return fallbackMessage;

  if (Array.isArray(data.errors) && data.errors.length > 0) {
    const first = data.errors[0];
    if (typeof first?.msg === "string") {
      return first.msg.replace("Value error, ", "");
    }
  }

  if (typeof data.detail === "string") return data.detail;
  if (typeof data.message === "string") return data.message;

  return fallbackMessage;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!localStorage.getItem("token")) return;
    api.get("/auth/me").then((res) => {
      setUser(res.data);
      localStorage.setItem("user", JSON.stringify(res.data));
    }).catch(() => {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      setUser(null);
    });
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const res = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      const me = await api.get("/auth/me");
      setUser(me.data);
      localStorage.setItem("user", JSON.stringify(me.data));
      return { ok: true };
    } catch (error) {
      return { ok: false, message: extractApiError(error, "Login failed") };
    } finally {
      setLoading(false);
    }
  };

  const register = async (payload) => {
    setLoading(true);
    try {
      await api.post("/auth/register", payload);
      return { ok: true };
    } catch (error) {
      return { ok: false, message: extractApiError(error, "Registration failed") };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, loading, login, register, logout, isAuthenticated: Boolean(user) }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}

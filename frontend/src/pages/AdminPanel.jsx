import { useEffect, useState } from "react";
import api from "../api/axios";

export default function AdminPanel() {
  const [tab, setTab] = useState("users");
  const [users, setUsers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState("");

  const loadData = async () => {
    setError("");
    try {
      const [usersRes, tasksRes] = await Promise.all([
        api.get("/admin/users/"),
        api.get("/admin/tasks/"),
      ]);
      setUsers(usersRes.data);
      setTasks(tasksRes.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load admin data");
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const changeRole = async (id, role) => {
    await api.put(`/admin/users/${id}/role`, { role: role === "admin" ? "user" : "admin" });
    loadData();
  };

  const setUserActiveStatus = async (id, isActive) => {
    await api.put(`/admin/users/${id}/status`, { is_active: isActive });
    loadData();
  };

  const removeUser = async (id) => {
    await api.delete(`/admin/users/${id}`);
    loadData();
  };

  const deleteTask = async (id) => {
    await api.delete(`/admin/tasks/${id}`);
    loadData();
  };

  return (
    <section className="page-wrap">
      <h1>Admin Command Center</h1>
      <div className="tab-row">
        <button className={tab === "users" ? "tab active" : "tab"} onClick={() => setTab("users")}>Users</button>
        <button className={tab === "tasks" ? "tab active" : "tab"} onClick={() => setTab("tasks")}>Tasks</button>
      </div>
      {error && <p className="error-text">{error}</p>}

      {tab === "users" && (
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>Email</th><th>Username</th><th>Role</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.email}</td>
                  <td>{user.username}</td>
                  <td>{user.role}</td>
                  <td>{user.is_active ? "Active" : "Inactive"}</td>
                  <td>
                    <button className="btn btn-outline" onClick={() => changeRole(user.id, user.role)}>Toggle Role</button>
                    {user.is_active ? (
                      <button className="btn btn-outline" onClick={() => setUserActiveStatus(user.id, false)}>Deactivate</button>
                    ) : (
                      <button className="btn btn-primary" onClick={() => setUserActiveStatus(user.id, true)}>Activate</button>
                    )}
                    <button className="btn btn-danger" onClick={() => removeUser(user.id)}>Remove</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === "tasks" && (
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>Title</th><th>Owner ID</th><th>Status</th><th>Priority</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {tasks.map((task) => (
                <tr key={task.id}>
                  <td>{task.title}</td>
                  <td>{task.owner_id}</td>
                  <td>{task.status}</td>
                  <td>{task.priority}</td>
                  <td><button className="btn btn-danger" onClick={() => deleteTask(task.id)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

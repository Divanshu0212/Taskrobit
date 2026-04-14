import { useEffect, useMemo, useState } from "react";
import api from "../api/axios";
import TaskCard from "../components/TaskCard";
import TaskForm from "../components/TaskForm";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [formOpen, setFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState({ status: "", priority: "" });
  const [error, setError] = useState("");

  const query = useMemo(() => {
    const params = new URLSearchParams();
    if (filter.status) params.set("status", filter.status);
    if (filter.priority) params.set("priority", filter.priority);
    return params.toString();
  }, [filter]);

  const fetchTasks = async () => {
    setLoading(true);
    setError("");
    try {
      const url = query ? `/tasks/?${query}` : "/tasks/";
      const res = await api.get(url);
      setTasks(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to fetch tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [query]);

  const onSubmitForm = async (payload) => {
    setLoading(true);
    try {
      if (editingTask) {
        await api.put(`/tasks/${editingTask.id}`, payload);
      } else {
        await api.post("/tasks/", payload);
      }
      setFormOpen(false);
      setEditingTask(null);
      fetchTasks();
    } catch (err) {
      setError(err?.response?.data?.detail || "Operation failed");
    } finally {
      setLoading(false);
    }
  };

  const onDelete = async (id) => {
    if (!window.confirm("Delete this task?")) return;
    try {
      await api.delete(`/tasks/${id}`);
      fetchTasks();
    } catch (err) {
      setError(err?.response?.data?.detail || "Delete failed");
    }
  };

  return (
    <section className="page-wrap">
      <div className="section-head">
        <h1>Mission Dashboard</h1>
        <button className="btn btn-primary" onClick={() => { setEditingTask(null); setFormOpen(true); }}>Create Task</button>
      </div>

      <div className="filter-bar">
        <select onChange={(e) => setFilter((prev) => ({ ...prev, status: e.target.value }))}>
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        <select onChange={(e) => setFilter((prev) => ({ ...prev, priority: e.target.value }))}>
          <option value="">All Priority</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      {error && <p className="error-text">{error}</p>}
      {loading && <p>Loading...</p>}

      <div className="task-grid">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onEdit={(value) => {
              setEditingTask(value);
              setFormOpen(true);
            }}
            onDelete={onDelete}
          />
        ))}
      </div>

      {formOpen && (
        <div className="modal-overlay" onClick={() => setFormOpen(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <TaskForm
              initialValue={editingTask}
              onSubmit={onSubmitForm}
              onCancel={() => {
                setEditingTask(null);
                setFormOpen(false);
              }}
              loading={loading}
            />
          </div>
        </div>
      )}
    </section>
  );
}

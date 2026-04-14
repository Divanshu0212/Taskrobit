import { useEffect, useState } from "react";

const emptyForm = {
  title: "",
  description: "",
  priority: "medium",
  due_date: "",
};

export default function TaskForm({ initialValue, onSubmit, onCancel, loading }) {
  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    if (!initialValue) {
      setForm(emptyForm);
      return;
    }

    setForm({
      title: initialValue.title || "",
      description: initialValue.description || "",
      priority: initialValue.priority || "medium",
      due_date: initialValue.due_date ? initialValue.due_date.slice(0, 16) : "",
      status: initialValue.status,
    });
  }, [initialValue]);

  return (
    <form
      className="task-form"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(form);
      }}
    >
      <h3>{initialValue ? "Edit Task" : "Create Task"}</h3>
      <input
        placeholder="Title"
        value={form.title}
        onChange={(e) => setForm((prev) => ({ ...prev, title: e.target.value }))}
        required
      />
      <textarea
        placeholder="Description"
        value={form.description}
        onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
      />
      <div className="grid-2">
        <select
          value={form.priority}
          onChange={(e) => setForm((prev) => ({ ...prev, priority: e.target.value }))}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <input
          type="datetime-local"
          value={form.due_date}
          onChange={(e) => setForm((prev) => ({ ...prev, due_date: e.target.value }))}
        />
      </div>
      {initialValue && (
        <select
          value={form.status || "pending"}
          onChange={(e) => setForm((prev) => ({ ...prev, status: e.target.value }))}
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      )}
      <div className="actions-row">
        <button disabled={loading} className="btn btn-primary" type="submit">
          {loading ? "Saving..." : "Save"}
        </button>
        <button className="btn btn-outline" type="button" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  );
}

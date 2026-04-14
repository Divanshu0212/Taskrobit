export default function TaskCard({ task, onEdit, onDelete }) {
  return (
    <article className="task-card">
      <div className="task-top">
        <h3>{task.title}</h3>
        <div className="task-badges">
          <span className={`badge status-${task.status}`}>{task.status}</span>
          <span className={`badge prio-${task.priority}`}>{task.priority}</span>
        </div>
      </div>
      <p>{task.description || "No description"}</p>
      <small>{task.due_date ? `Due: ${new Date(task.due_date).toLocaleString()}` : "No due date"}</small>
      <div className="task-actions">
        <button className="btn btn-outline" onClick={() => onEdit(task)}>Edit</button>
        <button className="btn btn-danger" onClick={() => onDelete(task.id)}>Delete</button>
      </div>
    </article>
  );
}

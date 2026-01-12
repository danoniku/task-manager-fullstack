import { useEffect, useState } from "react";

const API_URL = import.meta.env.DEV ? "http://127.0.0.1:8000" : "/api";


function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTask, setNewTask] = useState("");

  async function loadTasks() {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_URL}/tasks`);
      if (!response.ok) {
        throw new Error("Failed to fetch tasks");
      }

      const data = await response.json();
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function addTask() {
    if (!newTask.trim()) return;

    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: newTask }),
      });

      if (!response.ok) {
        throw new Error("Failed to add task");
      }

      setNewTask("");
      loadTasks();
    } catch (err) {
      alert(err.message);
    }
  }

  async function toggleTask(task) {
    try {
      const response = await fetch(`${API_URL}/tasks/${task.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ completed: !task.completed }),
      });

      if (!response.ok) {
        throw new Error("Failed to update task");
      }

      loadTasks();
    } catch (err) {
      alert(err.message);
    }
  }

  async function deleteTask(id) {
    try {
      const response = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete task");
      }

      loadTasks();
    } catch (err) {
      alert(err.message);
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", fontFamily: "Arial" }}>
      <h1 style={{ textAlign: "center", marginTop: "20px" }}>
        Task Manager
      </h1>

      <div style={{ marginBottom: "20px", textAlign: "center" }}>
        <input
          type="text"
          placeholder="New task..."
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          style={{ padding: "8px", width: "70%" }}
        />
        <button
          onClick={addTask}
          style={{ padding: "8px 12px", marginLeft: "8px" }}
        >
          Add
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {tasks.map((task) => (
          <li
            key={task.id}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "8px",
              cursor: "pointer",
              textDecoration: task.completed ? "line-through" : "none",
            }}
          >
            <span onClick={() => toggleTask(task)}>
              {task.completed ? "✅" : "⬜"} {task.title}
            </span>

            <button
              onClick={() => deleteTask(task.id)}
              style={{
                border: "none",
                background: "transparent",
                color: "red",
                fontSize: "16px",
                cursor: "pointer",
              }}
            >
              ❌
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

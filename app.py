from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)
tasks = {}
next_id = 1

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/tasks")
def list_tasks():
    return jsonify(list(tasks.values())), 200

@app.post("/tasks")
def create_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(error="title is required"), 400
    task = {"id": next_id, "title": title, "completed": False,
            "created_at": datetime.utcnow().isoformat() + "Z"}
    tasks[next_id] = task
    next_id += 1
    return jsonify(task), 201

@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify(error="task not found"), 404
    data = request.get_json(silent=True) or {}
    if "title" in data:
        title = str(data["title"]).strip()
        if not title:
            return jsonify(error="title cannot be empty"), 400
        task["title"] = title
    if "completed" in data:
        task["completed"] = bool(data["completed"])
    return jsonify(task), 200

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify(error="task not found"), 404
    del tasks[task_id]
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

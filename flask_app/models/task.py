from datetime import datetime
import json

from flask import flash

from flask_app.config.sqliteconnection import connect_to_sqlite


class Task:
    @staticmethod
    def _normalize_steps(raw_steps):
        if not raw_steps:
            return []

        parsed = raw_steps
        if isinstance(raw_steps, str):
            try:
                parsed = json.loads(raw_steps)
            except json.JSONDecodeError:
                return []

        if not isinstance(parsed, list):
            return []

        cleaned_steps = []
        for step in parsed:
            if not isinstance(step, str):
                continue
            normalized = step.strip()
            if normalized:
                cleaned_steps.append(normalized)

        return cleaned_steps[:10]

    @staticmethod
    def _serialize_steps(steps):
        return json.dumps(Task._normalize_steps(steps))

    @staticmethod
    def validate_task(data):
        is_valid = True

        if len(data.get("title", "").strip()) < 2:
            flash("Task title must be at least 2 characters.", "task_error")
            is_valid = False

        if len(data.get("description", "").strip()) < 5:
            flash("Description must be at least 5 characters.", "task_error")
            is_valid = False

        if not data.get("due_date", "").strip():
            flash("Due date is required.", "task_error")
            is_valid = False

        if data.get("priority") not in {"low", "medium", "high"}:
            flash("Priority must be low, medium, or high.", "task_error")
            is_valid = False

        if data.get("status") not in {"todo", "in-progress", "done"}:
            flash("Status must be todo, in-progress, or done.", "task_error")
            is_valid = False

        return is_valid

    @classmethod
    def create(cls, data):
        timestamp = datetime.utcnow().isoformat(timespec="seconds")
        payload = {
            "user_id": data["user_id"],
            "title": data["title"].strip(),
            "description": data["description"].strip(),
            "due_date": data["due_date"],
            "priority": data["priority"],
            "status": data["status"],
            "suggested_steps": cls._serialize_steps(data.get("suggested_steps", [])),
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        query = """
        INSERT INTO tasks (user_id, title, description, due_date, priority, status, suggested_steps, created_at, updated_at)
        VALUES (:user_id, :title, :description, :due_date, :priority, :status, :suggested_steps, :created_at, :updated_at);
        """
        return connect_to_sqlite().query_db(query, payload)

    @classmethod
    def get_all(cls, user_id, status_filter=None, search_term=None):
        query = """
        SELECT *
        FROM tasks
        WHERE user_id = :user_id
        """
        data = {"user_id": user_id}

        if status_filter and status_filter != "all":
            query += " AND status = :status "
            data["status"] = status_filter

        if search_term:
            query += " AND LOWER(title) LIKE :search "
            data["search"] = f"%{search_term.strip().lower()}%"

        query += " ORDER BY due_date ASC, created_at DESC;"
        tasks = connect_to_sqlite().query_db(query, data)
        for task in tasks:
            task["suggested_steps"] = cls._normalize_steps(task.get("suggested_steps"))
        return tasks

    @classmethod
    def get_by_id(cls, task_id, user_id):
        query = """
        SELECT *
        FROM tasks
        WHERE id = :id AND user_id = :user_id;
        """
        result = connect_to_sqlite().query_db(query, {"id": task_id, "user_id": user_id})
        if not result:
            return None

        task = result[0]
        task["suggested_steps"] = cls._normalize_steps(task.get("suggested_steps"))
        return task

    @classmethod
    def update(cls, data):
        payload = {
            "id": data["id"],
            "user_id": data["user_id"],
            "title": data["title"].strip(),
            "description": data["description"].strip(),
            "due_date": data["due_date"],
            "priority": data["priority"],
            "status": data["status"],
            "updated_at": datetime.utcnow().isoformat(timespec="seconds"),
        }
        query = """
        UPDATE tasks
        SET title = :title,
            description = :description,
            due_date = :due_date,
            priority = :priority,
            status = :status,
            updated_at = :updated_at
        WHERE id = :id AND user_id = :user_id;
        """
        return connect_to_sqlite().query_db(query, payload)

    @classmethod
    def delete(cls, task_id, user_id):
        query = "DELETE FROM tasks WHERE id = :id AND user_id = :user_id;"
        return connect_to_sqlite().query_db(query, {"id": task_id, "user_id": user_id})

    @classmethod
    def update_suggested_steps(cls, task_id, user_id, steps):
        payload = {
            "id": task_id,
            "user_id": user_id,
            "suggested_steps": cls._serialize_steps(steps),
            "updated_at": datetime.utcnow().isoformat(timespec="seconds"),
        }
        query = """
        UPDATE tasks
        SET suggested_steps = :suggested_steps,
            updated_at = :updated_at
        WHERE id = :id AND user_id = :user_id;
        """
        return connect_to_sqlite().query_db(query, payload)

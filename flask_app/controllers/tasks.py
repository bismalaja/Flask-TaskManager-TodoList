from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.task import Task
from flask_app.services.ollama_steps import generate_suggested_steps


@app.route("/dashboard", methods=["GET"])
def dashboard():
    status_filter = request.args.get("status", "all")
    search_term = request.args.get("search", "").strip()
    tasks = Task.get_all(session["user_id"], status_filter, search_term)

    return render_template(
        "dashboard.html",
        tasks=tasks,
        status_filter=status_filter,
        search_term=search_term,
    )


@app.route("/tasks/new", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        if not Task.validate_task(request.form):
            return redirect("/tasks/new")

        task_data = {
            "user_id": session["user_id"],
            "title": request.form["title"],
            "description": request.form["description"],
            "due_date": request.form["due_date"],
            "priority": request.form["priority"],
            "status": request.form["status"],
            "suggested_steps": [],
        }
        task_id = Task.create(task_data)

        steps, ai_error = generate_suggested_steps(
            task_data["title"],
            task_data["description"],
            task_data["status"],
        )

        if steps:
            Task.update_suggested_steps(task_id, session["user_id"], steps)
        elif ai_error:
            flash("Task saved, but AI suggested steps are unavailable right now.", "task_error")

        flash("Task created.", "task_success")
        return redirect("/dashboard")

    return render_template("task_form.html", form_mode="create", task=None)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def view_task(task_id):
    task = Task.get_by_id(task_id, session["user_id"])
    if not task:
        flash("Task not found.", "task_error")
        return redirect("/dashboard")

    return render_template("task_details.html", task=task)


@app.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.get_by_id(task_id, session["user_id"])
    if not task:
        flash("Task not found.", "task_error")
        return redirect("/dashboard")

    if request.method == "POST":
        if not Task.validate_task(request.form):
            return redirect(f"/tasks/edit/{task_id}")

        updated_title = request.form["title"]
        updated_description = request.form["description"]
        updated_status = request.form["status"]

        should_refresh_steps = (
            task["status"] != updated_status
            or task["title"].strip() != updated_title.strip()
            or task["description"].strip() != updated_description.strip()
        )

        Task.update(
            {
                "id": task_id,
                "user_id": session["user_id"],
                "title": updated_title,
                "description": updated_description,
                "due_date": request.form["due_date"],
                "priority": request.form["priority"],
                "status": updated_status,
            }
        )

        if updated_status == "done":
            Task.update_suggested_steps(task_id, session["user_id"], [])
        elif should_refresh_steps:
            steps, ai_error = generate_suggested_steps(
                updated_title,
                updated_description,
                updated_status,
            )

            if steps:
                Task.update_suggested_steps(task_id, session["user_id"], steps)
            elif ai_error:
                flash("Task updated, but AI suggested steps are unavailable right now.", "task_error")

        flash("Task updated.", "task_success")
        return redirect("/dashboard")

    return render_template("task_form.html", form_mode="edit", task=task)


@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    deleted = Task.delete(task_id, session["user_id"])
    if not deleted:
        flash("Task not found.", "task_error")
        return redirect("/dashboard")

    flash("Task deleted.", "task_success")
    return redirect("/dashboard")

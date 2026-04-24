# Flask Task Manager / Todo List

A simple but powerful Task Management application built with Flask and SQLite. This application allows users to manage their tasks, with an added feature of AI-powered suggested steps to break down complex tasks.

## Features

- **User Authentication**: Register, login, and logout flows with password hashing (`Flask-Bcrypt`) and session-based access control.
- **Task Management**: Create, Read, Update, and Delete (CRUD) operations for tasks.
- **Per-User Task Isolation**: Each user can only view and manage their own tasks.
- **Task Filtering and Search**: Filter tasks by status (To Do, In Progress, Done) and search for tasks by title.
- **AI-Powered Suggested Steps**: Tasks can include AI-generated suggested steps via Ollama; steps are refreshed when key task fields change and cleared when a task is marked done.
- **Validation and Feedback**: Server-side validation and flash messages for user and task forms.
- **Responsive UI**: A clean and simple user interface built with Bootstrap.
- **Unit Tests**: Lightweight tests for task/user validation and Ollama step parsing behavior.

## Project Structure

The project is structured as a standard Flask application with the following layout:

```
.
├── app.py
├── app.db
├── flask_app
│   ├── __init__.py
│   ├── config
│   │   └── sqliteconnection.py
│   ├── controllers
│   │   ├── tasks.py
│   │   └── users.py
│   ├── models
│   │   ├── task.py
│   │   └── user.py
│   ├── services
│   │   ├── __init__.py
│   │   └── ollama_steps.py
│   ├── static
│   │   └── main.css
│   └── templates
│       ├── dashboard.html
│       ├── layout.html
│       ├── login.html
│       ├── register.html
│       ├── task_details.html
│       └── task_form.html
└── tests
    ├── test_ollama_steps.py
    ├── test_task_model.py
    └── test_user_model.py
```

- **app.py**: The main entry point for the Flask application.
- **app.db**: Local SQLite database file, created automatically at runtime.
- **flask_app/config/sqliteconnection.py**: Handles SQLite connections and initializes/migrates required tables.
- **flask_app/controllers/**: Contains the route handlers for different parts of the application (users and tasks).
- **flask_app/models/**: Contains the data models for the application (`Task` and `User`).
- **flask_app/services/ollama_steps.py**: A service that integrates with the Ollama AI to provide suggested steps for tasks.
- **flask_app/static/**: Contains static assets like CSS and JavaScript files.
- **flask_app/templates/**: Contains the HTML templates for the application.
- **tests/**: Unit tests for validation rules and AI step parsing helpers.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask-Bcrypt
- pytest (for tests)
- (Optional) Ollama for AI features

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bismalaja/Flask-TaskManager-TodoList.git
    cd Flask-TaskManager-TodoList
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install Flask Flask-Bcrypt pytest
    ```

4.  **Initialize the database:**
    The application will automatically create and initialize the `app.db` SQLite database file when you first run it.

## Usage

1.  **Run the application:**
    ```bash
    python app.py
    ```

2.  **Open your browser and navigate to `http://127.0.0.1:5000`**.

You will be taken to the main dashboard where you can start adding and managing your tasks.

## Running Unit Tests

Run the lightweight unit test suite with:

```bash
python -m pytest -q
```

To run the tests with verbose output:

```bash
python -m pytest -v
```

## AI Integration

This project uses [Ollama](https://ollama.ai/) to provide AI-powered suggested steps for your tasks. When you create or edit a task, the application sends a request to the Ollama service with the task's title, description, and status. The service then returns a list of suggested steps to help you break down the task into smaller, more manageable chunks.

### Configuring Ollama

To use the AI features, you need to have Ollama installed and running on your machine. You can configure the Ollama service by setting the following environment variables:

- `OLLAMA_BASE_URL`: The base URL of your Ollama instance (defaults to `http://127.0.0.1:11434`).
- `OLLAMA_MODEL`: The name of the Ollama model you want to use.
- `OLLAMA_MODEL_CANDIDATES`: A comma-separated list of fallback models to try if the primary model is not available.
- `OLLAMA_TIMEOUT_SECONDS`: The timeout for requests to the Ollama service (defaults to 20 seconds).
- `OLLAMA_MODEL_CACHE_SECONDS`: How long to cache resolved model selection before refreshing (defaults to 300 seconds).

If Ollama is not available, the application will still function normally, but the suggested steps feature will be disabled.

## Future Improvements

- **Task Categories/Tags**: Add the ability to categorize or tag tasks for better organization.
- **File Attachments**: Allow users to attach files to their tasks.
- **More AI Features**: Expand the AI integration to include features like task prioritization, deadline suggestions, and more.

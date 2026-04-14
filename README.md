# Flask Task Manager

A simple but powerful Task Management application built with Flask and SQLite. This application allows users to manage their tasks, with an added feature of AI-powered suggested steps to break down complex tasks.

## Features

- **User Management**: A simplified user system (currently with a single mock user).
- **Task Management**: Create, Read, Update, and Delete (CRUD) operations for tasks.
- **Task Filtering and Search**: Filter tasks by status (To Do, In Progress, Done) and search for tasks by title.
- **AI-Powered Suggested Steps**: For each task, the application can suggest a series of steps to complete the task, using the Ollama service.
- **Responsive UI**: A clean and simple user interface built with Bootstrap.

## Project Structure

The project is structured as a standard Flask application with the following layout:

```
.
├── app.db
├── app.py
├── flask_app
│   ├── config
│   │   └── sqliteconnection.py
│   ├── controllers
│   │   ├── tasks.py
│   │   └── users.py
│   ├── __init__.py
│   ├── models
│   │   └── task.py
│   ├── services
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
```

- **app.py**: The main entry point for the Flask application.
- **flask_app/config/sqliteconnection.py**: Handles the connection to the SQLite database.
- **flask_app/controllers/**: Contains the route handlers for different parts of the application (users and tasks).
- **flask_app/models/**: Contains the data models for the application (e.g., the `Task` model).
- **flask_app/services/ollama_steps.py**: A service that integrates with the Ollama AI to provide suggested steps for tasks.
- **flask_app/static/**: Contains static assets like CSS and JavaScript files.
- **flask_app/templates/**: Contains the HTML templates for the application.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
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
    pip install Flask
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

## AI Integration

This project uses [Ollama](https://ollama.ai/) to provide AI-powered suggested steps for your tasks. When you create or edit a task, the application sends a request to the Ollama service with the task's title, description, and status. The service then returns a list of suggested steps to help you break down the task into smaller, more manageable chunks.

### Configuring Ollama

To use the AI features, you need to have Ollama installed and running on your machine. You can configure the Ollama service by setting the following environment variables:

- `OLLAMA_BASE_URL`: The base URL of your Ollama instance (defaults to `http://127.0.0.1:11434`).
- `OLLAMA_MODEL`: The name of the Ollama model you want to use.
- `OLLAMA_MODEL_CANDIDATES`: A comma-separated list of fallback models to try if the primary model is not available.
- `OLLAMA_TIMEOUT_SECONDS`: The timeout for requests to the Ollama service (defaults to 20 seconds).

If Ollama is not available, the application will still function normally, but the suggested steps feature will be disabled.

## Future Improvements

- **Task Categories/Tags**: Add the ability to categorize or tag tasks for better organization.
- **File Attachments**: Allow users to attach files to their tasks.
- **More AI Features**: Expand the AI integration to include features like task prioritization, deadline suggestions, and more.

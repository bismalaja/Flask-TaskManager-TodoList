# Sasquatch Websighting

A web application for reporting and managing Sasquatch sightings. Users can register, log in, report new sightings, and manage their reports. Other users can express skepticism by marking sightings as "skeptical."

---

## Features

- User registration and login with secure password hashing.
- Dashboard to view all reported sightings.
- Ability to add, edit, and delete sightings (only by the original reporter).
- Skeptic system: Users can mark sightings as "skeptical."
- Responsive and user-friendly interface.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS (with inline styles)
- **Authentication**: Flask-Bcrypt for password hashing
- **Session Management**: Flask-Session
- **Database Connection**: PyMySQL

---

## Installation

### Prerequisites

1. Python 3.7 or higher
2. MySQL Server
3. Pip (Python package manager)

### Steps to Install

#### 1. Clone the Repository

pip install -r requirements.txt
Set Up the Database:

Import the database schema from flaskappdatabase.mwb (MySQL Workbench file).
Alternatively, use the SQL scripts provided to create the database and tables.
Configure the Application:

Edit mysqlconnection.py with your database credentials:

self.connection = pymysql.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database_name",
    cursorclass=pymysql.cursors.DictCursor
)

## Run the Application:

python app.py
Access the Application: Open your browser and navigate to:

#### Usage

User Workflow

## Registration:

New users can register with their email, name, and password.

## Login:
Registered users can log in to access the dashboard.

## Dashboard:
View all reported sightings, along with the number of skeptics.
Buttons are provided for editing, deleting, or expressing skepticism.

## Reporting Sightings:
Users can report a new sighting by providing a location, date, number of Sasquatches, and a description of the event.

## Skeptic System:
Click the "I'm Skeptical" button to increase skepticism for a sighting.
Clicking again removes your skepticism.


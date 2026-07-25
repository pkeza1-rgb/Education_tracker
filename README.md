# University Student Education Tracker

## Project Overview

The University Student Education Tracker is a Python-based command-line application designed to help universities manage student academic information efficiently. The system allows administrators to register students, manage courses, record grades, track attendance, and update student records. Students can securely log in to view their own profiles, grades, and attendance information.

The application uses SQLite as the database management system and follows a modular design where different functionalities are separated into independent Python files.

---

# Features

## Authentication System
- Secure login system with role-based access.
- Supports:
  - Administrator accounts
  - Student accounts
- Limits login attempts for security.

## Student Management
Administrators can:
- Register new students.
- Generate unique student IDs.
- View all registered students.
- Search students by ID or name.
- Update student information.
- Delete student records.

## Course Management
Administrators can:
- View available courses.
- Assign courses to students.
- Prevent duplicate course enrollments.

## Grade Management
Administrators can:
- Add grades for students.
- Ensure grades are within valid ranges.
- View student academic performance.

Students can:
- View their own grades.

## Attendance Management
Administrators can:
- Mark student attendance.
- Record attendance status:
  - Present
  - Absent
  - Late

Students can:
- View their attendance reports.
- Monitor their attendance rate.

## Database Management
The system uses SQLite with:
- Primary keys
- Foreign keys
- Data validation constraints
- Unique constraints
- Relational database structure

---

# Technologies Used

- Python 3
- SQLite3
- SQL
- Git & GitHub
- Linux Terminal

---

# Project Structure

```
Education_tracker/
│
├── database.py          # Database setup and table creation
├── auth.py              # Login and authentication system
├── register.py          # Student registration
├── courses.py           # Course assignment management
├── grades.py            # Grade management
├── attendance.py        # Attendance tracking
├── view_search.py       # Student viewing and searching
├── update_delete.py     # Update and delete operations
├── university.db        # Local SQLite database (generated automatically)
└── README.md            # Project documentation
```

---

# Installation and Setup

## 1. Clone the repository

```bash
git clone https://github.com/pkeza1-rgb/Education_tracker.git
```

## 2. Navigate into the project directory

```bash
cd Education_tracker
```

## 3. Create the database

Run:

```bash
python3 database.py
```

Expected output:

```
Database initialized successfully.
```

This creates the local SQLite database:

```
university.db
```

---

# Running the Application

Run the main application:

```bash
python3 main.py
```

The system will display the login screen.

---

# Default Administrator Account

The database automatically creates a default admin account:

```
Username: admin
Password: admin123
Role: Administrator
```

Administrators can use this account to manage students, courses, grades, and attendance.

---

# Student Accounts

When a student is registered, the system automatically creates a student login account.

Default credentials:

```
Username: Student ID
Password: Student ID
```

Example:

```
Student ID: S001

Username: S001
Password: S001
```

---

# Database Design

The system contains the following main tables:

### Students
Stores student personal and academic information.

### Users
Stores login credentials and user roles.

### Courses
Stores available university courses.

### Enrollments
A junction table connecting students and courses.

### Grades
Stores student academic results.

### Attendance
Stores student attendance records.

### Enrollment History
Tracks changes in student enrollment status.

---

# Data Integrity

The database includes:

- Foreign key relationships
- Unique student-course enrollment prevention
- Grade validation (0-100)
- Attendance status validation
- Required fields using NOT NULL constraints

---

# Team Contribution

| Member | Contribution |
|---|---|
| Member 1 | Database setup, authentication system |
| Member 2 | Student registration and management |
| Member 3 | Student search and profile viewing |
| Member 4 | Update and delete functionality |
| Member 5 | Courses, grades, and attendance modules |

---

# Future Improvements

Possible future enhancements include:

- Graphical user interface (GUI)
- Password encryption
- Online database integration
- Automated academic reports
- Email notifications
- Student performance analytics

---

# License

This project was developed as an academic project for learning Python programming, database management, and software development practices.

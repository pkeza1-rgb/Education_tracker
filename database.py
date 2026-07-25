# =============================================================
# database.py — MEMBER 1 (Paradis Keza)
# DB setup, schema creation, connection function
# =============================================================
import sqlite3

DB_NAME = "university.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id        TEXT PRIMARY KEY,
            full_name         TEXT NOT NULL,
            age               INTEGER NOT NULL,
            gender            TEXT NOT NULL,
            date_of_birth     TEXT NOT NULL,
            nationality       TEXT NOT NULL,
            phone_number      TEXT NOT NULL,
            email             TEXT NOT NULL,
            program           TEXT NOT NULL,
            year_of_study     INTEGER NOT NULL,
            admission_date    TEXT NOT NULL,
            enrollment_status TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollment_history (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            status     TEXT NOT NULL,
            changed_on TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role     TEXT NOT NULL
        )
    ''')

    # courses — needed by courses.py, grades.py, attendance.py
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id   TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            lecturer    TEXT NOT NULL,
            credits     INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print('Database initialized successfully.')

if __name__ == '__main__':
    initialize_database()

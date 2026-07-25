# =============================================================
# courses.py — MEMBER 5
# Assign courses to students.
# Record grades for students.
# Display academic transcript.
# =============================================================

import sqlite3
from database import get_connection

def assign_course():
    print('\n' + '='*50)
    print('        ASSIGN COURSE TO STUDENT')
    print('='*50)
    student_id = input('  Enter Student ID: ').strip().upper()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT full_name FROM students WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        if not student:
            print(f'  Student {student_id} not found.')
            conn.close()
            return

        cursor.execute('SELECT course_id, course_name FROM courses')
        courses = cursor.fetchall()
        print('\n  Available Courses:')
        for c in courses:
            print(f"   [{c['course_id']}] {c['course_name']}")

        course_id = input('\n  Enter Course ID to assign: ').strip().upper()
        cursor.execute('SELECT course_name FROM courses WHERE course_id = ?', (course_id,))
        course = cursor.fetchone()
        if not course:
            print(f'  Course {course_id} not found.')
            conn.close()
            return

        cursor.execute('SELECT * FROM enrollments WHERE student_id = ? AND course_id = ?',
                       (student_id, course_id))
        if cursor.fetchone():
            print(f"  Student is already enrolled in {course['course_name']}.")
            conn.close()
            return

        cursor.execute('INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)',
                       (student_id, course_id))
        conn.commit()
        conn.close()
        print(f"\n  Successfully assigned {course['course_name']} to {student['full_name']}!")

    except sqlite3.Error as e:
        print(f'  Database error: {e}')
    except Exception as e:
        print(f'  Unexpected error: {e}')
        
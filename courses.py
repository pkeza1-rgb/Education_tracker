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

def generate_course_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM courses')
    count = cursor.fetchone()[0]
    conn.close()
    return f'C{str(count + 1).zfill(3)}'

def add_course():
    print('\n' + '=' * 50)
    print('        ADD NEW COURSE')
    print('=' * 50)
    course_name = input('  Course Name: ').strip()
    lecturer = input('  Lecturer Name: ').strip()
    credits_str = input('  Credit Hours (1-6): ').strip()

    if not credits_str.isdigit() or not (1 <= int(credits_str) <= 6):
        print('  Invalid credit hours. Must be a number between 1 and 6.')
        return

    course_id = generate_course_id()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO courses VALUES (?,?,?,?)',
            (course_id, course_name, lecturer, int(credits_str))
        )
        conn.commit()
        conn.close()
        print(f'\n  Course added successfully!')
        print(f'  Course ID: {course_id}')
    except sqlite3.Error as e:
        print(f'  Database error: {e}')
    except Exception as e:
        print(f'  Unexpected error: {e}')

def view_all_courses():
    print('\n' + '=' * 65)
    print('  ALL COURSES')
    print('=' * 65)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses ORDER BY course_id')
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print('  No courses added yet.')
            return

        print(f"  {'ID':<8} {'Course Name':<30} {'Lecturer':<20} Credits")
        print('  ' + '-' * 60)
        for row in rows:
            print(f"  {row['course_id']:<8} {row['course_name']:<30} "
                  f"{row['lecturer']:<20} {row['credits']}")
        print('  ' + '-' * 60)
        print(f'  Total Courses: {len(rows)}')
    except Exception as e:
        print(f'  Error retrieving courses: {e}')
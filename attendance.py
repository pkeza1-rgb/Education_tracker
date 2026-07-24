# =============================================================
# attendance.py — MEMBER 5 (Paradis Ange Keza)
# Mark attendance for a student in a course.
# View attendance report for a student.
# Students can view their own attendance.
# =============================================================
import sqlite3
from database import get_connection
from datetime import datetime

def mark_attendance():
    print('\n' + '='*50)
    print('        MARK ATTENDANCE')
    print('='*50)
    student_id = input('  Enter Student ID: ').strip().upper()
    course_id  = input('  Enter Course ID: ').strip().upper()
    date_str   = input('  Date (DD/MM/YYYY) or press Enter for today: ').strip()

    if not date_str:
        date_str = datetime.now().strftime('%d/%m/%Y')
    else:
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            print('  Invalid date format. Use DD/MM/YYYY.')
            return

    status = input('  Status (Present/Absent/Late): ').strip().capitalize()
    if status not in ['Present', 'Absent', 'Late']:
        print('  Invalid status. Choose Present, Absent, or Late.')
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT full_name FROM students WHERE student_id = ?',
                       (student_id,))
        student = cursor.fetchone()
        if not student:
            print(f'  Student {student_id} not found.')
            conn.close()
            return

        cursor.execute('SELECT course_name FROM courses WHERE course_id = ?',
                       (course_id,))
        course = cursor.fetchone()
        if not course:
            print(f'  Course {course_id} not found.')
            conn.close()
            return

        # Check not already marked for this date
        cursor.execute('''
            SELECT id FROM attendance
            WHERE student_id = ? AND course_id = ? AND date = ?
        ''', (student_id, course_id, date_str))
        if cursor.fetchone():
            print(f'  Attendance already marked for {date_str}.')
            conn.close()
            return

        cursor.execute('''
            INSERT INTO attendance (student_id, course_id, date, status)
            VALUES (?,?,?,?)
        ''', (student_id, course_id, date_str, status))
        conn.commit()
        conn.close()
        print(f"\n  Attendance marked successfully!")
        print(f"  {student['full_name']} | {course['course_name']} | {date_str} | {status}")
    except sqlite3.Error as e:
        print(f'  Database error: {e}')
    except Exception as e:
        print(f'  Unexpected error: {e}')

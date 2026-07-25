# =============================================================
# grades.py — MEMBER 5 (Rudakemwa Aldo)
# Add a grade for a student in a course.
# View all grades for a student.
# Calculate and display GPA.
# Students can view their own grades.
# =============================================================
import sqlite3
from database import get_connection
from datetime import datetime

def add_grade():
    print('\n' + '='*50)
    print('        ADD GRADE')
    print('='*50)
    student_id = input('  Enter Student ID: ').strip().upper()
    course_id  = input('  Enter Course ID: ').strip().upper()
    grade_str  = input('  Enter Grade (0-100): ').strip()

    if not grade_str.replace('.', '', 1).isdigit():
        print('  Invalid grade. Enter a number between 0 and 100.')
        return
    grade = float(grade_str)
    if not (0 <= grade <= 100):
        print('  Grade must be between 0 and 100.')
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT full_name FROM students WHERE student_id = ?',
            (student_id,)
        )
        student = cursor.fetchone()
        if not student:
            print(f'  Student {student_id} not found.')
            conn.close()
            return

        cursor.execute(
            'SELECT course_name FROM courses WHERE course_id = ?',
            (course_id,)
        )
        course = cursor.fetchone()
        if not course:
            print(f'  Course {course_id} not found.')
            conn.close()
            return

        cursor.execute('''
            SELECT id FROM enrollments
            WHERE student_id = ? AND course_id = ?
        ''', (student_id, course_id))

        if not cursor.fetchone():
            print(f"  {student['full_name']} is not enrolled in {course['course_name']}.")
            print('  Please enroll the student in this course first.')
            conn.close()
            return

        cursor.execute('''
            INSERT INTO grades (student_id, course_id, grade, grade_date)
            VALUES (?,?,?,?)
        ''', (
            student_id,
            course_id,
            grade,
            datetime.now().strftime('%d/%m/%Y')
        ))

        conn.commit()
        conn.close()

        letter = _to_letter(grade)

        print("\n  Grade recorded successfully!")
        print(f"  {student['full_name']} | {course['course_name']} | {grade} ({letter})")

    except sqlite3.Error as e:
        print(f'  Database error: {e}')

    except Exception as e:
        print(f'  Unexpected error: {e}')
        
def _to_letter(grade):
    if grade >= 90: return 'A+'
    if grade >= 80: return 'A'
    if grade >= 75: return 'B+'
    if grade >= 70: return 'B'
    if grade >= 65: return 'C+'
    if grade >= 60: return 'C'
    if grade >= 50: return 'D'
    return 'F'
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

        cursor.execute('SELECT course_code, course_name FROM courses')
        courses = cursor.fetchall()
        print('\n  Available Courses:')
        for c in courses:
            print(f"   [{c['course_code']}] {c['course_name']}")

        course_code = input('\n  Enter Course Code to assign: ').strip().upper()
        cursor.execute('SELECT course_name FROM courses WHERE course_code = ?', (course_code,))
        course = cursor.fetchone()
        if not course:
            print(f'  Course {course_code} not found.')
            conn.close()
            return

        cursor.execute('SELECT * FROM enrollments WHERE student_id = ? AND course_code = ?',
                       (student_id, course_code))
        if cursor.fetchone():
            print(f"  Student is already enrolled in {course['course_name']}.")
            conn.close()
            return

        cursor.execute('INSERT INTO enrollments (student_id, course_code) VALUES (?, ?)',
                       (student_id, course_code))
        conn.commit()
        conn.close()
        print(f"\n  Successfully assigned {course['course_name']} to {student['full_name']}!")

    except sqlite3.Error as e:
        print(f'  Database error: {e}')
    except Exception as e:
        print(f'  Unexpected error: {e}')

        def record_grade():
    print('\n' + '='*50)
    print('        RECORD STUDENT GRADE')
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

        cursor.execute('''
            SELECT c.course_code, c.course_name 
            FROM enrollments e
            JOIN courses c ON e.course_code = c.course_code
            WHERE e.student_id = ?
        ''', (student_id,))
        enrolled = cursor.fetchall()

        if not enrolled:
            print(f'  Student {student_id} is not enrolled in any courses.')
            conn.close()
            return

        print('\n  Enrolled Courses:')
        for c in enrolled:
            print(f"   [{c['course_code']}] {c['course_name']}")

        course_code = input('\n  Enter Course Code to grade: ').strip().upper()
        valid_codes = [c['course_code'] for c in enrolled]
        if course_code not in valid_codes:
            print('  Student is not enrolled in that course.')
            conn.close()
            return

        grade_input = input('  Enter Grade (0 - 100): ').strip()
        try:
            grade = float(grade_input)
            if not (0 <= grade <= 100):
                print('  Grade must be between 0 and 100.')
                conn.close()
                return
        except ValueError:
            print('  Invalid grade input.')
            conn.close()
            return

        cursor.execute('''
            INSERT INTO grades (student_id, course_code, grade)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, course_code) 
            DO UPDATE SET grade = excluded.grade
        ''', (student_id, course_code, grade))

        conn.commit()
        conn.close()
        print(f"\n  Grade {grade} recorded for {course_code} successfully!")

    except sqlite3.Error as e:
        print(f'  Database error: {e}')
    except Exception as e:
        print(f'  Unexpected error: {e}')

def view_transcript():
    print('\n' + '='*50)
    print('        ACADEMIC TRANSCRIPT')
    print('='*50)
    student_id = input('  Enter Student ID: ').strip().upper()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT full_name, program FROM students WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        if not student:
            print(f'  Student {student_id} not found.')
            conn.close()
            return

        cursor.execute('''
            SELECT c.course_code, c.course_name, g.grade
            FROM enrollments e
            JOIN courses c ON e.course_code = c.course_code
            LEFT JOIN grades g ON e.student_id = g.student_id AND e.course_code = g.course_code
            WHERE e.student_id = ?
        ''', (student_id,))
        records = cursor.fetchall()

        print(f"\n  Transcript for: {student['full_name']} ({student_id})")
        print(f"  Program       : {student['program']}")
        print('  ' + '-'*45)
        print(f"  {'CODE':<10} {'COURSE NAME':<25} {'GRADE':<8}")
        print('  ' + '-'*45)

        if not records:
            print('  No courses assigned yet.')
        else:
            total_grades = []
            for r in records:
                grade_str = f"{r['grade']:.1f}" if r['grade'] is not None else 'N/A'
                if r['grade'] is not None:
                    total_grades.append(r['grade'])
                print(f"  {r['course_code']:<10} {r['course_name']:<25} {grade_str:<8}")

            print('  ' + '-'*45)
            if total_grades:
                gpa_avg = sum(total_grades) / len(total_grades)
                print(f"  Average Grade : {gpa_avg:.2f}%")

        conn.close()

    except sqlite3.Error as e:
        print(f'  Database error: {e}')
    except Exception as e:
        print(f'  Unexpected error: {e}')
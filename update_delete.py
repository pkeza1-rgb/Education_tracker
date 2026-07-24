# =============================================================
# update_delete.py — MEMBER 4 (Tenketem)
# Update any field on a student record.
# Delete a student record with confirmation.
# Handles all DB errors for these two operations.
# =============================================================

import sqlite3
from datetime import datetime
from database import get_connection

def _prompt(label, current):
    val = input(f'  {label} [{current}]: ').strip()
    return val if val else current

def update_student():
    print('\n' + '='*50)
    print('        UPDATE STUDENT INFORMATION')
    print('='*50)
    student_id = input('  Enter Student ID to update: ').strip().upper()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        if not student:
            print(f'  Student {student_id} not found.')
            conn.close()
            return
        print(f"\n  Updating record for: {student['full_name']}")
        print('  (Press Enter to keep the current value)\n')
        full_name   = _prompt('Full Name',         student['full_name'])
        age         = _prompt('Age',               str(student['age']))
        gender      = _prompt('Gender',            student['gender'])
        dob         = _prompt('Date of Birth',     student['date_of_birth'])
        nationality = _prompt('Nationality',       student['nationality'])
        phone       = _prompt('Phone Number',      student['phone_number'])
        email       = _prompt('Email',             student['email'])
        program     = _prompt('Program',           student['program'])
        year        = _prompt('Year of Study',     str(student['year_of_study']))
        adm_date    = _prompt('Admission Date',    student['admission_date'])
        status      = _prompt('Enrollment Status', student['enrollment_status'])

        if not age.isdigit() or not (18 <= int(age) <= 100):
            print('  Invalid age. Update cancelled.')
            conn.close()
            return
        if year not in ['1', '2', '3', '4']:
            print('  Invalid year of study. Update cancelled.')
            conn.close()
            return

        cursor.execute('''
            UPDATE students SET
                full_name=?, age=?, gender=?, date_of_birth=?,
                nationality=?, phone_number=?, email=?, program=?,
                year_of_study=?, admission_date=?, enrollment_status=?
            WHERE student_id=?
        ''', (full_name, int(age), gender, dob, nationality,
              phone, email, program, int(year), adm_date, status,
              student_id))

        if status != student['enrollment_status']:
            cursor.execute('''
                INSERT INTO enrollment_history (student_id, status, changed_on)
                VALUES (?,?,?)
            ''', (student_id, status, datetime.now().strftime('%d/%m/%Y')))

        conn.commit()
        conn.close()
        print(f'\n  Record for {student_id} updated successfully!')

    except sqlite3.Error as e:
        print(f'  Database error: {e}')
    except Exception as e:
        print(f'  Unexpected error: {e}')

def delete_student():
    print('\n' + '='*50)
    print('        DELETE A STUDENT RECORD')
    print('='*50)
    student_id = input('  Enter Student ID to delete: ').strip().upper()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        if not student:
            print(f'  Student {student_id} not found.')
            conn.close()
            return
        print('\n  +-------------------------------------+')
        print('  |         STUDENT TO DELETE           |')
        print('  +-------------------------------------+')
        print(f"  |  Name    : {student['full_name']:<26}|")
        print(f"  |  ID      : {student['student_id']:<26}|")
        print(f"  |  Program : {student['program']:<26}|")
        print(f"  |  Status  : {student['enrollment_status']:<26}|")
        print('  +-------------------------------------+')
        confirm = input('\n  Are you sure you want to delete? (Y/N): ').strip().upper()
        if confirm == 'Y':
            # Delete in correct order to respect foreign keys
            cursor.execute('DELETE FROM attendance WHERE student_id = ?',       (student_id,))
            cursor.execute('DELETE FROM grades WHERE student_id = ?',            (student_id,))
            cursor.execute('DELETE FROM enrollments WHERE student_id = ?',       (student_id,))
            cursor.execute('DELETE FROM enrollment_history WHERE student_id = ?',(student_id,))
            cursor.execute('DELETE FROM users WHERE username = ?',               (student_id,))
            cursor.execute('DELETE FROM students WHERE student_id = ?',          (student_id,))
            conn.commit()
            print(f"\n  Record for {student['full_name']} deleted successfully.")
        elif confirm == 'N':
            print('  Deletion cancelled. Returning to menu.')
        else:
            print('  Invalid input. Deletion cancelled.')
        conn.close()
    except sqlite3.Error as e:
        print(f'  Database error: {e}')
    except Exception as e:
        print(f'  Unexpected error: {e}')
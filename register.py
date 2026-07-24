# =============================================================
# register.py 
# Student registration with full input validation.
# Also creates a student login account after registration.
# =============================================================

import re
import sqlite3
from datetime import datetime
from database import get_connection
from auth import create_student_account

def validate_name(name):
    return bool(re.match(r'^[A-Za-z\s]+$', name.strip()))

def validate_age(age_str):
    return age_str.strip().isdigit() and 18 <= int(age_str.strip()) <= 100

def validate_gender(gender):
    return gender.strip().capitalize() in ['Male', 'Female', 'Other']

def validate_email(email):
    return '@' in email and '.' in email.split('@')[-1]

def validate_phone(phone):
    return phone.strip().isdigit() and len(phone.strip()) >= 7

def validate_year(year_str):
    return year_str.strip() in ['1', '2', '3', '4']

def validate_date(date_str):
    try:
        datetime.strptime(date_str.strip(), '%d/%m/%Y')
        return True
    except ValueError:
        return False

def validate_status(status):
    return status.strip().capitalize() in [
        'Active', 'Inactive', 'Graduated', 'Deferred', 'Withdrawn']

def get_input(prompt, validator, error_msg):
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f'  X {error_msg}')

def generate_student_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM students')
    count = cursor.fetchone()[0]
    conn.close()
    return f'S{str(count + 1).zfill(3)}'

def register_student():
    print('\n' + '='*50)
    print('        REGISTER NEW STUDENT')
    print('='*50)

    full_name     = get_input('  Full Name: ', validate_name,
                              'Use only letters and spaces.')
    age           = get_input('  Age: ', validate_age,
                              'Enter a number between 18 and 100.')
    gender        = get_input('  Gender (Male/Female/Other): ', validate_gender,
                              'Enter Male, Female, or Other.')
    dob           = get_input('  Date of Birth (DD/MM/YYYY): ', validate_date,
                              'Use DD/MM/YYYY format.')
    nationality   = input('  Nationality: ').strip()
    phone_number  = get_input('  Phone Number: ', validate_phone,
                              'Digits only, minimum 7 digits.')
    email         = get_input('  Email Address: ', validate_email,
                              'Must contain @ and a valid domain.')
    program       = input('  Program of Study: ').strip()
    year_of_study = get_input('  Year of Study (1-4): ', validate_year,
                              'Enter 1, 2, 3, or 4.')
    admission_date = get_input('  Admission Date (DD/MM/YYYY): ', validate_date,
                               'Use DD/MM/YYYY format.')
    status = get_input(
        '  Enrollment Status (Active/Inactive/Graduated/Deferred/Withdrawn): ',
        validate_status,
        'Choose: Active, Inactive, Graduated, Deferred, or Withdrawn.')

    student_id = generate_student_id()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (student_id, full_name, int(age), gender.capitalize(),
              dob, nationality, phone_number, email,
              program, int(year_of_study), admission_date,
              status.capitalize()))
        cursor.execute('''
            INSERT INTO enrollment_history (student_id, status, changed_on)
            VALUES (?,?,?)
        ''', (student_id, status.capitalize(),
              datetime.now().strftime('%d/%m/%Y')))
        conn.commit()
        conn.close()

        # Create login account for this student
        create_student_account(student_id)

        print(f'\n  Student registered successfully!')
        print(f'  Student ID : {student_id}')
        print(f'  Login ID   : {student_id}')
        print(f'  Password   : {student_id}  (student should change this)')

    except sqlite3.IntegrityError:
        print(f'  Error: ID {student_id} already exists.')
    except Exception as e:
        print(f'  Unexpected error: {e}')
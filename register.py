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
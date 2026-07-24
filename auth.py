# =============================================================
# auth.py — MEMBER 1 (Paradis Keza)
# Login system. Returns the logged-in user and their role.
# Called by main.py before showing any menu.
# =============================================================
from database import get_connection

def login():
    print('\n' + '='*50)
    print('   UNIVERSITY STUDENT EDUCATION TRACKER')
    print('='*50)
    print('  Please log in to continue.')
    print('='*50)

    attempts = 0
    while attempts < 3:
        username = input('\n  Username: ').strip()
        password = input('  Password: ').strip()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE username = ? AND password = ?',
                (username, password)
            )
            user = cursor.fetchone()
            conn.close()

            if user:
                print(f'\n  Login successful. Welcome, {username}!')
                print(f'  Role: {user["role"].upper()}')
                return {'username': username, 'role': user['role']}
            else:
                attempts += 1
                remaining = 3 - attempts
                if remaining > 0:
                    print(f'  Incorrect username or password. {remaining} attempt(s) remaining.')
                else:
                    print('  Too many failed attempts. Exiting.')
                    return None

        except Exception as e:
            print(f'  Login error: {e}')
            return None

def create_student_account(student_id):
    """Creates a login account for a newly registered student."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM users WHERE username = ?', (student_id,)
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                (student_id, student_id, 'student')
            )
            conn.commit()
        conn.close()
    except Exception as e:
        print(f'  Warning: Could not create student account: {e}')

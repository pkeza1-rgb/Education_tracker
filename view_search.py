
from database import get_connection
def view_all_students():
    print('\n' + '='*75)
    print('  ALL REGISTERED STUDENTS')
    print('='*75)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT student_id, full_name, program, year_of_study, enrollment_status
            FROM students ORDER BY student_id
        ''')
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            print('  No students registered yet.')
            return
        print(f"  {'ID':<8} {'Name':<25} {'Program':<25} {'Year':<6} Status")
        print('  ' + '-'*70)
        for row in rows:
            print(f"  {row['student_id']:<8} {row['full_name']:<25} "
                  f"{row['program']:<25} {row['year_of_study']:<6} "
                  f"{row['enrollment_status']}")
        print('  ' + '-'*70)
        print(f'  Total Students: {len(rows)}')
    except Exception as e:
        print(f'  Error retrieving students: {e}')
        def _print_profile(s):
    print('\n  ' + '='*45)
    print('          STUDENT PROFILE')
    print('  ' + '='*45)
    for label, key in [
        ('Student ID','student_id'), ('Full Name','full_name'), ('Age','age'),
        ('Gender','gender'), ('Date of Birth','date_of_birth'),
        ('Nationality','nationality'), ('Phone','phone_number'),
        ('Email','email'), ('Program','program'),
        ('Year of Study','year_of_study'), ('Admission Date','admission_date'),
        ('Status','enrollment_status')]:
        print(f'  {label:<22}: {s[key]}')
    print('  ' + '='*45)
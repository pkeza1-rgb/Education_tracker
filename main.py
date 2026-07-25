# =============================================================
# MEMBER 6 (Rebecca Isaboke)
# Entry point. Logs the user in, then shows the Admin menu or
# the Student menu depending on their role. Ties every module
# together. This file did not exist before — nothing actually
# ran the app end-to-end until now.
# =============================================================
from database import initialize_database
from auth import login
from register import register_student
from view_search import view_all_students, search_student, view_own_profile
from update_delete import update_student, delete_student
from courses import add_course, view_all_courses, assign_course
from grades import add_grade
from attendance import mark_attendance, view_attendance

# ── ADMIN MENU ────────────────────────────────────────────────
def admin_menu():
    while True:
        print('\n' + '=' * 50)
        print('              ADMIN MENU')
        print('=' * 50)
        print('  --- STUDENT MANAGEMENT ---')
        print('  1.  Register New Student')
        print('  2.  View All Students')
        print('  3.  Search for a Student')
        print('  4.  Update Student Information')
        print('  5.  Delete a Student Record')
        print('')
        print('  --- COURSE MANAGEMENT ---')
        print('  6.  Add New Course')
        print('  7.  View All Courses')
        print('  8.  Assign Student to Course')
        print('')
        print('  --- ACADEMIC RECORDS ---')
        print('  9.  Add Grade for Student')
        print('  10. Mark Attendance')
        print('  11. View Attendance Report')
        print('')
        print('  0.  Logout')
        print('=' * 50)

        choice = input('  Enter your choice: ').strip()

        if choice == '1':
            register_student()
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            add_course()
        elif choice == '7':
            view_all_courses()
        elif choice == '8':
            assign_course()
        elif choice == '9':
            add_grade()
        elif choice == '10':
            mark_attendance()
        elif choice == '11':
            view_attendance()
        elif choice == '0':
            print('\n  Logged out successfully.')
            break
        else:
            print('  Invalid choice. Enter a number from the menu.')

# ── STUDENT MENU ──────────────────────────────────────────────
def student_menu(username):
    while True:
        print('\n' + '=' * 50)
        print('             STUDENT MENU')
        print('=' * 50)
        print('  1. View My Profile')
        print('  2. View My Attendance Report')
        print('  0. Logout')
        print('=' * 50)

        choice = input('  Enter your choice: ').strip()

        if choice == '1':
            view_own_profile(username)
        elif choice == '2':
            view_attendance(username)
        elif choice == '0':
            print('\n  Logged out successfully.')
            break
        else:
            print('  Invalid choice. Enter 1, 2, or 0.')
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
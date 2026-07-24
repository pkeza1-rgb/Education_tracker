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

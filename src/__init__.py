"""
Student Success Tracking System
A comprehensive digital platform to monitor and enhance student academic performance.
"""

import os

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'src', 'data')
DB_PATH = os.path.join(DATA_DIR, 'student_tracking.db')

import sqlite3
import csv
import json
from datetime import datetime
import os
import re
from typing import Dict, List, Any

class SchemaUpdater:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_new_tables(self):
        """Create new required tables"""
        # Achievement tracking table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_achievements (
                id INTEGER PRIMARY KEY,
                student_id TEXT NOT NULL,
                achievement_type TEXT NOT NULL,
                achievement_name TEXT NOT NULL,
                description TEXT,
                date_achieved TIMESTAMP NOT NULL,
                verified_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(StudentID)
            )
        """)

        # Notification system table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY,
                student_id TEXT NOT NULL,
                notification_type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                read_status BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(StudentID)
            )
        """)

        # Device sync logs table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS device_sync_logs (
                id INTEGER PRIMARY KEY,
                student_id TEXT NOT NULL,
                device_id TEXT NOT NULL,
                device_type TEXT NOT NULL,
                last_sync_time TIMESTAMP NOT NULL,
                sync_status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(StudentID)
            )
        """)

    def alter_existing_tables(self):
        """Add new columns to existing tables"""
        # Students table updates
        student_columns = [
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "last_login TIMESTAMP",
            "device_info TEXT",  # JSON field
            "profile_status TEXT DEFAULT 'active'"
        ]

        # Exam results table updates
        exam_columns = [
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "grading_scale TEXT",
            "feedback TEXT",
            "verified_by TEXT"
        ]

        # Course table updates
        course_columns = [
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "active_status BOOLEAN DEFAULT TRUE",
            "prerequisites TEXT",  # JSON array
            "learning_outcomes TEXT"  # JSON array
        ]

        for column in student_columns:
            try:
                self.cursor.execute(f"ALTER TABLE students ADD COLUMN {column}")
            except sqlite3.OperationalError:
                continue

        for column in exam_columns:
            try:
                self.cursor.execute(f"ALTER TABLE exam_results ADD COLUMN {column}")
            except sqlite3.OperationalError:
                continue

        for column in course_columns:
            try:
                self.cursor.execute(f"ALTER TABLE courses ADD COLUMN {column}")
            except sqlite3.OperationalError:
                continue

    def standardize_syllabus_covered(self):
        """Convert syllabus_covered from percentage string to decimal"""
        self.cursor.execute("SELECT id, SyllabusCovered FROM exam_results")
        rows = self.cursor.fetchall()
        
        for row_id, syllabus in rows:
            if syllabus and '%' in syllabus:
                decimal_value = float(syllabus.strip('%')) / 100
                self.cursor.execute(
                    "UPDATE exam_results SET SyllabusCovered = ? WHERE id = ?",
                    (decimal_value, row_id)
                )

    def standardize_strengths_weaknesses(self):
        """Standardize the format of strengths and weaknesses fields"""
        self.cursor.execute("SELECT StudentID, Strengths, Weaknesses FROM students")
        rows = self.cursor.fetchall()
        
        for student_id, strengths, weaknesses in rows:
            if strengths:
                # Convert to standardized JSON format
                strengths_list = [s.strip() for s in re.split(r'[;,]', strengths)]
                strengths_json = json.dumps(strengths_list)
                
                self.cursor.execute(
                    "UPDATE students SET Strengths = ? WHERE StudentID = ?",
                    (strengths_json, student_id)
                )
            
            if weaknesses:
                # Convert to standardized JSON format
                weaknesses_list = [w.strip() for w in re.split(r'[;,]', weaknesses)]
                weaknesses_json = json.dumps(weaknesses_list)
                
                self.cursor.execute(
                    "UPDATE students SET Weaknesses = ? WHERE StudentID = ?",
                    (weaknesses_json, student_id)
                )

    def validate_email_format(self):
        """Validate and standardize email formats"""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        self.cursor.execute("SELECT StudentID, Email FROM students")
        rows = self.cursor.fetchall()
        
        invalid_emails = []
        for student_id, email in rows:
            if not email_pattern.match(email):
                invalid_emails.append((student_id, email))
        
        return invalid_emails

    def migrate(self):
        """Run the complete migration process"""
        try:
            self.connect()
            
            # Create backup
            backup_path = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(self.db_path, 'rb') as src, open(backup_path, 'wb') as dst:
                dst.write(src.read())
            
            # Start migration
            self.create_new_tables()
            self.alter_existing_tables()
            self.standardize_syllabus_covered()
            self.standardize_strengths_weaknesses()
            
            # Validate email formats
            invalid_emails = self.validate_email_format()
            if invalid_emails:
                print("Warning: Found invalid email formats:")
                for student_id, email in invalid_emails:
                    print(f"StudentID: {student_id}, Email: {email}")
            
            self.conn.commit()
            print("Migration completed successfully!")
            
        except Exception as e:
            self.conn.rollback()
            print(f"Error during migration: {str(e)}")
            raise
        finally:
            self.close()

if __name__ == "__main__":
    db_path = "d:/CascadeProjects/student_tracking_system/data/student_tracking.db"  # Updated absolute path
    updater = SchemaUpdater(db_path)
    updater.migrate()

import sqlite3
from contextlib import contextmanager
from datetime import datetime
import json
import re

class DatabaseValidationError(Exception):
    """Custom exception for database validation errors"""
    pass

class DatabaseManager:
    def __init__(self, db_path='student_tracking.db'):
        self.db_path = db_path
        self._create_tables()

    @contextmanager
    def get_connection(self, commit_on_success=True):
        """Context manager for database connections with transaction handling"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        try:
            yield conn
            if commit_on_success:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _create_tables(self):
        """Create database tables with proper constraints and cascade rules"""
        with self.get_connection() as conn:
            conn.executescript('''
                -- Students table
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL CHECK(length(name) >= 2),
                    email TEXT UNIQUE CHECK(email LIKE '%@%.%'),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Textbooks/Courses table
                CREATE TABLE IF NOT EXISTS textbooks (
                    textbook_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_code TEXT NOT NULL UNIQUE CHECK(length(course_code) >= 2),
                    title TEXT NOT NULL CHECK(length(title) >= 3),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Topics table
                CREATE TABLE IF NOT EXISTS topics (
                    topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    textbook_id INTEGER NOT NULL,
                    topic_name TEXT NOT NULL CHECK(length(topic_name) >= 3),
                    description TEXT,
                    chapter_number INTEGER CHECK(chapter_number > 0),
                    importance_level INTEGER CHECK(importance_level BETWEEN 1 AND 5),
                    estimated_hours REAL CHECK(estimated_hours > 0),
                    prerequisites TEXT,  -- JSON array of prerequisite topic_ids
                    learning_outcomes TEXT,  -- JSON array of learning outcomes
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (textbook_id) REFERENCES textbooks(textbook_id)
                        ON DELETE CASCADE
                );

                -- Study Materials table
                CREATE TABLE IF NOT EXISTS study_materials (
                    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic_id INTEGER NOT NULL,
                    material_type TEXT CHECK(material_type IN ('summary', 'notes', 'practice_questions', 'examples')),
                    content TEXT NOT NULL CHECK(length(content) > 0),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
                        ON DELETE CASCADE
                );

                -- Topic Progress table
                CREATE TABLE IF NOT EXISTS topic_progress (
                    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    topic_id INTEGER NOT NULL,
                    completion_status TEXT CHECK(completion_status IN ('not_started', 'in_progress', 'completed')),
                    understanding_level INTEGER CHECK(understanding_level BETWEEN 1 AND 5),
                    time_spent_hours REAL CHECK(time_spent_hours >= 0),
                    last_studied TIMESTAMP,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
                        ON DELETE CASCADE,
                    UNIQUE(student_id, topic_id)
                );

                -- Study Schedule table
                CREATE TABLE IF NOT EXISTS study_schedules (
                    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    topic_id INTEGER NOT NULL,
                    scheduled_date DATE NOT NULL,
                    planned_hours REAL CHECK(planned_hours > 0),
                    actual_hours REAL CHECK(actual_hours >= 0),
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
                        ON DELETE CASCADE
                );
            ''')

    def validate_student(self, student_data):
        """Validate student data"""
        errors = []
        
        # Validate student_id format (e.g., STU001)
        if not re.match(r'^STU\d{3}$', student_data.get('student_id', '')):
            errors.append("Invalid student ID format. Must be 'STU' followed by 3 digits")

        # Validate name
        name = student_data.get('name', '')
        if len(name) < 2:
            errors.append("Name must be at least 2 characters long")

        # Validate email
        email = student_data.get('email', '')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Invalid email format")

        if errors:
            raise DatabaseValidationError("\n".join(errors))

    def validate_topic(self, topic_data):
        """Validate topic data"""
        errors = []

        # Validate topic name
        if len(topic_data.get('topic_name', '')) < 3:
            errors.append("Topic name must be at least 3 characters long")

        # Validate importance level
        importance = topic_data.get('importance_level')
        if not (isinstance(importance, int) and 1 <= importance <= 5):
            errors.append("Importance level must be between 1 and 5")

        # Validate estimated hours
        hours = topic_data.get('estimated_hours')
        if not (isinstance(hours, (int, float)) and hours > 0):
            errors.append("Estimated hours must be greater than 0")

        # Validate prerequisites format
        prereqs = topic_data.get('prerequisites')
        if prereqs:
            try:
                prereq_list = json.loads(prereqs) if isinstance(prereqs, str) else prereqs
                if not isinstance(prereq_list, list):
                    errors.append("Prerequisites must be a list")
                elif not all(isinstance(x, int) for x in prereq_list):
                    errors.append("Prerequisites must be a list of topic IDs")
            except json.JSONDecodeError:
                errors.append("Invalid prerequisites format")

        if errors:
            raise DatabaseValidationError("\n".join(errors))

    def validate_progress(self, progress_data):
        """Validate progress data"""
        errors = []

        # Validate completion status
        status = progress_data.get('completion_status')
        if status not in ['not_started', 'in_progress', 'completed']:
            errors.append("Invalid completion status")

        # Validate understanding level
        understanding = progress_data.get('understanding_level')
        if not (isinstance(understanding, int) and 1 <= understanding <= 5):
            errors.append("Understanding level must be between 1 and 5")

        # Validate time spent
        time_spent = progress_data.get('time_spent_hours', 0)
        if not (isinstance(time_spent, (int, float)) and time_spent >= 0):
            errors.append("Time spent must be non-negative")

        if errors:
            raise DatabaseValidationError("\n".join(errors))

    def add_student(self, student_data):
        """Add a new student with validation"""
        self.validate_student(student_data)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (student_id, name, email)
                VALUES (?, ?, ?)
            ''', (student_data['student_id'], student_data['name'], student_data['email']))
            return cursor.lastrowid

    def add_topic(self, topic_data):
        """Add a new topic with validation"""
        self.validate_topic(topic_data)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO topics (
                    textbook_id, topic_name, description, chapter_number,
                    importance_level, estimated_hours, prerequisites, learning_outcomes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                topic_data['textbook_id'],
                topic_data['topic_name'],
                topic_data.get('description'),
                topic_data['chapter_number'],
                topic_data['importance_level'],
                topic_data['estimated_hours'],
                json.dumps(topic_data.get('prerequisites', [])),
                json.dumps(topic_data.get('learning_outcomes', []))
            ))
            return cursor.lastrowid

    def update_progress(self, progress_data):
        """Update topic progress with validation"""
        self.validate_progress(progress_data)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO topic_progress (
                    student_id, topic_id, completion_status,
                    understanding_level, time_spent_hours,
                    last_studied, notes
                ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
            ''', (
                progress_data['student_id'],
                progress_data['topic_id'],
                progress_data['completion_status'],
                progress_data['understanding_level'],
                progress_data['time_spent_hours'],
                progress_data.get('notes')
            ))
            return cursor.lastrowid

    def delete_student(self, student_id):
        """Delete a student and all related data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
            return cursor.rowcount > 0

    def delete_topic(self, topic_id):
        """Delete a topic and all related data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM topics WHERE topic_id = ?', (topic_id,))
            return cursor.rowcount > 0

# Example usage
if __name__ == "__main__":
    db = DatabaseManager()
    
    # Test student validation
    try:
        student_data = {
            'student_id': 'STU001',
            'name': 'John Doe',
            'email': 'john.doe@example.com'
        }
        db.add_student(student_data)
        print("Student added successfully")
    except DatabaseValidationError as e:
        print(f"Validation error: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

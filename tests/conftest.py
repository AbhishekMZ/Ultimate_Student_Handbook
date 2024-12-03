import pytest
import os
import tempfile
import sqlite3
from src.api.app import app
from backend.core.database_manager import DatabaseManager

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_db():
    """Create a temporary test database"""
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE'] = db_path
    
    # Initialize test database with schema
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript('''
            CREATE TABLE students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                enrollment_date TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT
            );

            CREATE TABLE student_progress (
                progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                completion_percentage REAL DEFAULT 0,
                understanding_level INTEGER CHECK (understanding_level BETWEEN 1 AND 5),
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (student_id),
                FOREIGN KEY (course_id) REFERENCES courses (course_id)
            );
        ''')
        
        # Insert test data
        cursor.executescript('''
            INSERT INTO students (name, email) VALUES 
                ('Test Student 1', 'test1@example.com'),
                ('Test Student 2', 'test2@example.com');

            INSERT INTO courses (code, name, description) VALUES
                ('CS101', 'Introduction to Programming', 'Basic programming concepts'),
                ('CS102', 'Data Structures', 'Fundamental data structures');

            INSERT INTO student_progress (student_id, course_id, completion_percentage, understanding_level) VALUES
                (1, 1, 75.5, 4),
                (1, 2, 45.0, 3),
                (2, 1, 90.0, 5);
        ''')
        
        conn.commit()

    yield db_path

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def db_manager(test_db):
    """Create a database manager instance with test database"""
    return DatabaseManager(db_path=test_db)

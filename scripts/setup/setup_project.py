import os
import sqlite3
from pathlib import Path

# Create necessary directories
directories = [
    'src/data',
    'src/data/raw',
    'src/data/raw/textbook_sections',
    'src/data/processed',
    'src/data/processed/csv'
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)

# Initialize database
DB_PATH = 'src/data/student_tracking.db'

# Create database tables
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON")

# Create tables
cursor.executescript('''
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
    textbook_id INTEGER,
    topic_name TEXT NOT NULL CHECK(length(topic_name) >= 2),
    description TEXT,
    difficulty_level INTEGER CHECK(difficulty_level BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (textbook_id) REFERENCES textbooks(textbook_id) ON DELETE CASCADE
);

-- Topic Progress table
CREATE TABLE IF NOT EXISTS topic_progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    topic_id INTEGER,
    completion_status TEXT CHECK(completion_status IN ('Not Started', 'In Progress', 'Completed')),
    understanding_level INTEGER CHECK(understanding_level BETWEEN 1 AND 5),
    time_spent_hours REAL CHECK(time_spent_hours >= 0),
    last_studied TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE,
    UNIQUE(student_id, topic_id)
);

-- Exam Results table
CREATE TABLE IF NOT EXISTS exam_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    exam_name TEXT NOT NULL,
    marks_obtained REAL CHECK(marks_obtained >= 0),
    max_marks REAL CHECK(max_marks > 0),
    exam_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Student Survey table
CREATE TABLE IF NOT EXISTS student_surveys (
    survey_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    survey_type TEXT CHECK(survey_type IN ('Technical', 'Soft Skills', 'Learning')),
    responses TEXT NOT NULL,  -- JSON format
    feedback TEXT,
    survey_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Improvement Plans table
CREATE TABLE IF NOT EXISTS improvement_plans (
    student_id TEXT PRIMARY KEY,
    name TEXT,
    avg_performance REAL,
    critical_weaknesses TEXT,
    monthly_goals TEXT,
    quarterly_goals TEXT,
    last_updated DATE,
    FOREIGN KEY (student_id) REFERENCES students (student_id)
);
''')

# Insert sample data
cursor.executescript('''
-- Sample students
INSERT OR IGNORE INTO students (student_id, name, email) VALUES
    ('ST001', 'John Doe', 'john.doe@example.com'),
    ('ST002', 'Jane Smith', 'jane.smith@example.com'),
    ('ST003', 'Bob Wilson', 'bob.wilson@example.com');

-- Sample courses
INSERT OR IGNORE INTO textbooks (course_code, title, description) VALUES
    ('DBMS', 'Database Management Systems', 'Comprehensive study of database concepts and implementations'),
    ('AISE', 'AI-integrated Software Engineering', 'Modern software engineering with AI integration'),
    ('MLOPS', 'Machine Learning Operations', 'MLOps practices and tools');

-- Sample topics
INSERT OR IGNORE INTO topics (textbook_id, topic_name, description, difficulty_level) VALUES
    (1, 'SQL Basics', 'Introduction to SQL queries', 2),
    (1, 'Database Design', 'ER diagrams and normalization', 4),
    (2, 'Requirements Engineering', 'Gathering and analyzing requirements', 3);

-- Sample progress data
INSERT OR IGNORE INTO topic_progress (student_id, topic_id, completion_status, understanding_level, time_spent_hours) VALUES
    ('ST001', 1, 'Completed', 4, 10.5),
    ('ST001', 2, 'In Progress', 3, 5.0),
    ('ST002', 1, 'Completed', 5, 8.0);

-- Sample exam results
INSERT OR IGNORE INTO exam_results (student_id, exam_name, marks_obtained, max_marks, exam_date) VALUES
    ('ST001', 'DBMS Mid-term', 85, 100, '2024-01-15'),
    ('ST002', 'DBMS Mid-term', 92, 100, '2024-01-15'),
    ('ST003', 'DBMS Mid-term', 78, 100, '2024-01-15');
''')

conn.commit()
conn.close()

print("Project setup completed successfully!")
print("- Created necessary directories")
print("- Initialized database with tables")
print("- Added sample data")

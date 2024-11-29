import sqlite3
import json
from datetime import datetime

def create_study_resources_tables():
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Create Textbooks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS textbooks (
        textbook_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT NOT NULL,
        title TEXT NOT NULL,
        author TEXT,
        edition TEXT,
        publisher TEXT,
        isbn TEXT,
        total_chapters INTEGER,
        FOREIGN KEY (course_code) REFERENCES courses(course_code)
    )
    ''')

    # Create Topics table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS topics (
        topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        textbook_id INTEGER,
        chapter_number INTEGER,
        topic_name TEXT NOT NULL,
        description TEXT,
        importance_level INTEGER CHECK(importance_level BETWEEN 1 AND 5),
        estimated_hours FLOAT,
        prerequisites TEXT,
        learning_outcomes TEXT,
        FOREIGN KEY (textbook_id) REFERENCES textbooks(textbook_id)
    )
    ''')

    # Create Study Guides table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_guides (
        guide_id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER,
        content_type TEXT CHECK(content_type IN ('summary', 'notes', 'practice_questions', 'examples')),
        content TEXT,
        difficulty_level INTEGER CHECK(difficulty_level BETWEEN 1 AND 5),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
    )
    ''')

    # Create Topic Progress table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS topic_progress (
        progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        topic_id INTEGER,
        completion_status TEXT CHECK(completion_status IN ('not_started', 'in_progress', 'completed')),
        understanding_level INTEGER CHECK(understanding_level BETWEEN 1 AND 5),
        time_spent_hours FLOAT,
        last_reviewed DATETIME,
        notes TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
    )
    ''')

    # Create Deadlines table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS deadlines (
        deadline_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        topic_id INTEGER,
        deadline_type TEXT CHECK(deadline_type IN ('assignment', 'exam', 'project', 'reading')),
        due_date DATETIME,
        priority INTEGER CHECK(priority BETWEEN 1 AND 5),
        status TEXT CHECK(status IN ('pending', 'completed', 'overdue')),
        reminder_frequency TEXT CHECK(reminder_frequency IN ('daily', 'weekly', 'custom')),
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
    )
    ''')

    # Create Topic Dependencies table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS topic_dependencies (
        dependency_id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER,
        prerequisite_topic_id INTEGER,
        dependency_type TEXT CHECK(dependency_type IN ('required', 'recommended')),
        FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
        FOREIGN KEY (prerequisite_topic_id) REFERENCES topics(topic_id)
    )
    ''')

    # Insert sample textbooks for our courses
    sample_textbooks = [
        ('CD252IA', 'Database System Concepts', 'Silberschatz, Korth, Sudarshan', '7th', 'McGraw-Hill', '978-0078022159', 12),
        ('AI255TBA', 'Software Engineering: A Practitioner\'s Approach', 'Roger S. Pressman', '8th', 'McGraw-Hill', '978-0078022128', 14),
        ('AI254TA', 'Machine Learning Engineering', 'Andriy Burkov', '1st', 'True Positive Inc.', '978-1999579579', 10),
        ('AI253IA', 'Neural Networks and Deep Learning', 'Michael Nielsen', '1st', 'Determination Press', '978-0071746564', 8),
        ('HS251TA', 'Principles of Management', 'P.C. Tripathi', '5th', 'McGraw-Hill', '978-0070151673', 10)
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO textbooks (course_code, title, author, edition, publisher, isbn, total_chapters)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_textbooks)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_study_resources_tables()
    print("Study resources tables created successfully!")

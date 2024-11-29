import sqlite3
import os

def reset_database():
    db_path = 'student_tracking.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database removed")
    
    # Create new database with schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
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
    
    # Insert sample courses
    sample_courses = [
        ('DBMS', 'Database Management Systems'),
        ('AISE', 'AI-integrated Software Engineering'),
        ('MLOPS', 'Machine Learning Operations'),
        ('ANN', 'Artificial Neural Networks'),
        ('PME', 'Principles of Management & Economics')
    ]
    
    cursor.executemany('''
        INSERT INTO textbooks (course_code, title)
        VALUES (?, ?)
    ''', sample_courses)
    
    conn.commit()
    conn.close()
    
    print("Database reset complete. Sample courses added.")

if __name__ == "__main__":
    reset_database()

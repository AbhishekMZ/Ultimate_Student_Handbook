import sqlite3

def create_tables():
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Create tables with proper foreign key relationships
    cursor.executescript('''
    -- Students table
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Textbooks/Courses table
    CREATE TABLE IF NOT EXISTS textbooks (
        textbook_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Topics table
    CREATE TABLE IF NOT EXISTS topics (
        topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        textbook_id INTEGER,
        topic_name TEXT NOT NULL,
        description TEXT,
        chapter_number INTEGER,
        importance_level INTEGER CHECK (importance_level BETWEEN 1 AND 5),
        estimated_hours REAL,
        prerequisites TEXT,  -- JSON array of prerequisite topic_ids
        learning_outcomes TEXT,  -- JSON array of learning outcomes
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (textbook_id) REFERENCES textbooks(textbook_id)
    );

    -- Study Materials table
    CREATE TABLE IF NOT EXISTS study_materials (
        material_id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER,
        material_type TEXT CHECK (material_type IN ('summary', 'notes', 'practice_questions', 'examples')),
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
    );

    -- Topic Progress table
    CREATE TABLE IF NOT EXISTS topic_progress (
        progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        topic_id INTEGER,
        completion_status TEXT CHECK (completion_status IN ('not_started', 'in_progress', 'completed')),
        understanding_level INTEGER CHECK (understanding_level BETWEEN 1 AND 5),
        time_spent_hours REAL,
        last_studied TIMESTAMP,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
        UNIQUE(student_id, topic_id)
    );

    -- Study Schedule table
    CREATE TABLE IF NOT EXISTS study_schedules (
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        topic_id INTEGER,
        scheduled_date DATE,
        planned_hours REAL,
        actual_hours REAL,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
    );
    ''')

    # Insert sample student if not exists
    cursor.execute('''
    INSERT OR IGNORE INTO students (student_id, name, email)
    VALUES ('STU001', 'Sample Student', 'student@example.com')
    ''')

    # Insert sample courses if not exist
    sample_courses = [
        ('DBMS', 'Database Management Systems'),
        ('AISE', 'AI-integrated Software Engineering'),
        ('MLOPS', 'Machine Learning Operations'),
        ('ANN', 'Artificial Neural Networks'),
        ('PME', 'Principles of Management & Economics')
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO textbooks (course_code, title)
    VALUES (?, ?)
    ''', sample_courses)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()

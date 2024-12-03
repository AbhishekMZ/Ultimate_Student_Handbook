import sqlite3
import os

def get_db_connection():
    """Create a database connection and return it"""
    try:
        conn = sqlite3.connect('student_tracking.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS roles (
                role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role_id INTEGER,
                FOREIGN KEY (role_id) REFERENCES roles(role_id)
            );

            CREATE TABLE IF NOT EXISTS user_profiles (
                profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS academic_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                education_level TEXT CHECK(education_level IN ('10th', '12th', 'Current')),
                institution TEXT,
                board TEXT,
                percentage FLOAT,
                year_of_completion INTEGER,
                subjects TEXT,
                achievements TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS learning_profiles (
                profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                learning_style TEXT CHECK(learning_style IN ('Visual', 'Auditory', 'Reading/Writing', 'Kinesthetic')),
                preferred_study_time TEXT CHECK(preferred_study_time IN ('Morning', 'Afternoon', 'Evening', 'Night')),
                concentration_span INTEGER,
                subjects_of_interest TEXT,
                weak_areas TEXT,
                study_group_preference BOOLEAN,
                learning_pace TEXT CHECK(learning_pace IN ('Fast', 'Moderate', 'Slow')),
                attendance_percentage FLOAT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS topics (
                topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_name TEXT NOT NULL,
                description TEXT,
                course_id INTEGER
            );

            CREATE TABLE IF NOT EXISTS student_progress (
                progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                topic_id INTEGER,
                understanding_level INTEGER CHECK(understanding_level BETWEEN 1 AND 5),
                completion_status TEXT CHECK(completion_status IN ('Not Started', 'In Progress', 'Completed')),
                time_spent_hours FLOAT,
                last_assessment_score FLOAT,
                notes TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
            );
        ''')
        
        # Insert default roles if they don't exist
        cursor.executescript('''
            INSERT OR IGNORE INTO roles (role_name) VALUES ('admin');
            INSERT OR IGNORE INTO roles (role_name) VALUES ('teacher');
            INSERT OR IGNORE INTO roles (role_name) VALUES ('student');
        ''')
        
        conn.commit()
        print("Database initialized successfully")
        
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()

import sqlite3
from datetime import datetime

def create_learning_schema():
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Create Course table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Course (
        CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Description TEXT,
        Duration INTEGER,
        DifficultyLevel TEXT CHECK(DifficultyLevel IN ('Beginner', 'Intermediate', 'Advanced')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Topic table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Topic (
        TopicID INTEGER PRIMARY KEY AUTOINCREMENT,
        CourseID INTEGER NOT NULL,
        Title TEXT NOT NULL,
        ContentURL TEXT,
        RecommendedTime INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON DELETE CASCADE
    )
    ''')

    # Create TextbookResource table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TextbookResource (
        ResourceID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Type TEXT CHECK(Type IN ('PDF', 'Video', 'URL', 'Article')) NOT NULL,
        ResourceURL TEXT NOT NULL,
        CourseID INTEGER,
        TopicID INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON DELETE SET NULL,
        FOREIGN KEY (TopicID) REFERENCES Topic(TopicID) ON DELETE SET NULL
    )
    ''')

    # Create Progress table with additional learning metrics
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Progress (
        ProgressID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        CourseID INTEGER NOT NULL,
        TopicID INTEGER,
        CompletionStatus REAL DEFAULT 0.0,
        Score REAL DEFAULT NULL,
        TimeSpent INTEGER DEFAULT 0,
        LastAccessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (StudentID) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON DELETE CASCADE,
        FOREIGN KEY (TopicID) REFERENCES Topic(TopicID) ON DELETE SET NULL
    )
    ''')

    # Create Goal table with enhanced tracking
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Goal (
        GoalID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        Title TEXT NOT NULL,
        Description TEXT,
        Deadline DATE NOT NULL,
        Priority TEXT CHECK(Priority IN ('Low', 'Medium', 'High')) DEFAULT 'Medium',
        Status TEXT CHECK(Status IN ('In Progress', 'Completed', 'Overdue')) DEFAULT 'In Progress',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (StudentID) REFERENCES users(user_id) ON DELETE CASCADE
    )
    ''')

    # Create Notification table with enhanced features
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Notification (
        NotificationID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        Message TEXT NOT NULL,
        Type TEXT CHECK(Type IN ('Reminder', 'Recommendation', 'Alert', 'Achievement')) NOT NULL,
        Priority TEXT CHECK(Priority IN ('Low', 'Medium', 'High')) DEFAULT 'Medium',
        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ExpiryDate DATETIME,
        ReadStatus BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (StudentID) REFERENCES users(user_id) ON DELETE CASCADE
    )
    ''')

    # Create Achievement table with gamification elements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Achievement (
        AchievementID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        Type TEXT CHECK(Type IN ('Badge', 'Milestone', 'Streak', 'Special')) NOT NULL,
        Title TEXT NOT NULL,
        Description TEXT NOT NULL,
        Points INTEGER DEFAULT 0,
        AwardedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (StudentID) REFERENCES users(user_id) ON DELETE CASCADE
    )
    ''')

    # Create DeviceSync table with enhanced tracking
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DeviceSync (
        SyncID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        DeviceType TEXT CHECK(DeviceType IN ('Laptop', 'Mobile', 'Tablet', 'Other')) NOT NULL,
        DeviceIdentifier TEXT,
        LastSyncTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        SyncStatus TEXT CHECK(SyncStatus IN ('Success', 'Failed', 'In Progress')) DEFAULT 'Success',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (StudentID) REFERENCES users(user_id) ON DELETE CASCADE
    )
    ''')

    # Add learning-related columns to user_profiles if they don't exist
    cursor.execute("PRAGMA table_info(user_profiles)")
    columns = [col[1] for col in cursor.fetchall()]
    
    new_columns = [
        ('streak_count', 'INTEGER DEFAULT 0'),
        ('total_study_time', 'INTEGER DEFAULT 0'),
        ('preferred_learning_style', 'TEXT'),
        ('learning_goals', 'TEXT'),
        ('last_active_date', 'DATETIME')
    ]

    for col_name, col_type in new_columns:
        if col_name not in columns:
            cursor.execute(f'''
            ALTER TABLE user_profiles
            ADD COLUMN {col_name} {col_type}
            ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_learning_schema()
    print("Learning schema created successfully with enhanced features!")

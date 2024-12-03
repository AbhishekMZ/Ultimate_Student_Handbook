import sqlite3
import csv
from pathlib import Path

def create_database(db_path):
    """Create the initial database with base tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        StudentID TEXT PRIMARY KEY,
        Name TEXT NOT NULL,
        Email TEXT NOT NULL,
        TenthMarks REAL,
        TwelfthMarks REAL,
        Strengths TEXT,
        Weaknesses TEXT,
        Semester INTEGER,
        Courses TEXT
    )
    """)

    # Create exam_results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID TEXT NOT NULL,
        CourseCode TEXT NOT NULL,
        TestNumber INTEGER NOT NULL,
        TestDate DATE NOT NULL,
        SyllabusCovered TEXT,
        MaxMarks INTEGER NOT NULL,
        MarksObtained INTEGER NOT NULL,
        FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    )
    """)

    # Create courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        CourseCode TEXT PRIMARY KEY,
        CourseName TEXT NOT NULL,
        Credits INTEGER NOT NULL,
        Department TEXT NOT NULL
    )
    """)

    conn.commit()

    # Import data from CSV files
    data_dir = Path("d:/CascadeProjects/student_tracking_system/data/processed/csv")
    
    # Import students data
    with open(data_dir / "students.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
            INSERT OR REPLACE INTO students 
            (StudentID, Name, Email, TenthMarks, TwelfthMarks, Strengths, Weaknesses, Semester, Courses)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['StudentID'], row['Name'], row['Email'],
                float(row['TenthMarks']), float(row['TwelfthMarks']),
                row['Strengths'], row['Weaknesses'],
                int(row['Semester']), row['Courses']
            ))

    # Import exam results data
    with open(data_dir / "exam_results.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
            INSERT OR REPLACE INTO exam_results 
            (StudentID, CourseCode, TestNumber, TestDate, SyllabusCovered, MaxMarks, MarksObtained)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row['StudentID'], row['CourseCode'],
                int(row['TestNumber']), row['TestDate'],
                row['SyllabusCovered'], int(row['MaxMarks']),
                int(row['MarksObtained'])
            ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = "d:/CascadeProjects/student_tracking_system/data/student_tracking.db"
    create_database(db_path)
    print("Database initialized successfully!")

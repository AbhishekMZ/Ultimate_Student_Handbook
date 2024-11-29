import sqlite3
import csv
import json
from datetime import datetime

def create_database():
    # Connect to SQLite database (creates if not exists)
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Create Students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        tenth_percentage REAL,
        twelfth_percentage REAL,
        semester INTEGER,
        strengths TEXT,
        weaknesses TEXT
    )
    ''')

    # Create Courses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        course_code TEXT PRIMARY KEY,
        course_name TEXT NOT NULL
    )
    ''')

    # Create ExamResults table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exam_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        course_code TEXT,
        test_number INTEGER,
        test_date DATE,
        syllabus_covered REAL,
        max_marks INTEGER,
        marks_obtained REAL,
        FOREIGN KEY (student_id) REFERENCES students (student_id),
        FOREIGN KEY (course_code) REFERENCES courses (course_code)
    )
    ''')

    # Create Goals table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        goal_type TEXT,  -- 'monthly' or 'quarterly'
        goal_description TEXT,
        target_skill TEXT,
        created_date DATE,
        FOREIGN KEY (student_id) REFERENCES students (student_id)
    )
    ''')

    # Insert course data
    courses = [
        ('CD252IA', 'Database Management Systems'),
        ('AI255TBA', 'AI-integrated Software Engineering'),
        ('AI254TA', 'Machine Learning Operations'),
        ('AI253IA', 'Artificial Neural Networks'),
        ('HS251TA', 'Principles of Management & Economics')
    ]
    cursor.executemany('INSERT OR REPLACE INTO courses VALUES (?, ?)', courses)

    # Import student data
    with open('students.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cursor.execute('''
            INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['StudentID'],
                row['Name'],
                row['Email'],
                None,  # Phone (not in our current data)
                float(row['TenthMarks']),
                float(row['TwelfthMarks']),
                int(row['Semester']),
                row['Strengths'],
                row['Weaknesses']
            ))

    # Import exam results
    with open('exam_results.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Convert percentage string to float
            syllabus_covered = float(row['SyllabusCovered'].strip('%')) / 100.0
            
            cursor.execute('''
            INSERT INTO exam_results (student_id, course_code, test_number, test_date, 
                                    syllabus_covered, max_marks, marks_obtained)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['StudentID'],
                row['CourseCode'],
                int(row['TestNumber']),
                datetime.strptime(row['TestDate'], '%Y-%m-%d').date(),
                syllabus_covered,
                int(row['MaxMarks']),
                float(row['MarksObtained'])
            ))

    # Import goals
    with open('student_goals.json', 'r') as file:
        goals_data = json.load(file)
        for student_goals in goals_data:
            student_id = student_goals['StudentID']
            
            # Insert monthly goals
            for goal in student_goals['MonthlyGoals'].split('; '):
                if goal:
                    skill = goal.split(':')[0] if ':' in goal else 'General'
                    cursor.execute('''
                    INSERT INTO goals (student_id, goal_type, goal_description, target_skill, created_date)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        student_id,
                        'monthly',
                        goal,
                        skill,
                        datetime.now().date()
                    ))
            
            # Insert quarterly goals
            for goal in student_goals['QuarterlyGoals'].split('; '):
                if goal:
                    skill = goal.split(':')[0] if ':' in goal else 'General'
                    cursor.execute('''
                    INSERT INTO goals (student_id, goal_type, goal_description, target_skill, created_date)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        student_id,
                        'quarterly',
                        goal,
                        skill,
                        datetime.now().date()
                    ))

    # Create useful views
    
    # Student Performance Summary
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS student_performance_summary AS
    SELECT 
        s.student_id,
        s.name,
        c.course_code,
        c.course_name,
        COUNT(er.result_id) as tests_taken,
        AVG(er.marks_obtained * 100.0 / er.max_marks) as average_percentage
    FROM students s
    JOIN exam_results er ON s.student_id = er.student_id
    JOIN courses c ON er.course_code = c.course_code
    GROUP BY s.student_id, c.course_code
    ''')

    # Student Goals Summary
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS student_goals_summary AS
    SELECT 
        s.student_id,
        s.name,
        g.goal_type,
        COUNT(g.goal_id) as total_goals,
        GROUP_CONCAT(DISTINCT g.target_skill) as target_skills
    FROM students s
    JOIN goals g ON s.student_id = g.student_id
    GROUP BY s.student_id, g.goal_type
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created successfully with all data imported!")

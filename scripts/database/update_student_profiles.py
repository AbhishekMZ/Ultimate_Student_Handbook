import sqlite3
import random
from datetime import datetime

def create_academic_tables():
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Create Academic History table
    cursor.execute('''
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
    )
    ''')

    # Create Learning Profile table
    cursor.execute('''
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
    )
    ''')

    conn.commit()
    conn.close()

def get_random_academic_data(education_level, year):
    boards = {
        '10th': ['CBSE', 'ICSE', 'State Board'],
        '12th': ['CBSE', 'ICSE', 'State Board'],
        'Current': ['VTU']
    }
    
    institutions = {
        '10th': [
            'Delhi Public School', 'Kendriya Vidyalaya', 'Ryan International',
            'DAV Public School', 'St. Mary\'s School'
        ],
        '12th': [
            'Delhi Public School', 'Kendriya Vidyalaya', 'Ryan International',
            'DAV Public School', 'St. Mary\'s School'
        ],
        'Current': ['RV College of Engineering']
    }
    
    subjects = {
        '10th': 'Mathematics, Science, Social Studies, English, Second Language',
        '12th': 'Physics, Chemistry, Mathematics, Computer Science, English',
        'Current': 'Data Structures, Algorithms, Database Systems, Machine Learning'
    }
    
    achievements = [
        'School topper', 'District rank holder', 'Science Olympiad finalist',
        'Mathematics competition winner', 'Perfect attendance award',
        'Best student award', 'Quiz competition winner'
    ]

    return {
        'board': random.choice(boards[education_level]),
        'institution': random.choice(institutions[education_level]),
        'percentage': round(random.uniform(85, 98), 2),
        'year': year,
        'subjects': subjects[education_level],
        'achievements': random.choice(achievements) if random.random() > 0.5 else None
    }

def get_random_learning_profile():
    return {
        'learning_style': random.choice(['Visual', 'Auditory', 'Reading/Writing', 'Kinesthetic']),
        'preferred_study_time': random.choice(['Morning', 'Afternoon', 'Evening', 'Night']),
        'concentration_span': random.randint(30, 120),
        'subjects_of_interest': random.choice([
            'Machine Learning, AI, Data Science',
            'Algorithms, Data Structures, System Design',
            'Database Systems, Web Development, Cloud Computing',
            'Computer Networks, Cybersecurity, DevOps'
        ]),
        'weak_areas': random.choice([
            'Complex Mathematics',
            'Theory Subjects',
            'Programming Concepts',
            'Technical Writing'
        ]),
        'study_group_preference': random.choice([True, False]),
        'learning_pace': random.choice(['Fast', 'Moderate', 'Slow']),
        'attendance_percentage': round(random.uniform(75, 98), 2)
    }

def update_student_profiles():
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Get all students
    cursor.execute('''
        SELECT u.user_id, u.username 
        FROM users u 
        JOIN roles r ON u.role_id = r.role_id 
        WHERE r.role_name = 'student'
    ''')
    students = cursor.fetchall()

    for student_id, usn in students:
        # Add academic history
        academic_data = {
            '10th': get_random_academic_data('10th', 2020),
            '12th': get_random_academic_data('12th', 2022),
            'Current': get_random_academic_data('Current', 2024)
        }

        for level, data in academic_data.items():
            try:
                cursor.execute('''
                INSERT INTO academic_history 
                (user_id, education_level, institution, board, percentage, 
                year_of_completion, subjects, achievements)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    student_id, level, data['institution'], data['board'],
                    data['percentage'], data['year'], data['subjects'],
                    data['achievements']
                ))
            except sqlite3.IntegrityError:
                print(f"Academic history already exists for {usn} - {level}")

        # Add learning profile
        profile_data = get_random_learning_profile()
        try:
            cursor.execute('''
            INSERT INTO learning_profiles 
            (user_id, learning_style, preferred_study_time, concentration_span,
            subjects_of_interest, weak_areas, study_group_preference,
            learning_pace, attendance_percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_id, profile_data['learning_style'],
                profile_data['preferred_study_time'],
                profile_data['concentration_span'],
                profile_data['subjects_of_interest'],
                profile_data['weak_areas'],
                profile_data['study_group_preference'],
                profile_data['learning_pace'],
                profile_data['attendance_percentage']
            ))
        except sqlite3.IntegrityError:
            print(f"Learning profile already exists for {usn}")

    conn.commit()
    conn.close()

def display_student_profiles():
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Get all students with their profiles
    cursor.execute('''
        SELECT 
            u.username,
            up.first_name,
            up.last_name,
            ah_10.percentage as tenth_percentage,
            ah_10.board as tenth_board,
            ah_12.percentage as twelfth_percentage,
            ah_12.board as twelfth_board,
            lp.learning_style,
            lp.preferred_study_time,
            lp.concentration_span,
            lp.subjects_of_interest,
            lp.weak_areas,
            lp.learning_pace,
            lp.attendance_percentage
        FROM users u
        JOIN user_profiles up ON u.user_id = up.user_id
        JOIN academic_history ah_10 ON u.user_id = ah_10.user_id AND ah_10.education_level = '10th'
        JOIN academic_history ah_12 ON u.user_id = ah_12.user_id AND ah_12.education_level = '12th'
        JOIN learning_profiles lp ON u.user_id = lp.user_id
        JOIN roles r ON u.role_id = r.role_id
        WHERE r.role_name = 'student'
        ORDER BY u.username
    ''')
    
    students = cursor.fetchall()
    conn.close()

    # Display the results in a formatted way
    print("\nStudent Profiles Summary")
    print("=" * 100)
    
    for student in students:
        print(f"\nUSN: {student[0]} ({student[1]} {student[2]})")
        print("-" * 50)
        print(f"Academic Performance:")
        print(f"  10th: {student[3]}% ({student[4]})")
        print(f"  12th: {student[5]}% ({student[6]})")
        print("\nLearning Profile:")
        print(f"  Learning Style: {student[7]}")
        print(f"  Preferred Study Time: {student[8]}")
        print(f"  Concentration Span: {student[9]} minutes")
        print(f"  Subjects of Interest: {student[10]}")
        print(f"  Areas for Improvement: {student[11]}")
        print(f"  Learning Pace: {student[12]}")
        print(f"  Attendance: {student[13]}%")
        print("-" * 50)

if __name__ == "__main__":
    print("Creating academic and learning profile tables...")
    create_academic_tables()
    
    print("Updating student profiles with academic history and learning profiles...")
    update_student_profiles()
    
    print("\nDisplaying student profiles:")
    display_student_profiles()

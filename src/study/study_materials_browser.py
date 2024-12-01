import sqlite3
import json
from datetime import datetime
import os
from src import DB_PATH, DATA_DIR
from src.core.database_manager import DatabaseManager
from tabulate import tabulate
from src.progress.progress_tracker import ProgressTracker

class StudyMaterialsBrowser:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_manager = DatabaseManager()
        self.materials_dir = os.path.join(DATA_DIR, 'raw', 'textbook_sections')
        self.courses = {
            'DBMS': 'Database Management Systems',
            'AISE': 'AI-integrated Software Engineering',
            'MLOPS': 'Machine Learning Operations',
            'ANN': 'Artificial Neural Networks',
            'PME': 'Principles of Management & Economics'
        }
        self.progress_tracker = ProgressTracker()

    def list_courses(self):
        """Display available courses"""
        print("\n=== Available Courses ===")
        table_data = []
        for code, name in self.courses.items():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(DISTINCT t.topic_id)
                FROM topics t
                JOIN textbooks tb ON t.textbook_id = tb.textbook_id
                WHERE tb.course_code LIKE ?
            ''', (f'{code}%',))
            topic_count = cursor.fetchone()[0]
            conn.close()
            
            table_data.append([code, name, topic_count])
        
        print(tabulate(table_data, headers=['Code', 'Course Name', 'Topics'], tablefmt='grid'))

    def list_topics_by_course(self, course_code):
        """Display topics for a specific course"""
        if course_code not in self.courses:
            print(f"Error: Course code '{course_code}' not found.")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT t.topic_id, t.topic_name, t.importance_level, t.estimated_hours,
                   COUNT(DISTINCT sg.guide_id) as material_count
            FROM topics t
            JOIN textbooks tb ON t.textbook_id = tb.textbook_id
            LEFT JOIN study_guides sg ON t.topic_id = sg.topic_id
            WHERE tb.course_code LIKE ?
            GROUP BY t.topic_id
            ORDER BY t.chapter_number, t.topic_id
        ''', (f'{course_code}%',))

        topics = cursor.fetchall()
        conn.close()

        if not topics:
            print(f"\nNo topics found for course: {self.courses[course_code]}")
            return

        print(f"\n=== Topics for {self.courses[course_code]} ===")
        table_data = []
        for topic in topics:
            table_data.append([
                topic[0],  # topic_id
                topic[1],  # topic_name
                '⭐' * topic[2],  # importance_level as stars
                f"{topic[3]}h",  # estimated_hours
                topic[4]   # material_count
            ])
        
        print(tabulate(table_data, 
                      headers=['ID', 'Topic Name', 'Importance', 'Est. Hours', 'Materials'],
                      tablefmt='grid'))

    def view_topic_details(self, topic_id):
        """Display detailed information about a specific topic"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get topic information
        cursor.execute('''
            SELECT t.topic_id, t.topic_name, t.description, t.importance_level,
                   t.estimated_hours, t.prerequisites, t.learning_outcomes,
                   tb.course_code, tb.title
            FROM topics t
            JOIN textbooks tb ON t.textbook_id = tb.textbook_id
            WHERE t.topic_id = ?
        ''', (topic_id,))

        topic = cursor.fetchone()
        if not topic:
            print(f"Error: Topic ID '{topic_id}' not found.")
            return

        # Get study materials
        cursor.execute('''
            SELECT content_type, content, difficulty_level, created_at
            FROM study_guides
            WHERE topic_id = ?
            ORDER BY content_type
        ''', (topic_id,))
        materials = cursor.fetchall()

        conn.close()

        # Display topic information
        print(f"\n=== Topic Details: {topic[1]} ===")
        print(f"Course: {self.courses.get(topic[7][:4], topic[7])}")
        print(f"Textbook: {topic[8]}")
        print(f"Description: {topic[2]}")
        print(f"Importance Level: {'⭐' * topic[3]}")
        print(f"Estimated Study Hours: {topic[4]}")
        
        # Display prerequisites
        prereqs = json.loads(topic[5]) if topic[5] else []
        if prereqs:
            print("\nPrerequisites:")
            for prereq in prereqs:
                print(f"- {prereq}")

        # Display learning outcomes
        outcomes = json.loads(topic[6]) if topic[6] else []
        if outcomes:
            print("\nLearning Outcomes:")
            for i, outcome in enumerate(outcomes, 1):
                print(f"{i}. {outcome}")

        # Display available materials
        if materials:
            print("\nAvailable Study Materials:")
            table_data = []
            for material in materials:
                table_data.append([
                    material[0].replace('_', ' ').title(),
                    '🌟' * material[2],
                    material[3][:10]
                ])
            print(tabulate(table_data, 
                          headers=['Type', 'Difficulty', 'Created'],
                          tablefmt='grid'))

    def view_study_material(self, topic_id, material_type):
        """Display specific study material content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT content, difficulty_level
            FROM study_guides
            WHERE topic_id = ? AND content_type = ?
        ''', (topic_id, material_type))

        material = cursor.fetchone()
        conn.close()

        if not material:
            print(f"Error: No {material_type} found for topic ID {topic_id}")
            return

        print(f"\n=== {material_type.replace('_', ' ').title()} ===")
        print(f"Difficulty Level: {'🌟' * material[1]}")
        print("\nContent:")
        print(material[0])

    def update_topic_progress(self, student_id, topic_id):
        """Update progress for a specific topic"""
        print(f"\n=== Update Progress for Topic {topic_id} ===")
        
        # Get current progress
        current = self.progress_tracker.get_topic_progress(student_id, topic_id)
        if current:
            print(f"Current Status: {current[1] or 'not started'}")
            print(f"Current Understanding: {current[2] or 0}/5")
            print(f"Time Spent: {current[3] or 0} hours")
        
        # Get new progress
        print("\nStatus options: not_started, in_progress, completed")
        status = input("Enter new status: ").lower()
        if status not in ['not_started', 'in_progress', 'completed']:
            print("Invalid status. Progress update cancelled.")
            return

        try:
            understanding = int(input("Enter understanding level (1-5): "))
            if not 1 <= understanding <= 5:
                raise ValueError
        except ValueError:
            print("Invalid understanding level. Progress update cancelled.")
            return

        try:
            time_spent = float(input("Enter time spent in hours: "))
            if time_spent < 0:
                raise ValueError
        except ValueError:
            print("Invalid time spent. Progress update cancelled.")
            return

        notes = input("Enter any notes (optional): ")

        # Update progress
        if self.progress_tracker.update_progress(
            student_id, topic_id, status, understanding, time_spent, notes
        ):
            print("Progress updated successfully!")
        else:
            print("Failed to update progress.")

    def view_course_progress(self, student_id, course_code):
        """View progress report for a course"""
        report = self.progress_tracker.generate_progress_report(student_id, course_code)
        print(report)
        
        # Generate and save progress trends
        self.progress_tracker.plot_progress_trends(student_id, course_code)
        print("\nProgress trends have been saved to 'progress_trends.png'")

def main():
    browser = StudyMaterialsBrowser()
    student_id = 'STU001'  # You can modify this to support multiple students
    
    while True:
        print("\n=== Study Materials Browser ===")
        print("1. List all courses")
        print("2. Browse topics by course")
        print("3. View topic details")
        print("4. View study material")
        print("5. Update topic progress")
        print("6. View course progress")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            browser.list_courses()
        
        elif choice == '2':
            browser.list_courses()
            course_code = input("\nEnter course code (e.g., DBMS): ").upper()
            browser.list_topics_by_course(course_code)
        
        elif choice == '3':
            topic_id = input("Enter topic ID: ")
            try:
                browser.view_topic_details(int(topic_id))
            except ValueError:
                print("Invalid topic ID")
        
        elif choice == '4':
            topic_id = input("Enter topic ID: ")
            print("\nMaterial types: summary, notes, practice_questions, examples")
            material_type = input("Enter material type: ").lower()
            try:
                browser.view_study_material(int(topic_id), material_type)
            except ValueError:
                print("Invalid topic ID")
        
        elif choice == '5':
            topic_id = input("Enter topic ID: ")
            try:
                browser.update_topic_progress(student_id, int(topic_id))
            except ValueError:
                print("Invalid topic ID")
        
        elif choice == '6':
            browser.list_courses()
            course_code = input("\nEnter course code (e.g., DBMS): ").upper()
            if course_code in browser.courses:
                browser.view_course_progress(student_id, course_code)
            else:
                print("Invalid course code")
        
        elif choice == '7':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

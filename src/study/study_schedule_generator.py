import sqlite3
import json
from datetime import datetime, timedelta
import os
from backend.database.database import DB_PATH
from backend.core.database_manager import DatabaseManager
from ..progress.progress_tracker import ProgressTracker

class StudyScheduleGenerator:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_manager = DatabaseManager()
        self.progress_tracker = ProgressTracker()

    def get_student_workload(self, student_id):
        """Get current workload for student across all courses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            SELECT 
                tb.course_code,
                COUNT(DISTINCT t.topic_id) as total_topics,
                SUM(CASE WHEN tp.completion_status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(t.estimated_hours) as total_hours,
                SUM(COALESCE(tp.time_spent_hours, 0)) as spent_hours
            FROM topics t
            JOIN textbooks tb ON t.textbook_id = tb.textbook_id
            LEFT JOIN topic_progress tp ON t.topic_id = tp.topic_id AND tp.student_id = ?
            GROUP BY tb.course_code
            ''', (student_id,))

            return cursor.fetchall()
        finally:
            conn.close()

    def get_topic_priorities(self, student_id, course_code):
        """Calculate priority scores for topics based on various factors"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            SELECT 
                t.topic_id,
                t.topic_name,
                t.importance_level,
                t.estimated_hours,
                tp.completion_status,
                tp.understanding_level,
                tp.time_spent_hours,
                t.prerequisites
            FROM topics t
            JOIN textbooks tb ON t.textbook_id = tb.textbook_id
            LEFT JOIN topic_progress tp ON t.topic_id = tp.topic_id AND tp.student_id = ?
            WHERE tb.course_code LIKE ?
            ORDER BY t.chapter_number, t.topic_id
            ''', (student_id, f'{course_code}%'))

            topics = cursor.fetchall()
            priorities = []

            for topic in topics:
                # Base priority starts with importance level (1-5)
                priority = topic[2]

                # Adjust based on completion status
                status = topic[4] or 'not_started'
                if status == 'completed':
                    priority = 0  # Skip completed topics
                elif status == 'in_progress':
                    priority += 2  # Prioritize in-progress topics
                else:
                    priority += 1  # New topics get medium priority

                # Adjust based on understanding level
                understanding = topic[5] or 0
                if understanding < 3 and status != 'not_started':
                    priority += (3 - understanding)  # Prioritize poorly understood topics

                # Check prerequisites
                prereqs = json.loads(topic[7]) if topic[7] else []
                prereqs_completed = True
                for prereq in prereqs:
                    cursor.execute('''
                    SELECT completion_status
                    FROM topic_progress
                    WHERE student_id = ? AND topic_id = ?
                    ''', (student_id, prereq))
                    result = cursor.fetchone()
                    if not result or result[0] != 'completed':
                        prereqs_completed = False
                        break

                if not prereqs_completed:
                    priority = 0  # Can't study this yet

                priorities.append({
                    'topic_id': topic[0],
                    'topic_name': topic[1],
                    'priority': priority,
                    'estimated_hours': topic[3],
                    'status': status,
                    'understanding': understanding
                })

            return sorted(priorities, key=lambda x: x['priority'], reverse=True)

        finally:
            conn.close()

    def generate_schedule(self, student_id, course_code, available_hours_per_day, 
                         study_days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
                         start_date=None):
        """Generate a study schedule based on topic priorities and available time"""
        if start_date is None:
            start_date = datetime.now()

        # Get prioritized topics
        topics = self.get_topic_priorities(student_id, course_code)
        
        # Filter out completed topics and those with prerequisites not met
        active_topics = [t for t in topics if t['priority'] > 0]

        if not active_topics:
            return "No topics to schedule! All topics are either completed or waiting for prerequisites."

        # Calculate total available study time per week
        weekly_hours = len(study_days) * available_hours_per_day

        # Generate schedule
        schedule = []
        current_date = start_date
        remaining_topics = active_topics.copy()

        while remaining_topics and len(schedule) < 28:  # Limit to 4 weeks
            if current_date.strftime('%A').lower() in study_days:
                # Get topics for today
                daily_schedule = []
                remaining_hours = available_hours_per_day

                while remaining_hours > 0 and remaining_topics:
                    topic = remaining_topics[0]
                    
                    # Calculate study time for this topic
                    if topic['status'] == 'in_progress':
                        # For in-progress topics, use remaining estimated time
                        study_time = min(remaining_hours, max(1, topic['estimated_hours'] / 2))
                    else:
                        # For new topics, use full estimated time
                        study_time = min(remaining_hours, topic['estimated_hours'])

                    daily_schedule.append({
                        'topic_id': topic['topic_id'],
                        'topic_name': topic['topic_name'],
                        'study_hours': study_time,
                        'priority': topic['priority']
                    })

                    remaining_hours -= study_time
                    topic['estimated_hours'] -= study_time

                    if topic['estimated_hours'] <= 0:
                        remaining_topics.pop(0)
                    
                if daily_schedule:
                    schedule.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'day': current_date.strftime('%A'),
                        'topics': daily_schedule
                    })

            current_date += timedelta(days=1)

        return schedule

    def format_schedule(self, schedule):
        """Format the schedule for display"""
        if isinstance(schedule, str):
            return schedule

        output = ["\n=== Study Schedule ===\n"]
        
        for day in schedule:
            output.append(f"Date: {day['date']} ({day['day']})")
            
            table_data = []
            for topic in day['topics']:
                table_data.append([
                    topic['topic_name'],
                    f"{topic['study_hours']:.1f}h",
                    '⭐' * int(topic['priority'])
                ])
            
            output.append(tabulate(table_data,
                                 headers=['Topic', 'Duration', 'Priority'],
                                 tablefmt='grid'))
            output.append("")  # Empty line between days

        return '\n'.join(output)

    def get_study_preferences(self):
        """Get study preferences from user input"""
        print("\n=== Study Schedule Preferences ===")
        
        # Get available days
        print("\nAvailable study days:")
        print("1. Monday")
        print("2. Tuesday")
        print("3. Wednesday")
        print("4. Thursday")
        print("5. Friday")
        print("6. Saturday")
        print("7. Sunday")
        
        days_input = input("Enter day numbers (e.g., 1,2,3,4,5): ").strip()
        day_map = {
            '1': 'monday', '2': 'tuesday', '3': 'wednesday',
            '4': 'thursday', '5': 'friday', '6': 'saturday', '7': 'sunday'
        }
        
        study_days = []
        for day_num in days_input.split(','):
            if day_num.strip() in day_map:
                study_days.append(day_map[day_num.strip()])

        if not study_days:
            study_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

        # Get hours per day
        while True:
            try:
                hours = float(input("\nHow many hours can you study per day? "))
                if 0 < hours <= 12:
                    break
                print("Please enter a reasonable number of hours (1-12)")
            except ValueError:
                print("Please enter a valid number")

        # Get start date
        while True:
            date_str = input("\nStart date (YYYY-MM-DD, press Enter for today): ").strip()
            if not date_str:
                start_date = datetime.now()
                break
            try:
                start_date = datetime.strptime(date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Please enter a valid date in YYYY-MM-DD format")

        return study_days, hours, start_date

def main():
    generator = StudyScheduleGenerator()
    student_id = 'STU001'  # Example student ID

    # Get current workload
    workload = generator.get_student_workload(student_id)
    
    print("\n=== Current Course Workload ===")
    table_data = []
    for course in workload:
        completion = (course[2] / course[1] * 100) if course[1] > 0 else 0
        table_data.append([
            course[0],  # course_code
            course[1],  # total_topics
            f"{completion:.1f}%",  # completion percentage
            f"{course[4]}/{course[3]}h"  # hours spent/total
        ])
    
    print(tabulate(table_data,
                  headers=['Course', 'Topics', 'Completion', 'Hours (Spent/Total)'],
                  tablefmt='grid'))

    # Get course selection
    course_code = input("\nEnter course code to schedule: ").upper()
    
    # Get study preferences
    study_days, hours_per_day, start_date = generator.get_study_preferences()
    
    # Generate and display schedule
    schedule = generator.generate_schedule(
        student_id, course_code, hours_per_day, study_days, start_date
    )
    print(generator.format_schedule(schedule))

if __name__ == "__main__":
    main()

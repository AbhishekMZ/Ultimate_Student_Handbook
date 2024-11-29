import sqlite3
from datetime import datetime, timedelta
import json
from collections import defaultdict, deque

class LearningPathGenerator:
    def __init__(self, db_path='student_tracking.db'):
        self.db_path = db_path

    def add_topic_dependency(self, topic_id, prerequisite_topic_id, dependency_type='required'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT INTO topic_dependencies (topic_id, prerequisite_topic_id, dependency_type)
            VALUES (?, ?, ?)
            ''', (topic_id, prerequisite_topic_id, dependency_type))
            conn.commit()
        finally:
            conn.close()

    def get_topic_dependencies(self, topic_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            SELECT t.topic_name, td.dependency_type
            FROM topic_dependencies td
            JOIN topics t ON td.prerequisite_topic_id = t.topic_id
            WHERE td.topic_id = ?
            ''', (topic_id,))
            return cursor.fetchall()
        finally:
            conn.close()

    def generate_learning_path(self, student_id, course_code):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get all topics for the course
            cursor.execute('''
            SELECT t.topic_id, t.topic_name, t.importance_level, t.estimated_hours,
                   tp.completion_status, tp.understanding_level
            FROM topics t
            JOIN textbooks tb ON t.textbook_id = tb.textbook_id
            LEFT JOIN topic_progress tp ON t.topic_id = tp.topic_id AND tp.student_id = ?
            WHERE tb.course_code = ?
            ORDER BY t.chapter_number, t.topic_id
            ''', (student_id, course_code))
            
            topics = cursor.fetchall()
            
            # Build dependency graph
            graph = defaultdict(list)
            in_degree = defaultdict(int)
            
            cursor.execute('''
            SELECT topic_id, prerequisite_topic_id
            FROM topic_dependencies
            WHERE dependency_type = 'required'
            ''')
            
            for topic_id, prereq_id in cursor.fetchall():
                graph[prereq_id].append(topic_id)
                in_degree[topic_id] += 1

            # Topological sort with priority queue
            queue = deque()
            for topic in topics:
                topic_id = topic[0]
                if in_degree[topic_id] == 0:
                    queue.append(topic_id)

            learning_path = []
            while queue:
                current_topic = queue.popleft()
                learning_path.append(current_topic)
                
                for next_topic in graph[current_topic]:
                    in_degree[next_topic] -= 1
                    if in_degree[next_topic] == 0:
                        queue.append(next_topic)

            # Generate detailed learning path with time estimates
            detailed_path = []
            current_date = datetime.now()
            
            for topic_id in learning_path:
                for topic in topics:
                    if topic[0] == topic_id:
                        topic_info = {
                            'topic_id': topic[0],
                            'topic_name': topic[1],
                            'importance_level': topic[2],
                            'estimated_hours': topic[3],
                            'status': topic[4] or 'not_started',
                            'understanding_level': topic[5] or 0,
                            'start_date': current_date.strftime('%Y-%m-%d'),
                            'end_date': (current_date + timedelta(days=max(1, topic[3]//4))).strftime('%Y-%m-%d')
                        }
                        detailed_path.append(topic_info)
                        current_date += timedelta(days=max(1, topic[3]//4))
                        break

            return detailed_path

        finally:
            conn.close()

    def create_study_schedule(self, student_id, course_code, start_date=None):
        if start_date is None:
            start_date = datetime.now()

        learning_path = self.generate_learning_path(student_id, course_code)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Clear existing deadlines for this course
            cursor.execute('''
            DELETE FROM deadlines
            WHERE student_id = ? AND topic_id IN (
                SELECT t.topic_id
                FROM topics t
                JOIN textbooks tb ON t.textbook_id = tb.textbook_id
                WHERE tb.course_code = ?
            )
            ''', (student_id, course_code))

            # Create new deadlines based on learning path
            current_date = start_date
            for topic in learning_path:
                # Add reading deadline
                cursor.execute('''
                INSERT INTO deadlines (
                    student_id, topic_id, deadline_type,
                    due_date, priority, status, reminder_frequency
                ) VALUES (?, ?, 'reading', ?, ?, 'pending', 'daily')
                ''', (
                    student_id,
                    topic['topic_id'],
                    current_date.strftime('%Y-%m-%d'),
                    topic['importance_level']
                ))

                # Add assignment deadline
                assignment_date = current_date + timedelta(days=max(1, topic['estimated_hours']//4))
                cursor.execute('''
                INSERT INTO deadlines (
                    student_id, topic_id, deadline_type,
                    due_date, priority, status, reminder_frequency
                ) VALUES (?, ?, 'assignment', ?, ?, 'pending', 'daily')
                ''', (
                    student_id,
                    topic['topic_id'],
                    assignment_date.strftime('%Y-%m-%d'),
                    topic['importance_level']
                ))

                current_date = assignment_date + timedelta(days=1)

            conn.commit()
            return True

        finally:
            conn.close()

    def get_student_schedule(self, student_id, start_date=None, end_date=None):
        if start_date is None:
            start_date = datetime.now()
        if end_date is None:
            end_date = start_date + timedelta(days=30)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            SELECT d.deadline_id, t.topic_name, d.deadline_type,
                   d.due_date, d.priority, d.status,
                   tb.course_code, tb.title as textbook_title
            FROM deadlines d
            JOIN topics t ON d.topic_id = t.topic_id
            JOIN textbooks tb ON t.textbook_id = tb.textbook_id
            WHERE d.student_id = ? AND d.due_date BETWEEN ? AND ?
            ORDER BY d.due_date, d.priority DESC
            ''', (
                student_id,
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            ))

            schedule = []
            for row in cursor.fetchall():
                schedule.append({
                    'deadline_id': row[0],
                    'topic_name': row[1],
                    'deadline_type': row[2],
                    'due_date': row[3],
                    'priority': row[4],
                    'status': row[5],
                    'course_code': row[6],
                    'textbook_title': row[7]
                })

            return schedule

        finally:
            conn.close()

if __name__ == "__main__":
    # Example usage
    generator = LearningPathGenerator()
    
    # Add some sample dependencies
    generator.add_topic_dependency(2, 1, 'required')  # Topic 2 requires Topic 1
    generator.add_topic_dependency(3, 2, 'required')  # Topic 3 requires Topic 2
    
    # Generate learning path for a student
    learning_path = generator.generate_learning_path('STU001', 'CD252IA')
    print("Generated Learning Path:")
    for topic in learning_path:
        print(f"Topic: {topic['topic_name']}")
        print(f"Start Date: {topic['start_date']}")
        print(f"End Date: {topic['end_date']}")
        print("---")
    
    # Create study schedule
    generator.create_study_schedule('STU001', 'CD252IA')
    print("\nStudy schedule created successfully!")

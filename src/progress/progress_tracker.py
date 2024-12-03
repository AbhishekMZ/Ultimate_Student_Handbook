import sqlite3
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from backend.database.database import DB_PATH
from backend.core.database_manager import DatabaseManager

class ProgressTracker:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_manager = DatabaseManager()

    def get_topic_progress(self, student_id, topic_id):
        """Get progress for a specific topic"""
        with self.db_manager.get_connection(commit_on_success=False) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT progress_id, completion_status, understanding_level, 
                       time_spent_hours, last_studied, notes
                FROM topic_progress
                WHERE student_id = ? AND topic_id = ?
            ''', (student_id, topic_id))
            return cursor.fetchone()

    def update_progress(self, student_id, topic_id, status, understanding, time_spent, notes=None):
        """Update or create progress entry for a topic"""
        try:
            progress_data = {
                'student_id': student_id,
                'topic_id': topic_id,
                'completion_status': status,
                'understanding_level': understanding,
                'time_spent_hours': time_spent,
                'notes': notes
            }
            return self.db_manager.update_progress(progress_data)
        except (DatabaseValidationError, sqlite3.Error) as e:
            print(f"Error updating progress: {e}")
            return False

    def generate_progress_report(self, student_id, course_code):
        """Generate a detailed progress report for a course"""
        with self.db_manager.get_connection(commit_on_success=False) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    SELECT 
                        t.topic_id,
                        t.topic_name,
                        tp.completion_status,
                        tp.understanding_level,
                        tp.time_spent_hours,
                        tp.last_studied
                    FROM topics t
                    JOIN textbooks tb ON t.textbook_id = tb.textbook_id
                    LEFT JOIN topic_progress tp ON t.topic_id = tp.topic_id 
                        AND tp.student_id = ?
                    WHERE tb.course_code = ?
                    ORDER BY t.chapter_number, t.topic_id
                ''', (student_id, course_code))

                topics = cursor.fetchall()
                if not topics:
                    return "No topics found for this course."

                # Calculate summary statistics
                total_topics = len(topics)
                completed = sum(1 for t in topics if t[2] == 'completed')
                in_progress = sum(1 for t in topics if t[2] == 'in_progress')
                not_started = sum(1 for t in topics if not t[2] or t[2] == 'not_started')
                total_time = sum(t[4] or 0 for t in topics)
                avg_understanding = np.mean([t[3] or 0 for t in topics if t[3] is not None])

                # Format report
                report = [
                    f"\n=== Progress Report for {course_code} ===\n",
                    "Overall Progress:",
                    f"Total Topics: {total_topics}",
                    f"Completed: {completed} ({completed/total_topics*100:.1f}%)",
                    f"In Progress: {in_progress}",
                    f"Not Started: {not_started}",
                    f"Total Time Spent: {total_time:.1f} hours",
                    f"Average Understanding: {avg_understanding:.1f}/5\n",
                    "Topic Details:"
                ]

                # Create topic details table
                table_data = []
                for topic in topics:
                    status = topic[2] or 'Not Started'
                    understanding = '⭐' * (topic[3] or 0) if topic[3] else '-'
                    time_spent = f"{topic[4]:.1f}h" if topic[4] else '-'
                    last_studied = topic[5].split()[0] if topic[5] else '-'

                    table_data.append([
                        topic[1],  # topic_name
                        status.title(),
                        understanding,
                        time_spent,
                        last_studied
                    ])

                report.append(tabulate(table_data,
                                    headers=['Topic', 'Status', 'Understanding', 
                                            'Time Spent', 'Last Reviewed'],
                                    tablefmt='grid'))

                return '\n'.join(report)

            except sqlite3.Error as e:
                return f"Error generating report: {e}"

    def plot_progress_trends(self, student_id, course_code):
        """Generate and save progress visualization"""
        with self.db_manager.get_connection(commit_on_success=False) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    SELECT 
                        t.topic_name,
                        tp.understanding_level,
                        tp.time_spent_hours,
                        tp.completion_status
                    FROM topics t
                    JOIN textbooks tb ON t.textbook_id = tb.textbook_id
                    LEFT JOIN topic_progress tp ON t.topic_id = tp.topic_id 
                        AND tp.student_id = ?
                    WHERE tb.course_code = ?
                    ORDER BY t.chapter_number, t.topic_id
                ''', (student_id, course_code))

                data = cursor.fetchall()
                if not data:
                    return False

                # Prepare data for plotting
                topics = [row[0] for row in data]
                understanding = [row[1] or 0 for row in data]
                time_spent = [row[2] or 0 for row in data]
                completion = [1 if row[3] == 'completed' 
                            else 0.5 if row[3] == 'in_progress' 
                            else 0 for row in data]

                # Create figure with subplots
                plt.figure(figsize=(15, 10))

                # Understanding levels
                plt.subplot(3, 1, 1)
                plt.bar(topics, understanding, color='skyblue')
                plt.title('Understanding Levels by Topic')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, 5)

                # Time spent
                plt.subplot(3, 1, 2)
                plt.bar(topics, time_spent, color='lightgreen')
                plt.title('Time Spent (hours) by Topic')
                plt.xticks(rotation=45, ha='right')

                # Completion status
                plt.subplot(3, 1, 3)
                plt.bar(topics, completion, color='salmon')
                plt.title('Completion Status by Topic')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, 1)
                plt.yticks([0, 0.5, 1], ['Not Started', 'In Progress', 'Completed'])

                plt.tight_layout()
                plt.savefig('progress_trends.png')
                plt.close()

                return True

            except Exception as e:
                print(f"Error plotting trends: {e}")
                return False

def main():
    tracker = ProgressTracker()
    # Add test code here if needed

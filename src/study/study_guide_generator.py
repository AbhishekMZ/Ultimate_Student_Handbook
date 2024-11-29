import sqlite3
import json
from datetime import datetime
import random

class StudyGuideGenerator:
    def __init__(self, db_path='student_tracking.db'):
        self.db_path = db_path

    def add_topic(self, textbook_id, chapter_number, topic_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT INTO topics (
                textbook_id, chapter_number, topic_name, description,
                importance_level, estimated_hours, prerequisites, learning_outcomes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                textbook_id,
                chapter_number,
                topic_data['name'],
                topic_data['description'],
                topic_data['importance_level'],
                topic_data['estimated_hours'],
                json.dumps(topic_data.get('prerequisites', [])),
                json.dumps(topic_data.get('learning_outcomes', []))
            ))
            
            topic_id = cursor.lastrowid
            conn.commit()
            return topic_id
        finally:
            conn.close()

    def generate_study_guide(self, topic_id, content_type='summary'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get topic information
            cursor.execute('''
            SELECT t.topic_name, t.description, t.learning_outcomes, tb.title
            FROM topics t
            JOIN textbooks tb ON t.textbook_id = tb.textbook_id
            WHERE t.topic_id = ?
            ''', (topic_id,))
            
            topic_info = cursor.fetchone()
            if not topic_info:
                return None

            topic_name, description, learning_outcomes, textbook_title = topic_info
            learning_outcomes = json.loads(learning_outcomes)

            # Generate content based on type
            if content_type == 'summary':
                content = self._generate_summary(topic_name, description, learning_outcomes)
            elif content_type == 'notes':
                content = self._generate_notes(topic_name, description, learning_outcomes)
            elif content_type == 'practice_questions':
                content = self._generate_practice_questions(topic_name, learning_outcomes)
            elif content_type == 'examples':
                content = self._generate_examples(topic_name, learning_outcomes)
            else:
                raise ValueError(f"Invalid content type: {content_type}")

            # Save study guide
            cursor.execute('''
            INSERT INTO study_guides (topic_id, content_type, content, difficulty_level)
            VALUES (?, ?, ?, ?)
            ''', (topic_id, content_type, content, random.randint(1, 5)))

            guide_id = cursor.lastrowid
            conn.commit()
            return guide_id

        finally:
            conn.close()

    def _generate_summary(self, topic_name, description, learning_outcomes):
        summary = f"# {topic_name}\n\n"
        summary += "## Overview\n"
        summary += f"{description}\n\n"
        summary += "## Learning Outcomes\n"
        for i, outcome in enumerate(learning_outcomes, 1):
            summary += f"{i}. {outcome}\n"
        return summary

    def _generate_notes(self, topic_name, description, learning_outcomes):
        notes = f"# Detailed Notes: {topic_name}\n\n"
        notes += "## Introduction\n"
        notes += f"{description}\n\n"
        notes += "## Key Concepts\n"
        
        # Generate detailed notes for each learning outcome
        for outcome in learning_outcomes:
            notes += f"### {outcome}\n"
            notes += "- Key points...\n"
            notes += "- Important concepts...\n"
            notes += "- Related examples...\n\n"
        
        return notes

    def _generate_practice_questions(self, topic_name, learning_outcomes):
        questions = f"# Practice Questions: {topic_name}\n\n"
        
        # Generate questions based on learning outcomes
        for i, outcome in enumerate(learning_outcomes, 1):
            questions += f"## Question Set {i}\n"
            questions += f"Learning Outcome: {outcome}\n\n"
            
            # Generate multiple types of questions
            questions += "1. Multiple Choice Question\n"
            questions += "   - Option A\n"
            questions += "   - Option B\n"
            questions += "   - Option C\n"
            questions += "   - Option D\n\n"
            
            questions += "2. Short Answer Question\n"
            questions += "   [Answer space...]\n\n"
            
            questions += "3. Problem Solving Question\n"
            questions += "   [Problem statement...]\n\n"
        
        return questions

    def _generate_examples(self, topic_name, learning_outcomes):
        examples = f"# Examples: {topic_name}\n\n"
        
        # Generate examples for each learning outcome
        for i, outcome in enumerate(learning_outcomes, 1):
            examples += f"## Example Set {i}\n"
            examples += f"Illustrating: {outcome}\n\n"
            
            examples += "### Basic Example\n"
            examples += "[Basic example details...]\n\n"
            
            examples += "### Intermediate Example\n"
            examples += "[Intermediate example details...]\n\n"
            
            examples += "### Advanced Example\n"
            examples += "[Advanced example details...]\n\n"
        
        return examples

    def track_progress(self, student_id, topic_id, status='in_progress', understanding_level=3):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT OR REPLACE INTO topic_progress (
                student_id, topic_id, completion_status,
                understanding_level, time_spent_hours, last_reviewed
            ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (student_id, topic_id, status, understanding_level, 0.0))
            
            conn.commit()
        finally:
            conn.close()

    def add_deadline(self, student_id, topic_id, deadline_type, due_date, priority=3):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT INTO deadlines (
                student_id, topic_id, deadline_type,
                due_date, priority, status, reminder_frequency
            ) VALUES (?, ?, ?, ?, ?, 'pending', 'weekly')
            ''', (student_id, topic_id, deadline_type, due_date, priority))
            
            conn.commit()
        finally:
            conn.close()

if __name__ == "__main__":
    # Example usage
    generator = StudyGuideGenerator()
    
    # Sample topic data
    sample_topic = {
        'name': 'Introduction to Databases',
        'description': 'Basic concepts and fundamental principles of database systems',
        'importance_level': 5,
        'estimated_hours': 4,
        'prerequisites': ['Basic computer concepts'],
        'learning_outcomes': [
            'Understand what is a database',
            'Identify different types of databases',
            'Explain the importance of DBMS',
            'Describe basic database architecture'
        ]
    }
    
    # Add topic and generate study materials
    topic_id = generator.add_topic(1, 1, sample_topic)
    if topic_id:
        generator.generate_study_guide(topic_id, 'summary')
        generator.generate_study_guide(topic_id, 'notes')
        generator.generate_study_guide(topic_id, 'practice_questions')
        generator.generate_study_guide(topic_id, 'examples')
        print("Study materials generated successfully!")

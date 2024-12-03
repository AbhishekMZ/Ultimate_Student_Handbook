import os
import csv
import logging
from flask import Blueprint, jsonify, current_app
from ..database.database import get_db_connection
import sqlite3

bp = Blueprint('student_performance', __name__)
logger = logging.getLogger(__name__)

# Helper function to read CSV files
def read_csv_file(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                          'data', 'processed', 'csv', filename)
    logger.debug(f"Reading CSV file from: {filepath}")
    
    if not os.path.exists(filepath):
        logger.error(f"CSV file not found: {filepath}")
        raise FileNotFoundError(f"CSV file not found: {filename}")
        
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            logger.debug(f"Successfully read {len(data)} rows from {filename}")
    except Exception as e:
        logger.error(f"Error reading CSV file {filename}: {str(e)}")
        raise
        
    return data

@bp.route('/api/students', methods=['GET'])
def get_students():
    logger.debug("Handling /api/students request")
    try:
        students = read_csv_file('students.csv')
        formatted_students = []
        for student in students:
            if student.get('StudentID') and student.get('Name'):
                formatted_students.append({
                    'studentId': student['StudentID'],
                    'name': student['Name'],
                    'email': student.get('Email', ''),
                    'tenthMarks': float(student.get('TenthMarks', 0)),
                    'twelfthMarks': float(student.get('TwelfthMarks', 0)),
                    'semester': int(student.get('Semester', 0)),
                    'strengths': [s.strip() for s in student.get('Strengths', '').split(';') if s.strip()],
                    'weaknesses': [w.strip() for w in student.get('Weaknesses', '').split(';') if w.strip()],
                    'courses': [c.strip() for c in student.get('Courses', '').split(',') if c.strip()]
                })
        logger.debug(f"Returning {len(formatted_students)} students")
        return jsonify(formatted_students)
    except Exception as e:
        logger.error(f"Error in get_students: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/students/<student_id>', methods=['GET'])
def get_student_details(student_id):
    logger.debug(f"Handling /api/students/{student_id} request")
    try:
        students = read_csv_file('students.csv')
        student_data = next((student for student in students if student['StudentID'] == student_id), None)
        
        if not student_data:
            return jsonify({'error': 'Student not found'}), 404
            
        formatted_student = {
            'studentId': student_data['StudentID'],
            'name': student_data['Name'],
            'email': student_data.get('Email', ''),
            'tenthMarks': float(student_data.get('TenthMarks', 0)),
            'twelfthMarks': float(student_data.get('TwelfthMarks', 0)),
            'semester': int(student_data.get('Semester', 0)),
            'strengths': [s.strip() for s in student_data.get('Strengths', '').split(';') if s.strip()],
            'weaknesses': [w.strip() for w in student_data.get('Weaknesses', '').split(';') if w.strip()],
            'courses': [c.strip() for c in student_data.get('Courses', '').split(',') if c.strip()]
        }
        
        return jsonify(formatted_student)
    except Exception as e:
        logger.error(f"Error in get_student_details: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/courses', methods=['GET'])
def get_courses():
    logger.debug("Handling /api/courses request")
    try:
        courses = read_csv_file('courses.csv')
        formatted_courses = [{
            'code': course['CourseCode'],
            'name': course['CourseName'],
            'category': course['Category'],
            'credits': course['Credits'],
            'totalHours': course['TotalHours'],
            'cie': int(course['CIE']) if course['CIE'] else None,
            'see': int(course['SEE']) if course['SEE'] else None,
            'semester': int(course['Semester'])
        } for course in courses]
        logger.debug(f"Returning {len(formatted_courses)} courses")
        return jsonify(formatted_courses)
    except Exception as e:
        logger.error(f"Error in get_courses: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/academic/<int:student_id>', methods=['GET'])
def get_academic_history(student_id):
    logger.debug(f"Handling /api/academic/{student_id} request")
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                education_level,
                institution,
                board,
                percentage,
                year_of_completion,
                subjects,
                achievements
            FROM academic_history
            WHERE user_id = ?
            ORDER BY year_of_completion DESC
        ''', (student_id,))
        
        records = cursor.fetchall()
        academic_history = []
        
        for record in records:
            academic_history.append({
                'education_level': record[0],
                'institution': record[1],
                'board': record[2],
                'percentage': record[3],
                'year_of_completion': record[4],
                'subjects': record[5],
                'achievements': record[6]
            })
            
        logger.debug(f"Returning {len(academic_history)} academic history records for student {student_id}")
        return jsonify(academic_history)
        
    except sqlite3.Error as e:
        logger.error(f"Error in get_academic_history: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@bp.route('/api/learning/<int:student_id>', methods=['GET'])
def get_learning_profile(student_id):
    logger.debug(f"Handling /api/learning/{student_id} request")
    try:
        students = read_csv_file('students.csv')
        student = next((s for s in students if s['StudentID'] == f'1RV22AI{student_id:03d}'), None)
        
        if student:
            strengths = [s.strip() for s in student['Strengths'].split(';')] if student['Strengths'] else []
            weaknesses = [w.strip() for w in student['Weaknesses'].split(';')] if student['Weaknesses'] else []
            
            learning_profile = {
                'strengths': strengths,
                'weaknesses': weaknesses,
                'tenth_marks': student['TenthMarks'],
                'twelfth_marks': student['TwelfthMarks']
            }
            logger.debug(f"Returning learning profile for student {student_id}")
            return jsonify(learning_profile)
        logger.error(f"Student not found: {student_id}")
        return jsonify({'error': 'Student not found'}), 404
        
    except Exception as e:
        logger.error(f"Error in get_learning_profile: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/progress/<int:student_id>', methods=['GET'])
def get_student_progress(student_id):
    logger.debug(f"Handling /api/progress/{student_id} request")
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                sp.topic_id,
                t.topic_name,
                sp.completion_status,
                sp.understanding_level,
                sp.time_spent,
                sp.last_activity_date,
                sp.notes
            FROM student_progress sp
            JOIN topics t ON sp.topic_id = t.topic_id
            WHERE sp.user_id = ?
            ORDER BY sp.last_activity_date DESC
        ''', (student_id,))
        
        records = cursor.fetchall()
        progress_list = []
        
        for record in records:
            progress_list.append({
                'topic_id': record[0],
                'topic_name': record[1],
                'status': record[2],
                'understanding_level': record[3],
                'time_spent': record[4],
                'last_activity': record[5],
                'notes': record[6]
            })
            
        logger.debug(f"Returning {len(progress_list)} progress records for student {student_id}")
        return jsonify(progress_list)
        
    except sqlite3.Error as e:
        logger.error(f"Error in get_student_progress: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

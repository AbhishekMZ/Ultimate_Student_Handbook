from flask import Blueprint, jsonify
from database import get_db_connection
import sqlite3

bp = Blueprint('student_performance', __name__)

@bp.route('/api/academic/<int:student_id>', methods=['GET'])
def get_academic_history(student_id):
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
            
        return jsonify(academic_history)
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@bp.route('/api/learning/<int:student_id>', methods=['GET'])
def get_learning_profile(student_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                learning_style,
                study_time_preference,
                concentration_span,
                subjects_of_interest,
                weak_areas,
                study_group_preference
            FROM learning_profiles
            WHERE user_id = ?
        ''', (student_id,))
        
        record = cursor.fetchone()
        if record:
            learning_profile = {
                'learning_style': record[0],
                'study_time_preference': record[1],
                'concentration_span': record[2],
                'subjects_of_interest': record[3],
                'weak_areas': record[4],
                'study_group_preference': record[5]
            }
            return jsonify(learning_profile)
        return jsonify({'error': 'Learning profile not found'}), 404
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@bp.route('/api/progress/<int:student_id>', methods=['GET'])
def get_student_progress(student_id):
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
            
        return jsonify(progress_list)
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@bp.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                u.user_id as id,
                up.first_name || ' ' || up.last_name as name,
                u.username as email
            FROM users u
            JOIN user_profiles up ON u.user_id = up.user_id
            JOIN roles r ON u.role_id = r.role_id
            WHERE r.role_name = 'student'
            ORDER BY up.first_name, up.last_name
        ''')
        
        students = cursor.fetchall()
        student_list = []
        
        for student in students:
            student_list.append({
                'id': student[0],
                'name': student[1],
                'email': student[2]
            })
            
        return jsonify(student_list)
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@bp.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                c.course_id as id,
                c.course_name as name,
                c.description,
                c.duration,
                c.difficulty,
                GROUP_CONCAT(t.topic_name) as topics,
                COUNT(DISTINCT sp.user_id) as enrolled_count
            FROM courses c
            LEFT JOIN topics t ON t.course_id = c.course_id
            LEFT JOIN student_progress sp ON sp.topic_id = t.topic_id
            GROUP BY c.course_id
            ORDER BY c.course_name
        ''')
        
        courses = cursor.fetchall()
        course_list = []
        
        for course in courses:
            course_list.append({
                'id': course[0],
                'name': course[1],
                'description': course[2],
                'duration': course[3],
                'difficulty': course[4],
                'topics': course[5],
                'enrolled_count': course[6]
            })
            
        return jsonify(course_list)
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

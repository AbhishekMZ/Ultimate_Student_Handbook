from flask import Flask, request, jsonify
from flask_cors import CORS
from src.core.database_manager import DatabaseManager
from src.analytics.analyze_performance import PerformanceAnalyzer
from src.progress.progress_tracker import ProgressTracker
from src.study.study_materials_browser import StudyMaterialsBrowser
from src.feedback.student_survey import SurveyManager
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
db_manager = DatabaseManager()
performance_analyzer = PerformanceAnalyzer()
progress_tracker = ProgressTracker()
materials_browser = StudyMaterialsBrowser()
survey_manager = SurveyManager()

# Error handler for database errors
@app.errorhandler(sqlite3.Error)
def handle_database_error(error):
    return jsonify({
        'error': 'Database error occurred',
        'message': str(error)
    }), 500

# Students endpoints
@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()
            return jsonify([{
                'id': student[0],
                'name': student[1],
                'email': student[2],
                'enrollment_date': student[3]
            } for student in students])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
            student = cursor.fetchone()
            if student:
                return jsonify({
                    'id': student[0],
                    'name': student[1],
                    'email': student[2],
                    'enrollment_date': student[3]
                })
            return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    required_fields = ['name', 'email']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO students (name, email) VALUES (?, ?)',
                (data['name'], data['email'])
            )
            return jsonify({'id': cursor.lastrowid, 'message': 'Student created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Courses endpoints
@app.route('/api/courses', methods=['GET'])
def get_courses():
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses')
            courses = cursor.fetchall()
            return jsonify([{
                'id': course[0],
                'code': course[1],
                'name': course[2],
                'description': course[3]
            } for course in courses])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses WHERE course_id = ?', (course_id,))
            course = cursor.fetchone()
            if course:
                return jsonify({
                    'id': course[0],
                    'code': course[1],
                    'name': course[2],
                    'description': course[3]
                })
            return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Progress endpoints
@app.route('/api/progress/<int:student_id>', methods=['GET'])
def get_student_progress(student_id):
    try:
        progress_data = progress_tracker.get_topic_progress(student_id, None)
        return jsonify(progress_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/<int:student_id>/course/<int:course_id>', methods=['GET'])
def get_course_progress(student_id, course_id):
    try:
        progress_data = progress_tracker.generate_progress_report(student_id, course_id)
        return jsonify(progress_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Analytics endpoints
@app.route('/api/analytics/performance/<int:student_id>', methods=['GET'])
def get_performance_analytics(student_id):
    try:
        analytics_data = performance_analyzer.analyze_student_performance(student_id)
        return jsonify(analytics_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/course/<int:course_id>', methods=['GET'])
def get_course_analytics(course_id):
    try:
        analytics_data = performance_analyzer.analyze_course_performance(course_id)
        return jsonify(analytics_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Study materials endpoints
@app.route('/api/materials/course/<int:course_id>', methods=['GET'])
def get_course_materials(course_id):
    try:
        materials = materials_browser.list_course_materials(course_id)
        return jsonify(materials)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Survey endpoints
@app.route('/api/surveys/<int:student_id>', methods=['GET'])
def get_student_surveys(student_id):
    try:
        surveys = survey_manager.get_student_surveys(student_id)
        return jsonify(surveys)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/surveys', methods=['POST'])
def submit_survey():
    data = request.get_json()
    try:
        survey_id = survey_manager.submit_survey(
            data.get('student_id'),
            data.get('responses')
        )
        return jsonify({'id': survey_id, 'message': 'Survey submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard data endpoint
@app.route('/api/dashboard/summary', methods=['GET'])
def get_dashboard_summary():
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get total students
            cursor.execute('SELECT COUNT(*) FROM students')
            total_students = cursor.fetchone()[0]
            
            # Get total courses
            cursor.execute('SELECT COUNT(*) FROM courses')
            total_courses = cursor.fetchone()[0]
            
            # Get average progress
            cursor.execute('''
                SELECT AVG(completion_percentage)
                FROM student_progress
            ''')
            avg_progress = cursor.fetchone()[0] or 0
            
            # Get success rate (students with progress > 70%)
            cursor.execute('''
                SELECT COUNT(DISTINCT student_id) * 100.0 / (SELECT COUNT(*) FROM students)
                FROM student_progress
                WHERE completion_percentage > 70
            ''')
            success_rate = cursor.fetchone()[0] or 0
            
            return jsonify({
                'total_students': total_students,
                'total_courses': total_courses,
                'average_progress': round(avg_progress, 2),
                'success_rate': round(success_rate, 2)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

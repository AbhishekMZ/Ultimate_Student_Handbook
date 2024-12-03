from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import jwt
import os
from datetime import datetime

from core.app import StudentTrackingSystem
from core.auth import AuthResult

app = Flask(__name__)
CORS(app)

# Initialize the main application
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'student_tracking.db')
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
system = StudentTrackingSystem(DB_PATH, SECRET_KEY)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    password = data.pop('password', None)
    device_id = data.pop('device_id', None)

    if not password:
        return jsonify({'success': False, 'message': 'Password is required'}), 400

    result = system.register_student(data, password, device_id)
    return jsonify(result.__dict__), 200 if result.success else 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    result = system.login(data['email'], data['password'], data.get('device_id'))
    return jsonify(result.__dict__), 200 if result.success else 401

@app.route('/api/dashboard/<student_id>', methods=['GET'])
@token_required
def get_dashboard(current_user, student_id):
    if current_user['student_id'] != student_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    dashboard_data = system.get_student_dashboard(student_id)
    return jsonify(dashboard_data), 200

@app.route('/api/courses/<course_code>/progress/<student_id>', methods=['GET'])
@token_required
def get_course_progress(current_user, course_code, student_id):
    if current_user['student_id'] != student_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    progress = system.analytics.get_course_progress(student_id, course_code)
    if not progress:
        return jsonify({'message': 'Course progress not found'}), 404

    return jsonify(progress.__dict__), 200

@app.route('/api/notifications/<student_id>', methods=['GET'])
@token_required
def get_notifications(current_user, student_id):
    if current_user['student_id'] != student_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    notifications = system.notifications.get_notifications(
        student_id,
        unread_only=unread_only
    )
    return jsonify([n.__dict__ for n in notifications]), 200

@app.route('/api/notifications/<notification_id>/read', methods=['POST'])
@token_required
def mark_notification_read(current_user, notification_id):
    result = system.notifications.mark_as_read(notification_id)
    return jsonify({'success': result}), 200 if result else 400

@app.route('/api/sync/<student_id>/device/<device_id>', methods=['POST'])
@token_required
def sync_device(current_user, student_id, device_id):
    if current_user['student_id'] != student_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    sync_data = request.json
    result = system.sync_device_data(student_id, device_id, sync_data)
    return jsonify(result.__dict__), 200 if result.success else 400

@app.route('/api/achievements/<student_id>', methods=['POST'])
@token_required
def track_achievement(current_user, student_id):
    if current_user['student_id'] != student_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    achievement_data = request.json
    result = system.track_achievement(student_id, achievement_data)
    return jsonify({'success': result}), 200 if result else 400

@app.route('/api/courses/<student_id>', methods=['GET'])
@token_required
def get_student_courses(current_user, student_id):
    if current_user['student_id'] != student_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    # This endpoint would be implemented based on your course data structure
    # For now, returning a placeholder response
    courses = [
        {
            'course_code': 'CS101',
            'course_name': 'Introduction to Programming',
            'semester': 1,
            'credits': 4,
            'instructor': 'Dr. Smith'
        }
    ]
    return jsonify(courses), 200

@app.route('/api/performance/<student_id>/analytics', methods=['GET'])
@token_required
def get_performance_analytics(current_user, student_id):
    if current_user['student_id'] != student_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    performance = system.analytics.get_student_performance(student_id)
    if not performance:
        return jsonify({'message': 'Performance data not found'}), 404

    return jsonify(performance.__dict__), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

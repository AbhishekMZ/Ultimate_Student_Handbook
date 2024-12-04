from flask import Blueprint, jsonify
from src.models.user import User, db

student_bp = Blueprint('students', __name__)

@student_bp.route('/api/students', methods=['GET'])
def get_students():
    try:
        # Query only users with role 'student'
        students = User.query.filter_by(role='student').all()
        
        # Convert students to list of dictionaries
        students_data = [{
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'student_id': student.student_id
        } for student in students]
        
        return jsonify(students_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch students', 'details': str(e)}), 500

@student_bp.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student = User.query.filter_by(id=student_id, role='student').first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
            
        student_data = {
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'student_id': student.student_id
        }
        
        return jsonify(student_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch student', 'details': str(e)}), 500

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import User
from src.models.course import Course
from src.models.enrollment import Enrollment
from src.app import db

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['name', 'email', 'password', 'role']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            role=data['role']
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        access_token = create_access_token(identity=new_user.id)
        return jsonify({
            'token': access_token,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_routes.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    try:
        students = User.query.filter_by(role='student').all()
        return jsonify([student.to_dict() for student in students]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_routes.route('/progress/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_progress(student_id):
    try:
        student = User.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        # Mock progress data - replace with actual data from your database
        progress_data = {
            'overall_progress': 75,
            'recent_activities': [
                {
                    'id': '1',
                    'timestamp': '2024-01-20T10:30:00',
                    'description': 'Completed Assignment 1',
                    'type': 'assignment'
                },
                {
                    'id': '2',
                    'timestamp': '2024-01-19T14:45:00',
                    'description': 'Attended Python Programming Class',
                    'type': 'attendance'
                },
                {
                    'id': '3',
                    'timestamp': '2024-01-18T11:00:00',
                    'description': 'Scored 85% in Quiz 2',
                    'type': 'assessment'
                }
            ],
            'performance_metrics': {
                'attendance': 90,
                'assignments_completed': 85,
                'average_score': 88
            }
        }
        return jsonify(progress_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_routes.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

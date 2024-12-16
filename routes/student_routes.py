# routes/student_routes.py

from flask import Blueprint, request, jsonify
from bson import ObjectId

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard/<student_id>', methods=['GET'])
def get_dashboard(student_id):
    try:
        student_service = StudentService(current_app.db)
        dashboard_data = student_service.get_student_dashboard(student_id)
        return jsonify(dashboard_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@student_bp.route('/progress/update', methods=['POST'])
def update_progress():
    try:
        data = request.get_json()
        progress_model = ProgressModel(current_app.db)
        result = progress_model.update_progress(
            data['student_id'],
            data['course_id'],
            data['progress_data']
        )
        return jsonify({"message": "Progress updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
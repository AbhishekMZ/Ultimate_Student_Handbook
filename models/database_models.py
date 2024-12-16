# models/database_models.py

from datetime import datetime
from bson import ObjectId

class StudentModel:
    def __init__(self, db):
        self.collection = db['students']

    def create_student(self, student_data):
        student = {
            "email": student_data['email'],
            "password": student_data['hashed_password'],
            "full_name": student_data['full_name'],
            "created_at": datetime.utcnow(),
            "last_login": None,
            "active_devices": [],
            "courses": []
        }
        return self.collection.insert_one(student)

class ProgressModel:
    def __init__(self, db):
        self.collection = db['progress']

    def update_progress(self, student_id, course_id, progress_data):
        progress = {
            "student_id": ObjectId(student_id),
            "course_id": ObjectId(course_id),
            "completion_percentage": progress_data['completion_percentage'],
            "last_updated": datetime.utcnow(),
            "topics_completed": progress_data['topics_completed'],
            "assessment_scores": progress_data['assessment_scores']
        }
        return self.collection.update_one(
            {"student_id": ObjectId(student_id), "course_id": ObjectId(course_id)},
            {"$set": progress},
            upsert=True
        )

class NotificationModel:
    def __init__(self, db):
        self.collection = db['notifications']

    def create_notification(self, notification_data):
        notification = {
            "student_id": ObjectId(notification_data['student_id']),
            "type": notification_data['type'],
            "message": notification_data['message'],
            "created_at": datetime.utcnow(),
            "read": False
        }
        return self.collection.insert_one(notification)
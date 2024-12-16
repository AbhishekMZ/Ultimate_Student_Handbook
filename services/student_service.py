# services/student_service.py

from bson import ObjectId

class StudentService:
    def __init__(self, db):
        self.db = db
        self.students = db['students']
        self.progress = db['progress']

    def get_student_dashboard(self, student_id):
        pipeline = [
            {
                "$match": {"_id": ObjectId(student_id)}
            },
            {
                "$lookup": {
                    "from": "progress",
                    "localField": "_id",
                    "foreignField": "student_id",
                    "as": "progress_data"
                }
            },
            {
                "$lookup": {
                    "from": "notifications",
                    "localField": "_id",
                    "foreignField": "student_id",
                    "as": "notifications"
                }
            }
        ]
        return self.students.aggregate(pipeline)

# services/analytics_service.py

class AnalyticsService:
    def __init__(self, db):
        self.db = db
        self.progress = db['progress']

    def get_student_analytics(self, student_id):
        pipeline = [
            {
                "$match": {"student_id": ObjectId(student_id)}
            },
            {
                "$group": {
                    "_id": "$course_id",
                    "average_score": {"$avg": "$assessment_scores"},
                    "completion_rate": {"$avg": "$completion_percentage"}
                }
            }
        ]
        return self.progress.aggregate(pipeline)
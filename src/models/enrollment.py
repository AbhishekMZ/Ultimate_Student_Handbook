from datetime import datetime
from src.models.user import db

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, completed, dropped
    progress = db.Column(db.Float, default=0.0)  # percentage of course completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref=db.backref('enrollments', lazy=True))
    course = db.relationship('Course', back_populates='enrollments')

    def __init__(self, student_id, course_id, status='active'):
        self.student_id = student_id
        self.course_id = course_id
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

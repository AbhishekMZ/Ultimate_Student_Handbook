from src.app import db, app
from src.models.user import User
from src.models.course import Course
from src.models.enrollment import Enrollment
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if we already have users
        if User.query.first() is None:
            # Create a test admin user
            admin = User(
                name='Admin User',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )

            # Create some test students
            students = [
                User(
                    name='John Doe',
                    email='john@example.com',
                    password=generate_password_hash('student123'),
                    role='student'
                ),
                User(
                    name='Jane Smith',
                    email='jane@example.com',
                    password=generate_password_hash('student123'),
                    role='student'
                )
            ]

            # Add users to database
            db.session.add(admin)
            for student in students:
                db.session.add(student)

            # Create some test courses
            courses = [
                Course(
                    name='Python Programming',
                    code='CS101',
                    description='Introduction to Python programming language'
                ),
                Course(
                    name='Web Development',
                    code='CS102',
                    description='Learn web development with HTML, CSS, and JavaScript'
                )
            ]

            # Add courses to database
            for course in courses:
                db.session.add(course)

            # Commit the changes
            db.session.commit()

            # Create enrollments
            for student in students:
                for course in courses:
                    enrollment = Enrollment(
                        student_id=student.id,
                        course_id=course.id
                    )
                    db.session.add(enrollment)

            # Commit all changes
            db.session.commit()

if __name__ == '__main__':
    init_db()

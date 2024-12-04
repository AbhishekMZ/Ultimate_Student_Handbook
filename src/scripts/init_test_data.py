from src.app import app, db
from src.models.user import User
from werkzeug.security import generate_password_hash

def init_test_data():
    with app.app_context():
        # Create tables
        db.create_all()

        # Create test students
        students = [
            {
                'name': 'John Doe',
                'email': 'john.doe@rvce.edu.in',
                'password': generate_password_hash('student123'),
                'role': 'student',
                'student_id': '1RV20CS001'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane.smith@rvce.edu.in',
                'password': generate_password_hash('student123'),
                'role': 'student',
                'student_id': '1RV20CS002'
            }
        ]

        for student_data in students:
            student = User(**student_data)
            db.session.add(student)

        # Commit changes
        db.session.commit()
        print("Test data initialized successfully!")

if __name__ == '__main__':
    init_test_data()

from datetime import datetime
import re
import jwt
from passlib.hash import pbkdf2_sha256
from typing import Optional, Dict, Any
import sqlite3
from dataclasses import dataclass

@dataclass
class AuthResult:
    success: bool
    message: str
    user_data: Optional[Dict[str, Any]] = None
    token: Optional[str] = None

class AuthenticationManager:
    def __init__(self, db_path: str, secret_key: str):
        self.db_path = db_path
        self.secret_key = secret_key
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.student_id_pattern = re.compile(r'^1RV[0-9]{2}[A-Z]{2}[0-9]{3}$')

    def validate_email(self, email: str) -> bool:
        return bool(self.email_pattern.match(email))

    def validate_student_id(self, student_id: str) -> bool:
        return bool(self.student_id_pattern.match(student_id))

    def hash_password(self, password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def verify_password(self, password: str, hash: str) -> bool:
        return pbkdf2_sha256.verify(password, hash)

    def generate_token(self, user_data: Dict[str, Any]) -> str:
        payload = {
            **user_data,
            'exp': datetime.utcnow().timestamp() + 24 * 3600  # 24 hour expiry
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None

    def login(self, email: str, password: str) -> AuthResult:
        if not self.validate_email(email):
            return AuthResult(success=False, message="Invalid email format")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT StudentID, Name, Email, password_hash, profile_status
                FROM students
                WHERE Email = ?
            """, (email,))
            
            user_data = cursor.fetchone()
            
            if not user_data:
                return AuthResult(success=False, message="User not found")

            student_id, name, email, password_hash, status = user_data

            if not self.verify_password(password, password_hash):
                return AuthResult(success=False, message="Invalid password")

            if status != 'active':
                return AuthResult(success=False, message="Account is not active")

            # Update last login
            cursor.execute("""
                UPDATE students
                SET last_login = ?, updated_at = ?
                WHERE StudentID = ?
            """, (datetime.utcnow().isoformat(), datetime.utcnow().isoformat(), student_id))

            conn.commit()

            user_dict = {
                'student_id': student_id,
                'name': name,
                'email': email
            }

            token = self.generate_token(user_dict)

            return AuthResult(
                success=True,
                message="Login successful",
                user_data=user_dict,
                token=token
            )

        except sqlite3.Error as e:
            return AuthResult(success=False, message=f"Database error: {str(e)}")
        finally:
            conn.close()

    def register(self, student_data: Dict[str, Any], password: str) -> AuthResult:
        if not self.validate_student_id(student_data.get('student_id', '')):
            return AuthResult(success=False, message="Invalid student ID format")

        if not self.validate_email(student_data.get('email', '')):
            return AuthResult(success=False, message="Invalid email format")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if student already exists
            cursor.execute("""
                SELECT StudentID FROM students
                WHERE StudentID = ? OR Email = ?
            """, (student_data['student_id'], student_data['email']))

            if cursor.fetchone():
                return AuthResult(success=False, message="Student ID or email already exists")

            # Hash password
            password_hash = self.hash_password(password)

            # Insert new student
            now = datetime.utcnow().isoformat()
            cursor.execute("""
                INSERT INTO students (
                    StudentID, Name, Email, password_hash,
                    TenthMarks, TwelfthMarks, Semester,
                    profile_status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_data['student_id'],
                student_data['name'],
                student_data['email'],
                password_hash,
                student_data.get('tenth_marks', 0),
                student_data.get('twelfth_marks', 0),
                student_data.get('semester', 1),
                'active',
                now,
                now
            ))

            conn.commit()

            user_dict = {
                'student_id': student_data['student_id'],
                'name': student_data['name'],
                'email': student_data['email']
            }

            token = self.generate_token(user_dict)

            return AuthResult(
                success=True,
                message="Registration successful",
                user_data=user_dict,
                token=token
            )

        except sqlite3.Error as e:
            return AuthResult(success=False, message=f"Database error: {str(e)}")
        finally:
            conn.close()

    def logout(self, token: str) -> AuthResult:
        user_data = self.verify_token(token)
        if not user_data:
            return AuthResult(success=False, message="Invalid token")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Update last_login to mark logout time
            cursor.execute("""
                UPDATE students
                SET updated_at = ?
                WHERE StudentID = ?
            """, (datetime.utcnow().isoformat(), user_data['student_id']))

            conn.commit()
            return AuthResult(success=True, message="Logout successful")

        except sqlite3.Error as e:
            return AuthResult(success=False, message=f"Database error: {str(e)}")
        finally:
            conn.close()

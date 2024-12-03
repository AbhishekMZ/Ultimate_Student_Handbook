import sqlite3
import json
from datetime import datetime
import re
from ..database.database import DB_PATH
from .database_manager import DatabaseManager

class UserManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_manager = DatabaseManager()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        )
        return salt, hash_obj.hex()

    def _validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_password(self, password):
        # Password must be at least 8 characters long and contain:
        # - At least one uppercase letter
        # - At least one lowercase letter
        # - At least one number
        # - At least one special character
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def create_user(self, username, email, password, role_name, first_name, last_name, **profile_data):
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        
        if not self._validate_password(password):
            raise ValueError(
                "Password must be at least 8 characters long and contain: "
                "uppercase letter, lowercase letter, number, and special character"
            )

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Get role_id
            cursor.execute('SELECT role_id FROM roles WHERE role_name = ?', (role_name,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Invalid role: {role_name}")
            role_id = result[0]

            # Hash password
            salt, password_hash = self._hash_password(password)

            # Create user
            cursor.execute('''
            INSERT INTO users (username, email, password_hash, salt, role_id)
            VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, salt, role_id))
            
            user_id = cursor.lastrowid

            # Create user profile
            profile_fields = ['user_id', 'first_name', 'last_name']
            profile_values = [user_id, first_name, last_name]

            # Add additional profile data if provided
            for key, value in profile_data.items():
                profile_fields.append(key)
                profile_values.append(value)

            placeholders = ','.join(['?' for _ in profile_values])
            fields = ','.join(profile_fields)
            
            cursor.execute(f'''
            INSERT INTO user_profiles ({fields})
            VALUES ({placeholders})
            ''', profile_values)

            conn.commit()
            return user_id

        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                raise ValueError("Username already exists")
            if 'email' in str(e):
                raise ValueError("Email already exists")
            raise e
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
            SELECT user_id, password_hash, salt, is_active, email_verified
            FROM users
            WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            if not result:
                return None, "Invalid username"

            user_id, stored_hash, salt, is_active, email_verified = result

            if not is_active:
                return None, "Account is deactivated"

            if not email_verified:
                return None, "Email not verified"

            # Verify password
            _, password_hash = self._hash_password(password, salt)
            
            if password_hash != stored_hash:
                return None, "Invalid password"

            # Update last login
            cursor.execute('''
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE user_id = ?
            ''', (user_id,))

            conn.commit()
            return user_id, "Success"

        finally:
            conn.close()

    def get_user_profile(self, user_id):
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
            SELECT u.username, u.email, u.role_id, r.role_name,
                   p.first_name, p.last_name, p.phone_number,
                   p.date_of_birth, p.address, p.city, p.state,
                   p.country, p.profile_picture_url, p.bio,
                   p.department, p.position
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
            JOIN user_profiles p ON u.user_id = p.user_id
            WHERE u.user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if not result:
                return None

            return {
                'username': result[0],
                'email': result[1],
                'role': {
                    'id': result[2],
                    'name': result[3]
                },
                'profile': {
                    'first_name': result[4],
                    'last_name': result[5],
                    'phone_number': result[6],
                    'date_of_birth': result[7],
                    'address': result[8],
                    'city': result[9],
                    'state': result[10],
                    'country': result[11],
                    'profile_picture_url': result[12],
                    'bio': result[13],
                    'department': result[14],
                    'position': result[15]
                }
            }

        finally:
            conn.close()

    def update_profile(self, user_id, **profile_data):
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Build update query dynamically
            set_clause = ', '.join([f'{key} = ?' for key in profile_data.keys()])
            values = list(profile_data.values()) + [user_id]

            cursor.execute(f'''
            UPDATE user_profiles
            SET {set_clause}, last_updated = CURRENT_TIMESTAMP
            WHERE user_id = ?
            ''', values)

            conn.commit()
            return cursor.rowcount > 0

        finally:
            conn.close()

    def create_password_reset_token(self, email):
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Get user_id
            cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            if not result:
                return None

            user_id = result[0]
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)

            cursor.execute('''
            INSERT INTO password_reset_tokens (user_id, token, expires_at)
            VALUES (?, ?, ?)
            ''', (user_id, token, expires_at))

            conn.commit()
            return token

        finally:
            conn.close()

    def reset_password(self, token, new_password):
        if not self._validate_password(new_password):
            raise ValueError(
                "Password must be at least 8 characters long and contain: "
                "uppercase letter, lowercase letter, number, and special character"
            )

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Get token info
            cursor.execute('''
            SELECT user_id, expires_at, is_used
            FROM password_reset_tokens
            WHERE token = ?
            ''', (token,))
            
            result = cursor.fetchone()
            if not result:
                return False, "Invalid token"

            user_id, expires_at, is_used = result
            
            if is_used:
                return False, "Token already used"
                
            if datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S') < datetime.now():
                return False, "Token expired"

            # Update password
            salt, password_hash = self._hash_password(new_password)
            
            cursor.execute('''
            UPDATE users
            SET password_hash = ?, salt = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            ''', (password_hash, salt, user_id))

            # Mark token as used
            cursor.execute('''
            UPDATE password_reset_tokens
            SET is_used = true
            WHERE token = ?
            ''', (token,))

            conn.commit()
            return True, "Password reset successful"

        finally:
            conn.close()

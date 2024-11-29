import sqlite3
import hashlib
import secrets
from datetime import datetime

def create_user_database():
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Create Roles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT UNIQUE NOT NULL,
        description TEXT,
        permissions TEXT
    )
    ''')

    # Create Users table with authentication info
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role_id INTEGER,
        is_active BOOLEAN DEFAULT true,
        email_verified BOOLEAN DEFAULT false,
        last_login DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (role_id) REFERENCES roles(role_id)
    )
    ''')

    # Create UserProfiles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT,
        date_of_birth DATE,
        address TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        profile_picture_url TEXT,
        bio TEXT,
        department TEXT,
        position TEXT,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')

    # Create PasswordResetTokens table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS password_reset_tokens (
        token_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        token TEXT UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        expires_at DATETIME NOT NULL,
        is_used BOOLEAN DEFAULT false,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')

    # Create LoginHistory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        login_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        ip_address TEXT,
        user_agent TEXT,
        success BOOLEAN,
        failure_reason TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')

    # Insert default roles
    default_roles = [
        ('admin', 'System Administrator', 'all_permissions'),
        ('teacher', 'Teacher/Faculty', 'view,edit,create_assignments,grade'),
        ('student', 'Student', 'view,submit_assignments'),
        ('parent', 'Parent/Guardian', 'view_only'),
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO roles (role_name, description, permissions)
    VALUES (?, ?, ?)
    ''', default_roles)

    # Create helper functions for user management
    def hash_password(password, salt=None):
        if salt is None:
            salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode(), 
            salt.encode(), 
            100000  # Number of iterations
        )
        return salt, hash_obj.hex()

    def create_user(username, email, password, role_name, first_name, last_name):
        # Get role_id
        cursor.execute('SELECT role_id FROM roles WHERE role_name = ?', (role_name,))
        role_id = cursor.fetchone()[0]

        # Hash password
        salt, password_hash = hash_password(password)

        # Create user
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, salt, role_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, salt, role_id))
        
        user_id = cursor.lastrowid

        # Create user profile
        cursor.execute('''
        INSERT INTO user_profiles (user_id, first_name, last_name)
        VALUES (?, ?, ?)
        ''', (user_id, first_name, last_name))

        return user_id

    # Create sample admin user
    try:
        create_user(
            username='admin',
            email='admin@school.edu',
            password='admin123',  # This should be changed immediately in production
            role_name='admin',
            first_name='Admin',
            last_name='User'
        )
    except sqlite3.IntegrityError:
        print("Admin user already exists")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_user_database()
    print("User database created successfully with default roles and admin user")

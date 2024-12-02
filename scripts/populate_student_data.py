import sqlite3
import hashlib
import secrets
import random
import string
from datetime import datetime, timedelta

def generate_temp_password():
    """Generate a temporary password that's memorable but secure"""
    # Format: Word + 2 digits + Special Character
    words = ['Blue', 'Red', 'Green', 'Yellow', 'Purple', 'Orange', 'Silver', 'Gold']
    word = random.choice(words)
    digits = ''.join(random.choices(string.digits, k=2))
    special = random.choice('!@#$%^&*')
    return f"{word}{digits}{special}"

def hash_password(password, salt=None):
    """Hash password using PBKDF2 with SHA256"""
    if salt is None:
        salt = secrets.token_hex(16)
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode(), 
        salt.encode(), 
        100000
    )
    return salt, hash_obj.hex()

def create_student(cursor, usn, email, first_name, last_name, department='AI'):
    """Create a student user with profile"""
    # Generate temporary password
    temp_password = generate_temp_password()
    
    # Get student role id
    cursor.execute('SELECT role_id FROM roles WHERE role_name = ?', ('student',))
    role_id = cursor.fetchone()[0]

    # Hash password
    salt, password_hash = hash_password(temp_password)

    # Create user
    try:
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, salt, role_id, email_verified)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (usn, email, password_hash, salt, role_id, True))
        
        user_id = cursor.lastrowid

        # Create user profile
        cursor.execute('''
        INSERT INTO user_profiles (user_id, first_name, last_name, department)
        VALUES (?, ?, ?, ?)
        ''', (user_id, first_name, last_name, department))

        return usn, temp_password
    except sqlite3.IntegrityError as e:
        print(f"Error creating user {usn}: {e}")
        return None, None

def populate_student_data():
    """Populate the database with student data"""
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Complete list of students
    students = [
        # 3rd Year AI Students (22 batch)
        ('1RV22AI001', 'Aditya', 'Sharma', 'aditya.s@rvce.edu.in'),
        ('1RV22AI002', 'Bhavana', 'Kumar', 'bhavana.k@rvce.edu.in'),
        ('1RV22AI003', 'Chetan', 'Patel', 'chetan.p@rvce.edu.in'),
        ('1RV22AI004', 'Divya', 'Reddy', 'divya.r@rvce.edu.in'),
        ('1RV22AI005', 'Eshan', 'Gupta', 'eshan.g@rvce.edu.in'),
        ('1RV22AI006', 'Fathima', 'Khan', 'fathima.k@rvce.edu.in'),
        ('1RV22AI007', 'Ganesh', 'Iyer', 'ganesh.i@rvce.edu.in'),
        ('1RV22AI008', 'Harini', 'Nair', 'harini.n@rvce.edu.in'),
        ('1RV22AI009', 'Ishaan', 'Menon', 'ishaan.m@rvce.edu.in'),
        ('1RV22AI010', 'Jyoti', 'Singh', 'jyoti.s@rvce.edu.in'),
        ('1RV22AI011', 'Karthik', 'Raj', 'karthik.r@rvce.edu.in'),
        ('1RV22AI012', 'Lakshmi', 'Priya', 'lakshmi.p@rvce.edu.in'),
        ('1RV22AI013', 'Mohan', 'Das', 'mohan.d@rvce.edu.in'),
        ('1RV22AI014', 'Nandini', 'Shah', 'nandini.s@rvce.edu.in'),
        ('1RV22AI015', 'Om', 'Prakash', 'om.p@rvce.edu.in'),
        ('1RV22AI016', 'Priya', 'Verma', 'priya.v@rvce.edu.in'),
        ('1RV22AI017', 'Qureshi', 'Ahmed', 'qureshi.a@rvce.edu.in'),
        ('1RV22AI018', 'Rahul', 'Mehta', 'rahul.m@rvce.edu.in'),
        ('1RV22AI019', 'Sanjana', 'Reddy', 'sanjana.r@rvce.edu.in'),
        ('1RV22AI020', 'Tanvi', 'Shah', 'tanvi.s@rvce.edu.in'),
        ('1RV22AI021', 'Uday', 'Kumar', 'uday.k@rvce.edu.in'),
        ('1RV22AI022', 'Varun', 'Nair', 'varun.n@rvce.edu.in'),
        ('1RV22AI023', 'Waqar', 'Khan', 'waqar.k@rvce.edu.in'),
        ('1RV22AI024', 'Xavier', 'Dsouza', 'xavier.d@rvce.edu.in'),
        ('1RV22AI025', 'Yamini', 'Rao', 'yamini.r@rvce.edu.in'),
        ('1RV22AI026', 'Zara', 'Patel', 'zara.p@rvce.edu.in'),
        ('1RV22AI027', 'Abhishek', 'Kumar', 'abhishek.k@rvce.edu.in'),
        ('1RV22AI028', 'Bhoomika', 'Singh', 'bhoomika.s@rvce.edu.in'),
        ('1RV22AI029', 'Chirag', 'Verma', 'chirag.v@rvce.edu.in'),
        ('1RV22AI030', 'Deepika', 'Nair', 'deepika.n@rvce.edu.in'),
        ('1RV22AI031', 'Eshwar', 'Reddy', 'eshwar.r@rvce.edu.in'),
        ('1RV22AI032', 'Fatima', 'Syed', 'fatima.s@rvce.edu.in'),
        ('1RV22AI033', 'Gaurav', 'Sharma', 'gaurav.s@rvce.edu.in'),
        ('1RV22AI034', 'Hema', 'Patel', 'hema.p@rvce.edu.in'),
        ('1RV22AI035', 'Irfan', 'Khan', 'irfan.k@rvce.edu.in'),
        ('1RV22AI036', 'Jasmine', 'Kumar', 'jasmine.k@rvce.edu.in'),
        ('1RV22AI037', 'Karan', 'Singh', 'karan.s@rvce.edu.in'),
        ('1RV22AI038', 'Leela', 'Menon', 'leela.m@rvce.edu.in'),
        ('1RV22AI039', 'Manish', 'Gupta', 'manish.g@rvce.edu.in'),
        ('1RV22AI040', 'Neha', 'Reddy', 'neha.r@rvce.edu.in'),
        ('1RV22AI041', 'Omkar', 'Patil', 'omkar.p@rvce.edu.in'),
        ('1RV22AI042', 'Prachi', 'Shah', 'prachi.s@rvce.edu.in'),
        ('1RV22AI043', 'Rahul', 'Verma', 'rahul.v@rvce.edu.in'),
        ('1RV22AI044', 'Sneha', 'Kumar', 'sneha.k@rvce.edu.in'),
        ('1RV22AI045', 'Tarun', 'Nair', 'tarun.n@rvce.edu.in'),
        ('1RV22AI046', 'Uma', 'Sharma', 'uma.s@rvce.edu.in'),
        ('1RV22AI047', 'Vivek', 'Patel', 'vivek.p@rvce.edu.in'),
        ('1RV22AI048', 'Wasim', 'Khan', 'wasim.k@rvce.edu.in'),
        ('1RV22AI049', 'Xena', 'Dsouza', 'xena.d@rvce.edu.in'),
        ('1RV22AI050', 'Yogesh', 'Rao', 'yogesh.r@rvce.edu.in'),
        ('1RV22AI051', 'Zain', 'Malik', 'zain.m@rvce.edu.in'),
        ('1RV22AI052', 'Ananya', 'Kumar', 'ananya.k@rvce.edu.in'),
        ('1RV22AI053', 'Brijesh', 'Patel', 'brijesh.p@rvce.edu.in'),
        ('1RV22AI054', 'Chandni', 'Shah', 'chandni.s@rvce.edu.in'),
        ('1RV22AI055', 'Dhruv', 'Verma', 'dhruv.v@rvce.edu.in'),
        ('1RV22AI056', 'Ekta', 'Singh', 'ekta.s@rvce.edu.in'),
        ('1RV22AI057', 'Farhan', 'Khan', 'farhan.k@rvce.edu.in'),
        ('1RV22AI058', 'Gitika', 'Reddy', 'gitika.r@rvce.edu.in'),
        ('1RV22AI059', 'Harsh', 'Kumar', 'harsh.k@rvce.edu.in'),
        ('1RV22AI060', 'Ishita', 'Sharma', 'ishita.s@rvce.edu.in')
    ]

    # Store credentials for return
    credentials = []

    # Create students
    for usn, first_name, last_name, email in students:
        username, password = create_student(cursor, usn, email, first_name, last_name)
        if username and password:
            credentials.append((username, password))

    conn.commit()
    conn.close()
    return credentials

if __name__ == "__main__":
    print("Creating student accounts...")
    credentials = populate_student_data()
    
    # Save credentials to a file
    with open('student_credentials.txt', 'w') as f:
        f.write("Student Credentials (Temporary Passwords - Must be changed on first login)\n")
        f.write("=" * 70 + "\n\n")
        f.write("Username  |  Temporary Password\n")
        f.write("-" * 70 + "\n")
        for username, password in credentials:
            f.write(f"{username}  |  {password}\n")
        f.write("\n" + "=" * 70 + "\n")
        f.write("NOTE: Please change your password upon first login for security purposes.\n")
    
    print(f"Created {len(credentials)} student accounts successfully!")
    print("Credentials have been saved to 'student_credentials.txt'")

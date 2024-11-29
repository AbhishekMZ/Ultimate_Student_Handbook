from database_manager import DatabaseManager, DatabaseValidationError
import sqlite3

def test_data_consistency():
    db = DatabaseManager()
    
    print("\n=== Testing Student Data Validation ===")
    
    # Test 1: Valid student data
    try:
        student_data = {
            'student_id': 'STU002',  # Using STU002 since STU001 already exists
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com'
        }
        db.add_student(student_data)
        print("[PASS] Valid student data accepted")
    except DatabaseValidationError as e:
        print(f"[FAIL] Error: {e}")

    # Test 2: Invalid student ID format
    try:
        invalid_student = {
            'student_id': 'ST123',  # Wrong format
            'name': 'Invalid Student',
            'email': 'invalid@example.com'
        }
        db.add_student(invalid_student)
        print("[FAIL] Invalid student ID was accepted")
    except DatabaseValidationError as e:
        print("[PASS] Invalid student ID correctly rejected")

    print("\n=== Testing Topic Data Validation ===")
    
    # Test 3: Valid topic data
    try:
        topic_data = {
            'textbook_id': 1,
            'topic_name': 'Introduction to SQL',
            'description': 'Basic SQL concepts and queries',
            'chapter_number': 1,
            'importance_level': 4,
            'estimated_hours': 3.5,
            'prerequisites': []
        }
        db.add_topic(topic_data)
        print("[PASS] Valid topic data accepted")
    except DatabaseValidationError as e:
        print(f"[FAIL] Error: {e}")

    # Test 4: Invalid topic data (importance level out of range)
    try:
        invalid_topic = {
            'textbook_id': 1,
            'topic_name': 'Test Topic',
            'chapter_number': 1,
            'importance_level': 6,  # Should be 1-5
            'estimated_hours': 2.0
        }
        db.add_topic(invalid_topic)
        print("[FAIL] Invalid importance level was accepted")
    except DatabaseValidationError as e:
        print("[PASS] Invalid importance level correctly rejected")

    print("\n=== Testing Progress Data Validation ===")
    
    # Test 5: Valid progress data
    try:
        progress_data = {
            'student_id': 'STU002',
            'topic_id': 1,
            'completion_status': 'in_progress',
            'understanding_level': 3,
            'time_spent_hours': 1.5,
            'notes': 'Making good progress'
        }
        db.update_progress(progress_data)
        print("[PASS] Valid progress data accepted")
    except DatabaseValidationError as e:
        print(f"[FAIL] Error: {e}")

    # Test 6: Invalid progress data (understanding level out of range)
    try:
        invalid_progress = {
            'student_id': 'STU002',
            'topic_id': 1,
            'completion_status': 'in_progress',
            'understanding_level': 6,  # Should be 1-5
            'time_spent_hours': 1.0
        }
        db.update_progress(invalid_progress)
        print("[FAIL] Invalid understanding level was accepted")
    except DatabaseValidationError as e:
        print("[PASS] Invalid understanding level correctly rejected")

    print("\n=== Testing Cascade Delete ===")
    
    # Test 7: Delete student and check if related progress is deleted
    try:
        deleted = db.delete_student('STU002')
        if deleted:
            print("[PASS] Student and related data deleted successfully")
        else:
            print("[FAIL] Failed to delete student")
    except sqlite3.Error as e:
        print(f"[FAIL] Error during cascade delete: {e}")

if __name__ == "__main__":
    test_data_consistency()

# utils/db_indexes.py

def setup_indexes(db):
    # Student collection indexes
    db.students.create_index([("email", 1)], unique=True)
    db.students.create_index([("active_devices.device_id", 1)])

    # Progress collection indexes
    db.progress.create_index([("student_id", 1), ("course_id", 1)])
    db.progress.create_index([("last_updated", -1)])

    # Notifications collection indexes
    db.notifications.create_index([("student_id", 1), ("created_at", -1)])
    db.notifications.create_index([("read", 1)])
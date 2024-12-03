# Schema Update Requirements

## 1. Student Profile Schema Updates
- Add `created_at` timestamp
- Add `updated_at` timestamp
- Add `last_login` timestamp
- Add `device_info` JSON field for sync tracking
- Standardize `strengths` and `weaknesses` format to use consistent separators
- Add `profile_status` field (active/inactive)

## 2. Exam Results Schema Updates
- Add `created_at` timestamp for result entry
- Add `updated_at` timestamp for any modifications
- Add `grading_scale` field
- Add `feedback` text field
- Add `verified_by` field for result verification
- Standardize `syllabus_covered` to decimal format

## 3. Course Management Updates
- Add `created_at` timestamp
- Add `updated_at` timestamp
- Add `active_status` field
- Add `prerequisites` array field
- Add `learning_outcomes` array field

## 4. Achievement Tracking Updates
New table required: `student_achievements`
```sql
CREATE TABLE student_achievements (
    id INTEGER PRIMARY KEY,
    student_id TEXT NOT NULL,
    achievement_type TEXT NOT NULL,
    achievement_name TEXT NOT NULL,
    description TEXT,
    date_achieved TIMESTAMP NOT NULL,
    verified_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(StudentID)
);
```

## 5. Notification System Updates
New table required: `notifications`
```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    student_id TEXT NOT NULL,
    notification_type TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    read_status BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(StudentID)
);
```

## 6. Device Sync Information
New table required: `device_sync_logs`
```sql
CREATE TABLE device_sync_logs (
    id INTEGER PRIMARY KEY,
    student_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    device_type TEXT NOT NULL,
    last_sync_time TIMESTAMP NOT NULL,
    sync_status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(StudentID)
);
```

## Implementation Steps:

1. Backup existing data
2. Create new tables
3. Alter existing tables to add new fields
4. Migrate existing data with default values for new fields
5. Update application code to handle new fields
6. Update CSV import/export scripts to include new fields

## Data Validation Rules:

1. Email format: username@domain.tld
2. Percentage fields: Decimal between 0 and 100
3. Timestamps: ISO 8601 format
4. Student ID: Must match pattern 1RV[0-9]{2}[A-Z]{2}[0-9]{3}
5. Course codes: Must match pattern [A-Z]{2}[0-9]{3}[A-Z]{2}

## Security Considerations:

1. Encrypt sensitive student data
2. Hash passwords using PBKDF2-SHA256
3. Implement role-based access control
4. Log all data modifications
5. Regular backup schedule

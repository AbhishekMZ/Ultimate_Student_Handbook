# Student Tracking System - Schema and Dataflow Information

## 1. Core Entities and Their Relationships

### Students (Central Entity)
- Primary Key: StudentID (Format: 1RV[YY][DEPT][###])
- Personal Information:
  * Name
  * Email
  * Academic History (10th, 12th marks)
  * Current Semester
  * Enrolled Courses
  * Strengths/Weaknesses (JSON format)
- Tracking Fields:
  * Profile Status
  * Last Login
  * Device Info
  * Created/Updated Timestamps

### Academic Performance
#### Exam Results
- Links to: Students (StudentID)
- Key Components:
  * Course Code
  * Test Number
  * Test Date
  * Syllabus Coverage
  * Marks (Obtained/Maximum)
  * Grading Scale
  * Verification Status
  * Feedback
- Tracking: Created/Updated Timestamps

### Course Management
#### Courses
- Primary Key: CourseCode
- Core Information:
  * Course Name
  * Credits
  * Department
  * Prerequisites (JSON)
  * Learning Outcomes
- Status:
  * Active Status
  * Created/Updated Timestamps

### Achievement System
#### Student Achievements
- Links to: Students (StudentID)
- Components:
  * Achievement Type
  * Achievement Name
  * Description
  * Date Achieved
  * Verification Status
  * Created/Updated Timestamps

### Notification System
#### Notifications
- Links to: Students (StudentID)
- Message Details:
  * Type
  * Title
  * Message Content
  * Read Status
  * Created/Read Timestamps

### Device Synchronization
#### Device Sync Logs
- Links to: Students (StudentID)
- Tracking:
  * Device ID
  * Device Type
  * Last Sync Time
  * Sync Status
  * Created Timestamp

## 2. Data Flow Patterns

### Input Flows
1. Student Registration
   - Personal Information Entry
   - Course Enrollment
   - Device Registration

2. Academic Updates
   - Exam Result Entry
   - Course Progress Updates
   - Achievement Recording

3. System Events
   - Login/Logout Events
   - Device Sync Events
   - Notification Triggers

### Output Flows
1. Student Analytics
   - Performance Reports
   - Progress Tracking
   - Achievement Summaries

2. Notifications
   - Academic Updates
   - Achievement Alerts
   - System Notifications

3. Sync Operations
   - Device Data Synchronization
   - Profile Updates
   - Course Material Access

## 3. Key Processing Points

### Authentication & Authorization
- Student Login Validation
- Profile Status Checks
- Device Authentication

### Academic Processing
- Grade Calculations
- Progress Tracking
- Performance Analytics

### Notification Processing
- Event Detection
- Notification Generation
- Delivery Status Tracking

### Synchronization
- Data Consistency Checks
- Conflict Resolution
- Update Propagation

## 4. Data Validation Rules

### Student Data
- Email Format: username@domain.tld
- StudentID Pattern: 1RV[0-9]{2}[A-Z]{2}[0-9]{3}
- Marks Range: 0-100

### Course Data
- CourseCode Pattern: [A-Z]{2}[0-9]{3}[A-Z]{2}
- Credits Range: 1-5
- Valid Prerequisites

### Achievement Data
- Valid Achievement Types
- Verification Requirements
- Date Constraints

## 5. Security Considerations

### Data Protection
- Encrypted Personal Information
- Secure Password Storage (PBKDF2-SHA256)
- Access Control Lists

### Audit Trail
- Transaction Logging
- Change History
- User Activity Tracking

### Compliance
- Data Retention Policies
- Privacy Requirements
- Academic Standards

## 6. Integration Points

### External Systems
- Email Service Integration
- Learning Management System
- Authentication Services

### API Endpoints
- Student Data Access
- Course Management
- Performance Analytics

### Backup Systems
- Regular Data Backups
- Recovery Procedures
- Archive Management

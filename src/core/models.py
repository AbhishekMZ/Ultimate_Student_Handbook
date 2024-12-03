from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Numeric, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    student_id = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    extra_data = Column(JSON)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(String(36), primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    extra_data = Column(JSON)

class CourseEnrollment(Base):
    __tablename__ = 'course_enrollments'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    course_id = Column(String(36), ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(DateTime, server_default=func.now())
    status = Column(String(20), nullable=False)
    completion_date = Column(DateTime)
    extra_data = Column(JSON)

class PerformanceRecord(Base):
    __tablename__ = 'performance_records'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    course_id = Column(String(36), ForeignKey('courses.id'), nullable=False)
    record_type = Column(String(50), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    extra_data = Column(JSON)

class PerformanceMetric(Base):
    __tablename__ = 'performance_metrics'

    id = Column(String(36), primary_key=True)
    record_id = Column(String(36), ForeignKey('performance_records.id'), nullable=False)
    metric_name = Column(String(50), nullable=False)
    metric_value = Column(Numeric(10, 2), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    extra_data = Column(JSON)

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    read_at = Column(DateTime)
    extra_data = Column(JSON)

class DeviceSync(Base):
    __tablename__ = 'device_syncs'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    device_id = Column(String(255), nullable=False)
    last_sync = Column(DateTime)
    sync_status = Column(String(20), nullable=False)
    data_hash = Column(String(64))
    created_at = Column(DateTime, server_default=func.now())
    extra_data = Column(JSON)

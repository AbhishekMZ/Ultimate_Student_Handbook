"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2023-11-08 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    # Drop existing tables if they exist
    if 'device_syncs' in tables:
        op.drop_table('device_syncs')
    if 'notifications' in tables:
        op.drop_table('notifications')
    if 'performance_metrics' in tables:
        op.drop_table('performance_metrics')
    if 'performance_records' in tables:
        op.drop_table('performance_records')
    if 'course_enrollments' in tables:
        op.drop_table('course_enrollments')
    if 'courses' in tables:
        op.drop_table('courses')
    if 'users' in tables:
        op.drop_table('users')

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('student_id', sa.String(50), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.TIMESTAMP),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('extra_data', sqlite.JSON),
        sa.CheckConstraint("role IN ('student', 'teacher', 'admin')", name='valid_role')
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_student_id', 'users', ['student_id'])

    # Create courses table
    op.create_table('courses',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(20), unique=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('credits', sa.Integer, nullable=False),
        sa.Column('semester', sa.Integer, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('extra_data', sqlite.JSON)
    )
    op.create_index('idx_courses_code', 'courses', ['code'])

    # Create course_enrollments table
    op.create_table('course_enrollments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('course_id', sa.String(36), nullable=False),
        sa.Column('enrollment_date', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('completion_date', sa.TIMESTAMP),
        sa.Column('extra_data', sqlite.JSON),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.CheckConstraint("status IN ('enrolled', 'completed', 'dropped', 'pending')", name='valid_status')
    )
    op.create_index('idx_enrollments_user', 'course_enrollments', ['user_id'])
    op.create_index('idx_enrollments_course', 'course_enrollments', ['course_id'])

    # Create performance_records table
    op.create_table('performance_records',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('course_id', sa.String(36), nullable=False),
        sa.Column('record_type', sa.String(50), nullable=False),
        sa.Column('value', sa.Numeric(10, 2), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('extra_data', sqlite.JSON),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'])
    )
    op.create_index('idx_performance_user', 'performance_records', ['user_id'])
    op.create_index('idx_performance_course', 'performance_records', ['course_id'])
    op.create_index('idx_performance_type', 'performance_records', ['record_type'])

    # Create performance_metrics table
    op.create_table('performance_metrics',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('record_id', sa.String(36), nullable=False),
        sa.Column('metric_name', sa.String(50), nullable=False),
        sa.Column('metric_value', sa.Numeric(10, 2), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('extra_data', sqlite.JSON),
        sa.ForeignKeyConstraint(['record_id'], ['performance_records.id'])
    )
    op.create_index('idx_metrics_record', 'performance_metrics', ['record_id'])
    op.create_index('idx_metrics_name', 'performance_metrics', ['metric_name'])

    # Create notifications table
    op.create_table('notifications',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('read', sa.Boolean, default=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('read_at', sa.TIMESTAMP),
        sa.Column('extra_data', sqlite.JSON),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )
    op.create_index('idx_notifications_user', 'notifications', ['user_id'])
    op.create_index('idx_notifications_type', 'notifications', ['type'])

    # Create device_syncs table
    op.create_table('device_syncs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('device_id', sa.String(255), nullable=False),
        sa.Column('last_sync', sa.TIMESTAMP),
        sa.Column('sync_status', sa.String(20), nullable=False),
        sa.Column('data_hash', sa.String(64)),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('extra_data', sqlite.JSON),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )
    op.create_index('idx_device_syncs_user', 'device_syncs', ['user_id'])
    op.create_index('idx_device_syncs_device', 'device_syncs', ['device_id'])

def downgrade() -> None:
    op.drop_table('device_syncs')
    op.drop_table('notifications')
    op.drop_table('performance_metrics')
    op.drop_table('performance_records')
    op.drop_table('course_enrollments')
    op.drop_table('courses')
    op.drop_table('users')

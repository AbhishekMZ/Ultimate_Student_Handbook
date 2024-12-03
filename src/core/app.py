from typing import Dict, Optional, Any
import os
from datetime import datetime
import json

from .auth import AuthenticationManager, AuthResult
from .analytics import PerformanceAnalytics, PerformanceMetrics, CourseProgress
from .notifications import NotificationManager, NotificationType
from .sync import DeviceSyncManager, SyncStatus, DeviceInfo, SyncResult

class StudentTrackingSystem:
    def __init__(self, db_path: str, secret_key: str):
        """Initialize the Student Tracking System with all core components."""
        self.db_path = db_path
        self.auth_manager = AuthenticationManager(db_path, secret_key)
        self.analytics = PerformanceAnalytics(db_path)
        self.notifications = NotificationManager(db_path)
        self.sync_manager = DeviceSyncManager(db_path)

    def register_student(
        self,
        student_data: Dict[str, Any],
        password: str,
        device_id: Optional[str] = None
    ) -> AuthResult:
        """Register a new student with optional device registration."""
        # Register student
        auth_result = self.auth_manager.register(student_data, password)
        
        if not auth_result.success:
            return auth_result

        # Register device if provided
        if device_id:
            device_type = student_data.get('device_type', 'unknown')
            self.sync_manager.register_device(
                student_data['student_id'],
                device_id,
                device_type
            )

        # Create welcome notification
        self.notifications.create_system_notification(
            student_data['student_id'],
            "Welcome to Student Tracking System",
            "Welcome! Start tracking your academic journey with us."
        )

        return auth_result

    def login(
        self,
        email: str,
        password: str,
        device_id: Optional[str] = None
    ) -> AuthResult:
        """Login a student with optional device sync."""
        auth_result = self.auth_manager.login(email, password)
        
        if not auth_result.success:
            return auth_result

        if device_id and auth_result.user_data:
            # Update device sync status
            self.sync_manager.update_sync_status(
                auth_result.user_data['student_id'],
                device_id,
                SyncStatus.SUCCESS
            )

        return auth_result

    def get_student_dashboard(
        self,
        student_id: str,
        include_notifications: bool = True
    ) -> Dict[str, Any]:
        """Get comprehensive student dashboard data."""
        dashboard = {
            'performance': None,
            'notifications': [],
            'sync_status': None,
            'last_login': None
        }

        # Get performance metrics
        performance = self.analytics.get_student_performance(student_id)
        if performance:
            dashboard['performance'] = {
                'average_score': performance.average_score,
                'completion_rate': performance.completion_rate,
                'strength_areas': performance.strength_areas,
                'weak_areas': performance.weak_areas,
                'improvement_rate': performance.improvement_rate,
                'recommendations': performance.recommendations
            }

        # Get recent notifications
        if include_notifications:
            notifications = self.notifications.get_notifications(
                student_id,
                unread_only=True,
                limit=5
            )
            dashboard['notifications'] = [
                {
                    'title': n.title,
                    'message': n.message,
                    'type': n.type.value,
                    'created_at': n.created_at.isoformat()
                }
                for n in notifications
            ]

        return dashboard

    def track_achievement(
        self,
        student_id: str,
        achievement_data: Dict[str, Any]
    ) -> bool:
        """Track a new student achievement and create notification."""
        try:
            # Create achievement notification
            self.notifications.create_achievement_notification(
                student_id,
                achievement_data['name'],
                achievement_data['description']
            )

            # Update analytics if needed
            if achievement_data.get('affects_performance', False):
                # Additional analytics processing could be added here
                pass

            return True
        except Exception as e:
            print(f"Error tracking achievement: {str(e)}")
            return False

    def sync_device_data(
        self,
        student_id: str,
        device_id: str,
        sync_data: Dict[str, Any]
    ) -> SyncResult:
        """Synchronize device data and update relevant components."""
        # Get current device info
        device_info = self.sync_manager.get_device_info(student_id, device_id)
        
        if not device_info:
            return SyncResult(
                success=False,
                message="Device not registered",
                status=SyncStatus.FAILED,
                timestamp=datetime.utcnow()
            )

        # Update sync status
        sync_result = self.sync_manager.update_sync_status(
            student_id,
            device_id,
            SyncStatus.SUCCESS,
            sync_data
        )

        if sync_result.success:
            # Create sync notification if needed
            if sync_data.get('notify_sync', False):
                self.notifications.create_system_notification(
                    student_id,
                    "Device Sync Complete",
                    f"Your device {device_id} has been synchronized successfully."
                )

        return sync_result

    def update_course_progress(
        self,
        student_id: str,
        course_code: str,
        progress_data: Dict[str, Any]
    ) -> Optional[CourseProgress]:
        """Update course progress and generate relevant notifications."""
        # Get current progress
        current_progress = self.analytics.get_course_progress(
            student_id,
            course_code
        )

        if not current_progress:
            return None

        # Create academic notification
        if progress_data.get('grade'):
            self.notifications.create_academic_notification(
                student_id,
                course_code,
                progress_data['grade'],
                "grade"
            )

        # Create reminder if deadline approaching
        if progress_data.get('upcoming_deadline'):
            self.notifications.create_reminder_notification(
                student_id,
                course_code,
                progress_data['deadline_date'],
                progress_data['task']
            )

        return current_progress

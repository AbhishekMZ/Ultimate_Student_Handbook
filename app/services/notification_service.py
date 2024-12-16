# app/services/notification_service.py
from fastapi import BackgroundTasks
from app.db.models.notification import Notification
from app.core.email import send_email

class NotificationService:
    async def create_notification(
        self,
        student_id: str,
        title: str,
        message: str,
        background_tasks: BackgroundTasks
    ):
        notification = Notification(
            student=student_id,
            title=title,
            message=message,
        )
        await notification.insert()
        # Fetch the student's email
        student = await Student.get(student_id)
        background_tasks.add_task(
            send_email,
            subject=title,
            message=message,
            to_email=student.email
        )
        return notification
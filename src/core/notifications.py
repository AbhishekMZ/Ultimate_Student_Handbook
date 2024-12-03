from datetime import datetime
from typing import List, Optional, Dict, Any
import sqlite3
from dataclasses import dataclass
from enum import Enum

class NotificationType(Enum):
    ACADEMIC = "academic"
    ACHIEVEMENT = "achievement"
    SYSTEM = "system"
    REMINDER = "reminder"
    ALERT = "alert"

@dataclass
class Notification:
    id: int
    student_id: str
    type: NotificationType
    title: str
    message: str
    read_status: bool
    created_at: datetime
    read_at: Optional[datetime] = None

class NotificationManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_notification(
        self,
        student_id: str,
        notification_type: NotificationType,
        title: str,
        message: str
    ) -> Optional[int]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO notifications (
                    student_id, notification_type, title,
                    message, read_status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                notification_type.value,
                title,
                message,
                False,
                datetime.utcnow().isoformat()
            ))

            notification_id = cursor.lastrowid
            conn.commit()
            return notification_id

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return None
        finally:
            conn.close()

    def get_notifications(
        self,
        student_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                SELECT id, notification_type, title, message,
                       read_status, created_at, read_at
                FROM notifications
                WHERE student_id = ?
            """

            if unread_only:
                query += " AND read_status = 0"

            query += " ORDER BY created_at DESC LIMIT ?"

            cursor.execute(query, (student_id, limit))
            rows = cursor.fetchall()

            notifications = []
            for row in rows:
                notifications.append(Notification(
                    id=row[0],
                    student_id=student_id,
                    type=NotificationType(row[1]),
                    title=row[2],
                    message=row[3],
                    read_status=bool(row[4]),
                    created_at=datetime.fromisoformat(row[5]),
                    read_at=datetime.fromisoformat(row[6]) if row[6] else None
                ))

            return notifications

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return []
        finally:
            conn.close()

    def mark_as_read(self, notification_id: int) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE notifications
                SET read_status = ?, read_at = ?
                WHERE id = ?
            """, (True, datetime.utcnow().isoformat(), notification_id))

            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return False
        finally:
            conn.close()

    def mark_all_as_read(self, student_id: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE notifications
                SET read_status = ?, read_at = ?
                WHERE student_id = ? AND read_status = 0
            """, (True, datetime.utcnow().isoformat(), student_id))

            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return False
        finally:
            conn.close()

    def delete_notification(self, notification_id: int) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM notifications
                WHERE id = ?
            """, (notification_id,))

            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return False
        finally:
            conn.close()

    def create_achievement_notification(
        self,
        student_id: str,
        achievement_name: str,
        description: str
    ) -> Optional[int]:
        title = f"New Achievement: {achievement_name}"
        message = f"Congratulations! {description}"
        return self.create_notification(
            student_id,
            NotificationType.ACHIEVEMENT,
            title,
            message
        )

    def create_academic_notification(
        self,
        student_id: str,
        course_code: str,
        grade: float,
        message_type: str = "grade"
    ) -> Optional[int]:
        if message_type == "grade":
            title = f"New Grade Posted: {course_code}"
            message = f"Your grade for {course_code} has been posted: {grade}%"
        else:
            title = f"Academic Update: {course_code}"
            message = f"There's an update in {course_code}: {grade}% completion"

        return self.create_notification(
            student_id,
            NotificationType.ACADEMIC,
            title,
            message
        )

    def create_reminder_notification(
        self,
        student_id: str,
        course_code: str,
        deadline: datetime,
        task: str
    ) -> Optional[int]:
        title = f"Upcoming Deadline: {course_code}"
        message = f"Reminder: {task} is due on {deadline.strftime('%Y-%m-%d')}"
        return self.create_notification(
            student_id,
            NotificationType.REMINDER,
            title,
            message
        )

    def create_system_notification(
        self,
        student_id: str,
        title: str,
        message: str
    ) -> Optional[int]:
        return self.create_notification(
            student_id,
            NotificationType.SYSTEM,
            title,
            message
        )

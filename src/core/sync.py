from datetime import datetime
from typing import Dict, List, Optional, Any
import sqlite3
from dataclasses import dataclass
import json
from enum import Enum

class SyncStatus(Enum):
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"
    CONFLICT = "conflict"

@dataclass
class DeviceInfo:
    device_id: str
    device_type: str
    last_sync_time: datetime
    sync_status: SyncStatus

@dataclass
class SyncResult:
    success: bool
    message: str
    status: SyncStatus
    timestamp: datetime

class DeviceSyncManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def register_device(
        self,
        student_id: str,
        device_id: str,
        device_type: str
    ) -> SyncResult:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if device already registered
            cursor.execute("""
                SELECT device_id FROM device_sync_logs
                WHERE student_id = ? AND device_id = ?
            """, (student_id, device_id))

            if cursor.fetchone():
                return SyncResult(
                    success=False,
                    message="Device already registered",
                    status=SyncStatus.FAILED,
                    timestamp=datetime.utcnow()
                )

            # Register new device
            now = datetime.utcnow()
            cursor.execute("""
                INSERT INTO device_sync_logs (
                    student_id, device_id, device_type,
                    last_sync_time, sync_status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                device_id,
                device_type,
                now.isoformat(),
                SyncStatus.SUCCESS.value,
                now.isoformat()
            ))

            conn.commit()
            return SyncResult(
                success=True,
                message="Device registered successfully",
                status=SyncStatus.SUCCESS,
                timestamp=now
            )

        except sqlite3.Error as e:
            return SyncResult(
                success=False,
                message=f"Database error: {str(e)}",
                status=SyncStatus.FAILED,
                timestamp=datetime.utcnow()
            )
        finally:
            conn.close()

    def get_device_info(
        self,
        student_id: str,
        device_id: str
    ) -> Optional[DeviceInfo]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT device_type, last_sync_time, sync_status
                FROM device_sync_logs
                WHERE student_id = ? AND device_id = ?
            """, (student_id, device_id))

            row = cursor.fetchone()
            if not row:
                return None

            return DeviceInfo(
                device_id=device_id,
                device_type=row[0],
                last_sync_time=datetime.fromisoformat(row[1]),
                sync_status=SyncStatus(row[2])
            )

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return None
        finally:
            conn.close()

    def update_sync_status(
        self,
        student_id: str,
        device_id: str,
        status: SyncStatus,
        sync_data: Optional[Dict[str, Any]] = None
    ) -> SyncResult:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            now = datetime.utcnow()

            # Update device sync status
            cursor.execute("""
                UPDATE device_sync_logs
                SET last_sync_time = ?,
                    sync_status = ?
                WHERE student_id = ? AND device_id = ?
            """, (
                now.isoformat(),
                status.value,
                student_id,
                device_id
            ))

            # Update student device info if sync data provided
            if sync_data:
                cursor.execute("""
                    UPDATE students
                    SET device_info = ?,
                        updated_at = ?
                    WHERE StudentID = ?
                """, (
                    json.dumps(sync_data),
                    now.isoformat(),
                    student_id
                ))

            conn.commit()
            return SyncResult(
                success=True,
                message="Sync status updated successfully",
                status=status,
                timestamp=now
            )

        except sqlite3.Error as e:
            return SyncResult(
                success=False,
                message=f"Database error: {str(e)}",
                status=SyncStatus.FAILED,
                timestamp=datetime.utcnow()
            )
        finally:
            conn.close()

    def resolve_conflict(
        self,
        student_id: str,
        device_id: str,
        resolution_data: Dict[str, Any]
    ) -> SyncResult:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            now = datetime.utcnow()

            # Update device sync status to resolved
            cursor.execute("""
                UPDATE device_sync_logs
                SET last_sync_time = ?,
                    sync_status = ?
                WHERE student_id = ? AND device_id = ?
            """, (
                now.isoformat(),
                SyncStatus.SUCCESS.value,
                student_id,
                device_id
            ))

            # Apply resolution data
            cursor.execute("""
                UPDATE students
                SET device_info = ?,
                    updated_at = ?
                WHERE StudentID = ?
            """, (
                json.dumps(resolution_data),
                now.isoformat(),
                student_id
            ))

            conn.commit()
            return SyncResult(
                success=True,
                message="Conflict resolved successfully",
                status=SyncStatus.SUCCESS,
                timestamp=now
            )

        except sqlite3.Error as e:
            return SyncResult(
                success=False,
                message=f"Database error: {str(e)}",
                status=SyncStatus.FAILED,
                timestamp=datetime.utcnow()
            )
        finally:
            conn.close()

    def get_sync_history(
        self,
        student_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT device_id, device_type, last_sync_time,
                       sync_status, created_at
                FROM device_sync_logs
                WHERE student_id = ?
                ORDER BY last_sync_time DESC
                LIMIT ?
            """, (student_id, limit))

            rows = cursor.fetchall()
            history = []

            for row in rows:
                history.append({
                    'device_id': row[0],
                    'device_type': row[1],
                    'last_sync_time': row[2],
                    'sync_status': row[3],
                    'created_at': row[4]
                })

            return history

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return []
        finally:
            conn.close()

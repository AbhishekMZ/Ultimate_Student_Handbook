from datetime import datetime, timedelta
from bson import ObjectId

class Achievement:
    ACHIEVEMENTS = {
        'COURSE_MASTER': {
            'name': 'Course Master',
            'description': 'Complete all tasks for a course',
            'icon': '📚',
            'points': 100,
            'requirement': 50  # tasks completed
        },
        'PERFECT_ATTENDANCE': {
            'name': 'Perfect Attendance',
            'description': 'Log in daily for a week',
            'icon': '🎯',
            'points': 50,
            'requirement': 7  # days
        },
        'NOTE_TAKER_NOVICE': {
            'name': 'Novice Note Taker',
            'description': 'Create 10 notes',
            'icon': '📝',
            'points': 30,
            'requirement': 10  # notes
        },
        'NOTE_TAKER_EXPERT': {
            'name': 'Expert Note Taker',
            'description': 'Create 50 notes',
            'icon': '📝',
            'points': 100,
            'requirement': 50  # notes
        },
        'TIME_MANAGER': {
            'name': 'Time Manager',
            'description': 'Complete 20 tasks before deadlines',
            'icon': '⏰',
            'points': 75,
            'requirement': 20  # on-time tasks
        }
    }

    def __init__(self, user_id, achievement_key, completed=False):
        achievement_data = self.ACHIEVEMENTS[achievement_key]
        self.user_id = user_id
        self.key = achievement_key
        self.name = achievement_data['name']
        self.description = achievement_data['description']
        self.icon = achievement_data['icon']
        self.points = achievement_data['points']
        self.requirement = achievement_data['requirement']
        self.completed = completed
        self.completed_at = None
        self.progress = 0

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "points": self.points,
            "requirement": self.requirement,
            "completed": self.completed,
            "completed_at": self.completed_at,
            "progress": self.progress
        }

class UserProgress:
    XP_REWARDS = {
        'create_note': 10,
        'complete_task': 20,
        'complete_on_time': 30,
        'daily_login': 5,
        'study_streak': 15
    }

    def __init__(self, user_id):
        self.user_id = user_id
        self.xp = 0
        self.level = 1
        self.achievements = self._initialize_achievements()
        self.daily_streak = 0
        self.last_login = None
        self.stats = {
            'total_notes': 0,
            'total_tasks_completed': 0,
            'tasks_completed_on_time': 0,
            'study_sessions': 0,
            'study_time': 0,  # in minutes
            'longest_study_streak': 0
        }
        self.last_activity = None
        self.study_streak_start = None

    def _initialize_achievements(self):
        return [Achievement(self.user_id, key) for key in Achievement.ACHIEVEMENTS]

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "xp": self.xp,
            "level": self.level,
            "achievements": [a.to_dict() for a in self.achievements],
            "daily_streak": self.daily_streak,
            "last_login": self.last_login,
            "stats": self.stats,
            "last_activity": self.last_activity,
            "study_streak_start": self.study_streak_start
        }

    @staticmethod
    def calculate_level(xp):
        # Enhanced level calculation with diminishing returns
        return max(1, int((xp ** 0.5) / 5))

    def add_xp(self, points):
        self.xp += points
        new_level = self.calculate_level(self.xp)
        if new_level > self.level:
            self.level = new_level
            return True
        return False

    def update_login_streak(self):
        now = datetime.now()
        if not self.last_login:
            self.daily_streak = 1
        else:
            days_diff = (now - self.last_login).days
            if days_diff == 1:
                self.daily_streak += 1
            elif days_diff > 1:
                self.daily_streak = 1
        self.last_login = now
        self.add_xp(self.XP_REWARDS['daily_login'])

    def record_activity(self, activity_type, additional_data=None):
        now = datetime.now()
        self.last_activity = now

        if activity_type in self.XP_REWARDS:
            self.add_xp(self.XP_REWARDS[activity_type])

        if activity_type == 'create_note':
            self.stats['total_notes'] += 1
        elif activity_type == 'complete_task':
            self.stats['total_tasks_completed'] += 1
            if additional_data and additional_data.get('on_time', False):
                self.stats['tasks_completed_on_time'] += 1
        elif activity_type == 'study_session':
            self.stats['study_sessions'] += 1
            if additional_data and 'duration' in additional_data:
                self.stats['study_time'] += additional_data['duration']
            
            if not self.study_streak_start:
                self.study_streak_start = now
            elif (now - self.study_streak_start).days > 1:
                self.study_streak_start = now

            streak_days = (now - self.study_streak_start).days + 1
            self.stats['longest_study_streak'] = max(
                self.stats['longest_study_streak'],
                streak_days
            )

class GamificationSystem:
    def __init__(self, db):
        self.db = db
        self.progress_collection = db.user_progress

    async def get_user_progress(self, user_id):
        progress_data = await self.progress_collection.find_one({"user_id": str(user_id)})
        if not progress_data:
            progress = UserProgress(user_id)
            await self.progress_collection.insert_one(progress.to_dict())
            return progress
        return UserProgress(**progress_data)

    async def update_user_progress(self, progress):
        await self.progress_collection.update_one(
            {"user_id": str(progress.user_id)},
            {"$set": progress.to_dict()},
            upsert=True
        )

    async def check_achievements(self, progress):
        updated = False
        stats = progress.stats

        for achievement in progress.achievements:
            if achievement.completed:
                continue

            if achievement.key == 'COURSE_MASTER':
                achievement.progress = min(100, (stats['total_tasks_completed'] / achievement.requirement) * 100)
                if stats['total_tasks_completed'] >= achievement.requirement:
                    updated = self._complete_achievement(achievement, progress)

            elif achievement.key == 'PERFECT_ATTENDANCE':
                achievement.progress = min(100, (progress.daily_streak / achievement.requirement) * 100)
                if progress.daily_streak >= achievement.requirement:
                    updated = self._complete_achievement(achievement, progress)

            elif achievement.key == 'NOTE_TAKER_NOVICE':
                achievement.progress = min(100, (stats['total_notes'] / achievement.requirement) * 100)
                if stats['total_notes'] >= achievement.requirement:
                    updated = self._complete_achievement(achievement, progress)

            elif achievement.key == 'NOTE_TAKER_EXPERT':
                achievement.progress = min(100, (stats['total_notes'] / achievement.requirement) * 100)
                if stats['total_notes'] >= achievement.requirement:
                    updated = self._complete_achievement(achievement, progress)

            elif achievement.key == 'TIME_MANAGER':
                achievement.progress = min(100, (stats['tasks_completed_on_time'] / achievement.requirement) * 100)
                if stats['tasks_completed_on_time'] >= achievement.requirement:
                    updated = self._complete_achievement(achievement, progress)

        if updated:
            await self.update_user_progress(progress)

    def _complete_achievement(self, achievement, progress):
        if not achievement.completed:
            achievement.completed = True
            achievement.completed_at = datetime.now()
            achievement.progress = 100
            progress.add_xp(achievement.points)
            return True
        return False

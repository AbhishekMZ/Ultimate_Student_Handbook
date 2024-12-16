from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional

class ChallengePeriod(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"

class ChallengeType(Enum):
    NOTE_CREATION = "note_creation"
    TASK_COMPLETION = "task_completion"
    STUDY_TIME = "study_time"
    LOGIN_STREAK = "login_streak"
    PERFECT_TASKS = "perfect_tasks"
    SKILL_IMPROVEMENT = "skill_improvement"

class ChallengeRequirement:
    def __init__(self, type: ChallengeType, target: int, current: int = 0):
        self.type = type
        self.target = target
        self.current = current

    def to_dict(self):
        return {
            "type": self.type.value,
            "target": self.target,
            "current": self.current
        }

    @staticmethod
    def from_dict(data: Dict):
        return ChallengeRequirement(
            type=ChallengeType(data["type"]),
            target=data["target"],
            current=data.get("current", 0)
        )

class Challenge:
    def __init__(
        self,
        title: str,
        description: str,
        period: ChallengePeriod,
        requirements: List[ChallengeRequirement],
        xp_reward: int,
        skill_rewards: Dict[str, int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        icon: str = "🎯"
    ):
        self.title = title
        self.description = description
        self.period = period
        self.requirements = requirements
        self.xp_reward = xp_reward
        self.skill_rewards = skill_rewards or {}
        self.start_date = start_date or datetime.now()
        self.end_date = end_date
        self.icon = icon

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "period": self.period.value,
            "requirements": [req.to_dict() for req in self.requirements],
            "xp_reward": self.xp_reward,
            "skill_rewards": self.skill_rewards,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "icon": self.icon
        }

    @staticmethod
    def from_dict(data: Dict):
        return Challenge(
            title=data["title"],
            description=data["description"],
            period=ChallengePeriod(data["period"]),
            requirements=[ChallengeRequirement.from_dict(req) for req in data["requirements"]],
            xp_reward=data["xp_reward"],
            skill_rewards=data.get("skill_rewards", {}),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            icon=data.get("icon", "🎯")
        )

class UserChallenge:
    def __init__(
        self,
        user_id: str,
        challenge: Challenge,
        accepted_at: datetime = None,
        completed_at: Optional[datetime] = None,
        progress: Dict[str, int] = None
    ):
        self.user_id = user_id
        self.challenge = challenge
        self.accepted_at = accepted_at or datetime.now()
        self.completed_at = completed_at
        self.progress = progress or {req.type.value: 0 for req in challenge.requirements}

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "challenge": self.challenge.to_dict(),
            "accepted_at": self.accepted_at,
            "completed_at": self.completed_at,
            "progress": self.progress
        }

    @staticmethod
    def from_dict(data: Dict):
        return UserChallenge(
            user_id=data["user_id"],
            challenge=Challenge.from_dict(data["challenge"]),
            accepted_at=data.get("accepted_at"),
            completed_at=data.get("completed_at"),
            progress=data.get("progress", {})
        )

class ChallengeSystem:
    def __init__(self, db):
        self.db = db
        self.challenges_collection = db.challenges
        self.user_challenges_collection = db.user_challenges

    def _create_daily_challenges(self) -> List[Challenge]:
        return [
            Challenge(
                title="Note-Taking Sprint",
                description="Create 3 detailed notes today",
                period=ChallengePeriod.DAILY,
                requirements=[
                    ChallengeRequirement(ChallengeType.NOTE_CREATION, 3)
                ],
                xp_reward=50,
                skill_rewards={"organization": 5},
                icon="📝"
            ),
            Challenge(
                title="Task Master",
                description="Complete 5 tasks today",
                period=ChallengePeriod.DAILY,
                requirements=[
                    ChallengeRequirement(ChallengeType.TASK_COMPLETION, 5)
                ],
                xp_reward=75,
                skill_rewards={"time_management": 5},
                icon="✅"
            ),
            Challenge(
                title="Study Session",
                description="Study for 2 hours total today",
                period=ChallengePeriod.DAILY,
                requirements=[
                    ChallengeRequirement(ChallengeType.STUDY_TIME, 120)
                ],
                xp_reward=100,
                skill_rewards={"focus": 10},
                icon="📚"
            )
        ]

    def _create_weekly_challenges(self) -> List[Challenge]:
        return [
            Challenge(
                title="Perfect Week",
                description="Complete all daily tasks for 7 days",
                period=ChallengePeriod.WEEKLY,
                requirements=[
                    ChallengeRequirement(ChallengeType.PERFECT_TASKS, 7)
                ],
                xp_reward=200,
                skill_rewards={"time_management": 20},
                icon="🌟"
            ),
            Challenge(
                title="Knowledge Builder",
                description="Create 15 notes this week",
                period=ChallengePeriod.WEEKLY,
                requirements=[
                    ChallengeRequirement(ChallengeType.NOTE_CREATION, 15)
                ],
                xp_reward=150,
                skill_rewards={"organization": 15},
                icon="📚"
            )
        ]

    async def generate_challenges(self):
        """Generate new challenges for different periods"""
        now = datetime.now()
        
        # Daily challenges
        daily_end = datetime.now().replace(hour=23, minute=59, second=59)
        for challenge in self._create_daily_challenges():
            challenge.end_date = daily_end
            await self.challenges_collection.insert_one(challenge.to_dict())

        # Weekly challenges (if it's Monday)
        if now.weekday() == 0:
            week_end = now + timedelta(days=6, hours=23-now.hour, minutes=59-now.minute)
            for challenge in self._create_weekly_challenges():
                challenge.end_date = week_end
                await self.challenges_collection.insert_one(challenge.to_dict())

    async def get_available_challenges(self, user_id: str) -> List[Challenge]:
        """Get available challenges for a user"""
        now = datetime.now()
        challenges = await self.challenges_collection.find({
            "end_date": {"$gt": now}
        }).to_list(length=None)
        
        # Filter out challenges the user has already accepted
        accepted_challenges = await self.user_challenges_collection.find({
            "user_id": user_id,
            "completed_at": None
        }).to_list(length=None)
        
        accepted_ids = [c["challenge"]["title"] for c in accepted_challenges]
        return [Challenge.from_dict(c) for c in challenges if c["title"] not in accepted_ids]

    async def accept_challenge(self, user_id: str, challenge_title: str) -> Optional[UserChallenge]:
        """Accept a challenge for a user"""
        challenge_data = await self.challenges_collection.find_one({"title": challenge_title})
        if not challenge_data:
            return None

        challenge = Challenge.from_dict(challenge_data)
        user_challenge = UserChallenge(user_id, challenge)
        await self.user_challenges_collection.insert_one(user_challenge.to_dict())
        return user_challenge

    async def update_challenge_progress(self, user_id: str, activity_type: str, amount: int = 1):
        """Update progress for all active challenges based on an activity"""
        active_challenges = await self.user_challenges_collection.find({
            "user_id": user_id,
            "completed_at": None
        }).to_list(length=None)

        for challenge_data in active_challenges:
            challenge = UserChallenge.from_dict(challenge_data)
            if activity_type in challenge.progress:
                challenge.progress[activity_type] += amount
                
                # Check if challenge is completed
                all_completed = all(
                    challenge.progress.get(req.type.value, 0) >= req.target
                    for req in challenge.challenge.requirements
                )
                
                if all_completed:
                    challenge.completed_at = datetime.now()
                
                await self.user_challenges_collection.update_one(
                    {"_id": challenge_data["_id"]},
                    {"$set": challenge.to_dict()}
                )

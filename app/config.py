import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'
    MONGODB_NAME = os.environ.get('MONGODB_NAME') or 'student_tracking'
    
    # Gamification settings
    XP_PER_LOGIN = 10
    XP_PER_STUDY_SESSION = 20
    XP_PER_COMPLETED_TASK = 15
    
    # Challenge settings
    DAILY_CHALLENGE_XP = 50
    WEEKLY_CHALLENGE_XP = 200
    MONTHLY_CHALLENGE_XP = 500

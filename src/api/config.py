import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    FLASK_APP = os.getenv('FLASK_APP', 'src/api/app.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'

    # Database configuration
    DB_PATH = os.getenv('DB_PATH', 'student_tracking.db')

    # Server configuration
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', 'localhost')

    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DB_PATH = 'test_database.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

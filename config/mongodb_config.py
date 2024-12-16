# config/mongodb_config.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDBConfig:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        self.db = self.client[os.getenv('DB_NAME', 'student_tracking_system')]

    def get_database(self):
        return self.db

    def close_connection(self):
        self.client.close()
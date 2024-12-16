from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    
    # Setup MongoDB
    app.config['MONGO_CLIENT'] = MongoClient(app.config['MONGODB_URI'])
    app.config['MONGO_DB'] = app.config['MONGO_CLIENT'][app.config['MONGODB_NAME']]
    
    # Register blueprints
    from app.routes.auth import auth
    from app.routes.gamification import gamification
    
    app.register_blueprint(auth)
    app.register_blueprint(gamification)
    
    return app
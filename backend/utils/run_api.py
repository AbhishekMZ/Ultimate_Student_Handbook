from src.api.app import app
from src.api.config import config
import os

if __name__ == '__main__':
    # Get configuration based on environment
    env = os.getenv('FLASK_ENV', 'development')
    config_obj = config[env]
    
    # Run the application
    app.run(
        host=config_obj.HOST,
        port=config_obj.PORT,
        debug=config_obj.DEBUG
    )

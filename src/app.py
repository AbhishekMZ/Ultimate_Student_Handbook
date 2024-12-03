from flask import Flask
from flask_cors import CORS
from routes import student_performance
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Register blueprints
app.register_blueprint(student_performance.bp)

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(debug=True, port=5000)

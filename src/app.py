from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from src.models.user import db
from src.api.routes.student_routes import student_bp

app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_tracking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
CORS(app)
jwt = JWTManager(app)
db.init_app(app)

# Register blueprints
app.register_blueprint(student_bp)

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

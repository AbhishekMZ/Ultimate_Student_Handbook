from flask import Flask
from flask_cors import CORS
from routes import student_performance

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(student_performance.bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import pymongo
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["student_handbook"]
users_collection = db["users"]
notes_collection = db["notes"]
tasks_collection = db["tasks"]

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        user = users_collection.find_one({'username': username, 'password': password})
        
        if user:
            session['username'] = username
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if users_collection.find_one({'username': username}):
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        users_collection.insert_one({
            'username': username,
            'password': password,
            'email': email,
            'created_at': datetime.now()
        })
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Main Routes
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_notes = notes_collection.find({'username': username}).sort('created_at', -1)
    user_tasks = tasks_collection.find({'username': username}).sort('due_date', 1)
    
    return render_template('dashboard.html', username=username, notes=user_notes, tasks=user_tasks)

# API Routes
@app.route('/api/notes', methods=['GET', 'POST'])
def handle_notes():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    if request.method == 'GET':
        notes = list(notes_collection.find({'username': session['username']}))
        return jsonify({'success': True, 'notes': notes})
    
    if request.method == 'POST':
        data = request.get_json()
        note = {
            'username': session['username'],
            'title': data.get('title'),
            'content': data.get('content'),
            'created_at': datetime.now()
        }
        notes_collection.insert_one(note)
        return jsonify({'success': True, 'message': 'Note created'})

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    if request.method == 'GET':
        tasks = list(tasks_collection.find({'username': session['username']}))
        return jsonify({'success': True, 'tasks': tasks})
    
    if request.method == 'POST':
        data = request.get_json()
        task = {
            'username': session['username'],
            'title': data.get('title'),
            'description': data.get('description'),
            'due_date': datetime.strptime(data.get('due_date'), '%Y-%m-%d'),
            'status': 'pending',
            'created_at': datetime.now()
        }
        tasks_collection.insert_one(task)
        return jsonify({'success': True, 'message': 'Task created'})

if __name__ == '__main__':
    app.run(debug=True)

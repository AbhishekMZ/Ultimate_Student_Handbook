import json
import pytest

def test_get_students(client):
    """Test getting all students"""
    response = client.get('/api/students')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == 'Test Student 1'
    assert data[1]['email'] == 'test2@example.com'

def test_get_student(client):
    """Test getting a specific student"""
    # Test existing student
    response = client.get('/api/students/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Student 1'
    assert data['email'] == 'test1@example.com'

    # Test non-existent student
    response = client.get('/api/students/999')
    assert response.status_code == 404

def test_create_student(client):
    """Test creating a new student"""
    new_student = {
        'name': 'New Student',
        'email': 'new@example.com'
    }
    response = client.post('/api/students',
                         data=json.dumps(new_student),
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['message'] == 'Student created successfully'

    # Test duplicate email
    response = client.post('/api/students',
                         data=json.dumps(new_student),
                         content_type='application/json')
    assert response.status_code == 400

def test_get_courses(client):
    """Test getting all courses"""
    response = client.get('/api/courses')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['code'] == 'CS101'
    assert data[1]['name'] == 'Data Structures'

def test_get_course(client):
    """Test getting a specific course"""
    response = client.get('/api/courses/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['code'] == 'CS101'
    assert data['description'] == 'Basic programming concepts'

def test_get_student_progress(client):
    """Test getting student progress"""
    response = client.get('/api/progress/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2  # Student 1 has progress in 2 courses
    assert any(p['completion_percentage'] == 75.5 for p in data)

def test_get_course_progress(client):
    """Test getting course progress"""
    response = client.get('/api/progress/1/course/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['completion_percentage'] == 75.5
    assert data['understanding_level'] == 4

def test_get_performance_analytics(client):
    """Test getting performance analytics"""
    response = client.get('/api/analytics/performance/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'performance_score' in data
    assert 'improvement_rate' in data

def test_get_dashboard_summary(client):
    """Test getting dashboard summary"""
    response = client.get('/api/dashboard/summary')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total_students'] == 2
    assert data['total_courses'] == 2
    assert 'average_progress' in data
    assert 'success_rate' in data

def test_error_handling(client):
    """Test error handling"""
    # Test invalid JSON
    response = client.post('/api/students',
                         data='invalid json',
                         content_type='application/json')
    assert response.status_code == 400

    # Test missing required fields
    response = client.post('/api/students',
                         data=json.dumps({'name': 'Missing Email'}),
                         content_type='application/json')
    assert response.status_code == 400

    # Test invalid route
    response = client.get('/api/invalid_route')
    assert response.status_code == 404

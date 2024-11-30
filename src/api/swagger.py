from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint

# Create APISpec
spec = APISpec(
    title="Student Success Tracking System API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    info={
        "description": "A comprehensive API for managing student academic performance and progress",
        "contact": {"email": "support@studentsuccess.com"}
    }
)

# Define schemas
spec.components.schema("Student", {
    "properties": {
        "id": {"type": "integer", "format": "int64"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "enrollment_date": {"type": "string", "format": "date"}
    },
    "required": ["name", "email"]
})

spec.components.schema("Course", {
    "properties": {
        "id": {"type": "integer", "format": "int64"},
        "code": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"}
    },
    "required": ["code", "name"]
})

spec.components.schema("Progress", {
    "properties": {
        "student_id": {"type": "integer", "format": "int64"},
        "course_id": {"type": "integer", "format": "int64"},
        "completion_percentage": {"type": "number", "format": "float"},
        "understanding_level": {"type": "integer", "minimum": 1, "maximum": 5},
        "last_updated": {"type": "string", "format": "date-time"}
    }
})

spec.components.schema("Analytics", {
    "properties": {
        "performance_score": {"type": "number", "format": "float"},
        "improvement_rate": {"type": "number", "format": "float"},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "areas_for_improvement": {"type": "array", "items": {"type": "string"}}
    }
})

spec.components.schema("Survey", {
    "properties": {
        "student_id": {"type": "integer", "format": "int64"},
        "responses": {
            "type": "object",
            "additionalProperties": {"type": "string"}
        },
        "submission_date": {"type": "string", "format": "date-time"}
    }
})

spec.components.schema("DashboardSummary", {
    "properties": {
        "total_students": {"type": "integer"},
        "total_courses": {"type": "integer"},
        "average_progress": {"type": "number", "format": "float"},
        "success_rate": {"type": "number", "format": "float"}
    }
})

# Error responses
spec.components.schema("Error", {
    "properties": {
        "error": {"type": "string"},
        "message": {"type": "string"}
    }
})

# Security schemes
spec.components.security_scheme("ApiKeyAuth", {
    "type": "apiKey",
    "in": "header",
    "name": "X-API-Key"
})

# Configure Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Student Success Tracking System API",
        'deepLinking': True,
        'displayOperationId': True
    }
)

# API Documentation
"""
@swagger.path('/api/students')
@swagger.path('/api/students/{student_id}')
class StudentsAPI:
    def get(self):
        '''
        Get all students
        ---
        tags:
          - Students
        responses:
          200:
            description: List of students
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Student'
          500:
            description: Server error
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Error'
        '''
        pass

@swagger.path('/api/courses')
@swagger.path('/api/courses/{course_id}')
class CoursesAPI:
    def get(self):
        '''
        Get all courses
        ---
        tags:
          - Courses
        responses:
          200:
            description: List of courses
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Course'
          500:
            description: Server error
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Error'
        '''
        pass

@swagger.path('/api/progress/{student_id}')
class ProgressAPI:
    def get(self, student_id):
        '''
        Get student progress
        ---
        tags:
          - Progress
        parameters:
          - in: path
            name: student_id
            schema:
              type: integer
            required: true
            description: Student ID
        responses:
          200:
            description: Student progress data
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Progress'
          404:
            description: Student not found
          500:
            description: Server error
        '''
        pass

@swagger.path('/api/analytics/performance/{student_id}')
class AnalyticsAPI:
    def get(self, student_id):
        '''
        Get student performance analytics
        ---
        tags:
          - Analytics
        parameters:
          - in: path
            name: student_id
            schema:
              type: integer
            required: true
            description: Student ID
        responses:
          200:
            description: Student analytics data
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Analytics'
          404:
            description: Student not found
          500:
            description: Server error
        '''
        pass

@swagger.path('/api/dashboard/summary')
class DashboardAPI:
    def get(self):
        '''
        Get dashboard summary
        ---
        tags:
          - Dashboard
        responses:
          200:
            description: Dashboard summary data
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/DashboardSummary'
          500:
            description: Server error
        '''
        pass
"""

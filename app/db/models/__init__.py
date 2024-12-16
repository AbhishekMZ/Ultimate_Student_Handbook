# app/db/models/__init__.py
from .student import Student
from .course import Course
from .progress import Progress
from .module import Module
from .achievement import Achievement

__beanie_models__ = [Student, Course, Progress, Module, Achievement]
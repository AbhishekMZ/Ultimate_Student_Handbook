# app/api/v1/endpoints/students.py
from fastapi import APIRouter, HTTPException
from app.schemas.student import StudentCreate, StudentRead
from app.services.student_service import StudentService

router = APIRouter()

@router.post("/", response_model=StudentRead)
async def create_student(student_in: StudentCreate):
    student_service = StudentService()
    existing_student = await student_service.get_student_by_email(student_in.email)
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    student = await student_service.create_student(student_in)
    return student

@router.get("/{student_id}", response_model=StudentRead)
async def read_student(student_id: str):
    student = await Student.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
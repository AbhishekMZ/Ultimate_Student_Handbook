# app/services/student_service.py
from app.db.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.core.security import get_password_hash

class StudentService:
    async def create_student(self, student_in: StudentCreate) -> Student:
        hashed_password = get_password_hash(student_in.password)
        student = Student(
            email=student_in.email,
            hashed_password=hashed_password,
            first_name=student_in.first_name,
            last_name=student_in.last_name,
        )
        await student.insert()
        return student

    async def get_student_by_email(self, email: str) -> Student:
        student = await Student.find_one(Student.email == email)
        return student

    async def update_student(self, student_id: str, student_in: StudentUpdate) -> Student:
        student = await Student.get(student_id)
        await student.update({"$set": student_in.dict(exclude_unset=True)})
        await student.save()
        return student
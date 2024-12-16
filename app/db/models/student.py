# app/db/models/student.py
from beanie import Document, Link
from typing import List, Optional
from pydantic import EmailStr

class Student(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    is_active: bool = True

    progress: Optional[List[Link["Progress"]]]
    achievements: Optional[List[Link["Achievement"]]]

    class Collection:
        name = "students"
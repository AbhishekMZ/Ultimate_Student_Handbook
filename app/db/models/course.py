# app/db/models/course.py
from beanie import Document, Link
from typing import List

class Course(BaseModel):
    title: str
    description: str
    duration: int  # in minutes

    modules: Optional[List[Link["Module"]]]

    class Collection:
        name = "courses"
# app/db/models/progress.py
from beanie import Document, Link

class Progress(BaseModel):
    student: Link[Student]
    course: Link[Course]
    completed_modules: List[str]
    score: float

    class Collection:
        name = "progress"
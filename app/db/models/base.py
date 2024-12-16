# app/db/models/base.py
from beanie import Document
from datetime import datetime

class BaseModel(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        use_state_management = True
        state_management_replace_objects = True
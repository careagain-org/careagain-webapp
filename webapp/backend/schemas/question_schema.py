from pydantic import BaseModel
from typing import Optional
import datetime as dt
import uuid

class Question(BaseModel):
    question_id: uuid.UUID
    title: str
    question: Optional[str]
    file_link: Optional[str]
    created_by: uuid.UUID
    deleted: bool

    class Config:
        from_attributes = True


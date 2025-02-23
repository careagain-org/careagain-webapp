from pydantic import BaseModel
from typing import Optional
import datetime as dt

class Video(BaseModel):
    video_id: Optional[int]
    name: Optional[str]
    youtube_link: str
    description: Optional[str]
    created_by: Optional[int]

    class Config:
        from_attributes = True


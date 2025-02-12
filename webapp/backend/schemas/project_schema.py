from pydantic import BaseModel
from typing import Optional
import datetime as dt
import uuid

class Project(BaseModel):
    project_id: uuid.UUID
    project_name: str
    link: Optional[str]
    description: Optional[str]
    image: Optional[str]

    class Config:
        from_attributes = True


class CreateProject(BaseModel):
    project_name: str


class User_Project(BaseModel):
    __tablename__= 'users_projects'
    rel_up_id:uuid.UUID
    user_id:uuid.UUID
    org_id:uuid.UUID
    member_type: Optional[str]
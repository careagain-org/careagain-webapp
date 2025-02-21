from pydantic import BaseModel
from typing import Optional
import datetime as dt
import uuid

class Project(BaseModel):
    __tablename__= 'projects'
    project_id: uuid.UUID
    name: str
    type: str
    classification: Optional[str]
    website: Optional[str]
    repo: Optional[str]
    description: Optional[str]
    image: Optional[str]
    logo: Optional[str]
    status: Optional[str]
    verified: Optional[bool]

    class Config:
        from_attributes = True


class CreateProject(BaseModel):
    __tablename__= 'projects'
    project_id: uuid.UUID
    name: str
    name: str
    type: str
    website: Optional[str]
    description: Optional[str]
    image: Optional[str]
    logo: Optional[str]
    
    class Config:
        from_attributes = True
        json_encoders = {
            dt.date: lambda v: v.isoformat()}


class User_Project(BaseModel):
    __tablename__= 'users_projects'
    rel_up_id:uuid.UUID
    user_id:uuid.UUID
    org_id:uuid.UUID
    member_type: Optional[str]
from pydantic import BaseModel
from typing import Optional
import datetime as dt
import uuid

class Organization(BaseModel):
    __tablename__='organizations'
    org_id: uuid.UUID
    name:str
    type: str
    address: Optional[str]
    email:Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    logo: Optional[str]
    website: Optional[str]
    activation_date: Optional[dt.date]
    active: Optional[bool]
    verified: Optional[bool]
    visible: Optional[bool]
    storage_path: Optional[str]

    class Config:
        from_attributes = True
        json_encoders = {
            dt.date: lambda v: v.isoformat()
        }

class CreateOrganization(BaseModel):
    __tablename__='organizations'
    org_id: uuid.UUID
    name:str
    type: str
    description: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    logo: Optional[str]
    website: Optional[str]
    email: Optional[str]
    visible:bool

    class Config:
        from_attributes = True
        json_encoders = {
            dt.date: lambda v: v.isoformat()}

class User_Org(BaseModel):
    __tablename__= 'users_orgs'
    rel_uo_id:uuid.UUID
    user_id:uuid.UUID
    org_id:uuid.UUID
    member_type: Optional[str]

class OrganizationUser(Organization):
    user_id:uuid.UUID

    class Config:
        from_attributes = True
        json_encoders = {
            dt.date: lambda v: v.isoformat()
        }
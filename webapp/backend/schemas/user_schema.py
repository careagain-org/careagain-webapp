from pydantic import BaseModel
from typing import Optional
import datetime as dt
import uuid

class UserCreate(BaseModel):
    email:str
    password:str

    class Config:
        from_attributes = True
        json_encoders = {
            dt.date: lambda v: v.isoformat()
        }
        
class ClerkUser(BaseModel):
    user_id:str
    username:str
    first_name:Optional[str]
    last_name:Optional[str]
    linkedin:Optional[str]
    description:Optional[str] 
    profile_image:Optional[str] 
    country:Optional[str] 
    role:Optional[str]


class User(BaseModel):
    user_id:str
    username:str
    first_name:Optional[str]
    last_name:Optional[str]
    linkedin:Optional[str]
    description:Optional[str] 
    profile_image:Optional[str] 
    country:Optional[str] 
    role:Optional[str]
    active:bool
    verified: bool
    visible: bool
    deactivation_date:Optional[dt.date]

    class Config:
        from_attributes = True
        json_encoders = {
            dt.date: lambda v: v.isoformat()
        }

class TokenData(BaseModel):
    user_id: str
    
class CreateUser(BaseModel):
    user_id:str
    username:str
    first_name:Optional[str]
    last_name:Optional[str]
    
    class Config:
        from_attributes = True
        json_encoders = {
            dt.date: lambda v: v.isoformat()}



    


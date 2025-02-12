from pydantic import BaseModel
from typing import Optional
import datetime as dt

class UserCreate(BaseModel):
    email:str
    password:str

    class Config:
        from_attributes = True
        json_encoders = {
            dt.date: lambda v: v.isoformat()
        }

class User(BaseModel):
    user_id:int
    username:str
    first_name:Optional[str]
    last_name1:Optional[str]
    last_name2:Optional[str] 
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
    user_id:int



    


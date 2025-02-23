from pydantic import BaseModel
from typing import Optional
import datetime as dt


class TokenBase(BaseModel):
    id: Optional[int]
    user_id: int
    access_token:str
    token_type:str

class TokenData(TokenBase):
    user_id: Optional[int]

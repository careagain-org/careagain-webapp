from fastapi import APIRouter,Depends,Response, HTTPException,security
from typing import List
from ..schemas import video_schema as schema, user_schema
from ..models import model
from sqlalchemy.orm import Session
# from ..config.db_setup import get_db
from ..config.supabase_config import get_db
from ..services import user_functions
import passlib.hash as hash

video_route = APIRouter(prefix="/api/videos")

@video_route.get("/",response_model=List[schema.Video],tags = ['videos'])
def show_videos(db:Session=Depends(get_db)):
    users = db.query(model.Video).all()
    return users

@video_route.post("/new_video/",tags = ['videos'])#,response_model=schema.video)
async def create_video(input:schema.Video,db:Session=Depends(get_db),
                         user:user_schema.User = Depends(user_functions.get_current_user)):
    #db_user = await user_functions.get_user_by_email(input.email,db)
    # if db_user:
    #     raise HTTPException(status_code=400, detail= "Email already in use")
    # else:
    video_obj = model.Video(name=input.name,
                                youtube_link=input.youtube_link,
                                description=input.description,
                                created_by=user.user_id)
    db.add(video_obj)
    db.commit()
    db.refresh(video_obj)
    return video_obj 
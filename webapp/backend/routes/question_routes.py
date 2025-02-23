from fastapi import APIRouter,Depends,Response, HTTPException,security
from typing import List
from ..schemas import question_schema as schema, user_schema
from ..models import model
from sqlalchemy.orm import Session
from sqlalchemy import desc
#from ..config.db_setup import get_db
from ..config.supabase_config import get_db
from ..services import user_functions
import passlib.hash as hash

question_route = APIRouter(prefix="/api/questions")

@question_route.get("/",response_model=List[schema.Question],tags = ['questions'])
def show_projects(db:Session=Depends(get_db)):
    questions = db.query(model.Question).order_by(desc(model.Question.question_id)).all()
    return questions

@question_route.post("/new_question/",tags = ['questions'])#,response_model=schema.Project)
async def create_question(input:schema.Question,db:Session=Depends(get_db),
                         user:user_schema.User = Depends(user_functions.get_current_user)):
    #db_user = await user_functions.get_user_by_email(input.email,db)
    # if db_user:
    #     raise HTTPException(status_code=400, detail= "Email already in use")
    # else:
    question_obj = model.Question(title=input.title,
                                question=input.question,
                                created_by=user.user_id)
    db.add(question_obj)
    db.commit()
    db.refresh(question_obj)
    return question_obj 
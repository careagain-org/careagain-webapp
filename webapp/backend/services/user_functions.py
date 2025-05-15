# import model and db
from fastapi import security, Depends, HTTPException, status, Response
from ..models import model
from ..schemas import user_schema as schema
from ..config.supabase_config import engine,Base,Session,get_db,supa_client
#from ..config.db_setup import engine,Base,Session,get_db
import json


from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/users/token")

async def get_user_by_username(username:str,db:Session,):
    '''Return the email if exists in db'''
    user = db.query(model.User).filter(model.User.username == username).first()
    return user 

# async def authenticate_user(email:str,password:str,db:Session):
#     '''Checks if the email exist and verify the password and return the user if so'''
#     user = await get_user_by_email(email,db)
#     if not user:
#         return False
#     if not user.verify_password(password):
#         return False
#     return user



async def get_current_user(db:Session=Depends(get_db),token:str = Depends(oauth2schema)):
    '''Get current user logged in'''
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                         detail = "Could not validate credentials",
                                         headers = {"WWW-Authenticate": "Bearer"})

    try:
        response = supa_client.auth.get_user(token)
        data = response.json() 
        parsed_data = json.loads(data)
        user_id = parsed_data.get("user").get("id")

        if user_id is None:
            raise credential_exception

    except Exception:
        raise credential_exception
    
    user = db.query(model.User).filter(model.User.user_id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

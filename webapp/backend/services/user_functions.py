# import model and db
from fastapi import security, Depends, HTTPException, status, Response,Request
from ..models import model
from ..schemas import user_schema as schema
from ..config.supabase_config import engine,Base,Session,get_db,supa_client
#from ..config.db_setup import engine,Base,Session,get_db
from jose import JWTError, jwt
import os
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv
import random as rn

load_dotenv()

from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))
cookie2schema = security.APIKeyCookie(name="__session")
oauth2schema = security.OAuth2PasswordBearer("/api/auth/auth_token")
# oauth2schema = security.APIKeyCookie(name="auth_token")

credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                         detail = "User not authenticated ",
                                         headers = {"WWW-Authenticate": "Bearer"})

async def get_user_by_username(username:str,db:Session,):
    '''Return the email if exists in db'''
    user = db.query(model.User).filter(model.User.username == username).first()
    return user 

def get_token(token:str=Depends(oauth2schema)):
    return token

def get_cookie_dict(token:str=Depends(oauth2schema)):
    '''Get info from the cookie'''
    try:
        data = jwt.decode(token,os.getenv("JWT_KEY"), algorithms=["RS256"])
        return data
    except JWTError:
        raise credential_exception


def get_current_user(token:str= Depends(oauth2schema),
                    db:Session=Depends(get_db)):
                        #    token:str = Depends(oauth2schema)):
    '''Get current user logged in'''

    try:
        data = jwt.decode(token,os.getenv("CLERK_SECRET_KEY"), algorithms=["HS256"])

        if data['role']=='authenticated':
            user_id = data["id"]
            user = db.query(model.User).filter(model.User.user_id == user_id).first()
            if user is None:
                user_obj = model.User(user_id = data["id"],
                                        username = data["username"],
                                        first_name = data["first_name"],
                                        last_name = data["last_name"],
                                        profile_image = data["profile_image_url"],
                                        country = "",
                                        role = "",
                                        linkedin = "",
                                        description = "",
                                        active = True)
            
                db.add(user_obj)
                db.commit()
                db.refresh(user_obj)
            else:
                return user
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not authenticated"
        )
    
    except JWTError:
        raise credential_exception


def create_user(input:dict,
                db:Session=Depends(get_db),
                token:str=Depends(cookie2schema),):
    
    try:
        user = db.query(model.User).filter(model.User.user_id == input["id"]).first()

        if user != []:
            return {"detail": "User details retrieved","user_details":user}
        else:
            try:
                user_obj = model.User(user_id = input["id"],
                                        username = input["username"],
                                        first_name = input["first_name"],
                                        last_name = input["last_name"],
                                        profile_image = input["profile_image_url"],
                                        country = "",
                                        role = "",
                                        linkedin = "",
                                        description = "",
                                        active = True)
            
                db.add(user_obj)
                db.commit()
                db.refresh(user_obj)
            except Exception as e:
                user_obj = model.User(user_id = input["id"],
                                        username = input["first_name"]+input["last_name"][0:2] +str(rn.randint(1,100)),
                                        first_name = input["first_name"],
                                        last_name = input["last_name"],
                                        profile_image = input["profile_image_url"],
                                        country = "",
                                        role = "",
                                        linkedin = "",
                                        description = "",
                                        active = True)
            
                db.add(user_obj)
                db.commit()
                db.refresh(user_obj)
            
            return {"detail": "User details retrieved","user_details":user_obj}
    except JWTError:
        raise credential_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
def delete_user(input:dict,
                db:Session=Depends(get_db)):
    try:
        
        if input["deleted"]:
            (db.query(model.User_Organization).filter(model.User_Organization.user_id == input["id"]).delete(synchronize_session='fetch'))
            (db.query(model.User_Project).filter(model.User_Project.user_id == input["id"]).delete(synchronize_session='fetch'))
            (db.query(model.Action).filter(model.Action.performed_by == input["id"]).delete(synchronize_session='fetch'))
            (db.query(model.User).filter(model.User.user_id == input["id"]).delete())

        db.commit()

        return {"detail": "User deleted"}
    except JWTError:
        raise credential_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def update_user(input:dict,
                      db:Session=Depends(get_db)):
    try:
            
        user = db.query(model.User).filter(model.User.user_id == input["id"]).first()
        # Set the attribute dynamically
        user.username = input.get("username")
        user.first_name = input.get("first_name")
        user.last_name = input.get("last_name")
        user.profile_image = input.get("profile_image_url")

        db.commit()
        db.refresh(user)

        return {"detail": "User updated","user_details":user}
    except JWTError:
        raise credential_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

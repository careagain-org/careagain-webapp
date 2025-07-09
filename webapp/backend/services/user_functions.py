# import model and db
from fastapi import security, Depends, HTTPException, status, Response,Request
from ..models import model
from ..schemas import user_schema as schema
from ..config.supabase_config import engine,Base,Session,get_db,supa_client
#from ..config.db_setup import engine,Base,Session,get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
import json
from typing import Annotated
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv
import random as rn

load_dotenv()

clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
# oauth2schema = security.APIKeyCookie(name="__session")
oauth2schema = security.OAuth2PasswordBearer("/api/auth/auth_token")

credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                         detail = "Could not validate credentials",
                                         headers = {"WWW-Authenticate": "Bearer"})

async def get_user_by_username(username:str,db:Session,):
    '''Return the email if exists in db'''
    user = db.query(model.User).filter(model.User.username == username).first()
    return user 


def get_current_user(token:str=Depends(oauth2schema),
                            db:Session=Depends(get_db)):
                        #    token:str = Depends(oauth2schema)):
    '''Get current user logged in'''

    try:
        data = jwt.decode(token,os.getenv("JWT_KEY"), algorithms=["RS256"])
        if data['role']=='authenticated':
            user_id = data["sub"]
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
                    db:Session=Depends(get_db)):
    
    try:
        user = db.query(model.User).filter(model.User.user_id == input["user_id"]).first()

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
    
    
def delete_user(input:dict,
                      token:str=Depends(oauth2schema),
                      db:Session=Depends(get_db)):
    try:
        response = jwt.decode(token,os.getenv("JWT_KEY"), algorithms=["RS256"])
        
        if response['role']=='authenticated':
            if input["deleted"]:
                (db.query(model.User_Organization).filter(model.User_Organization.user_id == input["id"]).delete(synchronize_session='fetch'))
                (db.query(model.User_Project).filter(model.User_Project.user_id == input["id"]).delete(synchronize_session='fetch'))
                (db.query(model.User).filter(model.User.user_id == input["id"]).delete())

            db.commit()

            return {"detail": "User deleted"}
    except JWTError:
        raise credential_exception
    

def update_user(input:dict,
                      token:str=Depends(oauth2schema),
                      db:Session=Depends(get_db)):
    try:
        response = jwt.decode(token,os.getenv("JWT_KEY"), algorithms=["RS256"])
        
        if response.get('role')=='authenticated':
            
            user = db.query(model.User).filter(model.User.user_id == input["id"]).first()
            # Set the attribute dynamically
            setattr(user, "username", input["username"])
            setattr(user, "first_name", input["first_name"])
            setattr(user, "last_name", input["last_name"])
            setattr(user, "profile_image_url", input["profile_image"])
            setattr(user, "username", input["username"])

            # Commit the changes to the database
            db.add(user)
            db.commit()
            db.refresh(user)

            return {"detail": "User updated","user_details":user}
    except JWTError:
        raise credential_exception
    
    
    # try:
    #     response = supa_client.auth.sign_in_with_id_token(
    #         {
    #             "provider": "clerk",
    #             "token": f"{token}",
    #         }
    #     )
    #     # get_user(token)
    #     data = response.json() 
    #     parsed_data = json.loads(data)
    #     user_id = parsed_data.get("user").get("id")

    #     if user_id is None:
    #         raise credential_exception

    # except JWTError:
    #     token = None
    #     raise credential_exception
    
    # user = db.query(model.User).filter(model.User.user_id == user_id).first()

    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found"
    #     )

    # return user





# async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400,detail = "Inactive user")
#     return current_user

# async def get_current_user(db:Session=Depends(get_db),token:str = Depends(oauth2schema)):
#     '''Get current user logged in'''
#     credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
#                                          detail = "Could not validate credentials",
#                                          headers = {"WWW-Authenticate": "Bearer"})

#     try:
#         payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
#         user_id: int = payload.get("user_id")
#         if user_id is None:
#             raise credential_exception

#         #token_data = schema.User(user_id=user_id)

#     except JWTError:
#         raise credential_exception
    
#     user = db.query(model.User).filter(model.User.user_id == user_id).first()

#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )

#     return user


# async def create_token(user:model.User): #expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES):
#     '''Create a token for each user when opening session'''
#     user_obj =  {"user_id":user.user_id}
#     # if expires_delta:
#     #     expire = datetime.utcnow + expires_delta
    
#     token = jwt.encode(user_obj,SECRET_KEY,algorithm=ALGORITHM)

#     # Set token in cookie (HTTP-only and secure)
#     # response.set_cookie(
#     #     key="access_token",  # Name of the cookie
#     #     value=token,  # The token itself
#     #     httponly=True,       # Prevents JavaScript access to the cookie (for security)
#     #     secure=True,         # Ensures the cookie is only sent over HTTPS
#     #     samesite="lax"       # Protects against CSRF
#     # )

#     # Return a success response (or return any data you need)
#     print("message Token set in cookie")

    # return token#dict(access_token = token, token_type="bearer")
from fastapi import APIRouter,Depends,Response, HTTPException,security
from fastapi.responses import JSONResponse
from typing import List
from ..schemas import user_schema as schema
# from ..config.db_setup import get_db
from ..models import model
from sqlalchemy.orm import Session
from ..config.supabase_config import get_db,supa_client
from ..services import user_functions
import passlib.hash as hash
from pydantic import BaseModel
from typing import Optional
from urllib.parse import unquote
import json


auth_route = APIRouter(prefix="/api/auth")
supa = supa_client
oauth2schema = security.OAuth2PasswordBearer(tokenUrl="api/auth/token")


# Modelo para credenciales
class AuthCredentials(BaseModel):
    email: str
    password: str

class AuthCredentialsToken(BaseModel):
    email: str
    password: str
    token:str
    refresh_token:str

@auth_route.post("/sign_up",tags = ['auth'])
async def sign_up(input:AuthCredentials,db:Session=Depends(get_db)):
    try:
        response = supa.auth.sign_up(
        {"email": unquote(input.email), "password": unquote(input.password)})
        data = response.json() 
        parsed_data = json.loads(data)

        try:
            # add to careagain db
            user_obj = model.User(user_id = parsed_data.get("user").get("id"),
                                  username = input.email.split("@")[0])
            db.add(user_obj)
            db.commit()

            return {"detail": "Confirmation email sent to your email", "data": parsed_data}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"User already registered, please log in")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sign up error: {str(e)}")



@auth_route.get("/sign_out",tags = ['auth'])
def sign_out():
    try:
        response = supa.auth.sign_out()
        return {"detail": "User logged out", "data": response}
    except Exception as e:
        raise HTTPException(status_code=response.status, detail=f"Log out error: {str(e)}")

@auth_route.post("/token", tags=["auth"])
def login_with_cookie(form_data: security.OAuth2PasswordRequestForm = Depends()):
    try:
        response = supa.auth.get_session()
        # print(response)
        # if response is not None:
        if response:
            data = response.json() 
            parsed_data = json.loads(data)
            return parsed_data
        else:
        # Authenticate and get tokens
            response = supa.auth.sign_in_with_password(
                {"email": unquote(form_data.username), "password": unquote(form_data.password)}
            )
            data = response.json()
            parsed_data = json.loads(data)

            # Create a response with cookies
            access_token = parsed_data["session"]["access_token"]
            refresh_token = parsed_data["session"]["refresh_token"]

            response = JSONResponse(
                content={"detail": "Login successful"},
                status_code=200
            )
            response.set_cookie(key="access_token", value=access_token, httponly=True)
            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
            return parsed_data["session"]

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Login error: {str(e)}")
    

# @auth_route.post("/token",tags = ['auth'])
# def get_token(form_data:security.OAuth2PasswordRequestForm = Depends()):
#     try:
#         response = supa.auth.sign_in_with_password(
#         {"email": unquote(form_data.username), "password": unquote(form_data.password)})
#         data = response.json() 
#         parsed_data = json.loads(data) 
#         return  parsed_data["session"] #{"access_token": data.get("access_token"),"token_type":"bearer"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Sign in error: {str(e)}")



# @auth_route.post("/token",tags = ['auth'])
# def get_token(form_data:security.OAuth2PasswordRequestForm = Depends()):
#     try:
#         response = supa.auth.get_session(
#         {"email": unquote(form_data.username), "password": unquote(form_data.password)})
#         data = response.json() 
#         parsed_data = json.loads(data) 
#         return  parsed_data["session"] #{"access_token": data.get("access_token"),"token_type":"bearer"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Sign in error: {str(e)}")
    
    
    
@auth_route.post("/reset_password",tags = ['auth'])
def reset_password(input:AuthCredentials):
    try:
        response = supa.auth.reset_password_for_email(unquote(input.email), {
        "redirect_to": "http://localhost:3000/reset_password",
        })
        return response
        # return parsed_data {"access_token": response.json()["access_token"],"token_type":"bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Reset password error: {str(e)}")

    
@auth_route.put("/update_password",tags = ['auth'])
def update_password(input:AuthCredentialsToken):
    try:
        supa.auth.set_session(access_token=input.token, refresh_token=input.refresh_token)
        response = supa.auth.update_user({  
                    "password": input.password
                    })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Reset password error:{str(e)}")
    
@auth_route.post("/login_without_password",tags = ['auth'])
def login_without_password(input:AuthCredentials):
    try:
        response = supa.auth.sign_in_with_otp(
            {
                "email": input.email,
                "options": {"email_redirect_to": "http://localhost:3000/platform"},
            })
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Email error: {str(e)}")


@auth_route.get("/current_user",tags = ['auth'])
def current_user():
    try:
        response = supa.auth.get_user()
        data = response.json() 
        parsed_data = json.loads(data)
        return {"detail": "User details retrieved", "data": parsed_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f": {str(e)}")
    
@auth_route.get("/session",tags = ['auth'])
def current_session():
    try:
        response = supa.auth.get_session()
        if response:
            data = response.json() 
            parsed_data = json.loads(data)
            return parsed_data
        else:
            raise HTTPException(status_code=401, detail="No session not authorized")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f": {str(e)}")
    

@auth_route.post("/refresh_session",tags = ['auth'])
def refresh_session(session = Depends(oauth2schema)):
    try:
        response = supa.auth.refresh_session()
        if response:
            data = response.json() 
            parsed_data = json.loads(data)
            return parsed_data["session"]
        else:
            return {"detail": "No session open"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f": {str(e)}")
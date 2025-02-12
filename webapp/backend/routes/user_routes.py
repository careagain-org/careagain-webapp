from fastapi import APIRouter,Depends,Response, HTTPException,security,UploadFile,File,Request
from typing import List
from ..schemas import user_schema as schema
from ..models import model
from sqlalchemy.orm import Session
# from ..config.db_setup import get_db
from ..config.supabase_config import get_db,url_s3_object,supa_client,bucket_s3
from ..services import user_functions
import passlib.hash as hash
from urllib.parse import unquote
import uuid


user_route = APIRouter(prefix="/api/users")


@user_route.get("/",response_model=List[schema.User],tags = ['users'])
def show_users(db:Session=Depends(get_db)):
    users = db.query(model.User).all()
    return users

# @user_route.post("/create_user",response_model=schema.User,tags = ['users'])
# async def create_users(input:schema.UserCreate,db:Session=Depends(get_db)):
#     db_user = await user_functions.get_user_by_email(input.email,db)
#     if db_user:
#         raise HTTPException(status_code=400, detail= "Email already in use")
#     else:
#         user_obj = model.User(email=input.email,
#                           hashed_password = hash.bcrypt.hash(input.password))
#         db.add(user_obj)
#         db.commit()
#         db.refresh(user_obj)
#         return user_obj


# @user_route.delete("/{user_id}",tags = ['users'])
# def delete_users(user_id_to_delete:int,db:Session=Depends(get_db)):
#     user = db.query(model.User).filter_by(user_id=user_id_to_delete).first()
#     db.delete(user)
#     return HTTPException(status_code=204,details= "Deleted user") 

# @user_route.post("/token",tags = ['users'])#, response_model=schema.Token)
# async def generate_token(form_data:security.OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
#     user = await user_functions.authenticate_user(form_data.username,form_data.password,db)
#     print(user)
#     if not user:
#         raise HTTPException(status_code = 401,detail = "Invalid Credentials")
#     access_token = await user_functions.create_token(user)
#     return  {"access_token": access_token, "token_type": "bearer"}
    

@user_route.get("/me",tags = ['users'])
async def get_user(user:schema.User = Depends(user_functions.get_current_user)):
    return user

# @user_route.get("/my_image",tags = ['users'])
# async def get_my_image(user:schema.User = Depends(user_functions.get_current_user)):
#     url_foto = f"{url_s3_object}/users/{user["user_id"]}/images/profile_img.jpeg"
#     return url_foto

@user_route.post("/upload_image",tags = ['users'])
async def upload_image(file: UploadFile= File(...),
                       user: schema.User = Depends(user_functions.get_current_user),
                       db: Session = Depends(get_db)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        user_id = user.user_id
        url_photo = f"users/{user_id}/images/{uuid.uuid4()}.png"
        print(url_photo)
        contents = await file.read()

        # Upload with auth headers
        response = supa_client.storage.from_(f"{bucket_s3}").upload(
            file=contents,
            path=url_photo,
            file_options={"content-type": file.content_type,
                        "cache-control": "3600", "upsert": "true",},
        )
        # Set the attribute dynamically
        setattr(user, "profile_image", f"{url_s3_object}/{url_photo}")

        # Commit the changes to the database
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {"filename":f"{url_s3_object}/{url_photo}", "detail": "Profile image uploaded","user_details":user}
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@user_route.put("/update_user", tags=['users'])
async def update_user(key: str, 
                      value: str, 
                      user: schema.User = Depends(user_functions.get_current_user),
                      db: Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the attribute exists on the user model
    if not hasattr(user, key):
        raise HTTPException(status_code=400, detail=f"Field '{key}' does not exist on user")

    # Set the attribute dynamically
    setattr(user, key, value)

    # Commit the changes to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
    

    
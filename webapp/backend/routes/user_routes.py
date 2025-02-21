from fastapi import APIRouter,Depends,Response, HTTPException,security,UploadFile,File,Request
from typing import List
from ..schemas import user_schema as schema
from ..models import model
from sqlalchemy.orm import Session
from sqlalchemy import desc
# from ..config.db_setup import get_db
from ..config.supabase_config import get_db,url_s3_object,supa_client,bucket_s3
from ..services import user_functions
import passlib.hash as hash
from urllib.parse import unquote
import uuid
import json

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


@user_route.get("/",response_model=List[schema.User],tags = ['users'])
def show_projects(db:Session=Depends(get_db)):
    users = db.query(model.User).order_by(desc(model.User.user_id)).all()
    return users


@user_route.post("/invite_user",tags = ['users']) 
def invite_user(email: str,
                  user: schema.User = Depends(user_functions.get_current_user),
                  db: Session = Depends(get_db)):
    try:
        response = supa_client.auth.admin.invite_user_by_email(email) #not working as admin permission needed

        if response:
            data = response.json() 
            parsed_data = json.loads(data)
            return {"detail": "Email sent","data": parsed_data}
        else:
            return {"detail": "Email could not be sent"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Email invitation error: {str(e)}")
    

@user_route.put("/join_project",tags = ['users'])
async def join_project(project_id:str,
                       user_id:str,
                       role:str,
                       db:Session=Depends(get_db)):
    admin_roles = db.query(model.User_Project).filter(model.User_Project.project_id == project_id,
                                              model.User_Project.member_type == "admin").all()
    
    my_roles = db.query(model.User_Project).filter(model.User_Project.project_id == project_id,
                                              model.User_Project.user_id == user_id).all()
    if my_roles==[]:
        if admin_roles==[]:
            rel_obj = model.User_Project(user_id = user_id,
                                        project_id = project_id,
                                        member_type = "admin")
            db.add(rel_obj)
            db.commit()
        else:
            rel_obj = model.User_Project(user_id = user_id,
                                        project_id = project_id,
                                        member_type = role)
            db.add(rel_obj)
            db.commit()
        
        return {"detail": "User joined the project"} 
    else:
        raise HTTPException(status_code=422, detail="User is already a member of this project")

    

@user_route.put("/join_org",tags = ['users'])
async def join_org(org_id:str,
                       user_id:str,
                       role:str,
                       db:Session=Depends(get_db)):
    admin_roles = db.query(model.User_Organization).filter(model.User_Organization.org_id == org_id,
                                              model.User_Organization.member_type == "admin").all()
    
    my_roles = db.query(model.User_Organization).filter(model.User_Organization.org_id == org_id,
                                              model.User_Organization.user_id == user_id).all()
    if my_roles==[]:
        if admin_roles==[]:
            rel_obj = model.User_Organization(user_id = user_id,
                                        org_id = org_id,
                                        member_type = "admin")
            db.add(rel_obj)
            db.commit()
        else:
            rel_obj = model.User_Organization(user_id = user_id,
                                        org_id = org_id,
                                        member_type = role)
            db.add(rel_obj)
            db.commit()
        
        return {"detail": "User joined the organization"} 
    else:
        raise HTTPException(status_code=422, detail="User is already a member of this organization")
    

@user_route.get("/user_projects",tags = ['users'])
async def get_user_projects(user_id:str,
                            db:Session=Depends(get_db)):
    projects = db.query(model.Project).join(
            model.User_Project,
            model.User_Project.project_id == model.Project.project_id
        ).filter(model.User_Project.user_id == user_id).all()
    my_roles = (db.query(model.User_Project)
        .filter(model.User_Project.user_id == user_id)).all()

    # Create a dictionary of users by user_id for fast lookups
    project_dict = {project.project_id: project for project in projects}

    # Now merge by matching user_id in both lists and merge all fields
    merged_list = []
    for role in my_roles:
        project = project_dict.get(role.project_id)  # Look up the corresponding Project
        if project:
            # Merge all fields from both the Project and the role
            merged_dict = {**project.__dict__, **role.__dict__}  # Combine all fields
            merged_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state attribute
            merged_list.append(merged_dict)
        
    return merged_list


@user_route.get("/user_orgs",tags = ['users'])
async def get_user_orgs(user_id:str,
                            db:Session=Depends(get_db)):
    orgs = db.query(model.Organization).join(
            model.User_Organization,
            model.User_Organization.org_id == model.Organization.org_id
        ).filter(model.User_Organization.user_id == user_id).all()
    my_roles = (db.query(model.User_Organization)
        .filter(model.User_Organization.user_id == user_id)).all()

    # Create a dictionary of users by user_id for fast lookups
    org_dict = {org.org_id: org for org in orgs}

    # Now merge by matching user_id in both lists and merge all fields
    merged_list = []
    for role in my_roles:
        org = org_dict.get(role.org_id)  # Look up the corresponding org
        if org:
            # Merge all fields from both the org and the role
            merged_dict = {**org.__dict__, **role.__dict__}  # Combine all fields
            merged_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state attribute
            merged_list.append(merged_dict)
        
    return merged_list
    
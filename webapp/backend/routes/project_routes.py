from fastapi import APIRouter,Depends,UploadFile,File,HTTPException
from typing import List
from ..schemas import project_schema, user_schema
from ..models import model
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..config.supabase_config import get_db,supa_client,bucket_s3,url_s3_object
from ..services import user_functions
import passlib.hash as hash
import logging

project_route = APIRouter(prefix="/api/projects")

@project_route.get("/",response_model=List[project_schema.Project],tags = ['projects'])
def show_projects(db:Session=Depends(get_db)):
    projects = db.query(model.Project).order_by(desc(model.Project.project_id)).all()
    return projects


@project_route.post("/create_project",tags = ['projects'])
async def create_project(input:project_schema.CreateProject,
                     db:Session=Depends(get_db),
                     user:user_schema.User = Depends(user_functions.get_current_user)):

    project_obj = model.Project(project_id=input.project_id,
                                 name = input.name,
                                 type = input.type,
                                 description= input.description,
                                 logo = f"{url_s3_object}projects/{input.project_id}/images/{input.logo}" if input.logo else "",
                                 image = f"{url_s3_object}projects/{input.project_id}/images/{input.image}" if input.image else "",
                                 website = input.website,
                                 )
    
    db.add(project_obj)
    db.commit()

    rel_obj = model.User_Project(user_id = user.user_id,
                                      project_id = project_obj.project_id,
                                      member_type = "admin")
    db.add(rel_obj)
    db.commit()

    db.refresh(project_obj)

    return {"detail": "New project uploaded","project_details":project_obj}


@project_route.post("/upload_image",tags = ['projects'])
async def upload_image(project_id: str,
                        file: UploadFile= File(...),
                        user: user_schema.User = Depends(user_functions.get_current_user),
                        db: Session = Depends(get_db)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        url_photo = f"projects/{project_id}/images/{file.filename}"
        print(url_photo)
        contents = await file.read()

        # Upload with auth headers
        response = supa_client.storage.from_(f"{bucket_s3}").upload(
            file=contents,
            path=url_photo,
            file_options={"content-type": file.content_type,
                        "cache-control": "3600", "upsert": "true",},
        )
        
        return {"filename":f"{url_s3_object}/{url_photo}", "detail": "Image uploaded","project_id":project_id}
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    

@project_route.delete("/delete_project",tags = ['projects'])
async def delete_project(project_id:str,
                            db:Session=Depends(get_db)):
    (db.query(model.User_Project).filter(model.User_Project.project_id == project_id).delete(synchronize_session='fetch'))
    (db.query(model.Project).filter(model.Project.project_id == project_id).delete())

    db.commit()

    return {"detail": "Project deleted"} 


@project_route.delete("/leave_project",tags = ['projects'])
async def leave_project(project_id:str,
                            user:user_schema.User = Depends(user_functions.get_current_user),
                            db:Session=Depends(get_db)):
    (db.query(model.User_Project).filter(model.User_Project.project_id == project_id,
                                              model.User_Project.user_id == user.user_id).delete(synchronize_session='fetch'))

    db.commit()

    return {"detail": "Project detached"} 

@project_route.put("/join_project",tags = ['projects'])
async def join_project(project_id:str,
                            user:user_schema.User = Depends(user_functions.get_current_user),
                            db:Session=Depends(get_db)):
    admin_roles = db.query(model.User_Project).filter(model.User_Project.project_id == project_id,
                                              model.User_Project.member_type == "admin").all()
    
    my_roles = db.query(model.User_Project).filter(model.User_Project.project_id == project_id,
                                              model.User_Project.user_id == user.user_id).all()
    if my_roles==[]:
        if admin_roles==[]:
            rel_obj = model.User_Project(user_id = user.user_id,
                                        project_id = project_id,
                                        member_type = "admin")
            db.add(rel_obj)
            db.commit()
        else:
            rel_obj = model.User_Project(user_id = user.user_id,
                                        project_id = project_id,
                                        member_type = "user")
            db.add(rel_obj)
            db.commit()
        
        return {"detail": "Project attached"} 
    else:
        raise HTTPException(status_code=422, detail="Project already attached to this user")


@project_route.get("/members",tags = ['projects'])
async def get_members(project_id:str,
                            db:Session=Depends(get_db)):
    members = db.query(model.User).join(
            model.User_Project,
            model.User_Project.user_id == model.User.user_id
        ).filter(model.User_Project.project_id == project_id).all()
    my_roles = (db.query(model.User_Project)
        .filter(model.User_Project.project_id == project_id)).all()

    # Create a dictionary of users by user_id for fast lookups
    user_dict = {user.user_id: user for user in members}

    # Now merge by matching user_id in both lists and merge all fields
    merged_list = []
    for role in my_roles:
        project = user_dict.get(role.user_id)  # Look up the corresponding Project
        if project:
            # Merge all fields from both the Project and the role
            merged_dict = {**project.__dict__, **role.__dict__}  # Combine all fields
            merged_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state attribute
            merged_list.append(merged_dict)
        
    return merged_list


@project_route.get("/my_projects" ,tags = ['projects']) 
async def show_projects(
    user: user_schema.User = Depends(user_functions.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all projects associated with the current user.

    Args:
        user (schemas.User): The current authenticated user.
        db (Session): The database session.

    Returns:
        List[schemas.projectUser]: A list of projects the user is associated with.
    """
    # Query the database for projects associated with the user
    my_projects = (db.query(model.Project)
        .join(
            model.User_Project,
            model.User_Project.project_id == model.Project.project_id
        )
        .filter(model.User_Project.user_id == user.user_id)).all()
    my_roles = (db.query(model.User_Project)
        .filter(model.User_Project.user_id == user.user_id)).all()

    # Create a dictionary of projects by project_id for fast lookups
    project_dict = {project.project_id: project for project in my_projects}

    # Now merge by matching project_id in both lists and merge all fields
    merged_list = []
    for role in my_roles:
        project = project_dict.get(role.project_id)  # Look up the corresponding Project
        if project:
            # Merge all fields from both the Project and the role
            merged_dict = {**project.__dict__, **role.__dict__}  # Combine all fields
            merged_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state attribute
            merged_list.append(merged_dict)


    # Return the list of Projects
    return merged_list


@project_route.put("/user_join_project",tags = ['projects'])
async def join_project(project_id:str,
                       user_id:str,
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
                                        member_type = "user")
            db.add(rel_obj)
            db.commit()
        
        return {"detail": "User joined the Project"} 
    else:
        raise HTTPException(status_code=422, detail="User is already a member of this Project")
    

@project_route.put("/user_dettached_project",tags = ['projects'])
async def dettach_project(project_id:str,
                       user_id:str,
                       db:Session=Depends(get_db)):
    (db.query(model.User_Project).filter(model.User_Project.project_id == project_id,
                                              model.User_Project.user_id == user_id).delete(synchronize_session='fetch'))

    db.commit()

    return {"detail": "User dettached from Project"} 


@project_route.get("/members",tags = ['projects'])
async def get_members(project_id:str,
                            db:Session=Depends(get_db)):
    members = db.query(model.User).join(
            model.User_Project,
            model.User_Project.user_id == model.User.user_id
        ).filter(model.User_Project.project_id == project_id).all()
    my_roles = (db.query(model.User_Project)
        .filter(model.User_Project.project_id == project_id)).all()

    # Create a dictionary of users by user_id for fast lookups
    user_dict = {user.user_id: user for user in members}

    # Now merge by matching user_id in both lists and merge all fields
    merged_list = []
    for role in my_roles:
        project = user_dict.get(role.user_id)  # Look up the corresponding Project
        if project:
            # Merge all fields from both the Project and the role
            merged_dict = {**project.__dict__, **role.__dict__}  # Combine all fields
            merged_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state attribute
            merged_list.append(merged_dict)
        
    return merged_list



@project_route.put("/update_project", tags=['projects'])
async def update_project(key: str, 
                      value: str, 
                      project_id: str,
                      db: Session = Depends(get_db)):
    
    project= (db.query(model.Project).filter(model.Project.project_id == project_id)).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the attribute exists on the user model
    if not hasattr(project, key):
        raise HTTPException(status_code=400, detail=f"Field '{key}' does not exist on Project")

    # Set the attribute dynamically
    setattr(project, key, value)

    # Commit the changes to the database
    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@project_route.put("/change_member_type",tags = ['projects'])
async def change_member_type(project_id:str,
                       user_id:str,
                       role:str,
                       db:Session=Depends(get_db)):
    
    user_project= (db.query(model.User_Project).filter(model.User_Project.project_id == project_id,
                                                        model.User_Project.user_id == user_id)).first()
    
    if user_project is None:
        raise HTTPException(status_code=404, detail="User not found in this Project")
    
    # Set the attribute dynamically
    setattr(user_project, "member_type", role)
    
    # Commit the changes to the database
    db.add(user_project)
    db.commit()
    db.refresh(user_project)

    return {"detail": "member_type changed"} 
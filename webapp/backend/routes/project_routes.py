from fastapi import APIRouter,Depends,Response, HTTPException,security
from typing import List
from ..schemas import project_schema as schema, user_schema
from ..models import model
from sqlalchemy.orm import Session
from sqlalchemy import desc
# from ..config.db_setup import get_db
from ..config.supabase_config import get_db
from ..config.storage_config import s3_client, BUCKET_NAME
from ..services import user_functions
import passlib.hash as hash
from botocore.exceptions import NoCredentialsError, ClientError
import logging

project_route = APIRouter(prefix="/api/projects")

@project_route.get("/",response_model=List[schema.Project],tags = ['projects'])
def show_projects(db:Session=Depends(get_db)):
    projects = db.query(model.Project).order_by(desc(model.Project.project_id)).all()
    return projects

@project_route.post("/new_project/",tags = ['projects'])#,response_model=schema.Project)
async def create_project(input:schema.Project,
                         user:user_schema.User = Depends(user_functions.get_current_user),
                         db:Session=Depends(get_db),):
    #db_user = await user_functions.get_user_by_email(input.email,db)
    # if db_user:
    #     raise HTTPException(status_code=400, detail= "Email already in use")
    # else:
    print(input)
    project_obj = model.Project(project_name=input.project_name,
                                description=input.description,
                                link=input.link,
                                image=input.image)
    db.add(project_obj)
    db.commit()
    db.refresh(project_obj)

    rel_obj = model.User_Project(user_id = user.user_id,
                                project_id = project_obj.project_id,
                                member_type = "admin")
    db.add(rel_obj)
    db.commit()
    db.refresh(rel_obj)
    
    return project_obj 

@project_route.post("/upload_image/",tags = ['projects'])
async def upload_file(file):
    try:
        # Upload file to MinIO using Boto3
        s3_client.upload_fileobj(
            file.file,  # File-like object
            BUCKET_NAME,  # Target bucket name
            file.filename,  # Object name in the bucket
            ExtraArgs={"ContentType": file.content_type}  # Set content type
        )
        return {"message": f"File '{file.filename}' uploaded successfully to MinIO bucket '{BUCKET_NAME}'"}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
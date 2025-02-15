from fastapi import APIRouter,Depends,UploadFile,File,HTTPException
from typing import List
from ..schemas import organization_schema as org_schema
from ..schemas import user_schema as schema
from ..models import model
from sqlalchemy.orm import Session
#from ..config.db_setup import get_db
from ..config.supabase_config import get_db,supa_client,bucket_s3,url_s3_object
from ..services import user_functions
import numpy as np
import datetime as dt
import uuid

organization_route = APIRouter(prefix="/api/orgs")

@organization_route.post("/upload_image",tags = ['organizations'])
async def upload_image(org_id: str,
                       file: UploadFile= File(...),
                        user: schema.User = Depends(user_functions.get_current_user),
                        db: Session = Depends(get_db)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        url_photo = f"orgs/{org_id}/images/{file.filename}"
        print(url_photo)
        contents = await file.read()

        # Upload with auth headers
        response = supa_client.storage.from_(f"{bucket_s3}").upload(
            file=contents,
            path=url_photo,
            file_options={"content-type": file.content_type,
                        "cache-control": "3600", "upsert": "true",},
        )
        
        return {"filename":f"{url_s3_object}/{url_photo}", "detail": "Image uploaded","org_id":org_id}
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))



@organization_route.post("/create_org",tags = ['organizations'])
async def create_org(input:org_schema.CreateOrganization,
                     db:Session=Depends(get_db),
                     user:schema.User = Depends(user_functions.get_current_user)):

    org_obj = model.Organization(org_id=input.org_id,
                                 name = input.name,
                                 type = input.type,
                                 address = input.address,
                                 description= input.description,
                                 latitude = input.latitude,
                                 longitude = input.longitude,
                                 logo = input.logo,
                                 web_link = input.web_link,
                                 visible = input.visible,
                                 )
    
    db.add(org_obj)
    db.commit()

    rel_obj = model.User_Organization(user_id = user.user_id,
                                      org_id = org_obj.org_id,
                                      member_type = "admin")
    db.add(rel_obj)
    db.commit()

    db.refresh(org_obj)

    return {"detail": "New organization uploaded","org_details":org_obj}


@organization_route.get("/organizations",tags = ['organizations'])
async def show_organizations(db:Session=Depends(get_db)):
    orgs = db.query(model.Organization).all()
    return orgs 


@organization_route.delete("/delete_org",tags = ['organizations'])
async def delete_organization(org_id:str,
                            db:Session=Depends(get_db)):
    (db.query(model.User_Organization).filter(model.User_Organization.org_id == org_id).delete(synchronize_session='fetch'))
    (db.query(model.Organization).filter(model.Organization.org_id == org_id).delete())

    db.commit()

    return {"detail": "Organization deleted"} 

@organization_route.delete("/leave_org",tags = ['organizations'])
async def leave_organization(org_id:str,
                            user:schema.User = Depends(user_functions.get_current_user),
                            db:Session=Depends(get_db)):
    (db.query(model.User_Organization).filter(model.User_Organization.org_id == org_id,
                                              model.User_Organization.user_id == user.user_id).delete(synchronize_session='fetch'))

    db.commit()

    return {"detail": "Organization detached"} 

@organization_route.put("/join_org",tags = ['organizations'])
async def join_organization(org_id:str,
                            user:schema.User = Depends(user_functions.get_current_user),
                            db:Session=Depends(get_db)):
    admin_roles = db.query(model.User_Organization).filter(model.User_Organization.org_id == org_id,
                                              model.User_Organization.member_type == "admin").all()
    
    my_roles = db.query(model.User_Organization).filter(model.User_Organization.org_id == org_id,
                                              model.User_Organization.user_id == user.user_id).all()
    if my_roles==[]:
        if admin_roles==[]:
            rel_obj = model.User_Organization(user_id = user.user_id,
                                        org_id = org_id,
                                        member_type = "admin")
            db.add(rel_obj)
            db.commit()
        else:
            rel_obj = model.User_Organization(user_id = user.user_id,
                                        org_id = org_id,
                                        member_type = "user")
            db.add(rel_obj)
            db.commit()
        
        return {"detail": "Organization attached"} 
    else:
        raise HTTPException(status_code=422, detail="Organization already attached to this user")


@organization_route.get("/members",tags = ['organizations'])
async def join_organization(org_id:str,
                            db:Session=Depends(get_db)):
    members = db.query(model.User).join(
            model.User_Organization,
            model.User_Organization.user_id == model.User.user_id
        ).filter(model.User_Organization.org_id == org_id).all()
    my_roles = (db.query(model.User_Organization)
        .filter(model.User_Organization.org_id == org_id)).all()

    # Create a dictionary of users by user_id for fast lookups
    user_dict = {user.user_id: user for user in members}

    # Now merge by matching user_id in both lists and merge all fields
    merged_list = []
    for role in my_roles:
        org = user_dict.get(role.user_id)  # Look up the corresponding organization
        if org:
            # Merge all fields from both the organization and the role
            merged_dict = {**org.__dict__, **role.__dict__}  # Combine all fields
            merged_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state attribute
            merged_list.append(merged_dict)
        
    return merged_list
    
@organization_route.get("/locations",tags = ['organizations'])
async def show_organizations(db:Session=Depends(get_db)):
    orgs = db.query(model.Organization).filter(model.Organization.latitude.isnot(None)).filter(model.Organization.visible==True).all()
    return orgs 


@organization_route.get("/my_organizations" ,tags = ['organizations']) 
async def show_organizations(
    user: schema.User = Depends(user_functions.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all organizations associated with the current user.

    Args:
        user (schemas.User): The current authenticated user.
        db (Session): The database session.

    Returns:
        List[schemas.OrganizationUser]: A list of organizations the user is associated with.
    """
    # Query the database for organizations associated with the user
    my_orgs = (db.query(model.Organization)
        .join(
            model.User_Organization,
            model.User_Organization.org_id == model.Organization.org_id
        )
        .filter(model.User_Organization.user_id == user.user_id)).all()
    my_roles = (db.query(model.User_Organization)
        .filter(model.User_Organization.user_id == user.user_id)).all()

    # Create a dictionary of orgs by org_id for fast lookups
    org_dict = {org.org_id: org for org in my_orgs}

    # Now merge by matching org_id in both lists and merge all fields
    merged_list = []
    for role in my_roles:
        org = org_dict.get(role.org_id)  # Look up the corresponding organization
        if org:
            # Merge all fields from both the organization and the role
            merged_dict = {**org.__dict__, **role.__dict__}  # Combine all fields
            merged_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state attribute
            merged_list.append(merged_dict)


    # Return the list of organizations
    return merged_list

@organization_route.put("/update_org", tags=['organizations'])
async def update_org(key: str, 
                      value: str, 
                      org_id: str,
                      db: Session = Depends(get_db)):
    
    org= (db.query(model.Organization).filter(model.Organization.org_id == org_id)).first()

    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Check if the attribute exists on the user model
    if not hasattr(org, key):
        raise HTTPException(status_code=400, detail=f"Field '{key}' does not exist on organization")

    # Set the attribute dynamically
    setattr(org, key, value)

    # Commit the changes to the database
    db.add(org)
    db.commit()
    db.refresh(org)

    return org


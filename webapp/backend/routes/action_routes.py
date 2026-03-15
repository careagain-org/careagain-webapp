from fastapi import APIRouter,Depends,UploadFile,File,HTTPException,security
from typing import List
from ..schemas import user_schema
from ..models import model
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from ..config.supabase_config import get_db
from ..services import user_functions

action_route = APIRouter(prefix="/api/actions")

@action_route.get("/my_actions" ,tags = ['actions']) 
async def show_actions(
    user: user_schema.User = Depends(user_functions.get_current_user),
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
    my_actions = (
        db.query(model.Action)
        .outerjoin(
            model.User_Organization,
            model.User_Organization.org_id == model.Action.received_by
        )
        .outerjoin(
            model.User_Project,
            model.User_Project.project_id == model.Action.received_by
        )
        .filter(
            or_(
                model.User_Organization.user_id == user.user_id,
                model.User_Project.user_id == user.user_id
            )
        ).order_by(desc(model.Action.action_date))
        .all()
    )

    return my_actions
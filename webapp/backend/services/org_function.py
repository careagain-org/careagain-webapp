from fastapi import security, Depends, HTTPException, status, Response
from ..models import model
from ..schemas import user_schema as schema
from ..config.supabase_config import engine,Base,Session,get_db

async def get_locations(db:Session,):
    with engine.connect() as connection:
        query = db.query(model.Organization.org_name,model.Organization.latitude,model.Organization.longitude).all
        result = connection.execute(query)
        locations = result.fetchall()  # Esto devuelve una lista de tuplas
    return locations
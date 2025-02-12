

from fastapi import APIRouter,Depends,Response, HTTPException,security
from typing import List
from ..schemas import user_schema as schema
# from ..config.db_setup import get_db
from ..config.supabase_config import get_db,supa_client
from ..services import user_functions
import passlib.hash as hash
from pydantic import BaseModel
from urllib.parse import unquote
from urllib.parse import urlparse, parse_qs


storage_route = APIRouter(prefix="/api/storage")
supa = supa_client

class LoadFile(BaseModel):
    bucket: str
    filename: str
    pathfile: str
    filetype: str

@storage_route.post("/upload_image",tags = ['storage'])
def upload_image(input: LoadFile):
    try:
        with open(input.filename, 'rb') as f:
            response = supa.storage.from_(input.bucket).upload(
                file=f,
                path=input.pathfile,
                file_options={"cache-control": "3600", "upsert": "true"},
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Download error: {str(e)}")

@storage_route.post("/download_file",tags = ['storage'])
def download_image(input: LoadFile):
    
    try:
        with open(input.filename, "wb+") as f:
            response = supa.storage.from_(input.bucket).download(
                input.pathfile
            )
            f.write(response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Download error: {str(e)}")
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to supabase storage
url_s3: str = os.environ.get("SUPABASE_S3_URL")
bucket_s3: str = os.environ.get("SUPABASE_S3_BUCKET")
url_s3_object: str = f"{os.environ.get("SUPABASE_S3_URL")}object/public/{os.environ.get("SUPABASE_S3_BUCKET")}"

# Set supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
schema: str = os.environ.get("SUPABASE_DB_SCHEMA")
supa_client: Client = create_client(url, key)

# Connect to supabase DB using sqlalchemy
uri_db: str = os.environ.get("SUPABASE_DB_URI")

engine = create_engine(uri_db)   
SessionLocal = sessionmaker(autocommit = False,autoflush = False, bind =engine)
Base = declarative_base()
conn = engine.connect()
meta = MetaData()

def get_db():
    try:
        db =SessionLocal()
        yield db
    finally:
        db.close()

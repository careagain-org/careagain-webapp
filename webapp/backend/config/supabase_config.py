from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to supabase storage
url: str = os.environ.get("SUPABASE_URL")
bucket_s3: str = os.environ.get("SUPABASE_S3_BUCKET")
url_s3_object: str = f"{os.environ.get("SUPABASE_URL")}storage/v1/object/public/{os.environ.get("SUPABASE_S3_BUCKET")}"

# Set supabase client
key: str = os.environ.get("SUPABASE_ANON_KEY")
schema: str = os.environ.get("SUPABASE_DB_SCHEMA")
supa_client: Client = create_client(url, key)

# Connect to supabase DB using sqlalchemy
uri_db: str = os.environ.get("SUPABASE_DB_URI")

engine = create_engine(uri_db,
                       pool_size=10,  # Adjust based on your needs
                        max_overflow=5,  # Additional connections allowed beyond pool_size
                        pool_timeout=30,  # Timeout for acquiring a connection
                        pool_recycle=1800,  # Recycle connections after 30 minutes
                    )  
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

# local --> to be replaced by supabase

# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import sessionmaker,Session
# from sqlalchemy.ext.declarative import declarative_base
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# URL_DATABASE = os.environ.get("URL_DATABASE")

# engine = create_engine(URL_DATABASE)
# SessionLocal = sessionmaker(autocommit = False,autoflush = False, bind =engine)
# Base = declarative_base()
# conn = engine.connect()
# meta = MetaData()

# def get_db():
#     try:
#         db =SessionLocal()
#         yield db
#     finally:
#         db.close()

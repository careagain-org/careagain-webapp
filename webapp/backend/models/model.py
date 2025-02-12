from sqlalchemy import Table,Boolean,Column, Integer, String,Float,DATE, ForeignKey,DATETIME,JSON, Text, UUID
from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.hybrid import hybrid_property
from ..config.supabase_config import Base,engine
from geopy.geocoders import Nominatim
import certifi
import datetime as dt
import passlib.hash as hash
import ssl
import os
import json
import uuid
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())


supabase_schema: str = os.environ.get("SUPABASE_DB_SCHEMA")


class User(Base):
    __tablename__='users'
    __table_args__ = {'schema': supabase_schema}

    user_id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    username = Column(String(255),unique=True)
    first_name = Column(String(255))
    last_name1 = Column(String(255))
    last_name2 = Column(String(255))
    profile_image = Column(String(255))
    country = Column(String(255))
    role = Column(String(255))
    active = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)
    visible = Column(Boolean, default=True)
    deactivation_date = Column(DATE)


class Organization(Base):
    __tablename__='organizations'
    __table_args__ = {'schema': supabase_schema}
    org_id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    name = Column(String(255))
    type = Column(String(255))
    description = Column(Text)
    address = Column(String(255))
    latitude = Column(Float,default=None)
    longitude = Column(Float,default=None)
    logo = Column(String(255)) 
    web_link = Column(String(255)) 
    activation_date = Column(DATE,default=dt.date.today)
    active = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)
    visible = Column(Boolean)
    storage_path  = Column(String(255))
    

class User_Organization(Base):
    __tablename__='users_orgs'
    __table_args__ = {'schema': supabase_schema}

    rel_uo_id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey(f"{supabase_schema}.users.user_id"))
    org_id = Column(UUID(as_uuid=True),ForeignKey(f"{supabase_schema}.organizations.org_id"))
    member_type = Column(String(255))


class Project(Base):
    __tablename__= 'projects'
    __table_args__ = {'schema': supabase_schema}
    project_id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    name = Column(String(100))
    type = Column(String(255))
    link = Column(String(255))
    description = Column(Text)
    image = Column(String(255))
    logo = Column(String(255))



class User_Project(Base):
    __tablename__= 'users_projects'
    __table_args__ = {'schema': supabase_schema}
    rel_up_id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey(f"{supabase_schema}.users.user_id"))
    project_id = Column(UUID(as_uuid=True),ForeignKey(f"{supabase_schema}.projects.project_id"))
    member_type = Column(String(255))


class Video(Base):
    __tablename__= 'videos'
    __table_args__ = {'schema': supabase_schema}
    video_id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    name = Column(String(100))
    description = Column(String(255))
    youtube_link = Column(String(255))
    created_by = Column(UUID(as_uuid=True),ForeignKey(f"{supabase_schema}.users.user_id"))
    deleted = Column(Boolean,default=False)


class Question(Base):
    __tablename__= 'questions'
    __table_args__ = {'schema': supabase_schema}
    question_id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    title = Column(String(255))
    question = Column(String(255))
    comments = Column(JSON)
    created_by = Column(UUID(as_uuid=True),ForeignKey(f"{supabase_schema}.users.user_id"))
    deleted = Column(Boolean,default=False)
    # file_link = Column(String(255))

    @hybrid_property
    def comments(self):
        if self._comments:
            return json.loads(self._comments)
        return {}

    @comments.setter
    def comments(self, value):
        self._comments = json.dumps(value)



# class Session(Base):
#     __tablename__='sessions'
#     session_id = Column(Integer,primary_key=True,index=True)
#     user_id = Column(Integer,ForeignKey("users.user_id"))
#     token = Column(String(255))
#     login_datetime = Column(DATETIME,default=dt.datetime.now)
#     logout_datetime = Column(DATETIME)

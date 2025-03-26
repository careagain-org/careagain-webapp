"""Welcome to Reflex! This file outlines the steps to create a basic app."""

# frontend imports
import reflex as rx
from webapp.frontend.pages import (ind_org_view, ind_org_edit, 
                                   ind_project_view, ind_project_edit, 
                                   ind_user_view,
                                   webpage,login, projects, signup,
                                   platform, projects, profile,
                                   videos,community, questions,
                                   reset_password) #contact,community,
from webapp.frontend.constants import urls
from rxconfig import config

# backend imports
# import fastAPI modules
from fastapi import FastAPI,Depends,security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# import routes from the backend
from webapp.backend.routes.default import default
from webapp.backend.routes.user_routes import user_route
from webapp.backend.routes.project_routes import project_route
from webapp.backend.routes.video_routes import video_route
from webapp.backend.routes.organizations_routes import organization_route
from webapp.backend.routes.question_routes import question_route
from webapp.backend.routes.auth_routes import auth_route

# import model and db
from webapp.backend.models import model
from webapp.backend.config.supabase_config import engine,Base,Session
from webapp.backend.config.tags_metadata import tags_metadata
import logging
# load env
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())


## ---------------- LOGGING CONFIG APP ---------------------- ##

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

## ---------------- RUN FRONTEND APP ---------------------- ##
app = rx.App(
    theme=rx.theme(
        appearance="light", 
        has_background=True, 
        panel_background="solid",
        scaling="90%",
        radius="medium", 
        accent_color="teal"
    )
)

## ---------------- ADD BACKEND --------------------------- ##

# create table in the database
model.Base.metadata.create_all(bind=engine)
model.automap_base()

# add all routes
app.api.include_router(default)
app.api.include_router(user_route)
app.api.include_router(project_route)
app.api.include_router(video_route)
app.api.include_router(organization_route)
app.api.include_router(question_route)
app.api.include_router(auth_route)

# CORS middleware to allow communication between frontend and backend
origins = [urls.WEB_URL,
           urls.API_URL] # specify the http where the api is going to run

app.api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

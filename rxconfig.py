import reflex as rx
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

SUPABASE_DB_URI = os.environ.get("SUPABASE_DB_URI")
ENV_API_URL = os.environ.get("API_URL")

config = rx.Config(
    app_name="webapp",
    stylesheets=[
        "/fonts/ArialRoundedMTBold/arial_rounded.css",  # This path is relative to assets/
    ],
    db_url=SUPABASE_DB_URI,
    api_url="https://api.careagain.org",#ENV_API_URL,
    frontend_port=3000,
    backend_port=8000
)
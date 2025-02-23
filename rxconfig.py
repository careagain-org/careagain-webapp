import reflex as rx
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

SUPABASE_DB_URI = os.environ.get("SUPABASE_DB_URI")

config = rx.Config(
    app_name="webapp",
    stylesheets=[
        "/fonts/ArialRoundedMTBold/arial_rounded.css",  # This path is relative to assets/
    ],
    # style = {
    #     "font_family": "Arial Rounded",
    #     "font_size": "16px",
    # },
    db_url = SUPABASE_DB_URI,
    frontend_port=3000,
    deploy_url='http://localhost:3000',
    api_url = "http://localhost:8000"
)
import reflex as rx
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

SUPABASE_DB_URI = os.environ.get("SUPABASE_DB_URI")
ENV_API_URL = os.environ.get("REFLEX_API_URL")

config = rx.Config(
    app_name="webapp",
    stylesheets=[
        "/fonts/ArialRoundedMTBold/arial_rounded.css",  # This path is relative to assets/
    ],
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.sitemap.SitemapPlugin(),
    ],
    # disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    
    # This is the URL of the Supabase database, which is used to store and retrieve
    # data for the application. It is set in the environment variable SUPABASE_DB_URI
    # and is used to connect to the Supabase database.
    backend_host="0.0.0.0",
    db_url=SUPABASE_DB_URI,
    api_url=ENV_API_URL,
    show_built_with_reflex=False,
)
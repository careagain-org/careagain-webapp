# ============================================================
# MedTrack QR — FastAPI Backend
# ============================================================
# Install: pip install fastapi uvicorn supabase python-dotenv pydantic
# Run:     uvicorn main:app --reload
# ============================================================

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from starlette.responses import RedirectResponse

from config.supabase_config import supa_client

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.supabase = supa_client
    yield

app = FastAPI(
    title="MedTrack QR API",
    description="Medical equipment management for LMICs",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "medtrack-api"}

@app.get('/')
def default_route():
    return RedirectResponse(url="/docs")
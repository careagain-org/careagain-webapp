from fastapi import APIRouter, Request, HTTPException, Depends
from ..config.supabase_config import get_db
from svix.webhooks import Webhook
from ..services.user_functions import create_user,delete_user,update_user
import os
import json

clerk_route = APIRouter(prefix="/api/clerk")

@clerk_route.post("/webhooks",tags=["clerk"])
async def handle_user_created(request: Request, db = Depends(get_db)):
    
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")

    if not webhook_secret:
        raise HTTPException(status_code=500, detail="CLERK_WEBHOOK_SECRET not set")

    body = await request.body()
    payload = body.decode("utf-8")
    headers = request.headers

    try:
        wh = Webhook(webhook_secret)
        wh.verify(payload, headers)

        data = json.loads(payload)

        if data.get("type") == "user.created":
            user_data = data.get("data", {})
            create_user(user_data,db)
            return {"status": "success"}
        elif data.get("type") == "user.deleted":
            user_data = data.get("data", {})
            delete_user(user_data,db)
            return {"status": "success"}

        elif data.get("type") == "user.updated":
            user_data = data.get("data", {})
            update_user(user_data,db) 
            return {"status": "success"}

        else:
            return {"status": "ignored"}

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
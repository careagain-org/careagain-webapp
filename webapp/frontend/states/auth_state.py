"""The authentication state."""
import reflex as rx
import reflex_clerk_api as reclerk
import httpx
from ..constants import urls
from typing import Optional,Dict
import threading
from urllib.parse import urlparse, parse_qs
import json
import asyncio
import jwt
import http.cookiejar
import urllib
import os
from datetime import datetime, timedelta, timezone
# from ..states.user_state import UserState

jwt_key = os.getenv("JWT_KEY")
secret_key = os.getenv("CLERK_SECRET_KEY")

class AuthState(rx.State):
    email: str = ""
    password: str = ""
    subject: str
    cookie_user: Optional[str] = rx.Cookie(
        name="user", max_age=3600,
        path="/",
        same_site="lax",
        secure=True,
    )
    token: Optional[str] = rx.Cookie(
        name="auth_token", max_age=30,
        path="/",
        same_site="lax",
        secure=True,
    )

    async def set_user_cookie(self) -> Optional[str]:
        clerk_state = await self.get_state(reclerk.ClerkState)
        if clerk_state.is_signed_in:
            user = clerk_state.user_id
            self.cookie_user = user
        else:
            self.cookie_user = None


    async def set_auth_token(self) -> Optional[str]:
        clerk_state = await self.get_state(reclerk.ClerkState)
        clerk_user = await self.get_state(reclerk.ClerkUser)
        
        if clerk_state.is_signed_in:
            payload = {
                "role": "authenticated",
                'id': clerk_state.user_id,
                'username': clerk_user.username,
                'first_name': clerk_user.first_name,
                'last_name': clerk_user.last_name,
                'profile_image_url': clerk_user.image_url,
                'exp': datetime.now(timezone.utc) + timedelta(seconds=60)  # Token expiration time
            }
            auth_token = jwt.encode(payload, secret_key, algorithm='HS256')
            self.token = auth_token
            return auth_token
        else:
            self.token = None
            return None
    
   
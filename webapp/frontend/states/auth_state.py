"""The authentication state."""
import reflex as rx
import httpx
from ..constants import urls
from typing import Optional,Dict
import threading
from urllib.parse import urlparse, parse_qs
import json
import asyncio
# from ..states.user_state import UserState

class AuthState(rx.State):
    email: str = ""
    password: str = ""
    token: Optional[str] = rx.Cookie(
                name="token",
                # same_site="strict",
                secure=True,
            ) 
    
    @rx.var(cache=True)
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        return self.token is not None

    def set_email(self, value: str):
        self.email = value

    def set_password(self, value: str):
        self.password = value
    
    
    # @rx.event(background=True)
    # async def auto_refresh(self):
    #     while self.is_authenticated:
    #         await asyncio.sleep(60 * 10)  # Every 10 mins
    #         await self.refresh_login()
            
    
    @rx.event
    async def handle_login(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{urls.API_URL}/api/auth/token",
                    data={
                        "username": self.email,
                        "password": self.password,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
            if response.status_code == 200:
                response_data = response.json()
                if response_data:
                    access_token = response_data.get("access_token")
                    
                    self.token=access_token
                    self.is_authenticated = True
                    # After calculation is done, chain to StoreEventsState
                    # lambda: UserState.get_token(self.token)
                    return [rx.redirect(urls.PLATFORM_URL),rx.toast.success(f'Successfully sign in!')]    
                else:
                    return rx.toast.error("No access token in response")
            else:
                response_detail = response.json().get("detail")
                self.token=None
                self.is_authenticated = False
                return rx.toast.error(f"{response_detail}")
        
        except Exception as err:
            self.token=None
            self.is_authenticated = False
            return rx.toast.error(f"There was an unexpected error:{err}")

    async def handle_signup(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{urls.API_URL}/api/auth/sign_up",
                    json={
                        "email": self.email,
                        "password": self.password,
                    },
                )
            
            if response.status_code == 200:
                response_detail = response.json().get("detail")
                return [rx.toast.success(f"{response_detail}")]

            else:
                response_details = response.json().get("detail")
                return rx.toast.error(f"{response_details}")
        
        except Exception as err:
            response_detail = response.json().get("detail")
            return rx.toast.error(f"{response_detail}")
        
        
    async def handle_logout(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/auth/sign_out",
            )

        if response.status_code == 200:
            response_data = response.json()
            self.email = ""
            self.password = ""
            self.is_authenticated = False
            self.token = None
            return [rx.remove_cookie("token"),rx.redirect(urls.HOME_URL),rx.toast.success('Successfully sign out!')]
        
        else:
            response_details = response.json().get("detail")
            return rx.toast.error(f"{response_details}")
        
    async def reset_password(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{urls.API_URL}/api/auth/reset_password",
                json={
                        "email": self.email,
                        "password": self.password,
                    },
            )

        if response.status_code == 200:
            response_data = response.json()
            self.is_authenticated = False
            return [rx.toast.success('Email sent to the email to reset your password')]
        
        else:
            response_details = response.json().get("detail")
            return rx.toast.error(f"{response_details}")
    
    async def update_password(self):
        url = self.router.page.raw_path
        access_token = url.split('access_token=')[1].split("&expires_at")[0]
        refresh_token = url.split('refresh_token=')[1].split("&token_type")[0]

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/auth/update_password",
                    json={
                            "email": self.email,
                            "password": self.password,
                            "token":access_token,
                            "refresh_token":refresh_token
                        },
            )

        if response.status_code == 200:
            response_data = response.json()
            self.is_authenticated = False
            return [rx.toast.success('Password updated!')]
        
        else:
            response_details = response.json().get("detail")
            return rx.toast.error(f"{response_details}")
    
    async def login_without_password(self):
       
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{urls.API_URL}/api/auth/token",
                    json={
                            "email": self.email,
                            "password": "",
                        },
            )

        if response.status_code == 200:
            response_data = response.json()
            self.is_authenticated = False
            return [rx.toast.success('An email has been sent. You will be able to access to the platform and change password.')]
        
        else:
            response_details = response.json().get("detail")
            return rx.toast.error(f"{response_details}")
             
    
    @rx.event
    async def check_session(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/auth/current_user",
                )
            if response.status_code == 200:
                access_token = response.json().get("access_token")
                if access_token:
                    self.token=access_token
                    self.is_authenticated = True
            else:
                response_detail = response.json().get("detail")
                self.is_authenticated = False
                return [rx.redirect(urls.LOGIN_URL),rx.toast.warning(f"Auth error {response_detail}")]
        
        except Exception as err:
            self.is_authenticated = False
            return rx.toast.warning(err)
        


    @rx.event
    async def refresh_login(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{urls.API_URL}/api/auth/refresh_session",
                )
            if response.status_code == 200:
                access_token = response.json().get("access_token")
                if access_token:
                    self.token=access_token
                    self.is_authenticated = True
            else:
                response_detail = response.json().get("detail")
                self.is_authenticated = False
                return rx.toast.error(f"Not authenticated or session expired")
        
        except Exception as err:
            self.is_authenticated = False
            return rx.toast.error(f"There was an unexpected error: {err}")

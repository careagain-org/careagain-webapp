"""The authentication state."""
import reflex as rx
import httpx
from ..constants import urls
from typing import Optional,Dict
import threading
from urllib.parse import urlparse, parse_qs

class AuthState(rx.State):
    email: str = ""
    password: str = ""
    auth_response: str = ""
    token: Optional[str] = rx.LocalStorage()
    is_authenticated: bool = False
    error_message: str = ""

    def set_email(self, value: str):
        self.email = value

    def set_password(self, value: str):
        self.password = value
    
    async def handle_login(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{urls.API_URL}api/auth/sign_in",
                    json={
                        "email": self.email,
                        "password": self.password,
                    })
                print(response)
            
            if response.status_code == 200:
                response_data = response.json()
                self.is_authenticated = True
                return [rx.redirect(urls.PLATFORM_URL),rx.toast.success('Successfully sign in!')]
            else:
                response_detail = response.json()["details"]
                self.is_authenticated = False
                return rx.toast.error(f"{response_detail}")
        
        except Exception as err:
            self.is_authenticated = False
            error_message = "There was an unexpected error"
            return rx.toast.error(error_message)

    async def handle_signup(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{urls.API_URL}api/auth/sign_up",
                    json={
                        "email": self.email,
                        "password": self.password,
                    },
                )
            
            if response.status_code == 200:
                response_details = response.json()["details"]
                return [rx.redirect(urls.LOGIN_URL),rx.toast.success(f"{response_details}")]

            else:
                response_details = response.json()["details"]
                return rx.toast.error(f"{response_details}")
        
        except Exception as err:
            response_details = response.json()["detail"]
            return rx.toast.error(f"{response_details}")
        
    async def handle_logout(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}api/auth/sign_out",
            )

        if response.status_code == 200:
            response_data = response.json()
            self.is_authenticated = False
            self.token = None
            return [rx.redirect(urls.HOME_URL),rx.toast.success('Successfully sign out!')]
        
        else:
            response_details = response.json()["detail"]
            return rx.toast.error(f"{response_details}")
        
    async def reset_password(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{urls.API_URL}api/auth/reset_password",
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
            response_details = response.json()["detail"]
            return rx.toast.error(f"{response_details}")
    
    async def update_password(self):
        url = self.router.page.raw_path
        access_token = url.split('=')[1].split("&")[0]

        print(access_token)
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}api/auth/update_password",
                    json={
                            "email": self.email,
                            "password": self.password,
                            "token":access_token
                        },
            )

        if response.status_code == 200:
            response_data = response.json()
            self.is_authenticated = False
            return [rx.toast.success('Password updated!')]
        
        else:
            response_details = response.json()["detail"]
            return rx.toast.error(f"{response_details}")
    
    async def login_without_password(self):
       
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{urls.API_URL}api/auth/login_without_password",
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
            response_details = response.json()["detail"]
            return rx.toast.error(f"{response_details}")

    
    # # Check if the user is authenticated by verifying the token
    # def check_auth(self):
    #     if self.token:
    #         # Optionally, add token validation logic here
    #         self.is_authenticated = True
    #     else:
    #         self.is_authenticated = False
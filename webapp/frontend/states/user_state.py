import reflex as rx
import httpx
from ..constants import urls
from typing import List, Dict 
from .auth_state import AuthState


class UserState(AuthState):
    
    my_details: Dict[str, str]

    async def get_my_details(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}api/auth/current_user"
                #headers={"Authorization": f"Bearer {self.token}"}
            )
        
        if response.status_code == 200:
            self.my_details = response.json()["data"]

            print(f"Successfull get user")
        else:
            print(f"Failed to get user: {response.status_code} ")

    async def update_user(self,key:str,value):
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}api/users/update_user",
                json={"key": key, "value": value},
                headers = {"Authorization": f"Bearer {self.token}"}
            )
        
        if response.status_code == 200:
            self.my_details = response.json()
            print(f"User name updated successfully")
        else:
            print(f"Failed to update user name: {response.status_code}, {response.text}")


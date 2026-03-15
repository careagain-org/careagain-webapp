import reflex as rx
import httpx
from ..constants import urls
from typing import List, Dict, Any, Optional
from .auth_state import AuthState
import datetime as dt

class ActionState(rx.State):
    my_notifications: List[Dict[str, Any]] = []
    token:Optional[str]=rx.Cookie(
                name=f"__session",
            ) 
    
    async def get_my_actions(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/actions/my_actions",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            self.my_notifications = response.json()
            
        else:
            print(f"Failed to get orgs: {response.status_code}, {response.text}")
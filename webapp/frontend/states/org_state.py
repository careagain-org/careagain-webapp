import reflex as rx
import httpx
from ..constants import urls
from typing import List, Dict, Any
from .auth_state import AuthState
import requests

class OrgState(rx.State):
    orgs: List[Dict[str, str]] = []
    orgs_locations: List[Dict[str, float]] = []
    org_id:str=""
    selected_org: Dict[str, str] = {}


    async def get_my_orgs(self,my_state:AuthState):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}api/orgs/my_organizations",
                headers = {"Authorization": f"Bearer {my_state.token}"}
            )
        
        if response.status_code == 200:
            self.orgs = response.json()
            return self.orgs
        else:
            print(f"Failed to get orgs: {response.status_code}, {response.text}")

    async def get_orgs(self) :

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}api/orgs/organizations",
            )
        
        if response.status_code == 200:
            self.orgs = response.json()
            return self.orgs
        else:
            print(f"Failed to get orgs: {response.status_code}, {response.text}")

    async def get_location(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}api/orgs/locations",
                )
            if response.status_code == 200:
                self.orgs_locations = response.json()
            else:
                print(f"Failed to get orgs: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def select_org(self,org_id:str):
        self.org_id = org_id
        self.selected_org = [d for d in self.orgs_locations if d['org_id']==int(org_id)][0]
        return rx.redirect(f"/{urls.INDIVIDUAL_ORG_URL}{org_id}")


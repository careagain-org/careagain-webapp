import reflex as rx
import httpx
import requests
from ..constants import urls
from typing import List, Dict
from .auth_state import AuthState 
import logging
import json 


class ProjectState(rx.State):
    projects: List[Dict[str, str]] = []
    selected_id:str=""
    selected_project: Dict[str, str] = {}

    async def get_list_projects(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}api/projects/",
            )
        
        if response.status_code == 200:
            self.projects = response.json()
 
    async def create_project(self,user_details=Dict[str,str]):
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{urls.API_URL}api/projects/new_project/",
                json.dumps(user_details))
            
        if response.status_code == 200:
            self.projects = response.json()
  
            logging("Project created successfully:", response.json())
        else: 
            logging("Failed to create project:", response.status_code)

    # async def create_project(self):

    #     async with httpx.AsyncClient() as client:
    #         response = await client.post(
    #             f"{urls.API_URL}api/projects/new_project/",
    #             headers = {"Authorization": f"Bearer {token}"},
    #         )
        
    #     if response.status_code == 200:
    #         self.projects = response.json()
    
    def select_project(self,selected_id:str):
        self.selected_id = selected_id
        self.selected_project = [d for d in self.projects if d['project_id']==int(selected_id)][0]
        return rx.redirect(f"/{urls.INDIVIDUAL_PROJECT_URL}{selected_id}")
    
    # async def get_individual_project(self):

    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(
    #             f"{urls.API_URL}api/projects/project{id_project}",
    #         )
        
    #     if response.status_code == 200:
    #         self.projects = response.json()

        
    

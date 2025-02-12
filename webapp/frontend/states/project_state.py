import reflex as rx
import httpx
import requests
from ..constants import urls
from typing import List, Dict
from .auth_state import AuthState 
import logging
import json 


class ProjectState(AuthState):
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
 
    async def create_project(self,project_details:Dict[str,str]):
        try:
            print(project_details)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{urls.API_URL}api/projects/new_project/",
                    json=project_details,
                    headers = {"Authorization": f"Bearer {self.token}"}
                    )
                
            if response.status_code == 200:
                self.project = response.json()
        except Exception as err:
            logging(f"Failed to create project:{err}")

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
    
    async def upload_image(self,file: rx.UploadFile):
        try:
            with open(file, "rb") as f:
                async with httpx.AsyncClient() as client:
                    # Make the asynchronous POST request
                    response = await client.post(f"{urls.API_URL}api/users/upload_image", 
                                    headers = {"Authorization": f"Bearer {self.token}",
                                                "Content-Type": "multipart/form-data"},
                                    file = f)
            
            if response.status_code == 200:
                self.my_details = response.json()["user_details"]
                return rx.toast(f"{response.json()["detail"]}")
            else:
                detail = response.json()["detail"]
                return rx.toast(f"User update error: {response.status_code}, {detail}")
        except:
            return rx.toast("Unexpected error")
    
    # async def get_individual_project(self):

    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(
    #             f"{urls.API_URL}api/projects/project{id_project}",
    #         )
        
    #     if response.status_code == 200:
    #         self.projects = response.json()

        
    

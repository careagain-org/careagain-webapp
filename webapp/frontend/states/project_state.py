import reflex as rx
import httpx
import requests
from ..constants import urls
from typing import List, Dict,Any
from .auth_state import AuthState 
import logging
import json 
import uuid


class ProjectState(AuthState):
    projects: List[Dict[str, str]] = []
    filtered_projects: List[Dict[str, str]] = []
    my_projects: List[Dict[str, str]] = []
    searched_projects: List[Dict[str, str]] = projects
    
    project_details: Dict[str, Any] = {}
    project_members: List[Dict[str, Any]] = []
    project_id:str=""
    selected_project: Dict[str, Any] = {}
    logo: str =None
    image: str = None
    
    def reset_project(self):
        self.logo =None
        self.image =None
        
    async def load_project_page(self):
        current_page_url = self.router.page.raw_path
        project_id =current_page_url.split("/")[-2]
        self.select_project(project_id)
        await self.find_members_project()
        

    async def get_list_projects(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/projects/",
            )
        
        if response.status_code == 200:
            self.projects = response.json()
            self.searched_projects = response.json()
 
    
    def select_project(self,project_id:str):
        self.project_id = project_id
        self.selected_project = [d for d in self.projects if d['project_id']==(project_id)][0]
    
    
    @rx.event
    async def handle_upload_image(self, my_files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        try:

            file=my_files[0]
            upload_data = await file.read()
            self.image = f"{uuid.uuid4()}.png"
            outfile = rx.get_upload_dir() / self.image

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

        except Exception as err:
            return rx.toast(err)
        
        
    @rx.event
    async def handle_upload_logo(self, my_files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        try:

            file=my_files[0]
            upload_data = await file.read()
            self.logo = f"{uuid.uuid4()}.png"
            outfile = rx.get_upload_dir() / self.logo

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

        except Exception as err:
            return rx.toast(err)
        
        
    @rx.event
    async def upload_project(self, my_files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        try:

            file=my_files[0]
            upload_data = await file.read()
            self.image = f"{uuid.uuid4()}.png"
            outfile = rx.get_upload_dir() / self.image

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

        except Exception as err:
            return rx.toast(err)
        
        
    async def supabase_upload(self,project_id,filename):
        try:
            outfile = rx.get_upload_dir() / filename

            with open(outfile, "rb") as image_file:
                files = {"file": (filename, image_file, "image/png")}
                data = {"project_id": project_id}
                headers = {"Authorization": f"Bearer {self.token}"}

                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{urls.API_URL}/api/projects/upload_image?project_id={project_id}", 
                                                files=files, data=data, headers=headers)

                if response.status_code == 200:
                    return response.json()["project_id"]
                else:
                    detail = response.json()["detail"]
                    return rx.toast(f"User update error: {response.status_code}, {detail}")
        except Exception as e:
            return rx.toast(f"File upload error: {str(e)}")
        
        
    async def create_new_project(self, form_data: dict):
        try:
            project_id = str(uuid.uuid4())

            if self.logo:
                await self.supabase_upload(project_id,self.logo)
            if self.image:
                await self.supabase_upload(project_id,self.image)

            input_data = {
                "project_id": project_id, 
                "name": form_data["name"],
                "type": form_data["type"],
                "status": form_data["status"],
                "description": form_data["description"],
                "logo": f"{self.logo}" if self.logo else "",
                "image": f"{self.image}" if self.image else "",
                "website": form_data["website"],
                "attachment": form_data["attachment"],
                "guide": form_data["guide"],
                "repo": form_data["repo"],
            }

            headers = {"Authorization": f"Bearer {self.token}"}

            async with httpx.AsyncClient() as client:
                response = await client.post(f"{urls.API_URL}/api/projects/create_project", 
                                            json=input_data, headers=headers)

            if response.status_code == 200:
                self.project_details = response.json()["project_details"]
                self.reset_project()
                await self.get_my_projects()
                await self.get_list_projects()
                return rx.toast("New project uploaded")
            else:
                detail = response.json()["detail"]
                return rx.toast(f"Project update error: {response.status_code}, {detail}")
        except Exception as err:
            return rx.toast(f"Project creation error: {str(err)}")
        
        
    async def delete_project(self,project_id):

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{urls.API_URL}/api/projects/delete_project?project_id={project_id}",
                # headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_projects()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to delete project: {response.status_code}, {response.text}")
        
    
    async def leave_project(self,project_id):

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{urls.API_URL}/api/projects/leave_project?project_id={project_id}",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_projects()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to leave project: {response.status_code}, {response.text}")
        

    async def join_project(self):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/projects/join_project?project_id={self.project_id}",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_projects()
            self.filtered_projects=[]
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to join project: {response.status_code}, {response.text}")
        
    
    async def filter_project(self,value:str=""):
        self.filtered_projects = [d for d in self.projects if (value.lower() in d['name'].lower()) and (value!="")]
        
    async def search_project(self,form_data):
        if form_data["search"]=="":
            self.searched_projects =self.projects
        else:
            self.searched_projects = [d for d in self.projects if (form_data["search"].lower() in (d['name']+d['description']+d["type"]).lower()) 
                                      and (form_data["search"]!="")]
        
        
    async def get_my_projects(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/projects/my_projects",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            self.my_projects = response.json()
        else:
            print(f"Failed to get projects: {response.status_code}, {response.text}")
            
            
    def to_project_view(self,project_id:str):
        self.project_id = project_id
        self.selected_project = [d for d in self.projects if d['project_id']==project_id][0]
        return rx.redirect(f"{urls.IND_PROJECT_URL}/{project_id}")
    
    
    def to_project_edit(self,project_id:str):
        self.project_id = project_id
        self.selected_project = [d for d in self.projects if d['project_id']==project_id][0]
        return rx.redirect(f"{urls.IND_EDIT_PROJECT_URL}/{project_id}")
    
    
    async def user_dettached_project(self,user_id:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/projects/user_dettached_project?project_id={self.project_id}&user_id={user_id}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.find_members_project()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to dettached project: {response.status_code}, {response.text}")
        
        
    async def user_join_project(self,user_id:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/projects/user_join_project?project_id={self.project_id}&user_id={user_id}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.find_members_project()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to join project: {response.status_code}, {response.text}")
        
        
    async def find_members_project(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/projects/members?project_id={self.project_id}",
                )
            if response.status_code == 200:
                self.project_members = response.json()
            else:
                print(f"Failed to get projects: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    
    async def change_member(self,user_id:str,role:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/projects/change_member_type?project_id={self.project_id}&user_id={user_id}&role={role}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.find_members_project()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Change member type: {response.status_code}, {response.text}")
        
    
    async def update_project(self,key:str,value:str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{urls.API_URL}/api/projects/update_project?key={key}&value={value}&project_id={self.project_id}",
                    headers = {"Authorization": f"Bearer {self.token}"}
                )
            
            if response.status_code == 200:
                self.selected_project = response.json()
                return rx.toast.success(f"{key} updated successfully")
            else:
                detail = response.json()["detail"]
                return rx.toast.error(f"project update error: {detail}")
        except Exception as err:
            return rx.toast(f"Unexpected error: {err}")

    
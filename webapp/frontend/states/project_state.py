from fileinput import filename
from datetime import datetime, timedelta, timezone
import reflex_clerk_api as reclerk
import jwt
import reflex as rx
import httpx
import requests
from ..constants import urls
from typing import List, Dict,Any,Optional
from .auth_state import AuthState 
import logging
import json 
import uuid
import os
import glob

secret_key = os.getenv("CLERK_SECRET_KEY")

class ProjectState(rx.State):
    projects: List[Dict[str, str]] = []
    filtered_projects: List[Dict[str, str]] = []
    my_projects: List[Dict[str, str]] = []
    searched_projects: List[Dict[str, str]] = projects
    
    project_details: Dict[str, Any] = {}
    project_members: List[Dict[str, Any]] = []
    project_orgs : List[Dict[str, Any]] = []
    project_id:str=""
    selected_project: Dict[str, Any] = {}
    logo: str = None
    image: str = None
    is_project_member: bool = False
    token:Optional[str]=rx.Cookie(
                name="auth_token", max_age=30,
                path="/",
                same_site="lax",
                secure=True,
            ) 
    
    
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
                'sub': clerk_state.user_id,
                'exp': datetime.now(timezone.utc) + timedelta(seconds=60)  # Token expiration time
            }
            auth_token = jwt.encode(payload, secret_key, algorithm='HS256')
            self.token = auth_token
            return auth_token
        else:
            self.token = None
            return None
    
    def reset_project(self):
        self.logo =None
        self.image =None
        
    async def load_project_page(self):
        current_page_url = self.router.page.raw_path
        project_id =current_page_url.split("/")[-2]
        self.select_project(project_id)
        await self.find_members_project()
        await self.find_orgs_project()
        

    async def get_list_projects(self):
        self.token = await self.set_auth_token()
        
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
            self.token = await self.set_auth_token()

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
            self.token = await self.set_auth_token()

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
            self.token = await self.set_auth_token()
            file=my_files[0]
            upload_data = await file.read()
            self.image = f"{uuid.uuid4()}.png"
            outfile = rx.get_upload_dir() / self.image

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

        except Exception as err:
            return rx.toast(err)
    
    async def remove_uploaded_files(self):
        files = glob.glob(f"{rx.get_upload_dir()}/*")
        for f in files:
            os.remove(f)
        
    async def supabase_upload_logo(self,project_id):
        try:
            self.token = await self.set_auth_token()
            outfile = rx.get_upload_dir() / self.logo

            with open(outfile, "rb") as image_file:
                files = {"file": (self.logo, image_file, "image/png")}
                data = {"project_id": project_id}
                headers = {"Authorization": f"Bearer {self.token}"}

                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{urls.API_URL}/api/projects/upload_image?project_id={project_id}", 
                                                files=files, data=data, headers=headers)

                if response.status_code == 200:
                    try:
                        logo  = f"{os.environ.get('SUPABASE_URL')}storage/v1/object/public/{os.environ.get('SUPABASE_S3_BUCKET')}/projects/{self.project_id}/images/{self.logo}"
                        await self.update_project("logo",logo)
                        await self.remove_uploaded_files()
                    except Exception as e:
                        await self.remove_uploaded_files()
                        return rx.toast(f"Logo upload error: {str(e)}")
                    self.logo = None
                    self.project_details = response.json()["project_id"]
                else:
                    detail = response.json()["detail"]
                    self.logo = None
                    return rx.toast(f"Project update error: {response.status_code}, {detail}")
        except Exception as e:
            self.logo = None
            return rx.toast(f"File upload error: {str(e)}")
        
        
    async def supabase_upload_image(self,project_id):
        try:
            self.token = await self.set_auth_token()
            outfile = rx.get_upload_dir() / self.image

            with open(outfile, "rb") as image_file:
                files = {"file": (self.image, image_file, "image/png")}
                data = {"project_id": project_id}
                headers = {"Authorization": f"Bearer {self.token}"}

                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{urls.API_URL}/api/projects/upload_image?project_id={project_id}", 
                                                files=files, data=data, headers=headers)

                if response.status_code == 200:
                    try:
                        image  = f"{os.environ.get('SUPABASE_URL')}storage/v1/object/public/{os.environ.get('SUPABASE_S3_BUCKET')}/projects/{self.project_id}/images/{self.image}"
                        await self.update_project("image",image)
                        await self.remove_uploaded_files()
                        self.image = None
                        self.project_details = response.json()["project_id"]
                    except Exception as e:
                        self.image = None
                        await self.remove_uploaded_files()
                        return rx.toast(f"Image upload error: {str(e)}")
                else:
                    detail = response.json()["detail"]
                    self.image = None
                    await self.remove_uploaded_files()
                    return rx.toast(f"Project update error: {response.status_code}, {detail}")
        except Exception as e:
            self.image = None
            await self.remove_uploaded_files()
            return rx.toast(f"File upload error: {str(e)}")
        
        
    async def create_new_project(self, form_data: dict):
        try:
            self.token = await self.set_auth_token()
            project_id = str(uuid.uuid4())

            if self.logo:
                await self.supabase_upload_logo(project_id)
            if self.image:
                await self.supabase_upload_image(project_id)

            input_data = {
                "project_id": project_id, 
                "name": form_data["name"],
                "type": form_data["type"],
                "status": form_data["status"],
                "description": form_data["description"] if form_data["description"] else "",
                "logo": f"{self.logo}" if self.logo else "",
                "image": f"{self.image}" if self.image else "",
                "website": form_data["website"]if form_data["website"] else "",
                "attachment": form_data["attachment"] if form_data["attachment"] else "",
                "guide": form_data["guide"] if form_data["guide"] else "",
                "repo": form_data["repo"] if form_data["repo"] else "",
                "org_name": form_data["org_name"] if form_data["org_name"] else "",
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
        self.token = await self.set_auth_token()
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{urls.API_URL}/api/projects/delete_project?project_id={project_id}",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_projects()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to delete project: {response.status_code}, {response.text}")
        
    
    async def leave_project(self,project_id):
        self.token = await self.set_auth_token()
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
        self.token = await self.set_auth_token()
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
        """Get the list of projects the user is a member of."""
        self.token = await self.set_auth_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/projects/my_projects",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            self.my_projects = response.json()
            self.is_project_member = any(d['project_id'] == self.selected_project.get("project_id") for d in self.my_projects)
        
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
        """Detach a user from the project."""
        
        self.token = await self.set_auth_token()
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/projects/user_dettached_project?project_id={self.project_id}&user_id={user_id}",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.find_members_project()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to detached project: {response.status_code}, {response.text}")


    async def user_join_project(self,user_id:str):
        """Join a user to the project."""
        
        self.token = await self.set_auth_token()
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/projects/user_join_project?project_id={self.project_id}&user_id={user_id}",
                headers = {"Authorization": f"Bearer {self.token}"},
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
            
    
    async def find_orgs_project(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/projects/orgs?project_id={self.project_id}",
                )
            if response.status_code == 200:
                self.project_orgs = response.json()
            else:
                print(f"Failed to get projects: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
            
    async def user_unfollow_project(self,user_id:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/projects/user_unfollow_project?project_id={self.project_id}&user_id={user_id}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_projects()
            self.is_project_member = any(d['project_id'] == self.project_id for d in self.my_projects)
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to unfollow project: {response.status_code}, {response.text}")
    
    async def user_follow_project(self,user_id:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/projects/user_follow_project?project_id={self.project_id}&user_id={user_id}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_projects()
            self.is_project_member = any(d['project_id'] == self.project_id for d in self.my_projects)
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to follow project: {response.status_code}, {response.text}")
    
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
            self.token = await self.set_auth_token()
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{urls.API_URL}/api/projects/update_project?key={key}&value={value}&project_id={self.project_id}",
                    headers = {"Authorization": f"Bearer {self.token}"}
                )
            
            if response.status_code == 200:
                self.selected_project = response.json()
                await self.get_list_projects()
                await self.load_project_page()
                return rx.toast.success(f"{key} updated successfully")
            else:
                detail = response.json()["detail"]
                return rx.toast.error(f"project update error: {detail}")
        except Exception as err:
            return rx.toast(f"Unexpected error: {err}")

    
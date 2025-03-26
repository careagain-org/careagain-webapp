import reflex as rx
import httpx
from ..constants import urls
from typing import List, Dict, Any, Optional
from .auth_state import AuthState
import uuid
import datetime as dt
import clipboard
import json
import os


class OrgState(AuthState):
    org_types: list[str] = ["Hospital", "Logistics & transport",
                            "Research & Development","Manufacturer"]
    orgs: List[Dict[str, str]] = []
    my_orgs: List[Dict[str, str]] = []
    filtered_orgs: List[Dict[str, str]] = []
    searched_orgs: List[Dict[str, str]]=[]
    orgs_locations: List[Dict[str, float]] = []
    selected_org: Dict[str, str] = {}
    org_details: Dict[str, str] = {}
    
    org_members:List[Dict[str, str]] = []
    org_id:str=""
    latitude: float =None
    longitude: float =None
    logo: str =""
    visible: bool =False
    org_type: str=None

    @rx.event
    def update_location(self):
        try:
            self.visible = True
            self.latitude = float(clipboard.paste().split(",")[0])
            self.longitude = float(clipboard.paste().split(",")[-1])
        except Exception as err:
            return rx.toast(err)

    def reset_org(self):
        self.org_id=None
        self.latitude=None
        self.longitude=None
        self.logo =""
        self.visible=False
        self.org_type=False

        
    @rx.event
    async def upload_org_logo(self, my_files: list[rx.UploadFile]):
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
    

    async def supabase_upload(self,org_id):
        try:
            outfile = rx.get_upload_dir() / self.logo 

            with open(outfile, "rb") as image_file:
                files = {"file": (self.logo, image_file, "image/png")}
                data = {"org_id": self.org_id}
                headers = {"Authorization": f"Bearer {self.token}"}

                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{urls.API_URL}/api/orgs/upload_image?org_id={org_id}", 
                                                files=files, data=data, headers=headers)

                if response.status_code == 200:
                    return response.json()["org_id"]
                else:
                    detail = response.json()["detail"]
                    return rx.toast(f"User update error: {response.status_code}, {detail}")
        except Exception as e:
            return rx.toast(f"File upload error: {str(e)}")
        
    
    async def filter_org(self,value:str=""):
        self.filtered_orgs = [d for d in self.orgs if (value.lower() in d['name'].lower()) and (value!="")]


    async def create_new_org(self, form_data: dict):
        try:
            org_id = str(uuid.uuid4())

            if self.logo:
                await self.supabase_upload(org_id)

            input_data = {
                "org_id": org_id, 
                "name": form_data["name"],
                "type": form_data["type"],
                "description": form_data["description"],
                "latitude": self.latitude,
                "longitude": self.longitude,
                "address": form_data["address"],
                "logo": f"{self.logo}" if self.logo else "",
                "website": form_data["website"],
                "email":form_data["email"],
                "visible": self.visible
            }

            headers = {"Authorization": f"Bearer {self.token}"}

            async with httpx.AsyncClient() as client:
                response = await client.post(f"{urls.API_URL}/api/orgs/create_org", 
                                            json=input_data, headers=headers)

            if response.status_code == 200:
                self.org_details = response.json()["org_details"]
                self.reset_org()
                await self.get_my_orgs()
                await self.get_orgs()
                return rx.toast("New organization uploaded")
            else:
                detail = response.json()["detail"]
                return rx.toast(f"Organization update error: {response.status_code}, {detail}")
        except Exception as err:
            return rx.toast(f"Organization creation error: {str(err)}")


    async def get_my_orgs(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/orgs/my_organizations",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            self.my_orgs = response.json()
        else:
            print(f"Failed to get orgs: {response.status_code}, {response.text}")
            

    async def delete_my_org(self,org_id):

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{urls.API_URL}/api/orgs/delete_org?org_id={org_id}",
                # headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_orgs()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to delete organization: {response.status_code}, {response.text}")
        
    
    async def leave_my_org(self,org_id):

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{urls.API_URL}/api/orgs/leave_org?org_id={org_id}",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_orgs()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to leave organization: {response.status_code}, {response.text}")
        

    async def join_org(self):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/orgs/join_org?org_id={self.org_id}",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_orgs()
            self.filtered_orgs=[]
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to join org: {response.status_code}, {response.text}")


    async def get_orgs(self) :

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/orgs/organizations",
            )
        
        if response.status_code == 200:
            self.orgs = response.json()
            self.searched_orgs= response.json()
        else:
            print(f"Failed to get orgs: {response.status_code}, {response.text}")
            
    
    async def search_orgs(self,form_data):
        if form_data["search"]=="":
            self.searched_orgs =self.orgs
        else:
            self.searched_orgs = [d for d in self.orgs if (form_data["search"].lower() in (d['name']+d['description']+d["type"]+d["address"]).lower()) 
                                      and (form_data["search"]!="")]


    async def get_location(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/orgs/locations",
                )
            if response.status_code == 200:
                self.orgs_locations = response.json()
            else:
                print(f"Failed to get orgs: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")


    async def find_members_org(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/orgs/members?org_id={self.org_id}",
                )
            if response.status_code == 200:
                self.org_members = response.json()
            else:
                print(f"Failed to get orgs: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")


    def select_org(self,org_id:str):
        self.org_id = org_id
        self.selected_org = [d for d in self.orgs if d['org_id']==org_id][0]


    def to_org_view(self,org_id:str):
        self.org_id = org_id
        self.selected_org = [d for d in self.orgs if d['org_id']==org_id][0]
        return rx.redirect(f"/org_view")
    
    
    def to_org_edit(self,org_id:str):
        self.org_id = org_id
        self.selected_org = [d for d in self.orgs if d['org_id']==org_id][0]
        return rx.redirect(f"/org_edit")
    
    
    async def update_org(self,key:str,value:str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{urls.API_URL}/api/orgs/update_org?key={key}&value={value}&org_id={self.org_id}",
                    headers = {"Authorization": f"Bearer {self.token}"}
                )
            
            if response.status_code == 200:
                self.selected_org = response.json()
                return rx.toast.success(f"{key} updated successfully")
            else:
                detail = response.json()["detail"]
                return rx.toast.error(f"Organization update error: {detail}")
        except:
            return rx.toast("Unexpected error")
    
    async def update_coordinates(self):
        lat = float(clipboard.paste().split(",")[0])
        lon = float(clipboard.paste().split(",")[-1])
        
        await self.update_org(key="latitude",value=lat)
        await self.update_org(key="longitude",value=lon)
        
        
    async def user_join_org(self,user_id:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/orgs/user_join_org?org_id={self.org_id}&user_id={user_id}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.find_members_org()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to join organization: {response.status_code}, {response.text}")
        
    
    async def user_dettached_org(self,user_id:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/orgs/user_dettached_org?org_id={self.org_id}&user_id={user_id}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.find_members_org()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to remove user: {response.status_code}, {response.text}")
        
    
    async def change_member(self,user_id:str,role:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/orgs/change_member_type?org_id={self.org_id}&user_id={user_id}&role={role}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.find_members_org()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Change member type: {response.status_code}, {response.text}")


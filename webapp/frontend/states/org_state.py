import reflex as rx
import reflex_clerk_api as reclerk
import httpx
from ..constants import urls
from typing import List, Dict, Any, Optional
from .auth_state import AuthState
import uuid
from datetime import datetime, timedelta, timezone
import clipboard
import pyperclip
import jwt
import os
import dotenv
import glob

secret_key = os.getenv("CLERK_SECRET_KEY")

class OrgState(rx.State):
    org_types: list[str] = ["Hospital", "Logistics & transport",
                            "Research & Development","Manufacturer"]
    orgs: List[Dict[str, Any]] = []
    my_orgs: List[Dict[str, Any]] = []
    filtered_orgs: List[Dict[str, Any]] = []
    searched_orgs: List[Dict[str, Any]]=[]
    orgs_locations: List[Dict[str, float]] = []
    selected_org: Dict[str, Any] = {}
    org_details: Dict[str, Any] = {}
    
    org_members:List[Dict[str, Any]] = []
    org_projects:List[Dict[str, Any]] =[]
    org_id:str=""
    logo_data: str =""
    is_org_member: bool=False
    is_org_follower: bool=False
    is_org_admin: bool=False
    token:Optional[str]=rx.Cookie(
                name="auth_token", max_age=30,
                path="/",
                same_site="lax",
                secure=True,
            ) 
    
    def set_logo(self, image_data: str):
        self.logo_data = image_data
    
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
    
    @rx.var(cache=True)
    def my_org_names(self) -> list[str]:
        return [f"{org["name"]} [{org["org_id"]}]" for org in self.my_orgs]

    
    @rx.event
    def update_location(self):
        try:
            self.visible = True
            # self.latitude = float(pyperclip.paste().split(",")[0])
            # self.longitude = float(pyperclip.paste().split(",")[-1])
        except Exception as err:
            return rx.toast(err)

        
    @rx.event
    async def upload_org_logo(self, my_files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        try:
            upload_data = self.logo_data
            file=my_files[0]
            upload_data = await file.read()
            logo_filename = f"{uuid.uuid4()}.png"
            outfile = rx.get_upload_dir() / logo_filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

        except Exception as err:
            return rx.toast(err)
    
    
    async def remove_uploaded_files(self):
        self.logo_data =""
        files = glob.glob(f"{rx.get_upload_dir()}/*")
        for f in files:
            os.remove(f)
                       

    async def supabase_upload(self,org_id, logo_name):
        """Upload the logo to Supabase storage and update the organization details."""
        self.token = await self.set_auth_token()
        try:
            logo_filename = f"{uuid.uuid4()}.png"
            outfile = rx.get_upload_dir() / logo_name
            print(outfile)
            with open(outfile, "rb") as image_file:
                files = {"file": (logo_filename, image_file, "image/png")}
                data = {"org_id": org_id}
                headers = {"Authorization": f"Bearer {self.token}"}

                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{urls.API_URL}/api/orgs/upload_image?org_id={org_id}", 
                                                files=files, data=data, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                try:
                    logo  = f"{os.environ.get("SUPABASE_URL")}storage/v1/object/public/{os.environ.get("SUPABASE_S3_BUCKET")}/orgs/{org_id}/images/{logo_filename}"
                    await self.update_org("logo",logo,org_id)
                except:
                    print("org doesn't exist")
                await self.remove_uploaded_files()
                return rx.toast(f"File uploaded")
            else:
                detail = response.json()["detail"]
                await self.remove_uploaded_files()
                return rx.toast(f"User update error: {response.status_code}, {detail}")
        except Exception as e:
            await self.remove_uploaded_files()
            return rx.toast(f"File upload error: {str(e)}")
        
    
    async def filter_org(self,value:str=""):
        self.filtered_orgs = [d for d in self.orgs if (value.lower() in d['name'].lower()) and (value!="")]

    def validate_float(self,my_string:str):
        try:
            if my_string is None or my_string=="":
                return None
            else:
                return float(my_string)
        except:
            print("Invalid float value")
            return None

    async def create_new_org(self, form_data: dict):
        """Create a new organization with the provided form data."""
        self.token= await self.set_auth_token()
        try:
            org_id = str(uuid.uuid4())

            input_data = {
                "org_id": org_id, 
                "name": form_data["name"],
                "type": form_data["type"],
                "description": form_data["description"],
                "latitude": self.validate_float(form_data["latitude"]),
                "longitude": self.validate_float(form_data["longitude"]),
                "address": form_data["address"],
                "logo": "",
                "website": form_data["website"],
                "email":form_data["email"],
                "visible": True
            }

            headers = {"Authorization": f"Bearer {self.token}"}

            async with httpx.AsyncClient() as client:
                response = await client.post(f"{urls.API_URL}/api/orgs/create_org", 
                                            json=input_data, headers=headers)
            print(form_data["logo"])
            if form_data["logo"] != "":
                await self.supabase_upload(org_id=org_id, logo_name=form_data["logo"])

            if response.status_code == 200:
                self.org_details = response.json()["org_details"]
                await self.get_my_orgs()
                await self.get_orgs()
                return rx.toast("New organization uploaded")
            else:
                detail = response.json()["detail"]
                return rx.toast(f"Organization creation error: {response.status_code}, {detail}")
        except Exception as err:
            return rx.toast(f"Organization creation error: {str(err)}")


    async def get_my_orgs(self):
        self.token = await self.set_auth_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/orgs/my_organizations",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            self.my_orgs = response.json()
            self.is_org_member = any(d['org_id'] == self.selected_org.get("org_id") for d in self.my_orgs)
            self.is_org_admin = any((d['org_id'] == self.selected_org.get("org_id") and d['member_type'] == "admin") for d in self.my_orgs)
        
        else:
            print(f"Failed to get orgs: {response.status_code}, {response.text}")
            

    async def delete_my_org(self,org_id):
        self.token = await self.set_auth_token()
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{urls.API_URL}/api/orgs/delete_org?org_id={org_id}",
                headers = {"Authorization": f"Bearer {self.token}"},
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_orgs()
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to delete organization: {response.status_code}, {response.text}")
        
    
    async def leave_my_org(self,org_id):
        self.token = await self.set_auth_token()
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
        self.token = await self.set_auth_token()
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


    async def find_members_org(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/orgs/members?org_id={self.org_id}",
                )
            if response.status_code == 200:
                self.org_members = response.json()
                self.is_org_member = any(d['org_id'] == self.selected_org.get("org_id") for d in self.my_orgs)
                self.is_org_admin = any((d['org_id'] == self.selected_org.get("org_id") and d['member_type'] == "admin") for d in self.my_orgs)
        
            else:
                print(f"Failed to get orgs: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
            
    async def find_projects_org(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/orgs/projects?org_id={self.org_id}",
                )
            if response.status_code == 200:
                self.org_projects = response.json()
                # self.is_org_member = any(d['org_id'] == self.selected_org.get("org_id") for d in self.my_orgs)
        
            else:
                print(f"Failed to get orgs: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
            
    async def load_org_page(self):
        await self.get_orgs()
        current_page_route = self.router.url.path
        org_id =current_page_route.split("/")[-1]
        self.select_org(org_id)
        await self.find_projects_org()
        await self.find_members_org()
        

    def select_org(self,org_id:str):
        self.org_id = org_id
        self.selected_org = [d for d in self.orgs if d['org_id']==org_id][0]


    def to_org_view(self,org_id:str):
        self.org_id = org_id
        self.selected_org = [d for d in self.orgs if d['org_id']==org_id][0]
        return rx.redirect(f"{urls.IND_ORG_URL}/{org_id}")
    
    
    def to_org_edit(self,org_id:str):
        self.org_id = org_id
        self.selected_org = [d for d in self.orgs if d['org_id']==org_id][0]
        return rx.redirect(f"{urls.IND_EDIT_ORG_URL}/{org_id}")
    
    
    async def update_org(self,key:str,value:str,org_id:str):
        try:
            self.token = await self.set_auth_token()
            value = value.strip()
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{urls.API_URL}/api/orgs/update_org",
                    params={"key": key, "value": value,"org_id": org_id},  # in the body, no encoding issues
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            
            if response.status_code == 200:
                self.selected_org = response.json()
                await self.get_my_orgs()
                await self.load_org_page()
                return rx.toast.success(f"{key} updated successfully")
            else:
                detail = response.json()["detail"]
                return rx.toast.error(f"Organization update error: {detail}")
        except Exception as e:
            return rx.toast(f"Unexpected error: {str(e)}")
    
    async def update_coordinates(self,form_data: dict):

        #[lat, lon] = await self.get_coordinates_from_map()
        lat = form_data["latitude"]
        lon = form_data["longitude"]
        
        await self.update_org(key="latitude",value=lat,org_id=self.org_id)
        await self.update_org(key="longitude",value=lon,org_id=self.org_id)
    
    # async def get_coordinates_from_map(self):
    #     lat = float(pyperclip.paste().split(",")[0])
    #     lon = float(pyperclip.paste().split(",")[-1])
    #     return lat, lon
        
        
        
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
      
        
    async def user_follow_org(self,user_id:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/orgs/user_follow_org?org_id={self.org_id}&user_id={user_id}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_orgs()
            await self.find_members_org()
            self.is_org_follower = any((d['org_id'] == self.selected_org.get("org_id") and d['member_type'] == "follower") for d in self.my_orgs)
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to follow org: {response.status_code}, {response.text}")
        
    
    async def user_unfollow_org(self,user_id:str):

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{urls.API_URL}/api/orgs/user_unfollow_org?org_id={self.org_id}&user_id={user_id}",
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            await self.get_my_orgs()
            await self.find_members_org()
            self.is_org_follower = any(d['org_id'] == self.selected_org.get("org_id") and d['member_type'] == "follower" for d in self.my_orgs)
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to unfollow org: {response.status_code}, {response.text}")
        
        
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


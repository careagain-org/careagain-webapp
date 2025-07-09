import reflex as rx
import reflex_clerk_api as reclerk
import clerk_backend_api as Clerk
import httpx
import http
import urllib
from ..constants import urls
from .auth_state import AuthState
from typing import List, Dict, Any, Optional
from gotrue.errors import AuthApiError
from starlette.requests import Request
import os
import dotenv
import requests

dotenv.load_dotenv()

# clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))


class UserState(rx.State):
    image_path: str 
    my_details: Dict[str, Any] = {}
    
    selected_user_id:str
    selected_user: Dict[str, str]
    users: List[Dict[str, str]]=[]
    filtered_users: List[Dict[str, str]]=[]
    searched_users: List[Dict[str, str]]=[]
    
    user_projects: List[Dict[str, str]]=[]
    user_orgs: List[Dict[str, str]]=[]
    
    token:Optional[str]=rx.Cookie(
                name="__session",
            ) 
    
    # @rx.var
    # def token(self)->str:
    #     cookie_token=rx.Cookie(
    #             name="__session",
    #             path="/",
    #             same_site="lax",
    #             secure=True,
    #         ) 
    #     return cookie_token
    
    async def user_whipeout(self):
        self.image_path: str =""
        self.my_details: Dict[str, str]=[]
        
        self.selected_user_id:str=""
        self.selected_user: Dict[str, str]={}
        self.users: List[Dict[str, str]]=[]
        self.filtered_users: List[Dict[str, str]]=[]
        self.searched_users: List[Dict[str, str]]=[]
        
        self.user_projects: List[Dict[str, str]]=[]
        self.user_orgs: List[Dict[str, str]]=[]


    async def load_user_page(self):
        current_page_route = self.router.page.raw_path
        user_id =current_page_route.split("/")[-2]
        print(f"User ID: {user_id}")
        self.selected_user_id = user_id
        self.selected_user = [d for d in self.users if d['user_id']==(user_id)][0]
    

    async def get_my_details(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{urls.API_URL}/api/users/me",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            
                if response.status_code == 200:
                    self.my_details = response.json()
                    print(f"Successfull get user")
                else:
                    print(f"Failed to get user: {response.status_code} ")
            except Exception as e:
                print(f"Failed to get user: {e}")


    async def update_user(self,key:str,value:str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{urls.API_URL}/api/users/update_user?key={key}&value={value}",
                    headers = {"Authorization": f"Bearer {self.token}"}
                )
            
            if response.status_code == 200:
                self.my_details = response.json()
                return rx.toast(f"{key} updated successfully")
            else:
                detail = response.json()["detail"]
                return rx.toast(f"User update error: {detail}")
        except AuthApiError as e:
            self.token = None
            return rx.toast("Unexpected error")
        
        
    @rx.event
    async def handle_upload(self, my_files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        try:
            for file in my_files:
                file=my_files[0]
                upload_data = await file.read()
                outfile = rx.get_upload_dir() / "uploaded.png"

                # Save the file.
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)
                
                # Open the image file in binary mode
                with open(outfile, "rb") as image_file:
                    files = {"file": ("image.jpg", image_file, "image/jpeg")}
                    data = {"description": "This is a sample image."}
                    headers = {"Authorization": f"Bearer {self.token}"}
                    clerk_state = await self.get_state(reclerk.ClerkState)

                    # Send the POST request
                    async with httpx.AsyncClient() as client:
                        response = await client.post(f"{urls.API_URL}/api/users/upload_image?user_id={str(clerk_state.user_id)}", 
                                                    files=files, data=data)
                                                    # , headers=headers)

                    if response.status_code == 200:
                        self.my_details = response.json()["user_details"]
                        return rx.toast(f"Image uploaded")
                    else:
                        detail = response.json()["detail"]
                        return rx.toast(f"User update error: {response.status_code}, {detail}")
        except:
            return rx.toast("Unexpected error")
        
    async def get_users(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}/api/users/",
            )
        
        if response.status_code == 200:
            self.users = response.json()
            self.searched_users= response.json()
            
        
    async def filter_user(self,value:str=""):
        self.filtered_users = [d for d in self.users if (value.lower() in f"{d['username']}{d['first_name']}{d['last_name']}".lower()) and (value!="")]
        
        
    def to_user_view(self,user_id:str):
        self.selected_user_id = user_id
        self.selected_user = [d for d in self.users if d['user_id']==user_id][0]
        return rx.redirect(f"{urls.IND_USER_URL}/{user_id}")
    
    
    def select_user(self,user_id:str):
        self.selected_user_id = user_id
        self.selected_user = [d for d in self.users if d['user_id']==(user_id)][0]
        
        
    def is_user_member(self, org_id: str) -> bool:
        return any(d['org_id'] == org_id for d in self.user_orgs)
    
    
    
    async def search_user(self,form_data):
        if form_data["search"]=="":
            self.searched_users =self.users
        else:
            self.searched_users = [d for d in self.users if (form_data["search"].lower() in (d['first_name']+d['description']+d["last_name"]+d["country"]).lower()) 
                                      and (form_data["search"]!="")]
    
    
    async def invite_user(self,form_data: dict):

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{urls.API_URL}/api/users/invite_user?email={form_data["email"]}",
                headers = {"Authorization": f"Bearer {self.token}"}
            )
        
        if response.status_code == 200:
            detail = response.json()["detail"]
            return rx.toast.success(detail)
        else:
            return rx.toast.error(f"Failed to join organization: {response.status_code}, {response.text}")
        

    async def get_user_projects(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/users/user_projects?user_id={self.selected_user_id}",
                )
            if response.status_code == 200:
                self.user_projects = response.json()
            else:
                print(f"Failed to get projects: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    
    async def get_user_orgs(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{urls.API_URL}/api/users/user_orgs?user_id={self.selected_user_id}",
                )
            if response.status_code == 200:
                self.user_orgs = response.json()
            else:
                print(f"Failed to get orgs: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    


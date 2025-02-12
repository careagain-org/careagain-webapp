import reflex as rx
import httpx
from ..constants import urls
from typing import List, Dict 
from .auth_state import AuthState

token=AuthState.token

class UserState(AuthState):
    image_path: str 
    my_details: Dict[str, str]


    async def get_image_path(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}api/users/my_foto",
                headers={"Authorization": f"Bearer {self.token}"}
            )
        
        if response.status_code == 200:
            self.image_path = response.json()

            print(f"Successfull get user")
        else:
            print(f"Failed to get user: {response.status_code} ")



    async def get_my_details(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{urls.API_URL}api/users/me",
                headers={"Authorization": f"Bearer {self.token}"}
            )
        
        if response.status_code == 200:
            self.my_details = response.json()

            print(f"Successfull get user")
        else:
            print(f"Failed to get user: {response.status_code} ")


    async def update_user(self,key:str,value:str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{urls.API_URL}api/users/update_user?key={key}&value={value}",
                    headers = {"Authorization": f"Bearer {self.token}"}
                )
            
            if response.status_code == 200:
                self.my_details = response.json()
                return rx.toast(f"{key} updated successfully")
            else:
                detail = response.json()["detail"]
                return rx.toast(f"User update error: {detail}")
        except:
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
                    # Prepare the files dictionary
                    files = {"file": ("image.jpg", image_file, "image/jpeg")}

                    # Additional data
                    data = {
                        "description": "This is a sample image."
                    }

                    # Add authentication token
                    headers = {
                        "Authorization": f"Bearer {self.token}"
                    }

                    # Send the POST request
                    async with httpx.AsyncClient() as client:
                        response = await client.post(f"{urls.API_URL}api/users/upload_image", 
                                                    files=files, data=data, headers=headers)

                    if response.status_code == 200:
                        self.my_details = response.json()["user_details"]
                        return rx.toast(f"Image uploaded")
                    else:
                        detail = response.json()["detail"]
                        return rx.toast(f"User update error: {response.status_code}, {detail}")
        except:
            return rx.toast("Unexpected error")


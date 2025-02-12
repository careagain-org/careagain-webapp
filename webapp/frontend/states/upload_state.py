import reflex as rx
from ..constants import urls
import httpx
from ..states.auth_state import AuthState
import logging
from pathlib import Path


class UploadState(AuthState):
    """The app state."""

    # The images to show.
    img: str
    upload_type: str

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
                        return rx.toast("hola") #f"{response.json()["detail"]}
                    else:
                        detail = response.json()["detail"]
                        return rx.toast(f"User update error: {response.status_code}, {detail}")
        except:
            return rx.toast("Unexpected error")
    


def upload_image(title:str,my_image:str) -> rx.Component():

    return rx.vstack(
        rx.heading(title,size="3", color = "grey"),
        rx.upload(
            rx.vstack(
                rx.cond(my_image=="",
                        rx.icon("image",size=40,color="teal"),
                        rx.image(my_image)),
                align="center",
                justify="center"),
            radius="full",
            border="1px dotted rgb(0,0,0)",
            spacing="2",
            width="15em",
            height="100%",
            multiple=False,
            accept = {
                "application/pdf": [".pdf"],
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
                "image/gif": [".gif"],
                "image/webp": [".webp"],
                "text/html": [".html", ".htm"],
            },
            _hover={"cursor": "pointer"},
            background_image=my_image,
            id="my_upload",
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files("my_upload"), rx.text
            )
        ),
        rx.hstack(
            rx.button(
                "Upload",
                variant = "surface",
                on_click=UploadState.handle_upload(rx.upload_files("my_upload")),
                align="start",
            ),
            rx.button(
                "Clear",
                variant = "outline",
                on_click=rx.clear_selected_files("my_upload"),
                align="end",
            ),
        ),

    )


# @rx.event
#     async def handle_upload(self, 
#                             type: rx.State,
#                             file: rx.UploadFile,
#                             token:str):
#         try:
#             async with httpx.AsyncClient() as client:
#                 with open(file, "rb") as file:
                    
#                     # Make the asynchronous POST request
#                     response = await client.post(f"{urls.API_URL}api/{type}/upload_image", 
#                                     headers = {"Authorization": f"Bearer {token}",
#                                                 "Content-Type": "multipart/form-data"},
#                                     file = file)
            
#             if response.status_code == 200:
#                 self.my_details = response.json()["user_details"]
#                 return rx.toast(f"{response.json()["detail"]}")
#             else:
#                 detail = response.json()["detail"]
#                 return rx.toast(f"User update error: {response.status_code}, {detail}")
#         except:
#             return rx.toast("Unexpected error")
# color = "rgb(107,99,246)"
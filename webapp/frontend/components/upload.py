import reflex as rx
from ..states.user_state import UserState
from ..states.org_state import OrgState
import os
from pathlib import Path
from typing import List

import reflex as rx


def upload_image_user(title:str,my_image:str) -> rx.Component():

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
            on_click = UserState.handle_upload(rx.upload_files("my_upload"))
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
                on_click=UserState.handle_upload(rx.upload_files("my_upload")),
                align="start",
            ),
            rx.button(
                "Clear",
                variant = "outline",
                on_click=rx.clear_selected_files("my_upload"),
                align="end",
            ),
        ),
        # rx.foreach(
        #     UploadState.img,
        #     lambda img: rx.image(
        #         src=rx.get_upload_url(img)
        #     ),
        # ),
    )



def upload_logo_org(title:str,my_image:str) -> rx.Component():

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
            background_image=rx.get_upload_url("logo_org.png"),
            id="upload_logo_org",
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files("upload_logo_org"), rx.text
            ),
        ),
        rx.hstack(
            rx.button(
                "Upload",
                variant = "surface",
                type="button",
                on_click=OrgState.upload_org_logo(rx.upload_files("upload_logo_org")),
                align="start",
            ),
            rx.button(
                "Clear",
                variant = "outline",
                type="button",
                on_click=rx.clear_selected_files("upload_logo_org"),
                align="end",
            ),
        ),
        # rx.foreach(
        #     UploadState.img,
        #     lambda img: rx.image(
        #         src=rx.get_upload_url(img)
        #     ),
        # ),
    )





# class State(rx.State):
#     """The app state."""

#     # Whether we are currently uploading files.
#     is_uploading: bool

#     # Progress visuals
#     upload_progress: int

#     @rx.var
#     def files(self) -> list[str]:
#         """Get the string representation of the uploaded files."""
#         files = [
#             "/".join(p.parts[1:])
#             for p in Path(rx.get_upload_dir()).rglob("*")
#             if p.is_file()
#         ]
#         return files

#     async def handle_upload(self, files: List[rx.UploadFile]):
#         """Handle the file upload."""
#         # Iterate through the uploaded files.
#         for file in files:
#             upload_data = await file.read()
#             outfile = Path(rx.get_upload_dir()) / file.filename.lstrip("/")
#             outfile.parent.mkdir(parents=True, exist_ok=True)
#             outfile.write_bytes(upload_data)

#     def on_upload_progress(self, prog: dict):
#         print("Got progress", prog)
#         if prog["progress"] < 1:
#             self.is_uploading = True
#         else:
#             self.is_uploading = False
#         self.upload_progress = round(prog["progress"] * 100)

#     def cancel_upload(self, upload_id: str):
#         self.is_uploading = False
#         return rx.cancel_upload(upload_id)


# color = "rgb(107,99,246)"
# upload_id = "upload1"


# def upload_image1():
#     return rx.vstack(
#         rx.upload(
#             rx.vstack(
#                 rx.button(
#                     "Select File(s)",
#                     height="70px",
#                     width="200px",
#                     color=color,
#                     bg="white",
#                     border=f"1px solid {color}",
#                 ),
#                 rx.text(
#                     "Drag and drop files here or click to select files",
#                     height="100px",
#                     width="200px",
#                 ),
#                 rx.cond(
#                     rx.selected_files(upload_id),
#                     rx.foreach(
#                         rx.selected_files(upload_id),
#                         rx.text,
#                     ),
#                     rx.text("No files selected"),
#                 ),
#                 align="center",
#             ),
#             id=upload_id,
#             border="1px dotted black",
#             padding="2em",
#         ),
#         rx.hstack(
#             rx.button(
#                 "Upload",
#                 on_click=UserState.handle_upload(
#                     rx.upload_files(
                        
#                         on_upload_progress=State.on_upload_progress
#                     )
#                 ),
#             ),
#         ),
#         rx.heading("Files:"),

#         rx.cond(
#             State.is_uploading,
#             rx.text("Uploading... ", rx.link("cancel", on_click=State.cancel_upload(upload_id))),
#         ),
#         rx.progress(value=State.upload_progress),
#         rx.vstack(
#            rx.foreach(State.files, lambda file: rx.link(file, href=rx.get_upload_url(file)))
#         ),
#         align="center",
#     )



import reflex as rx
from ..states.user_state import UserState
from ..states.project_state import ProjectState
import os
from pathlib import Path
from typing import List

import reflex as rx


def upload_image_project(title:str,my_image:str):

    return rx.vstack(
        rx.heading(title,size="3", color = "grey"),
        rx.upload(
            rx.center(
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
            id="upload_image_project",
            on_click = ProjectState.handle_upload_image(rx.upload_files("upload_image_project"))
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files("upload_image_project"), rx.text
            )
        ),
        rx.hstack(
            rx.button(
                "Upload",
                variant = "surface",
                on_click=ProjectState.handle_upload_image(rx.upload_files("upload_image_project")),
                align="start",
                type="button",
            ),
            rx.button(
                "Clear",
                variant = "outline",
                on_click=rx.clear_selected_files("upload_image_project"),
                align="end",
                type="button",
            ),
        ),
        # rx.foreach(
        #     UploadState.img,
        #     lambda img: rx.image(
        #         src=rx.get_upload_url(img)
        #     ),
        # ),
    )



def upload_logo_project(title:str,my_image:str):

    return rx.vstack(
        rx.heading(title,size="3", color = "grey"),
        rx.upload(
            rx.vstack(
                rx.cond(my_image=="",
                        rx.icon("image",size=40,color="teal",align="center"),
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
            id="upload_logo_project",
            on_click = ProjectState.handle_upload_logo(rx.upload_files("upload_logo_project"))
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files("upload_logo_project"), rx.text
            )
        ),
        rx.hstack(
            rx.button(
                "Upload",
                variant = "surface",
                on_click=ProjectState.handle_upload_logo(rx.upload_files("upload_logo_project")),
                align="start",
                type="button",
            ),
            rx.button(
                "Clear",
                variant = "outline",
                on_click=rx.clear_selected_files("upload_logo_project"),
                align="end",
                type="button",
            ),
        ),
        # rx.foreach(
        #     UploadState.img,
        #     lambda img: rx.image(
        #         src=rx.get_upload_url(img)
        #     ),
        # ),
    )
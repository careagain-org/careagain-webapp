import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..states.project_state import ProjectState
from ..states.auth_state import AuthState
from typing import Dict
from ..components.map import interactive_map
from ..components.user_card import users_grid_horizontal
from ..components.user_table import table_pagination
from ..components.project_input_text import ProjectEditableText,ProjectEditableTextArea
from ..components.project_upload import upload_logo_project,upload_image_project
from ..components.forms_popover import add_new,search_user

editable_text = ProjectEditableText.create
editable_textarea = ProjectEditableTextArea.create


def title_section(title:str, icon:str):
    return rx.hstack(
                rx.icon(icon),
                rx.heading(title,size="5"),
                align="start",
            ),
    

@rx.page(route=urls.IND_EDIT_PROJECT_URL,on_load=ProjectState.find_members_project)
def edit_project() -> rx.Component:
    project=ProjectState.selected_project
    my_child = rx.vstack(
        rx.link(rx.icon('arrow_left'),href=urls.PROFILE_URL),
        rx.hstack(
            rx.heading(project['name'], size="9"),
            rx.cond(project['verified'],
                    rx.badge("Verified",variant="surface",color_scheme="teal"),
                    rx.badge("Non-Verified",variant="surface",color_scheme="amber")),
            align="center",
        ),
        rx.hstack(
            rx.icon("globe"),
            editable_text(value = project["website"],key = "website"),
        ),
        rx.hstack(
            rx.icon("mail"),
            editable_text(value = project["email"],key = "email"),
            # rx.text(projectState.selected_project['email'])
        ),
        rx.divider(width='90%'),
        rx.flex(
            upload_image_project(title="Representative image",my_image=project["logo"]),
            rx.vstack(
                title_section("Description","file_text"),
                editable_textarea(value = project["description"],key = "description"),
                width="60%"
            ),
            align='start',
            spacing="5",
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("circle-user-round"),
            rx.heading("Members",size="5"),
        ),
        rx.hstack(
            # add_new("user"), #commented because I cannot invite without admin permissions
            rx.container(
                rx.hstack(
                search_user("project"),
                rx.text(f"Click to search an existing user"),
                align="center",
            ),),
            align="start",
            spacing="4",
        ),
        table_pagination(ProjectState.project_members,"project")
    )

    return platform_base(my_child)

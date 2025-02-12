import reflex as rx
from pathlib import Path
from .platform_base import platform_base
from ..constants import urls
from ..components.forms_popover import add_new_popover,search_popover
from ..components.input_text import EditableText
from ..components.upload import upload_image_user
from ..components.table import table_pagination
from ..components.list_institution import list_org_vertical
from ..states.user_state import UserState
from ..states.org_state import OrgState
from ..states.auth_state import AuthState

editable_text = EditableText.create

class Profile():
    value: str

def section_title(section_icon:str,section_title:str, go_to_section:str,section_link:str) -> rx.Component():
    return rx.hstack(
        rx.icon(section_icon,color = "teal"),
        rx.heading(section_title,size="5", color = "teal"),
        rx.link(f"Go to {go_to_section}",href=section_link),
        spacing = "5",
        color = "accent"
    )

def input_field_edit(title:str,key:str) -> rx.Component():
    default_value =UserState.my_details[f"{key}"]
    return rx.vstack(
            rx.heading(title,size="3", color = "grey"),
            editable_text(value = default_value,key = key),
        ),


# def upload_image() -> rx.Component():
#     return rx.upload(
#                 rx.vstack(
#                     rx.icon("user"),
#                     rx.text("Drag and drop files here \n or click to select files"),
#                     align="center",
#                     justify="center"),
#                 radius="full",
#                 border="1px dotted rgb(0,0,0)",
#                 padding="5em",
#                 spacing="2",
#                 height="100%",
#                 id="my_upload",
#             ),

def user_section() -> rx.Component():

    return rx.container(
        rx.tablet_and_desktop(
            rx.hstack(
                upload_image_user("Profile photo",UserState.my_details["profile_image"]), 
                rx.vstack(
                    input_field_edit(title= "First name",key = 'first_name'),
                    input_field_edit("Last name",key='last_name1'),
                    input_field_edit("Country",key='country'),
                    input_field_edit(title= "Username (unique id)",key = 'username'),
                    # input_field_edit("Phone number",UserState.my_details['phone_number']),
                    spacing="2",
                    padding="3",
                ),
                spacing="9",
                align="center",
                width="83em"    
            )
        ),
        rx.mobile_only(
            rx.vstack(
                # upload_image("Profile photo",UserState.image_path),
                rx.vstack(
                    # input_field_edit("First name",UserState.my_details['first_name']),
                    # input_field_edit("Last name",UserState.my_details['last_name1']),
                    # input_field_edit("Second last name",UserState.my_details['last_name2']),
                    # input_field_edit("Phone number",UserState.my_details['phone_number']),
                ),
                align="center",
                width="83em"    
            )
        )
    )

def add_new(text:str)->rx.Component():
    return rx.container(
        rx.hstack(
            add_new_popover(text),
            rx.text(f"Click to add a new {text}"),
            align="center",   
        )
    )

def search_existing(text:str)->rx.Component():
    return rx.container(
        rx.hstack(
            search_popover(text),
            rx.text(f"Click to search an existing {text}"),
            align="center", 
        )
    )


@rx.page(route=urls.PROFILE_URL, on_load= [UserState.get_my_details,OrgState.get_my_orgs])#OrgState.get_my_orgs])
def profile() -> rx.Component:
    profile = rx.vstack(
                rx.heading('My profile', size="9"),
                section_title("book-user",'My User',"Users", urls.PROJECTS_URL),
                user_section(),
                rx.divider(),
                section_title("building-2",'My Organizations',"Community", urls.PROJECTS_URL),
                rx.hstack(
                    add_new("organization"),
                    search_existing("organization"),
                    align="start",
                    justify="start",
                    spacing="5"),
                table_pagination(OrgState.my_orgs),
                #list_org_vertical(),
                rx.divider(),
                section_title("square-library",'My Projects',"Projects", urls.PROJECTS_URL),
                rx.hstack(
                    add_new("project"),
                    search_existing("project"),
                    align="start",
                    spacing="4",
                ),
                rx.divider(),
                section_title("square-play",'My Video',"Videos", urls.PROJECTS_URL),
                add_new("video"),
                spacing="5",
                align = "start",
                justify="start",
    )
    return platform_base(profile)
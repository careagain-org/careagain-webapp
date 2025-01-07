import reflex as rx
from .platform_base import platform_base
from ..constants import urls
from ..components.forms_popover import add_new_popover
from ..components.input_text import EditableText
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

def input_field_edit(title:str,default_text:str) -> rx.Component():
    return rx.container(
        rx.vstack(
            rx.heading(title,size="3", color = "grey"),
            editable_text(initial_value = default_text)
        ),
    )

def upload_image() -> rx.Component():
    return rx.upload(
                rx.vstack(
                    rx.icon("user"),
                    rx.text("Drag and drop files here \n or click to select files"),
                    align="center",
                    justify="center"),
                radius="full",
                border="1px dotted rgb(0,0,0)",
                padding="5em",
                spacing="2",
                height="100%",
                id="my_upload",
            ),

def user_section() -> rx.Component():

    return rx.container(
        rx.tablet_and_desktop(
            rx.hstack(
                # rx.image(urls.STORAGE_URL,UserState.my_details["user_id"]),
                upload_image(),
                rx.vstack(
                    input_field_edit(title= "First name",default_text=UserState.my_details['first_name']),
                    input_field_edit("Last name",UserState.my_details['last_name1']),
                    input_field_edit("Second last name",UserState.my_details['last_name2']),
                    input_field_edit("Phone number",UserState.my_details['phone_number']),
                ),
                align="center",
                width="100vh"    
            )
        ),
        rx.mobile_only(
            rx.vstack(
                upload_image(),
                rx.vstack(
                    # input_field_edit("First name",UserState.my_details['first_name']),
                    # input_field_edit("Last name",UserState.my_details['last_name1']),
                    # input_field_edit("Second last name",UserState.my_details['last_name2']),
                    # input_field_edit("Phone number",UserState.my_details['phone_number']),
                ),
                align="center",
                width="100vh"    
            )
        )
    )

def add_new(text:str)-> rx.Component():
    return rx.container(
        rx.hstack(
            add_new_popover(text),
            rx.text(f"Click to add a new {text}"),
            align="center",
            width="100vh"    
        )
    )


@rx.page(route=urls.PROFILE_URL, on_load= [UserState.get_my_details])#OrgState.get_my_orgs])
def profile() -> rx.Component:
    profile = rx.vstack(
                rx.text(f"{UserState.email}{UserState.password}"),
                rx.heading('My profile', size="9"),
                section_title("book-user",'My User',"Users", urls.PROJECTS_URL),
                user_section(),
                rx.divider(),
                section_title("building-2",'My Institution',"Institutions", urls.PROJECTS_URL),
                add_new("intitution"),
                #list_org_vertical(),
                rx.divider(),
                section_title("square-library",'My Projects',"Projects", urls.PROJECTS_URL),
                add_new("project"),
                rx.divider(),
                section_title("square-play",'My Video',"Videos", urls.PROJECTS_URL),
                add_new("video"),
                spacing="5",
                align = "start",
                justify="start",
                width ="100%"
    )
    return platform_base(profile)
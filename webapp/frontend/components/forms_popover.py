import reflex as rx
import reflex_clerk_api as reclerk
from .user_input_text import SimpleTextInput
from .forms import ProjectForm,InstitutionForm, VideoForm
from .org_forms  import form_org,search_org,upload_logo_org
from .project_forms  import form_project,search_project,upload_image,upload_logo
from .user_forms import form_user,search_user_org,search_user_project
from ..states.auth_state import AuthState
from ..constants import urls


def add_new(text:str):
    return rx.container(
        rx.hstack(
            add_new_popover(text),
            rx.text(f"Click to add a new {text}"),
            align="center",   
        )
    )

def search_existing(text:str):
    return rx.container(
        rx.hstack(
            search_popover(text),
            rx.text(f"Click to search an existing {text}"),
            align="center", 
        )
    )


def add_new_popover(my_title:str):
    return rx.dialog.root(
        rx.fragment(
            reclerk.signed_in(
                rx.tooltip(
                rx.dialog.trigger(rx.icon_button("square-plus", size="3")),
                content=f"Create a new {my_title}")
            ),
            reclerk.signed_out(
                rx.tooltip(
                rx.icon_button("square-plus", size="3",on_click=rx.redirect(urls.LOGIN_URL)),
                content=f"Log in Create a new {my_title}")
            ),
        ),  
        rx.match(
            my_title,
            ("project", form_project()),
            ("organization", form_org()),
            ("user", form_user()),
            form_org(),
            ),
        on_open_change=[upload_logo_org.State.clear_image,
                    upload_image.State.clear_image,
                    upload_logo.State.clear_image,]
    )

def search_popover(my_title:str):
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon_button("search-check", size="3")),
        rx.match(
            my_title,
            ("project", search_project()),
            ("organization", search_org()),
            form_org()),
    )
    
def search_user(my_title:str):
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon_button("user-round-search", size="3")),
        rx.match(
            my_title,
            ("project", search_user_project()),
            ("organization", search_user_org()),)
    )
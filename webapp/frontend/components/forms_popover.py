import reflex as rx
from .user_input_text import SimpleTextInput
from .forms import ProjectForm,InstitutionForm, VideoForm
from .org_forms  import form_org,search_org
from .project_forms  import form_project,search_project
from .user_forms import form_user,search_user_org,search_user_project


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
        rx.tooltip(rx.dialog.trigger(rx.icon_button("square-plus", size="3")),
                    content=f"Add new {my_title}"),
        rx.match(
            my_title,
            ("project", form_project()),
            ("organization", form_org()),
            ("user", form_user()),
            form_org(),
            ),
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
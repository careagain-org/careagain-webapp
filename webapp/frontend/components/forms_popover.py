import reflex as rx
from .user_input_text import SimpleTextInput
from .forms import ProjectForm,InstitutionForm, VideoForm
from .org_forms  import form_org,search_org

project_form = ProjectForm.create
video_form = VideoForm.create

def add_new_popover(my_title:str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon_button("square-plus", size="3")),
        
        rx.match(
            my_title,
            ("project", project_form()),
            ("organization", form_org()),
            ("video",video_form()),
            ("device", form_org()),
            form_org(),
            ),
        
    )

def search_popover(my_title:str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon_button("search-check", size="3")),
        
        rx.match(
            my_title,
            ("project", project_form()),
            ("organization", search_org()),
            ("video",video_form()),
            ("device", form_org()),
            form_org(),
            ),
        
    )
import reflex as rx
from ..components.upload import upload_image
from ..components.input_text import SimpleTextInput
from .forms import ProjectForm,InstitutionForm, VideoForm

project_form = ProjectForm.create
instittution_form = InstitutionForm.create
video_form = VideoForm.create

def add_new_popover(my_title:str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon_button("square-plus", size="3")),
        
        rx.match(
            my_title,
            ("project", project_form()),
            ("institution", instittution_form()),
            ("video",video_form()),
            ("device", instittution_form()),
            instittution_form(),
            ),
        
    )
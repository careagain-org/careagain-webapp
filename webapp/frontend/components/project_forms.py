import reflex as rx
import uuid
from typing import List,Dict
from .user_input_text import SimpleTextInput
from .project_upload import upload_logo_project,upload_image_project
from ..states.project_state import ProjectState
from ..states.org_state import OrgState
from .upload import upload_logo_org
from .map import interactive_map
from ..components.project_card import project_grid_vertical


def form_project() -> rx.Component:
        device_class: list[str] = ["Class I","Class IIa","Class IIb","Class III",
                                   "Not Classified"]
        device_type: list[str] = ["Diagnostic","Treatment","Support",
                                  "Biomedical Reaseach", "Rehabilitation",  
                                  "Software","Monitoring","Other"]

        return rx.dialog.content(
            rx.dialog.title(f"Add new project"),
            rx.dialog.description(
                    f"Add new project details, required fields marked with *",
                    size="2",
                    margin_bottom="16px",
                ),
           rx.form(
                rx.flex(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Name *",size="3"),
                            rx.input(placeholder="Enter project name",
                            name="name",
                            required=True,
                            width="100%"),
                            width="100%"
                        ),
                        rx.vstack(
                            rx.heading("Type of device *",size="3"),
                            rx.select(device_type, 
                                    placeholder="Select Device Type",
                                    name="type",
                                    required=True,
                                    width="100%"),
                            width="100%"
                        ),
                        width="100%",
                    ),
                    rx.heading("Project Device Description",size="3"),
                    rx.text_area(
                        placeholder="Type here...",
                        name="description",),
                    rx.heading("Website url (if aplicable)",size="3"),
                    rx.input(placeholder="Enter url link",
                                name= "website"),
                    rx.hstack(
                            upload_logo_project(title="Logo",my_image=rx.get_upload_url(ProjectState.logo)),
                            upload_image_project(title="Representative image",my_image=rx.get_upload_url(ProjectState.image))
                            ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                color_scheme="gray",
                                variant="soft",
                                justify="start",),
                        ),
                        rx.dialog.close(
                            rx.button("Save",
                                type ="submit",
                                justify="end",
                                color_scheme="teal",),
                        ),
                        spacing="3",
                        margin_top="16px",
                        justify="end",
                        width="100%",
                    ),
                    spacing = "3",
                    direction = "column",
                    width="100%",
                ),
                on_submit=ProjectState.create_new_project,
                reset_on_submit=True,
                )
            )


def search_project() -> rx.Component:

    return rx.dialog.content(
        rx.dialog.title(f"Search existing organization"),
        rx.form(
            rx.flex(
            rx.input(rx.icon("search"),
                        placeholder="Enter project name",
                        default_value="",
                        name="name",
                        required=True,
                        width="100%",
                        align="start",
                        on_change=lambda value:ProjectState.filter_project(value)),
            project_grid_vertical(ProjectState.filtered_projects),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        color_scheme="gray",
                        variant="soft",
                        justify="start",
                        type ="button",
                    ),
                ),
                rx.dialog.close(
                    rx.button("Add",
                        type ="submit",
                        justify="end",
                        color_scheme="teal")
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
                width="100%",
            ),
            width="100%",
            spacing = "3",
            direction = "column",
        ),
        on_submit=ProjectState.join_project,
        reset_on_submit=True,
    )
)
    
def discover_project():
    return rx.form(
            rx.text('Discover the different projects:',),
            rx.hstack(
                rx.input(name="search",
                         width="30vw"),
                rx.icon_button("search"),
                width="100%"
            ),
            on_submit=ProjectState.search_project,
            width="100%",
            spacing="2"
        ),


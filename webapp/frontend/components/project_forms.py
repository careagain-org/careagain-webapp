import reflex as rx
from .upload import ImageUpload
from ..states.project_state import ProjectState
from ..states.org_state import OrgState
from ..components.project_card import project_grid_vertical
from ..constants import urls

upload_logo = ImageUpload.create()
upload_image = ImageUpload.create()

def form_project() -> rx.Component:
        status: list[str] = ["Prototype","Technically tested","Clinically tested",
                             "Regulatory body approval"]
        device_class: list[str] = ["Class I","Class IIa","Class IIb","Class III",
                                   "Not Classified"]
        device_type: list[str] = ["Diagnostic","Treatment","Support",
                                  "Research", "Rehabilitation",  
                                  "Software","Monitoring","Other"]

        return rx.dialog.content(
            rx.dialog.title(f"Add new project"),
            rx.dialog.description(
                    rx.link("Click here to see documentation to create projects. ",href=urls.DOCS_URL),
                    f"Required fields marked with *",
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
                        rx.vstack(
                            rx.heading("Status *",size="3"),
                            rx.select(status, 
                                    placeholder="Select Project Status",
                                    name="status",
                                    required=True,
                                    width="100%"),
                            width="100%"
                        ),
                        width="100%",
                    ),
                    rx.heading("Organization of the project",size="3"),
                    rx.select(OrgState.my_org_names,
                                placeholder="Select your Organization / Institution /group participating in the project",
                                name="org_name",
                                width="100%"),
                    rx.heading("Project Device Description",size="3"),
                    rx.text_area(
                        placeholder="Type here...",
                        name="description",),
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Website url (if aplicable)",size="3"),
                            rx.input(placeholder="Enter url link",
                                name= "website",
                                width="100%"),
                            width="100%"
                        ),
                        rx.vstack(
                            rx.heading("Git repo (if aplicable)",size="3"),
                            rx.input(placeholder="Enter url link",
                                name= "repo",
                                width="100%"),
                            width="100%"
                        ),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.vstack(rx.heading("Project Logo",size="3"),
                            upload_logo,
                            rx.input(
                                name="logo",
                                value=upload_logo.State.image_name,
                                type="hidden",
                            ),),
                        rx.vstack(rx.heading("Project Image",size="3"),
                            upload_image,
                            rx.input(
                                name="image",
                                value=upload_image.State.image_name,
                                type="hidden",
                            ),),
                        width="100vw",
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Manual guide url (.pdf)",size="3"),
                            rx.input(placeholder="Enter url link to download",
                                name= "guide",
                                width="100%"),
                            width="100%"
                        ),
                        rx.vstack(
                            rx.heading("Attachment url (.zip)",size="3"),
                            rx.input(placeholder="Enter url link to download",
                                name= "attachment",
                                width="100%"),
                            width="100%"
                        ),
                        width="100%",
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
                on_submit=[ProjectState.create_new_project,ProjectState.remove_uploaded_files],
                reset_on_submit=True,
                )
            )


def search_project() -> rx.Component:

    return rx.dialog.content(
        rx.dialog.title(f"Search existing project"),
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
    

def update_logo_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Update project logo"), on_click=ProjectState.remove_uploaded_files),
        rx.dialog.content(
            rx.form(
                rx.dialog.title("Update project logo"),
                upload_logo,
                rx.spacer(size="5"),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            color_scheme="gray",
                            variant="soft",
                            justify="start",
                            type ="button",),
                    ),
                    rx.dialog.close(
                        rx.button("Save",
                            type ="submit",
                            justify="end",
                            color_scheme="teal"),
                    ),
                    
                    spacing="5",
                    margin_top="16px",
                    justify="end",
                    width="100%",
                    min_height="100px",
                ),
                spacing="5",
                align="center",
                on_submit=ProjectState.supabase_upload_logo(ProjectState.project_id, upload_logo.State.image_name),
                reset_on_submit=True,
            ),
        ),
        on_open_change=[upload_logo.State.clear_image],
    ),
    

def update_image_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Update image"), on_click=ProjectState.remove_uploaded_files),
        rx.dialog.content(
            rx.form(
                rx.dialog.title("Update image"),
                upload_image,
                rx.spacer(size="5"),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            color_scheme="gray",
                            variant="soft",
                            justify="start",
                            type ="button",),
                    ),
                    rx.dialog.close(
                        rx.button("Save",
                            type ="submit",
                            justify="end",
                            color_scheme="teal"),
                    ),
                    
                    spacing="5",
                    margin_top="16px",
                    justify="end",
                    width="100%",
                    min_height="100px",
                ),
                spacing="5",
                align="center",
                on_submit=ProjectState.supabase_upload_image(ProjectState.project_id,upload_image.State.image_name),
                reset_on_submit=True,
            ),
        ),
        on_open_change=[upload_image.State.clear_image],
    )



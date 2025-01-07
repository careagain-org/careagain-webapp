import reflex as rx
import httpx
from ..states.project_state import ProjectState
from ..constants import urls
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())
s3_url = os.environ.get("SUPABASE_S3_URL")
s3_bucket = os.environ.get("SUPABASE_S3_BUCKET")
s3_prfolder = "/projects/project_id"
s3_imfolder = "/images/"

def project_card_vertical(image: str, 
                          project_title: str, 
                          project_description: str, 
                          project_id: str,
                          group_logo:str)-> rx.Component:

    return rx.box(
        rx.card(
            rx.link(
            rx.hstack(
                rx.image(src=image,
                        width="120px",
                        height="120px"),
                rx.vstack(
                    # rx.image(src=group_logo,
                    #     height="40px",
                    #     align="right"),
                    rx.heading(project_title),
                    rx.text(project_description),
                    spacing="5"
                ),
            ),
            ),
            width = "100%",
            size="3",
            # align="center",
            on_click=ProjectState.select_project(project_id),
        ),
        height = 'auto',
        #width = '100vw',
        align='center',
        width = "90%",

    )

def project_grid_vertical()-> rx.Component:

    return rx.vstack(
        rx.cond(
            ProjectState.projects != [],
            rx.foreach(ProjectState.projects, lambda value, i: 
                        project_card_vertical(
                            image = value["image"],
                            project_title = value["project_name"],
                            project_description = value["description"],
                            project_id = value["project_id"],
                            group_logo = "logo1.png")),
            rx.spinner(),#rx.text("No projects available")
        ),   
        spacing_y="4",
        #width="100%",
        align ="start",
        justify = "start"
    )

def project_card_horizontal(image: str, 
                            project_title: str, 
                            project_description: str, 
                            project_id: str,
                            group_logo:str)-> rx.Component:

    return rx.container(
        rx.card(
            rx.link(
                rx.flex(
                    rx.image(src=image,
                            width="140px",
                            height="140px"),
                    rx.heading(project_title,align="center"),
                    spacing="2",
                    direction="column",
                    padding ="0",
                    align="center"
                ),
                href=f"/{urls.INDIVIDUAL_PROJECT_URL}{project_id}",
                on_click=ProjectState.select_project(project_id),
            ),
            # as_child=True,
            size="5",
            height='200px',
            width='150px',
            padding ="1%",
            # align="center",
        ),
        height = 'auto',
        align='start',
        width = '220px',

    )

def project_grid_horizontal()-> rx.Component:
    return rx.scroll_area(
        rx.hstack(
            rx.cond(
                ProjectState.projects != [],
                rx.foreach(ProjectState.projects, lambda value, i: 
                            project_card_horizontal(image = value["image"],
                                        project_title = value["project_name"],
                                        project_description = value["description"],
                                        project_id = value["project_id"],
                                        group_logo = "logo1.png")),
                rx.text("No projects available")
            ),   
            # spacing_y="1",
            #width="100%",
            align ="start",
            justify = "start"
        ),
        align ="start",
        justify = "start",
        type="hover",
        scrollbars="horizontal",
        style={"height": '220px'},
)
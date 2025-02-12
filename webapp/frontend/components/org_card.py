import reflex as rx
import httpx
from ..states.org_state import OrgState
from ..constants import urls
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())
s3_url = os.environ.get("SUPABASE_S3_URL")
s3_bucket = os.environ.get("SUPABASE_S3_BUCKET")
s3_prfolder = "/projects/project_id"
s3_imfolder = "/images/"

def org_card_vertical(org)-> rx.Component:
    return rx.box(
        rx.card(
            rx.hstack(
                rx.avatar(src=f"{org["logo"]}",
                        width="50px",
                        height="50px"),
                rx.vstack(
                    rx.heading(org["name"],size="3"),
                    rx.text(org["type"]),
                    rx.text(org["adress"]),
                    spacing="1",
                ),
                rx.cond(org["org_id"] == OrgState.org_id,
                        rx.button("Select",disabled=True,type="button"),
                        rx.button("Select",disabled=False,
                            on_click = lambda: OrgState.select_org(org["org_id"]),
                            type="button"),
                        )
            ),
            width = "100%",
            size="3",
            _hover={"color": "teal"}
        ),
        height = 'auto',
        #width = '100vw',
        align='start',
        width = "100%",

    )

def org_grid_vertical(orgs)-> rx.Component:

    return rx.vstack(
        rx.cond(
            orgs != [],
            rx.foreach(orgs, lambda org, i: 
                        org_card_vertical(org),),
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
                align="start"
            ),
            # as_child=True,
            size="5",
            height='220px',
            width='200px',
            padding ="1%",
            align="start",
        ),
        height = 'auto',
        align='start',
        width = '250px',

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
        style={"height": '250px'},
)
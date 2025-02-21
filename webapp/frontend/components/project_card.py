import reflex as rx
import httpx
from ..states.project_state import ProjectState
from ..constants import urls
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())

def big_project_card_vertical(project)-> rx.Component:

    return rx.box(
        rx.link(
            rx.card(
                rx.hstack(
                    rx.hstack(
                        rx.avatar(src=f"{project["image"]}",
                                width="100px",
                                height="100px",),
                        rx.vstack(
                            rx.heading(project["name"]),
                            rx.scroll_area(rx.text(project["description"]),
                                scrollbars="vertical",
                                style={"height": 60},),
                            spacing="2",
                        ),
                        align='start',),
                    rx.image(src=f"{project["logo"]}",
                                width="auto",
                                height="50px"),
                    justify="between",
                ),
                width = "100%",
                size="3",
            ),
            on_click=lambda: ProjectState.to_project_view(project["project_id"]),
        ),
        height = 'auto',
        width = "90%",
    )

def project_card_vertical(project)-> rx.Component:

    return rx.box(
        rx.card(
            rx.hstack(
                rx.avatar(src=f"{project["image"]}",
                        width="50px",
                        height="50px"),
                rx.vstack(
                    # rx.image(src=group_logo,
                    #     height="40px",
                    #     align="right"),
                    rx.heading(project["name"]),
                    rx.text(project["description"]),
                    spacing="5"
                ),
                rx.cond(project["project_id"] == ProjectState.project_id,
                        rx.button("Select",disabled=True,type="button"),
                        rx.button("Select",disabled=False,
                            on_click = lambda: ProjectState.select_project(project["project_id"]),
                            type="button"),
                        ),
            ),
            width = "100%",
            size="3",
        ),
        height = 'auto',
        align='start',
        width = "100%",

    )

def project_grid_vertical(projects)-> rx.Component:

    return rx.vstack(
        rx.cond(
            projects != [],
            rx.foreach(projects, lambda value, i: 
                        project_card_vertical(value)),
            rx.spinner(),#rx.text("No projects available")
        ),   
        spacing_y="4",
        #width="100%",
        align ="start",
        justify = "start"
    )
    
def big_project_grid_vertical(projects)-> rx.Component:

    return rx.vstack(
        rx.cond(
            projects != [],
            rx.foreach(projects, lambda value, i: 
                        big_project_card_vertical(value)),
            rx.spinner(),#rx.text("No projects available")
        ),   
        spacing_y="4",
        width="90%",
        align ="start",
        justify = "start"
    )

def project_card_horizontal(project)-> rx.Component:

    return rx.container(
        rx.card(
            rx.link(
                rx.flex(
                    rx.avatar(src=f"{project["image"]}",
                            width="140px",
                            height="140px"),
                    rx.heading(project["name"],align="center"),
                    spacing="2",
                    direction="column",
                    padding ="0",
                    align="center"
                ),
                href=urls.IND_PROJECT_URL,
                on_click=ProjectState.to_project_view(project["project_id"]),
                align="start"
            ),
            # as_child=True,
            size="5",
            height='220px',
            width='180px',
            padding ="5%",
            align="start",
        ),
        height = 'auto',
        align='start',
        width = '250px',

    )

def project_grid_horizontal(projects,cols:int,rows:int)-> rx.Component:
    return rx.grid(
        rx.cond(
            projects != [],
            rx.foreach(projects, lambda value, i: 
                        project_card_horizontal(value)),
            rx.text("No projects available")
        ),   
        spacing="5",
        columns=str(cols),
        rows=str(rows),
        width="100%",
        align ="start",
        justify = "start"
    ),
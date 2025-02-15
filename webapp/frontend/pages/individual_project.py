import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..states.project_state import ProjectState
from ..states.auth_state import AuthState
from typing import Dict
urls.INDIVIDUAL_PROJECT_URL

@rx.page(route=f"/[urls.INDIVIDUAL_PROJECT_URL][ProjectState.selected_id]")
def individual_project() -> rx.Component:
    my_child = rx.vstack(
        rx.link(rx.icon('arrow_left'),href=urls.PROJECTS_URL),
        rx.heading(ProjectState.selected_project['project_name'], size="9"),
        rx.hstack(
            rx.icon("globe"),
            rx.link("Link to Website",href=ProjectState.selected_project['link'])
        ),
        rx.hstack(
            rx.icon("building-2"),
            rx.link(f"Developed by: {'org'}",href=ProjectState.selected_project['link'])
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("file-text"),
            rx.heading("Description",size="5"),
            id="description_section",
            width='90%',
            align="start",
        ),
        rx.flex(
            rx.image(ProjectState.selected_project['image'],
                     width="30%"),
            rx.vstack(
                rx.text(ProjectState.selected_project['description']),
                width="60%"
            ),
            align='start',
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("download"),
            rx.heading("Downloads",size="5"),
        ),
        rx.button("Download",
                on_click=rx.download(
                    url={ProjectState.selected_project['image']},
                    filename="test",
                ),
                id="download_button",
            ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("newspaper"),
            rx.heading("News and Publications",size="5"),
        ),
        align = "start",
        justify="start",
        width ="100%"
    )

    return platform_base(my_child)
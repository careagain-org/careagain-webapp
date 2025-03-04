import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..states.project_state import ProjectState
from ..states.auth_state import AuthState
from typing import Dict
from ..components.user_card import users_grid_horizontal


@rx.page(route=urls.IND_PROJECT_URL,on_load=ProjectState.find_members_project)
def view_project() -> rx.Component:
    my_child = rx.vstack(
        rx.link(rx.icon('arrow_left'),href=urls.PROJECTS_URL),
        rx.hstack(
            rx.heading(ProjectState.selected_project['name'], size="9"),
            rx.avatar(src=f"{ProjectState.selected_project['logo']}", heigh="50px",justify="end"),
            justify="between",
        ),
        rx.hstack(
            rx.icon("globe"),
            rx.link(ProjectState.selected_project['website'],href=ProjectState.selected_project['website'])
        ),
        rx.hstack(
            rx.icon("github"),
            rx.link(ProjectState.selected_project['repo'])#,href=ProjectState.selected_project['repo'])
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
            rx.image(src=f"{ProjectState.selected_project['image']}",
                     width="30%"),
            rx.vstack(
                rx.text(ProjectState.selected_project['description']),
                width="60%"
            ),
            align='start',
            spacing="5",
            padding="5"
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
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("circle-user-round"),
            rx.heading("Members",size="5"),
        ),
        users_grid_horizontal(ProjectState.project_members,cols=6,rows=3),
        width ="100%",
        spacing="3"
    )

    return platform_base(my_child)
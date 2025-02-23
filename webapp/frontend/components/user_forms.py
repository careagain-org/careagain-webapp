import reflex as rx
import uuid
from typing import List,Dict
from .user_input_text import SimpleTextInput
from .upload import upload_logo_org
from ..states.project_state import ProjectState
from ..states.user_state import UserState
from ..states.org_state import OrgState
from .upload import upload_logo_org
from .map import interactive_map
import clipboard
import os
from ..components.user_card import user_grid_vertical

user_types=["admin","user"]


def form_user() -> rx.Component:

    return rx.dialog.content(
        rx.dialog.title(f"Invite new user"),
        rx.dialog.description(
                f"Send an invitation to join the community, required fields marked with *",
                size="2",
                margin_bottom="16px",
            ),
        rx.form(
            rx.flex(
                rx.vstack(
                    rx.input(placeholder="Enter email to send invitation",
                        name="email",
                        required=True,
                        width="100%"),
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
        on_submit=UserState.invite_user,
        reset_on_submit=True,
    ),
    )
                


def search_user_org() -> rx.Component:

    return rx.dialog.content(
        rx.dialog.title(f"Search for an existing user"),
        rx.dialog.description(
                f"Send name/username in the platform *",
                size="2",
                margin_bottom="16px",
            ),
        rx.form(
            rx.flex(
                rx.input(rx.icon("search"),
                            placeholder="Enter username in the platform",
                            default_value="",
                            name="username",
                            required=True,
                            align="start",
                            width="100%",
                            on_change=lambda value:UserState.filter_user(value)),
                user_grid_vertical(UserState.filtered_users),
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
            on_submit=lambda: OrgState.user_join_org(UserState.selected_user_id),
            reset_on_submit=True,
        )
    )


def search_user_project() -> rx.Component:

    return rx.dialog.content(
        rx.dialog.title(f"Search an existing user"),
        rx.form(
            rx.flex(
            rx.input(rx.icon("search"),
                        placeholder="Enter username in the platform",
                        default_value="",
                        name="username",
                        required=True,
                        width="100%",
                        align="start",
                        on_change=lambda value:UserState.filter_user(value)),
            user_grid_vertical(UserState.filtered_users),
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
        on_submit=lambda: ProjectState.user_join_project(UserState.selected_user_id),
        reset_on_submit=True,
    )
)
    
def discover_user():
    return rx.form(
            rx.text('Discover the users in the community:',),
            rx.hstack(
                rx.input(name="search",
                         width="30vw"),
                rx.icon_button("search"),
                width="100%"
            ),
            on_submit=UserState.search_user,
            width="100%",
            spacing="2"
        ),
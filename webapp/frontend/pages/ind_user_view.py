import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..states.user_state import UserState
from ..states.auth_state import AuthState
from typing import Dict
from ..components.map import interactive_map
from ..components.user_card import users_grid_horizontal
from ..components.org_table import table_pagination as orgs_tables
from ..components.project_table import table_pagination as projects_tables


@rx.page(route=f"{urls.IND_USER_URL}/[us_id]", on_load=[UserState.load_user_page,
                                                        UserState.get_user_projects,
                                                        UserState.get_user_orgs])
def view_user() -> rx.Component:
    
    my_child = rx.vstack(
        # rx.link(rx.icon('arrow_left'),href=urls.COMMUNITY_PLATFORM),
        rx.hstack(
            rx.image(src=f"{UserState.selected_user['profile_image']}",
                        border_radius="15px 15px 15px 15px",
                        width="20%",
                        heigth="auto"),
            rx.vstack(
                rx.hstack(
                    rx.heading(f"{UserState.selected_user['first_name']}  {UserState.selected_user['last_name']}", size="9"),
                    rx.cond(UserState.selected_user['verified'],
                            rx.badge("Verified",variant="surface",color_scheme="teal"),
                            rx.badge("Non-Verified",variant="surface",color_scheme="amber")),
                    align="center",
                ),
                rx.hstack(
                    rx.icon("globe"),
                    # rx.link(f"{UserState.selected_user['linkedin']}",href=f"{UserState.selected_user['web_link']}",is_external=True)
                ),
                rx.divider(width='90%'),
                rx.vstack(
                    rx.hstack(
                        rx.icon("file-text"),
                        rx.heading("Bio / Description",size="5"),
                        id="description_section",
                        width='90%',
                        align="start",
                    ),
                    rx.text(UserState.selected_user['description']),
                    width="60%"
                ),
                rx.divider(width='90%'),
                rx.hstack(
                    rx.icon("map-pin-house"),
                    rx.heading("Country",size="5"),
                ),
                rx.text(UserState.selected_user['country']),
                rx.divider(width='90%'),
                rx.hstack(
                    rx.icon("building-2"),
                    rx.heading("Organization",size="5"),
                ),
                orgs_tables(UserState.user_orgs),
                rx.divider(width='90%'),
                rx.hstack(
                    rx.icon("square-library"),
                    rx.heading("Projects",size="5"),
                ),
                projects_tables(UserState.user_projects),
                width="100%",
            ),
            width="100%",
            spacing="7",
        )
    )
    return platform_base(my_child)

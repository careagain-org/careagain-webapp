import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..states.org_state import OrgState
from ..states.auth_state import AuthState
from typing import Dict
from ..components.map import interactive_map,map_org
from ..components.user_card import users_grid_horizontal


@rx.page(route=urls.IND_ORG_URL)
def view_organization() -> rx.Component:
    my_child = rx.vstack(
        rx.link(rx.icon('arrow_left'),href=urls.COMMUNITY_PLATFORM),
        rx.hstack(
            rx.heading(OrgState.selected_org['name'], size="9"),
            rx.cond(OrgState.selected_org['verified'],
                    rx.badge("Verified",variant="surface",color_scheme="teal"),
                    rx.badge("Non-Verified",variant="surface",color_scheme="amber")),
            align="center",
        ),
        rx.hstack(
            rx.icon("globe"),
            rx.link(OrgState.selected_org['website'],href=OrgState.selected_org['website'])
        ),
        rx.hstack(
            rx.icon("mail"),
            rx.text(OrgState.selected_org['email'])
        ),
        rx.divider(width='90%'),
        
        rx.flex(
            rx.image(src=f"{OrgState.selected_org['logo']}",
                     width="30%"),
            rx.vstack(
                rx.hstack(
                    rx.icon("file-text"),
                    rx.heading("Description",size="5"),
                    id="description_section",
                    width='90%',
                    align="start",
                ),
                rx.text(OrgState.selected_org['description']),
                width="60%"
            ),
            align='start',
            spacing = "5",
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("map-pin-house"),
            rx.heading("Location",size="5"),
        ),
        rx.hstack(
            rx.box(
                map_org(),
                width="30%"
            ),
            rx.vstack(
                rx.heading("Address",size="3"),
                rx.text(OrgState.selected_org['address']),
                rx.text(OrgState.selected_org['country']),
                width="70%" 
            ),
            align="center",
            justify="center",
            width='100%'
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("circle-user-round"),
            rx.heading("Members",size="5"),
        ),
        users_grid_horizontal(OrgState.org_members,cols=6,rows=3)
        
    )

    return platform_base(my_child)

# @rx.page(route="/[urls.INDIVIDUAL_ORG_URL]/[OrgState.org_id]")
# def view_organization() -> rx.Component:
#     my_child = rx.vstack(
#         rx.heading(OrgState.selected_org['org_name'], size="9"),
#     )

#     return platform_base(my_child)
import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..states.org_state import OrgState
from ..states.auth_state import AuthState
from typing import Dict
from ..components.map import interactive_map
from ..components.user_card import users_grid_horizontal
from ..components.org_input_text import OrgEditableText

editable_text = OrgEditableText.create

@rx.page(route=f"/org_edit")
def edit_organization() -> rx.Component:
    org=OrgState.selected_org
    my_child = rx.vstack(
        rx.link(rx.icon('arrow_left'),href=urls.COMMUNITY_PLATFORM),
        rx.hstack(
            rx.heading(org['name'], size="9"),
            rx.cond(org['verified'],
                    rx.badge("Verified",variant="surface",color_scheme="teal"),
                    rx.badge("Non-Verified",variant="surface",color_scheme="amber")),
            align="center",
        ),
        rx.hstack(
            rx.icon("globe"),
            editable_text(value = org["web_link"],key = "web_link"),
        ),
        rx.hstack(
            rx.icon("mail"),
            editable_text(value = org["email"],key = "email"),
            # rx.text(OrgState.selected_org['email'])
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
            rx.image(org['logo'],
                     width="30%"),
            rx.vstack(
                editable_text(value = org["description"],key = "description"),
                width="60%"
            ),
            align='start',
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("map-pin-house"),
            rx.heading("Location",size="5"),
        ),
        rx.hstack(
            interactive_map(),
            rx.vstack(
                rx.heading("Address",size="3"),
                editable_text(value = org["address"],key = "address"),
            ),
            align="center",
            justify="center",
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("circle-user-round"),
            rx.heading("Members",size="5"),
        ),
        users_grid_horizontal(OrgState.org_members)
        
    )

    return platform_base(my_child)

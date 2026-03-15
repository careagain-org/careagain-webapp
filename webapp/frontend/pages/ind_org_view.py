import reflex as rx 
import reflex_clerk_api as reclerk
from ..layout import platform_layout
from ..constants import urls
from ..states.org_state import OrgState
from ..states.auth_state import AuthState
from ..states.user_state import UserState
from typing import Dict
from ..components.map import interactive_map,map_org
from ..components.user_card import users_grid_horizontal
from ..components.button_follow import FollowButton
from ..components.project_table import table_pagination

orgs_following = []

@rx.page(route=f"{urls.IND_ORG_URL}/[or_id]", on_load=[UserState.get_user_orgs,
                                                       OrgState.load_org_page,
                                                        OrgState.find_members_org,
                                                        OrgState.get_orgs])
def view_organization() -> rx.Component:
    my_child = rx.vstack(
        # rx.link(rx.icon('arrow_left'),href=urls.COMMUNITY_PLATFORM),
        rx.flex(
            rx.heading(OrgState.selected_org['name'], size="9"),
            reclerk.signed_in(
                rx.cond(OrgState.is_org_member,
                            rx.button("Unfollow",variant="outline",type="button",
                                    on_click = lambda: OrgState.user_unfollow_org(UserState.my_details["user_id"]),
                                    ),
                            rx.button("Follow",variant="solid",
                                on_click = lambda: OrgState.user_follow_org(UserState.my_details["user_id"]),
                                type="button"),
                            ),
            ),
            justify="start",
            direction="row",
            align="center",
            spacing="5",
            width="90%",
            
        ),
        rx.hstack(
                    rx.text("Status: ",color="accent"),
                    rx.cond(OrgState.selected_org['verified'],
                        rx.badge("Verified",variant="surface",color_scheme="teal"),
                        rx.badge("Non-Verified",variant="surface",color_scheme="amber")),
                    rx.text("Type: ",color="accent"),
                    rx.match(OrgState.selected_org["type"],
                     ("Research and Development",rx.badge("R&D",variant="surface",color_scheme="grass")),
                     ("Manufacturer",rx.badge("Manufacturer",variant="surface",color_scheme="brown")),
                     ("Logistics and Transport",rx.badge("Logistics and Transport",variant="surface",color_scheme="cyan")),
                     ("Hospital",rx.badge("Hospital or Health center",variant="surface",color_scheme="ruby")),
                     rx.badge("Not defined",variant="surface",color_scheme="gray")),
                    align="center",
                ),
        rx.hstack(
            rx.icon("globe"),
            rx.link(OrgState.selected_org['website'],href=str(OrgState.selected_org['website']),is_external=True)
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
                width="30%",
                min_height="200px",
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
        users_grid_horizontal(OrgState.org_members),
        rx.hstack(
            rx.icon("square-library"),
            rx.heading("Projects",size="5"),
        ),
        table_pagination(OrgState.org_projects,"organization"),
        width="100%",
        align="start",
    )

    return platform_layout(my_child)


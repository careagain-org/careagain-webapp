import reflex as rx 

from .platform_base import platform_base
from ..constants import urls
from ..components.map import create_map
from ..components.org_table import table_pagination
from ..components.org_card import big_org_grid_vertical
from ..components.user_card import users_grid_horizontal
from ..components.org_forms import discover_org
from ..components.user_forms import discover_user
from ..states.org_state import OrgState
from ..states.user_state import UserState
from ..components.forms_popover import add_new_popover
#from ..components.dropdown import selectors,SelectorsState

def filters_panel():
    return rx.flex(
            rx.vstack(
                rx.text('Discover workplaces close to you'),
                rx.input(      
                    rx.input.slot(rx.icon("search")),
                    placeholder="Search by address...",
                    type="search",
                    size="2",
                ),
            ),
            rx.vstack(
                rx.text('Organization Type'),
                rx.select(["Hospital", "Logistics & transport",
                            "Research & Development","Manufacturer"]),
            ),
            #selectors(),
            width="100%",
            spacing="9",
            justify='start',
            align_items="top",
            direction="row",
        ),


@rx.page(route=urls.COMMUNITY_PLATFORM,on_load=[OrgState.get_location,OrgState.get_orgs])
def community_page() -> rx.Component:
    my_child = rx.vstack(
                    rx.hstack(
                        rx.heading('Community', size="9"),
                        add_new_popover("organization"),
                        rx.tooltip(
                            rx.icon_button("file-cog",size="3",on_click=rx.redirect(urls.PROFILE_ORG_URL)),
                            content="Manage your organizations.",
                        ),
                        align="end",
                        spacing="5"
                    ),
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger("Map", value="tab-map",size="9"),
                            rx.tabs.trigger("Organizations", value="tab-orgs",size="5"),
                            rx.tabs.trigger("Users", value="tab-users",size="5"),
                            align="center",
                        ),
                        rx.tabs.content(
                            rx.vstack(
                                create_map(),
                                spacing="5",
                                weight="100%",
                                align="center"
                            ),
                            value="tab-map",
                        ),
                        rx.tabs.content(
                            rx.box(
                                rx.vstack(
                                    rx.spacer(),
                                    discover_org(),
                                    big_org_grid_vertical(OrgState.searched_orgs),
                                padding="2",
                                spacing="5"),),
                            value="tab-orgs",
                            spacing="5",
                            padding="5",
                            id="organizations",
                        ),
                        rx.tabs.content(
                            rx.spacer(size="5"),
                            rx.box(
                                rx.vstack(
                                    rx.spacer(),
                                    discover_user(),
                                    users_grid_horizontal(UserState.searched_users),
                                padding="2",
                                spacing="5"),),
                            value="tab-users",
                            id="users",
                        ),
                        default_value="tab-map",
                        spacing="5",
                        width="100%",
                    ),
                    spacing="5",
                    align="start",
                    id='community_page',
                )
    return platform_base(my_child)
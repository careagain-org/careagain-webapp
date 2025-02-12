import reflex as rx 

from .platform_base import platform_base
from ..constants import urls
from ..components.map import create_map
from ..components.table import table_pagination
from ..states.org_state import OrgState
#from ..components.dropdown import selectors,SelectorsState


@rx.page(route=urls.COMMUNITY_PLATFORM)
def community_page() -> rx.Component:
    my_child = rx.vstack(
                    rx.heading("Community",size="9"), 
                    rx.text('Discover workplaces close to you'),
                    rx.flex(
                        rx.vstack(
                            rx.input(      
                                rx.input.slot(rx.icon("search")),
                                placeholder="Search by address...",
                                type="search",
                                size="2",
                            )
                        ),
                        #selectors(),
                        width="100%",
                        spacing="9",
                        justify='between',
                        align_items="top",
                    ),
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger("Map", value="tab-map"),
                            rx.tabs.trigger("List", value="tab-list"),
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
                            table_pagination(OrgState.orgs),
                            value="tab-list",
                        ),
                        default_value="tab-map",
                        spacing="5",
                        width="100%",
                    ),
                    align="start",
                    id='community_page',
                    on_mount=[OrgState.get_location,OrgState.get_orgs]
                )
    return platform_base(my_child)
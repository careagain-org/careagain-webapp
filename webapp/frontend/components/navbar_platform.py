import reflex as rx
from ..components.notification_popover import notification_popover
from ..components.navbar_profile import navbar_profile
from ..constants import urls
from ..states import nav_state, auth_state

def navbar_icon(icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.icon(icon, weight="medium",color="teal"), 
        href=url,
        justify="center",
    )


def navbar_platform() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                # rx.input(      
                #     rx.input.slot(rx.icon("search")),
                #     placeholder="Search...",
                #     type="search",
                #     size="2",
                #     ),
                rx.menu.separator(),
                rx.color_mode.button(color="teal",size="3"),
                notification_popover(),
                navbar_profile(),
                spacing="5",
                justify="end",
                align_items="center"
            ),
        ),
        rx.mobile_and_tablet(
            
            rx.hstack(
                # navbar_icon("search", urls.HOME_URL),
                rx.menu.separator(),
                rx.color_mode.button(color="teal"),
                notification_popover(),
                navbar_profile(),
                spacing="5",
                justify="end",
                align_items="center"
            ),
        ),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="95%",
    )
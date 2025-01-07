import reflex as rx
from ..components.notification_popover import notification_popover
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
                rx.input(      
                    rx.input.slot(rx.icon("search")),
                    placeholder="Search...",
                    type="search",
                    size="2",
                    ),
                rx.menu.separator(),
                rx.color_mode.button(color="teal"),
                notification_popover(),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button("user", size="3",radius="full")
                    ),
                    rx.menu.content(
                        rx.menu.item("My profile", on_click=nav_state.NavState.to_profile),
                        rx.menu.separator(),
                        rx.menu.item("Log out",  on_click=auth_state.AuthState.handle_logout),
                    ),
                    justify="end",
                ),
                spacing="5",
                justify="end",
                align_items="center"
            ),
        ),
        rx.mobile_and_tablet(
            
            rx.hstack(
                navbar_icon("search", urls.HOME_URL),
                rx.menu.separator(),
                rx.color_mode.button(color="teal"),
                navbar_icon("bell", urls.HOME_URL),
                rx.icon_button(
                        rx.icon("user"),
                        size="3",
                        radius="full",
                    ),
                spacing="5",
                justify="end",
                align_items="center"
            ),
        ),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )
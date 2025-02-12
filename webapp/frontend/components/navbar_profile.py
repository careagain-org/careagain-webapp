import reflex as rx
from .notification_popover import notification_popover
from ..constants import urls
from ..states import nav_state, auth_state, user_state

def navbar_profile() -> rx.Component:
    return rx.menu.root(
            rx.menu.trigger(
                rx.button(rx.cond(user_state.UserState.my_details["profile_image"]=="",
                                  rx.icon("user", size=3,radius="full"),
                                  rx.avatar(src=user_state.UserState.my_details["profile_image"]),),
                                bg="transparent",
                                size="3",radius="full"),
            ),
            rx.menu.content(
                rx.menu.item("My profile", on_click=nav_state.NavState.to_profile),
                rx.menu.separator(),
                rx.menu.item("Log out",  on_click=auth_state.AuthState.handle_logout),
            ),
            justify="end",
        ),
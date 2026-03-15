import reflex as rx
import reflex_clerk_api as reclerk
from .notification_popover import notification_popover
from ..constants import urls
from ..states import nav_state, auth_state, user_state

reclerk.sign_out_button

def navbar_profile() -> rx.Component:
    return rx.menu.root(
            rx.menu.trigger(
                rx.button(rx.avatar(src=user_state.UserState.my_details["profile_image"],
                                    fallback=str(user_state.UserState.my_details["first_name"])[0:1],variant="solid"),
                                bg="transparent",
                                size="3",radius="full"),
            ),
            rx.menu.content(
                rx.menu.item(reclerk.sign_in_button("Log In")),#on_click=nav_state.NavState.to_login),
                rx.menu.item("My profile", on_click=nav_state.NavState.to_profile),
                rx.menu.separator(),
                rx.menu.item(reclerk.sign_out_button("Log out")), #  on_click=auth_state.AuthState.handle_logout),
            ),
            justify="end",
        ),
import reflex as rx
import reflex_clerk_api as reclerk
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
                rx.fragment(
                    reclerk.signed_out(
                        reclerk.sign_in_button(rx.button("Sign In", size="3", color="teal",variant ="soft",on_click=nav_state.NavState.to_login)),
                        reclerk.sign_up_button(rx.button("Sign Up", size="3", color="teal",variant ="outline",on_click=nav_state.NavState.to_signup)),
                    ),
                ),
                rx.fragment(
                    reclerk.signed_in(
                        reclerk.user_button()
                        # navbar_profile(),
                    ),
                ),
                spacing="4",
                justify="end",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            
            rx.hstack(
                # navbar_icon("search", urls.HOME_URL),
                rx.menu.separator(),
                rx.color_mode.button(color="teal"),
                notification_popover(),
                rx.fragment(
                    reclerk.signed_out(
                        reclerk.sign_in_button(rx.button("Sign In", size="3", color="teal",variant ="soft",on_click=nav_state.NavState.to_login)),
                    ),
                ),
                rx.fragment(
                    reclerk.signed_in(
                        reclerk.user_button()
                    ),
                ),
                spacing="4",
                justify="end",
                align_items="center"
            ),
        ),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
        # top="100%",
        # right="0",
        # padding_top="10px",
)
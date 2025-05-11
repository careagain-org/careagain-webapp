import reflex as rx

from ..constants import urls
from ..states import nav_state,auth_state
from .navbar_profile import navbar_profile

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium",color="teal"), href=url
    )

def sign_in_buttons() ->rx.Component:
    return rx.hstack(
            rx.button(
                "Sign Up",
                size="3",
                variant="outline",
                color="teal",
                on_click=nav_state.NavState.to_signup()
            ),
            rx.button("Log In", size="3", on_click=nav_state.NavState.to_login()),
        ),


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo0.png",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Care Again", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", urls.ABOUT_URL),
                    navbar_link("Problem", urls.PROBLEM_URL),
                    navbar_link("Vision", urls.SOLUTION_URL),
                    navbar_link("Community", urls.COMMUNITY_URL),
                    navbar_link("Contact", urls.CONTACT_URL),
                    spacing="5",
                ),
                rx.hstack(
                    rx.color_mode.button(color="teal"),
                    rx.hstack(
                            rx.button("Documentation",size="3",
                                variant="outline",
                                color="teal",on_click=nav_state.NavState.to_documentation()
                            ),
                            rx.button("Go to Platform", size="3", on_click=nav_state.NavState.to_platfom()),
                        ),
                    # rx.cond(auth_state.AuthState.is_authenticated,
                    #     navbar_profile(),
                    #     rx.hstack(
                    #         rx.button("Sign Up",size="3",
                    #             variant="outline",
                    #             color="teal",on_click=nav_state.NavState.to_signup()
                    #         ),
                    #         rx.button("Log In", size="3", on_click=nav_state.NavState.to_login()),
                    #     ),),
                    spacing="4",
                    justify="end",
                    color_scheme="teal",
                ),
                justify="between",
                align_items="center",
                color="teal"
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo0.png",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Care Again", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item("Home", on_click=nav_state.NavState.to_home),
                        # rx.menu.item("About us", on_click=nav_state.NavState.to_about_us),
                        # rx.menu.item("Community", on_click=nav_state.NavState.to_community),
                        # rx.menu.item("Contact", on_click=nav_state.NavState.to_contact),
                        rx.menu.separator(),
                        rx.menu.item("Platform",  on_click=nav_state.NavState.to_platfom),
                        rx.menu.item("Documentation", on_click=nav_state.NavState.to_documentation),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("teal", 3),
        padding="1em",
        position="fixed",
        top="0px",
        z_index="5",
        width="100%",
    )
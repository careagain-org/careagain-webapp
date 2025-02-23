import reflex as rx
from ..constants import urls
from ..states.auth_state import AuthState

def list_icons() ->rx.Component:
    return rx.fragment(
    rx.hstack(
                rx.divider(margin="0"),
                rx.text(
                    "Or continue with",
                    white_space="nowrap",
                    weight="medium",
                ),
                rx.divider(margin="0"),
                align="center",
                width="100%",
            ),
    rx.center(
                rx.icon_button(
                    rx.icon(tag="github"),
                    variant="soft",
                    size="3",
                ),
                rx.icon_button(
                    rx.icon(tag="facebook"),
                    variant="soft",
                    size="3",
                ),
                rx.icon_button(
                    rx.icon(tag="linkedin"),
                    variant="soft",
                    size="3",
                ),
                spacing="4",
                direction="row",
                width="100%",
            ))

def signup_multiple_thirdparty() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.hstack(
                    rx.image(
                        src="/logo0.png",
                        width="2.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                ),
                rx.heading(
                    "Create an account",
                    size="6",
                    as_="h2",
                    width="100%",
                ),
                rx.hstack(
                    rx.text(
                        "Already registered?",
                        size="3",
                        text_align="left",
                    ),
                    rx.link("Log in", href=urls.LOGIN_URL, size="3"),
                    spacing="2",
                    opacity="0.8",
                    width="100%",
                ),
                justify="start",
                direction="column",
                spacing="4",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Email address",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="user@reflex.dev",
                    type="email",
                    size="3",
                    width="100%",
                    on_change=AuthState.set_email(),
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Password",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                    on_change=AuthState.set_password(),
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.box(
                rx.checkbox(
                    rx.hstack(
                        rx.text(
                            "Agree to",
                            size="3",
                            text_align="left",
                        ),
                        rx.link("Terms and Conditions", href=urls.LOGIN_URL, size="3"),
                        spacing="2",
                        opacity="0.8",
                        width="100%"),
                    default_checked=True,
                    spacing="2",
                ),
                width="100%",
            ),
            rx.button("Register",size="3", width="100%",on_click=AuthState.handle_signup),
            #list_icons(),
        ),
        size="4",
        max_width="28em",
        width="100%",
    )
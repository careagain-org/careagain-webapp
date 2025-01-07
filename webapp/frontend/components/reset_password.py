import reflex as rx
from ..constants import urls
from ..states.auth_state import AuthState

def reset_password_card() -> rx.Component:
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
                    "Reset your password",
                    size="6",
                    as_="h2",
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
                    on_change=AuthState.set_email,
                ),
                spacing="2",
                justify="start",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Update your Password",
                        size="3",
                        weight="medium",
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                    on_change=AuthState.set_password,
                ),
                spacing="2",
                width="100%",
            ),
            rx.button("Reset password", size="3", width="100%", on_click=AuthState.update_password),
            #list_icons(),
            spacing="6",
            width="100%",
        ),
        size="4",
        max_width="28em",
        width="100%",
    )
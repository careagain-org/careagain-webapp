import reflex as rx
from ..constants import urls
from ..states.user_state import UserState

def sidebar_item(
    text: str, icon: str, href: str
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Home", "warehouse", urls.PLATFORM_URL),
        sidebar_item("Projects", "square-library", urls.PROJECTS_URL),
        sidebar_item("Community", "users", urls.COMMUNITY_PLATFORM),
        # sidebar_item("Videos", "square-play", urls.VIDEOS_URL),
        # sidebar_item("How-To's", "book", urls.PLATFORM_URL),
        # sidebar_item("Market", "store", urls.PLATFORM_URL),
        # sidebar_item("Dashboard", "layout-dashboard", urls.PLATFORM_URL),
        # sidebar_item("Analytics", "bar-chart-4", urls.PLATFORM_URL),
        # sidebar_item("Questions", "file-question", urls.QUESTIONS_URL),
        sidebar_item("Chat & FAQs", "message-square-code", urls.DISCORD_URL),
        # sidebar_item("Videos", "square-play", urls.YOUTUBE_URL),
        spacing="1",
        width="100%",
    )

def profile_button() -> rx.Component:
    return rx.container(
            rx.link(
                rx.hstack(
                    rx.cond(UserState.my_details["profile_image"]=="",
                        rx.icon_button(rx.icon("user"),
                                       size="3",
                                       radius="full",),
                        rx.avatar(src=UserState.my_details["profile_image"],
                                  size="3",
                                  radius="full",)),
                    rx.vstack(
                    rx.box(
                        rx.text(
                            "My profile",
                            size="3",
                            weight="bold",
                        ),
                        rx.text(
                            f"@{UserState.my_details["username"]}",
                            size="2",
                            weight="medium",
                        ),
                        width="100%",
                    ),
                    spacing="0",
                    align="start",
                    justify="start",
                    width="100%",
                ),
                padding_x="0.5rem",
                align="center",
                justify="start",
                width="100%",
            ),
            href=urls.PROFILE_URL,
        )
    )

def brand_header() ->rx.Component:
    return rx.hstack(
                rx.image(
                src="/logo0.png",
                width="2.25em",
                height="auto",
                border_radius="10%",
            ),
            rx.heading(
                "CareAgain", size="7", weight="bold"
            ),
            rx.badge("DEV",variant="solid",size="1"),
            align="center",
            justify="start",
            padding_x="0.5rem",
            width="100%",
            spacing="2",
        ),


def sidebar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                brand_header(),
                sidebar_items(),
                rx.spacer(),
                rx.vstack(
                    sidebar_item("Settings", "settings", "/#"),
                    #sidebar_item("Log out", "log-out", "/#"),
                    rx.divider(),
                    profile_button(),
                    width="100%",
                    spacing="1",
                ),
                spacing="5",
                position="fixed",
                left="0px",
                top="0px",
                z_index="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                height="100vh",
                width="17em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.icon("align-justify", size=30)
                ),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(
                                    rx.icon("x", size=30)
                                ),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                sidebar_item("Settings","settings","/#",),
                                #sidebar_item("Log out","log-out","/#",),
                                rx.divider(margin="0"),
                                profile_button(),
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
            height="100%",
            position="fixed",
        ),
    )
import reflex as rx
from ..constants import urls

def footer_item(text: str, href: str) -> rx.Component:
    return rx.link(rx.text(text, size="3"), href=href)


def footer_items_1() -> rx.Component:
    return rx.flex(
        rx.heading(
            "PRODUCTS", size="4", weight="bold", as_="h3"
        ),
        footer_item("Web Design", "/#"),
        footer_item("Web Development", "/#"),
        footer_item("E-commerce", "/#"),
        footer_item("Content Management", "/#"),
        footer_item("Mobile Apps", "/#"),
        spacing="4",
        text_align=["center", "center", "start"],
        flex_direction="column",
    )


def footer_items_2() -> rx.Component:
    return rx.flex(
        rx.heading(
            "RESOURCES", size="4", weight="bold", as_="h3"
        ),
        footer_item("Blog", "/#"),
        footer_item("Case Studies", "/#"),
        footer_item("Whitepapers", "/#"),
        footer_item("Webinars", "/#"),
        footer_item("E-books", "/#"),
        spacing="4",
        text_align=["center", "center", "start"],
        flex_direction="column",
    )

def footer_items_3() -> rx.Component:
    rx.vstack(
        rx.text(
            "JOIN OUR NEWSLETTER",
            size="4",
            weight="bold",
        ),
        rx.hstack(
            rx.input(
                placeholder="Your email address",
                type="email",
                size="3",
            ),
            rx.icon_button(
                rx.icon(
                    "arrow-right",
                    padding="0.15em",
                ),
                size="3",
            ),
            spacing="1",
            justify="center",
            width="100%",
        ),
        align_items=[
            "center",
            "center",
            "start",
        ],
        justify="center",
        height="100%",
    )


def social_link(icon: str, href: str) -> rx.Component:
    return rx.link(rx.icon(icon), href=href)


def socials() -> rx.Component:
    return rx.flex(
        # social_link("instagram", "/#"),
        # social_link("twitter", "/#"),
        # social_link("facebook", "/#"),
        social_link("youtube", urls.YOUTUBE_URL),
        social_link("linkedin", urls.LINKEDIN_URL),
        social_link("github",urls.GITHUB_URL),
        spacing="3",
        justify_content=["center", "center", "end"],
        width="100%",
    )

def low_footer()-> rx.Component:
    return rx.vstack(
        rx.divider(),
                rx.flex(
                    rx.hstack(
                        rx.image(
                            src="/logo0.png",
                            width="2em",
                            height="auto",
                            border_radius="25%",
                            white_space="nowrap",
                        ),
                        rx.text(
                            "© 2024 CareAgain, Inc",
                            size="3",
                            white_space="nowrap",
                            weight="medium",
                        ),
                        spacing="2",
                        align="center",
                        justify_content=[
                            "center",
                            "center",
                            "start",
                        ],
                        width="100%",
                    ),
                    socials(),
                    spacing="4",
                    flex_direction=["column", "column", "row"],
                    width="90%",
                ),
                spacing="5",
                width="100%",
                justify="center",
                align_items="center",
            ),


def footer_newsletter() -> rx.Component:
    return rx.el.footer(
        rx.container(
            rx.vstack(
                rx.flex(
                    footer_items_1(),
                    footer_items_2(),
                    rx.vstack(
                        rx.text(
                            "JOIN OUR NEWSLETTER",
                            size="4",
                            weight="bold",
                        ),
                        rx.hstack(
                            rx.input(
                                placeholder="Your email address",
                                type="email",
                                size="3",
                            ),
                            rx.icon_button(
                                rx.icon(
                                    "arrow-right",
                                    padding="0.15em",
                                ),
                                size="3",
                            ),
                            spacing="1",
                            justify="center",
                            width="100%",
                        ),
                        align_items=[
                            "center",
                            "center",
                            "start",
                        ],
                        justify="center",
                        height="100%",
                    ),
                    justify="between",
                    spacing="6",
                    flex_direction=["column", "column", "row"],
                    width="100%",
                ),
                low_footer(),
        ),
        width="100%",
        justify="center",
        align_items="center",
        id="box-footer",
        background_color="var(--gray-3)",
    )
 )
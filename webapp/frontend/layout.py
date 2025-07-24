import reflex as rx
import reflex_clerk_api as reclerk
from ..frontend.providers.clerk_provider import my_clerk_provider
from ..frontend.components.navbar import navbar
from ..frontend.components.navbar_platform import navbar_platform
from ..frontend.components.sidebar import sidebar
from ..frontend.components.footer import low_footer
from ..frontend.components.speed_dial import SpeedDialMenu

speed_dial_menu = SpeedDialMenu.create

# from podcast_discovery.ui.sidebar import user_sidebar

def render_menu():
    return rx.box(
        speed_dial_menu(),
        height="250px",
        position="relative",
        width="100%",
    )

def base_page(child: rx.Component ,*args,**kwargs) -> rx.Component:
    return my_clerk_provider(
        rx.fragment(
            navbar(),
            rx.box(
                # text_align="center", 
                height="3em"
            ),
            child,
            low_footer(),
            text_align="centre", 
            id="box-content-area",
            width="100%"
        ),
    )



def non_user_layout(child:rx.Component)-> rx.Component:

    return rx.fragment(
        rx.vstack(
            navbar_platform(),
            rx.box(
                child,
                id="box-content-area",
                width="100vw",
                height="100%"
            ), 
            low_footer(),
            width="100%",
            id='my-root-layout',),
            render_menu(),
            width="100%",
            height="100%"
        )



def user_layout(child:rx.Component)-> rx.Component:

    return rx.fragment(
            rx.hstack(
                sidebar(),
                rx.desktop_only(
                    rx.box(width="17em",height="100vh"),
                ),
                rx.vstack(
                    navbar_platform(),
                    rx.desktop_only(
                        rx.box(
                        child,
                        id="box-content-area",
                        width="80vw",
                        height="100%"
                    ), ),
                    rx.mobile_and_tablet(
                        rx.box(
                        child,
                        id="box-content-area",
                        width="100vw",
                        height="100vh"
                    ), ),
                    low_footer(),
                ),
            ),
            render_menu(),
            width="100%",
            height="100%"
        )


def platform_layout(child:rx.Component, *args, **kwargs)-> rx.Component:

    return my_clerk_provider(
        rx.fragment(
        reclerk.clerk_loading(
            user_layout(rx.center(rx.spinner())),
        ),
        reclerk.clerk_loaded(
            rx.cond(child is None,
                    user_layout(rx.spinner()),
                    user_layout(child) 
                    )
            ),
        ),
    )
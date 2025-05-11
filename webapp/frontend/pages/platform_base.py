import reflex as rx
from ..constants import urls
from ..components.sidebar import sidebar
from ..components.footer import footer_newsletter,low_footer
from ..components.navbar_platform import navbar_platform
from ..components.footer import low_footer
from ..components.speed_dial import SpeedDialMenu
# from ..states.kinde_auth import AuthState
from ..states.auth_state import AuthState
from .login import login_page

speed_dial_menu = SpeedDialMenu.create

def render_menu():
    return rx.box(
        speed_dial_menu(),
        height="250px",
        position="relative",
        width="100%",
    )

def platform_base(child: rx.Component ,*args,**kwargs) -> rx.Component:
    platform = rx.fragment(
            rx.hstack(
                sidebar(),
                rx.desktop_only(
                    rx.box(width="17em",),
                ),
                rx.vstack(
                    navbar_platform(),
                    rx.desktop_only(
                        rx.box(
                        child,
                        # text_align="center", 
                        id="box-content-area",
                        width="83vw"
                    ), ),
                    rx.mobile_and_tablet(
                        rx.box(
                        child,
                        # text_align="center", 
                        id="box-content-area",
                        width="100vw"
                    ), ),
                    low_footer(),
                ),
            ),
            render_menu(),
            width="100%",
            # on_mount= AuthState.check_session
        )
    return platform
    # rx.cond(
    #     AuthState.is_authenticated,
    #     platform,
    #     login_page() 
    # )

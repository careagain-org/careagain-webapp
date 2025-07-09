import reflex as rx
from ..components.footer import footer_newsletter,low_footer
from ..components.navbar import navbar
from ..components.footer import low_footer
from ..providers import my_clerk_provider

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

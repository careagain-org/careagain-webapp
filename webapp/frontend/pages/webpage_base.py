import reflex as rx
from ..components.footer import footer_newsletter,low_footer
from ..components.navbar import navbar
from ..components.footer import low_footer

def base_page(child: rx.Component ,*args,**kwargs) -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.box(
            child,
            text_align="centre", 
            id="box-content-area",
            width="100%"
        ),
        low_footer()
    )

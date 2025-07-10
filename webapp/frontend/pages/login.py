import reflex as rx 
import reflex_clerk_api as reclerk
from ..layout import platform_layout
from ..constants import urls
from ..components.login_card import login_multiple_thirdparty

@rx.page(route=urls.LOGIN_URL)
def login_page() -> rx.Component:
    my_child = rx.center(
            reclerk.sign_in(),
            #login_multiple_thirdparty(),
            spacing="5",
            justify="center",
            align="center",
            min_height="90vh",
            id='my-child',
        )
        
    return platform_layout(my_child)
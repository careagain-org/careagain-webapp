import reflex as rx 
import reflex_clerk_api as reclerk
from ..layout import platform_layout
from ..constants import urls
from ..components.signup_card import signup_multiple_thirdparty

@rx.page(route=urls.SIGNUP_URL)
def signup_page() -> rx.Component:
    my_child = rx.center(
                # signup_multiple_thirdparty(),
                reclerk.sign_up(),
                spacing="5",
                justify="center",
                align="center",
                min_height="90vh",
                id='my-child',
            )
    return platform_layout(my_child)
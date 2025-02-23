import reflex as rx 

from .webpage_base import base_page
from ..constants import urls
from ..components.signup_card import signup_multiple_thirdparty

@rx.page(route=urls.SIGNUP_URL)
def signup_page() -> rx.Component:
    my_child = rx.center(
                signup_multiple_thirdparty(),
                spacing="5",
                justify="center",
                align="center",
                min_height="90vh",
                id='my-child',
            )
    return base_page(my_child)
import reflex as rx 
from .webpage_base import base_page
from ..constants import urls
from ..components.reset_password import reset_password_card

@rx.page(route=urls.RESET_PASSWORD_URL)
def reset_password_page() -> rx.Component:
    my_child = rx.vstack(
            reset_password_card(),
            spacing="5",
            justify="center",
            align="center",
            min_height="90vh",
            id='my-child',
        )
        
    return base_page(my_child)
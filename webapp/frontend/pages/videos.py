import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..components.forms_popover import add_new_popover
from ..states.project_state import ProjectState
from ..states.auth_state import AuthState

@rx.page(route=urls.VIDEOS_URL) #on_load= ProjectState.get_list_projects)
def platform_projects() -> rx.Component:
    my_child = rx.vstack(
        rx.hstack(
            rx.heading('Videos', size="9"),
            add_new_popover("video"),
            align="end",
            spacing="5"
        ),
        rx.text(
            'Discover the different videos',
        ),
        #videos_grid(),
        align = "start",
        justify="start",
        width ="100%"
    )
    return platform_base(my_child)
    
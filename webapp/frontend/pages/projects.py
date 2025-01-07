import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..components.project_card import project_grid_vertical
from ..components.forms_popover import add_new_popover
from ..states.project_state import ProjectState
from ..states.auth_state import AuthState

@rx.page(route=urls.PROJECTS_URL, on_load= ProjectState.get_list_projects)
def platform_projects() -> rx.Component:
    my_child = rx.vstack(
        rx.hstack(
            rx.heading('Projects', size="9"),
            add_new_popover("project"),
            align="end",
            spacing="5"
        ),
        rx.text(
            'Discover the different projects',
        ),
        project_grid_vertical(),
        align = "start",
        justify="start",
        width ="100%"
    )
    return platform_base(my_child)
    
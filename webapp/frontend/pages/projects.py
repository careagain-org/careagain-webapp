import reflex as rx 
import reflex_clerk_api as reclerk
from ..layout import platform_layout
from ..constants import urls
from ..components.project_card import big_project_grid_vertical
from ..components.project_forms import discover_project
from ..components.forms_popover import add_new_popover
from ..states.project_state import ProjectState
from ..states.auth_state import AuthState

@rx.page(route=urls.PROJECTS_URL, on_load= [AuthState.set_user_cookie, ProjectState.get_list_projects])
def platform_projects() -> rx.Component:
    my_child = rx.vstack(
        rx.hstack(
            rx.heading('OpenSource Projects', size="9"),
            add_new_popover("project"),
            rx.fragment(
                reclerk.signed_in(
                    rx.tooltip(
                    rx.icon_button("file-cog",size="3",on_click=rx.redirect(urls.PROFILE_PROJECT_URL)),
                    content="Manage your projects.",
                ),),
                reclerk.signed_out(
                    rx.tooltip(
                    rx.icon_button("file-cog",size="3",on_click=rx.redirect(urls.LOGIN_URL)),
                    content="Log in to Manage your projects.",)
                )
            ),
            align="end",
            spacing="5"
        ),
        discover_project(),
        big_project_grid_vertical(ProjectState.searched_projects),
        align = "start",
        justify="start",
        width ="100%",
        spacing="3"
    )
    return platform_layout(my_child)
    
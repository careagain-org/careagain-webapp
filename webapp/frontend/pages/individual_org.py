import reflex as rx 
from .platform_base import platform_base
from ..constants import urls
from ..states.org_state import OrgState
from ..states.auth_state import AuthState
from typing import Dict


@rx.page(route="/[urls.INDIVIDUAL_ORG_URL]/[OrgState.org_id]")
def individual_project() -> rx.Component:
    my_child = rx.vstack(
        rx.heading(OrgState.selected_org['org_name'], size="9"),
    )

    return platform_base(my_child)
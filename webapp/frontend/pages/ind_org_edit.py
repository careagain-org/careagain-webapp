import reflex as rx 
import reflex_clerk_api as reclerk
from ..layout import platform_layout
from ..constants import urls
from ..states.org_state import OrgState
from ..states.auth_state import AuthState
from typing import Dict
from ..components.map import map_org
from ..components.user_card import users_grid_horizontal
from ..components.user_table import table_pagination
from ..components.project_table import table_pagination as project_table_pagination
from ..components.org_forms import update_coordinates_form,update_image_form
from ..components.forms_popover import add_new,search_user,search_popover
from ..components.input_text import EditableText, EditableTextArea

editable_text = EditableText.create
editable_textarea = EditableTextArea.create
all_organization: list[str] = ["Hospital", f"Logistics and Transport",
                                    f"Research and Development","Manufacturer"]

def title_section(title:str, icon:str):
    return rx.hstack(
                rx.icon(icon),
                rx.heading(title,size="5"),
                align="start",
            ),
    

@rx.page(route=f"{urls.IND_EDIT_ORG_URL}/[or_id]",on_load=[AuthState.set_user_cookie,
                                                           OrgState.load_org_page,
                                                            OrgState.find_members_org,
                                                            OrgState.find_projects_org])
def edit_organization() -> rx.Component:
    org=OrgState.selected_org
    my_child = rx.cond(OrgState.is_org_admin,
        rx.vstack(
        rx.link(rx.icon('arrow_left'),href=urls.PROFILE_URL),
        rx.hstack(
            rx.heading(org['name'], size="9"),
            rx.cond(org['verified'],
                    rx.badge("Verified",variant="surface",color_scheme="teal"),
                    rx.badge("Non-Verified",variant="surface",color_scheme="amber")),
            align="center",
        ),
        rx.hstack(
            rx.icon("building"),
            rx.text("Type: "),
            rx.select(all_organization, 
                        value=org["type"],
                        placeholder="Select type of organization",
                        name="type",
                        on_change= lambda value: OrgState.update_org("type",value,org["org_id"])),
        ),
        rx.hstack(
            rx.icon("globe"),
            editable_text(
                value = org["website"],
                on_save=lambda text: OrgState.update_org("website", text, org["org_id"]),
            ),
        ),
        rx.hstack(
            rx.icon("mail"),
            editable_text(
                value = org["email"],
                on_save=lambda text: OrgState.update_org("email", text, org["org_id"]),
            ),
        ),
        rx.divider(width='90%'),
        rx.flex(
            rx.vstack(
                rx.hstack(
                    title_section("Logo Image","image"),
                    update_image_form(),
                ),
                rx.image(src=org["logo"],
                            border_radius="15px 15px 15px 15px",
                            heigth="auto"),
                width="25vw",
            ),
            rx.vstack(
                title_section("Description","file_text"),
                editable_textarea(
                    value = org["description"],
                    on_save=lambda text: OrgState.update_org("description", text, org["org_id"]),
                ),
                width="50%"
            ),
            align='start',
            spacing="5",
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("map-pin-house"),
            rx.heading("Location",size="5"),
            update_coordinates_form(),
        ),
        rx.hstack(
            rx.box(
                map_org(),
                width="30%",
                align="start",
            ),
            rx.vstack(
                rx.heading("Address",size="3"),
                editable_textarea(
                    value = org["address"],
                    on_save=lambda text: OrgState.update_org("address", text, org["org_id"]),
                ),
            ),
            align="center",
            justify="start",
            width="100%",
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("circle-user-round"),
            rx.heading("Members",size="5"),
        ),
        rx.hstack(
            # add_new("user"), #commented because I cannot invite without admin permissions
            rx.container(
                rx.hstack(
                search_user("project"),
                rx.text(f"Click to search an existing user"),
                align="center",
            ),),
            align="start",
            spacing="4",
        ),
        table_pagination(OrgState.org_members,"organization"),
                rx.divider(width='90%'),
        rx.hstack(
            rx.icon("square-library"),
            rx.heading("Projects",size="5"),
        ),
        rx.hstack(
            # add_new("user"), #commented because I cannot invite without admin permissions
            rx.container(
                rx.hstack(
                search_popover("project"),
                rx.text(f"Click to search an existing project"),
                align="center",
            ),),
            align="start",
            spacing="4",
        ),
        project_table_pagination(OrgState.org_projects),
        with_="100%",
        id="organization-edit",
        ),
        rx.callout(
            "You need admin privileges to edit the organization information.",
            icon="info",
        )
    )
    return platform_layout(my_child)

import reflex as rx 
import reflex_clerk_api as reclerk
from ..layout import platform_layout
from ..constants import urls
from ..states.project_state import ProjectState
from ..states.auth_state import AuthState
from typing import Dict
from ..components.map import interactive_map
from ..components.user_card import users_grid_horizontal
from ..components.user_table import table_pagination
from ..components.org_table import table_pagination as org_table
from ..components.forms_popover import add_new,search_user
from ..components.project_forms import update_logo_form,update_image_form
from ..components.input_text import EditableText, EditableTextArea

editable_text = EditableText.create
editable_textarea = EditableTextArea.create
status: list[str] = ["Prototype","Technically tested","Clinically tested",
                             "Regulatory body approval"]


def title_section(title:str, icon:str, text:str = "") -> rx.Component:
    return rx.hstack(
                rx.icon(icon),
                rx.heading(title,size="5"),
                rx.text(text),
                align="start",
            ),
    

@rx.page(route=f"{urls.IND_EDIT_PROJECT_URL}/[pr_id]", on_load= [AuthState.set_user_cookie,      
                                                            ProjectState.load_project_page,
                                                            ProjectState.find_members_project,
                                                            ProjectState.find_orgs_project])
def edit_project() -> rx.Component:
    project=ProjectState.selected_project
    my_child = rx.cond(ProjectState.is_project_admin,
        rx.vstack(
        rx.link(rx.icon('arrow_left'),href=urls.PROFILE_URL),
        rx.flex(
            rx.vstack(
                rx.heading(project['name'], size="9"),
                rx.cond(project['verified'],
                        rx.badge("Verified",variant="surface",color_scheme="teal"),
                        rx.badge("Non-Verified",variant="surface",color_scheme="amber")),
                rx.hstack(
                    rx.text("Status: "),
                    rx.select(status, 
                              value=project["status"],
                              placeholder="Select Project Status",
                              name="status",
                              on_change= lambda value: ProjectState.update_project("status",value,project["project_id"])),
                ),
                rx.hstack(
                    rx.icon("globe"),
                    editable_text(
                        value = project["website"],
                        on_save=lambda text: ProjectState.update_project("website", text, project["project_id"]),
                    ),
                ),
                rx.hstack(
                    rx.icon("github"),
                    editable_text(
                        value = project["repo"],
                        on_save=lambda text: ProjectState.update_project("repo", text, project["project_id"]),
                    ),
                ),   
                justify="between",      
            ),
            rx.vstack(
                rx.image(src=project["logo"],
                            border_radius="15px 15px 15px 15px",
                            height="100px"),
                update_logo_form(),
                width="20vw",
                justify="center",
                align="center"
            ),
            justify="between",
            spacing="5",  
            direction="row",
            width="100%",
        ),
        rx.divider(width='90%'),
        rx.flex(
            rx.vstack(
                title_section("Representative Image","image"),
                rx.image(src=project["image"],
                            border_radius="15px 15px 15px 15px",
                            height="auto",),
                update_image_form(),
                width="30vw",
            ),
            rx.vstack(
                title_section("Description","file_text"),
                editable_textarea(
                    value = project["description"],
                    on_save=lambda text: ProjectState.update_project("description", text, project["project_id"]),
                ),
                width="60%"
            ),
            align='start',
            spacing="5",
        ),
        rx.divider(width='90%'),
        rx.hstack(
            title_section("Downloads","file_text",text="*(include https:// or http:// in the urls)"),
            id="download_section",
            width='90%',
            align="start",
        ),
        rx.vstack(
            title_section("Manual Guide","scroll-text"),
            editable_textarea(
                value = project["guide"],
                on_save=lambda text: ProjectState.update_project("guide", text, project["project_id"]),
            ),
            width="60%"
        ),
        rx.vstack(
            title_section("Attachment url","package"),
            editable_textarea(
                value = project["attachment"],
                on_save=lambda text: ProjectState.update_project("attachment", text, project["project_id"]),
            ),
            width="60%"
        ),
        rx.divider(width='90%'),
        rx.hstack(
            rx.icon("building-2"),
            rx.heading("Organizations involved",size="5"),
        ),
        # rx.hstack(
        #     # add_new("user"), #commented because I cannot invite without admin permissions
        #     rx.container(
        #         rx.hstack(
        #         search_user("project"),
        #         rx.text(f"Click to search an existing user"),
        #         align="center",
        #     ),),
        #     align="start",
        #     spacing="4",
        # ),
        org_table(ProjectState.project_orgs),
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
        table_pagination(ProjectState.project_members,"project"),
    ),
        rx.callout(
            "You need admin privileges to edit the project information.",
            icon="info",
        )
    )

    return platform_layout(my_child)
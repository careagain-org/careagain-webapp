import reflex as rx
import pandas as pd
from ..states.project_state import ProjectState
from ..constants import urls
from .project_button_actions import dialog_remove,dialog_leave,button_view,button_edit

def show_project(project,role:str):
    """Show a user in a table row."""
    return rx.table.row(
            rx.table.cell(
                rx.cond(project["image"]=="",
                rx.icon("building"),
                rx.avatar(src=f"{project["image"]}"),
            ),),
            rx.table.cell(project["name"]),
            rx.table.cell(project["type"]),
            rx.match(project["status"],
                     ("Regulatory body approval",rx.table.cell(rx.badge("RB Approved",variant="surface",color_scheme="grass"))),
                     ("Clinically tested",rx.table.cell(rx.badge("Clinically tested",variant="surface",color_scheme="violet"))),
                     ("Technically tested",rx.table.cell(rx.badge("Technically tested",variant="surface",color_scheme="cyan"))),
                     ("Prototype",rx.table.cell(rx.badge("Prototype",variant="surface",color_scheme="bronze"))),
                     rx.table.cell(rx.badge("Not defined",variant="surface",color_scheme="gray")),
            ),
            rx.table.cell(rx.link(f"{project["website"]}",href=f"{project["website"]}",is_external=True)),
            rx.match(project["verified"],
                     (True,rx.table.cell(rx.badge("Verified",variant="surface",color_scheme="teal"))),
                     (False,rx.table.cell(rx.badge("Non-Verified",variant="surface",color_scheme="amber"))),
            ),
            rx.match(role,
                     ("admin", rx.table.cell(rx.hstack(
                            button_view(project["project_id"]),
                            button_edit(project["project_id"]),
                            dialog_leave(project["project_id"]),    
                            dialog_remove(project["project_id"]),
                            spacing="3",
                            justify="start"
                            ),),),
                     ("user", rx.table.cell(rx.hstack(
                            button_view(project["project_id"]),
                            dialog_leave(project["project_id"]),
                            spacing="3",
                            justify="start"
                            ),),),
                     ("viewer", rx.table.cell(button_view(project["project_id"]),),),
                        rx.table.cell(button_view(project["project_id"]),),
                    ),
            style={"_hover": 
                {"bg": rx.color("gray", 3)}
            },
        align="center",
    )

def table_pagination(all_projects,my_role="viewer"):
    
    return rx.cond(all_projects !=[],
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Image"),
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Type"),
                    rx.table.column_header_cell("Status"),
                    rx.table.column_header_cell("Website"),
                    rx.table.column_header_cell("Verified"),
                    rx.table.column_header_cell("Actions"),
                ),
            ),
            rx.table.body(
                rx.foreach(all_projects, lambda project, i: 
                        rx.cond(project.contains("member_type") & my_role!="viewer",
                                show_project(project=project,role=project["member_type"]),
                                show_project(project=project,role="viewer"),
                            ),
                ),
            ),
            variant="surface",
            size="3",
            width="95%",
        ),
        rx.fragment(),
    )
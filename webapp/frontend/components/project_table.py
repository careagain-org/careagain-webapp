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
            rx.table.cell(project["website"]),
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
                    rx.table.column_header_cell("Website"),
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
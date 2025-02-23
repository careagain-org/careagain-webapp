import reflex as rx
import pandas as pd
from ..states.user_state import UserState
from ..states.org_state import OrgState
from ..states.project_state import ProjectState
from ..constants import urls
from .user_button_actions import dialog_leave,button_view

def show_user(user,field:str):
    """Show a user in a table row."""
    return rx.table.row(
            rx.table.cell(
                rx.cond(user["profile_image"]=="",
                rx.icon("user"),
                rx.avatar(src=f"{user["profile_image"]}"),
            ),),
            rx.table.cell(f"@{user["username"]}"),
            rx.table.cell(f"{user["first_name"]}  {user["last_name"]}"),
            rx.table.cell(user["country"]),
            rx.match(field,
                    ("organization",rx.table.cell(
                        rx.select(["user","admin"],
                            default_value=user["member_type"],
                            on_change=lambda value: OrgState.change_member(user["user_id"],value)),),),
                    ("project",rx.table.cell(
                        rx.select(["user","admin"],
                            value=user["member_type"],
                            on_change=lambda value: ProjectState.change_member(user["user_id"],value)),),),
                    ),
            rx.match(user["verified"],
                     (True,rx.table.cell(rx.badge("Verified",variant="surface",color_scheme="teal"))),
                     (False,rx.table.cell(rx.badge("Non-Verified",variant="surface",color_scheme="amber"))),
            ),
            rx.table.cell(rx.hstack(
                            button_view(user["user_id"]),
                            dialog_leave(user["user_id"],field),  
                            spacing="3",
                            justify="start"
                            ),),
            style={"_hover": 
                {"bg": rx.color("gray", 3)}
            },
        align="center",
    )

def table_pagination(all_users,field):
    # df=pd.read_csv("assets/test.csv")
    # print(df)
    return rx.cond(all_users !=[],
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell(rx.icon("image")),
                            rx.table.column_header_cell("username"),
                            rx.table.column_header_cell("Name"),
                            rx.table.column_header_cell("Country"),
                            rx.table.column_header_cell("Role"),
                            rx.table.column_header_cell("Verified"),
                            rx.table.column_header_cell("Actions"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(all_users, lambda user, i: 
                                    show_user(user=user,field=field),
                            )
                    ),
                    variant="surface",
                    size="3",
                    width="95%",
                ),
                rx.fragment(),
            )
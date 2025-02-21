import reflex as rx
import pandas as pd
from ..states.org_state import OrgState
from ..constants import urls
from .org_button_actions import dialog_remove,dialog_leave,button_view,button_edit

def show_user(org,role:str):
    """Show a user in a table row."""
    return rx.table.row(
            rx.table.cell(
                rx.cond(org["logo"]=="",
                rx.icon("building"),
                rx.avatar(src=f"{org["logo"]}"),
            ),),
            rx.table.cell(org["name"]),
            rx.table.cell(org["type"]),
            rx.table.cell(org["website"]),
            rx.match(org["verified"],
                     (True,rx.table.cell(rx.badge("Verified",variant="surface",color_scheme="teal"))),
                     (False,rx.table.cell(rx.badge("Non-Verified",variant="surface",color_scheme="amber"))),
            ),
            rx.match(role,
                     ("admin", rx.table.cell(rx.hstack(
                            button_view(org["org_id"]),
                            button_edit(org["org_id"]),
                            dialog_leave(org["org_id"]),    
                            dialog_remove(org["org_id"]),
                            spacing="3",
                            justify="start"
                            ),),),
                     ("user", rx.table.cell(rx.hstack(
                            button_view(org["org_id"]),
                            dialog_leave(org["org_id"]),
                            spacing="3",
                            justify="start"
                            ),),),
                     ("viewer", rx.table.cell(button_view(org["org_id"]),),),
                        rx.table.cell(button_view(org["org_id"]),),
                    ),
            style={"_hover": 
                {"bg": rx.color("gray", 3)}
            },
        align="center",
    )

def table_pagination(all_orgs):
    # df=pd.read_csv("assets/test.csv")
    # print(df)
    return rx.cond(all_orgs !=[],
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Logo"),
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Type"),
                    rx.table.column_header_cell("Website"),
                    rx.table.column_header_cell("Verified"),
                    rx.table.column_header_cell("Actions"),
                ),
            ),
            rx.table.body(
                rx.foreach(all_orgs, lambda org, i: 
                           rx.cond(org.contains("member_type"),
                               show_user(org=org,role=org["member_type"]),
                               show_user(org=org,role="viewer"),
                           )
                ),
            ),
            variant="surface",
            size="3",
            width="95%",
        ),
        rx.fragment(),
    )
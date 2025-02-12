import reflex as rx
import pandas as pd
from ..states.org_state import OrgState
from ..constants import urls
from ..components.button_actions import dialog_remove,dialog_leave

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
            rx.table.cell(org["web_link"]),
            rx.match(role,
                     ("admin", rx.table.cell(rx.hstack(
                            rx.icon_button("eye",variant="soft"),
                            rx.icon_button("pencil",variant="soft"),
                            dialog_leave(org["org_id"]),    
                            dialog_remove(org["org_id"]),
                            spacing="3",
                            justify="start"
                            ),),),
                     ("user", rx.table.cell(rx.hstack(
                            rx.icon_button("eye",variant="soft"),
                            dialog_leave(org["org_id"]),
                            spacing="3",
                            justify="start"
                            ),),),
                     ("viewer", rx.table.cell(rx.icon_button("eye",variant="soft"),),),
                        rx.table.cell(rx.icon_button("eye",variant="soft")),
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
import reflex as rx
import pandas as pd
from ..states.org_state import OrgState
from ..constants import urls

def show_user(org_id,org):
    """Show a user in a table row."""
    return rx.table.row(
            rx.table.cell(rx.link(rx.avatar(icon="building"),href=f"{urls.INDIVIDUAL_ORG_URL}{org_id}")),
                            #href= f"{urls.INDIVIDUAL_ORG_URL}",)),
                            #on_click=OrgState.select_org(org_id),)),
            rx.table.cell(org["org_name"]),
            rx.table.cell(org["web_link"]),
            rx.table.cell(org["latitude"]),
            style={"_hover": 
                {"bg": rx.color("gray", 3)}
            },
        align="center",
    )

def table_pagination():
    # df=pd.read_csv("assets/test.csv")
    # print(df)
    return rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Logo"),
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Link"),
                    rx.table.column_header_cell("Latitude"),
                ),
            ),
            rx.table.body(
                rx.foreach(OrgState.orgs_locations, lambda org, i: 
                    show_user(org_id=org["org_id"],
                              org=org)
                ),
            ),
            variant="surface",
            size="3",
            width="95%",
        ),

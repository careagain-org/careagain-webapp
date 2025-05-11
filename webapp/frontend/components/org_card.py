import reflex as rx
import httpx
from ..states.org_state import OrgState
from ..constants import urls
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())
s3_url = os.environ.get("SUPABASE_S3_URL")
s3_bucket = os.environ.get("SUPABASE_S3_BUCKET")
s3_prfolder = "/orgs/org_id"
s3_imfolder = "/images/"


def big_org_card_vertical(org)-> rx.Component:

    return rx.box(
        rx.link(
            rx.card(
                rx.hstack(
                    rx.hstack(
                        rx.avatar(src=f"{org["logo"]}",
                                width="100px",
                                height="100px",),
                        rx.vstack(
                            rx.heading(org["name"]),
                            rx.scroll_area(rx.text(org["description"]),
                                scrollbars="vertical",
                                style={"height": 60},),
                            spacing="2",
                        ),
                        align='start',),
                    justify="between",
                ),
                width = "100%",
                size="3",
            ),
            on_click=lambda: OrgState.to_org_view(org["org_id"]),
        ),
        height = 'auto',
        width = "90%",
    )
    
    
def big_org_grid_vertical(orgs)-> rx.Component:

    return rx.vstack(
        rx.cond(
            orgs != [],
            rx.foreach(orgs, lambda value, i: 
                        big_org_card_vertical(value)),
            rx.spinner(),#rx.text("No orgs available")
        ),   
        spacing_y="4",
        width="90%",
        align ="start",
        justify = "start"
    )


def org_card_vertical(org)-> rx.Component:
    return rx.box(
        rx.card(
            rx.hstack(
                rx.avatar(src=f"{org["logo"]}",
                        width="50px",
                        height="50px"),
                rx.vstack(
                    rx.heading(org["name"],size="3"),
                    rx.text(org["type"]),
                    rx.text(org["adress"]),
                    spacing="1",
                ),
                rx.cond(org["org_id"] == OrgState.org_id,
                        rx.button("Select",disabled=True,type="button"),
                        rx.button("Select",disabled=False,
                            on_click = lambda: OrgState.select_org(org["org_id"]),
                            type="button"),
                        )
            ),
            width = "100%",
            size="3",
            _hover={"color": "teal"}
        ),
        height = 'auto',
        #width = '100vw',
        align='start',
        width = "100%",

    )

def org_grid_vertical(orgs)-> rx.Component:

    return rx.vstack(
        rx.cond(
            orgs != [],
            rx.foreach(orgs, lambda org, i: 
                        org_card_vertical(org),),
            rx.spinner(),#rx.text("No orgs available")
        ),   
        spacing_y="4",
        #width="100%",
        align ="start",
        justify = "start"
    )

def org_card_horizontal(org)-> rx.Component:

    return rx.container(
        rx.card(
            rx.link(
                rx.flex(
                    rx.avatar(src=f"{org["logo"]}",
                            width="140px",
                            height="140px"),
                    rx.heading(org["name"],align="center"),
                    spacing="2",
                    direction="column",
                    padding ="0",
                    align="center"
                ),
                href=urls.IND_ORG_URL,
                on_click=OrgState.to_org_view(org["org_id"]),
                align="start"
            ),
            # as_child=True,
            size="5",
            height='220px',
            width='180px',
            padding ="5%",
            align="start",
        ),
        height = 'auto',
        align='start',
        width = '250px',

    )

def org_scroll_horizontal(orgs)-> rx.Component:
    return rx.scroll_area(
        rx.flex(
        rx.cond(
            orgs != [],
            rx.foreach(orgs, lambda value, i: 
                        org_card_horizontal(value)),
            rx.text("No orgs available")
        ),   
    ),
        spacing="2",
        flex_wrap="wrap",
        width="100%",
        justify = "start")
    
def org_grid_horizontal(orgs)-> rx.Component:
    return rx.flex(
        rx.cond(
            orgs != [],
            rx.foreach(orgs, lambda value, i: 
                        org_card_horizontal(value)),
            rx.text("No orgs available")
        ),   
        spacing="2",
        flex_wrap="wrap",
        width="100%",
        justify = "start")